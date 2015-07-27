# -*- coding: utf-8 -*-
__author__ = 'adam'

import unittest
import time
from pytrademonster import PyTradeMonster
from pytrademonster.constants import TradeMonsterConstants
from pytrademonster.services import AccountServices, OrderServices
from pytrademonster.objects import LimitOrder, OrderLeg, OrderStatus


"""
########################################################################
IMPORTANT: set this to a real account number to make the tests run
########################################################################
"""
ACCOUNT_NUMBER = 'xxxxxx'

class TestOrderService(unittest.TestCase):
    """
    Test most functionality surrounding submission, execution, and retrieval of orders
    """

    @classmethod
    def setUpClass(self):
        self.pyTradeMonster = PyTradeMonster('../cred.dat')
        self.orderService = OrderServices(self.pyTradeMonster)
        self.accountsService = AccountServices(self.pyTradeMonster)
        self.accounts = self.accountsService.getParsedAccountObjects()

    @classmethod
    def tearDownClass(self):
        '''
        Cancel all outstanding orders
        :return:
        '''
        print 'Going to cancel all outstanding orders from unit testing...'
        self.orderService.sendCancelAllOrders(self.accounts[ACCOUNT_NUMBER].accountNumber)



    def createSimpleLimitOrder(self):
        order = LimitOrder()
        orderLeg = OrderLeg()
        orderLeg.instrumentType = TradeMonsterConstants.INSTRUMENTS.EQUITY
        orderLeg.symbol = 'SPY'
        orderLeg.orderSide = OrderLeg.side.BUY
        order.price = 0.01
        order.quantity = 1
        order.orderLegs = [orderLeg]
        order.instrumentType = TradeMonsterConstants.INSTRUMENTS.EQUITY
        order.timeInForce = LimitOrder.timeInForceEnum.DAY
        order.marketSession = LimitOrder.marketSessionEnum.REG
        return order

    def testSingleLimitOrder(self):
        order = self.createSimpleLimitOrder()
        orderResponse = self.orderService.sendOrderAndGetParsedResponse(self.accounts[ACCOUNT_NUMBER], order)

        status = orderResponse.status
        print 'Status of order is {0}'.format(status)
        self.assertTrue(status in OrderStatus.status.__dict__.keys() )

    def testGetOrderConfirmation(self):
        order = self.createSimpleLimitOrder()
        orderResponse = self.orderService.sendOrderAndGetParsedResponse(self.accounts[ACCOUNT_NUMBER], order)

        print 'Trying to confirm order...'
        result = self.orderService.getOrderConfirmation(self.accounts[ACCOUNT_NUMBER], order, orderResponse)
        confirm = result[TradeMonsterConstants.ResponseRoots.RETRIEVE_ORDER_CONFIRMATION_ROOT]
        self.assertTrue(confirm['orderDescription'] != None)

    def testSpreadOrder(self):
        '''
        Test a simple buy spread (debit)
        :return:
        '''
        order = LimitOrder()
        shortLeg = OrderLeg()
        longLeg = OrderLeg()


        shortLeg.instrumentType = TradeMonsterConstants.INSTRUMENTS.OPTION
        shortLeg.symbol = 'SPYX1517C300000'
        shortLeg.orderSide = OrderLeg.side.SELL
        shortLeg.quantityRatio = 1

        longLeg.instrumentType = TradeMonsterConstants.INSTRUMENTS.OPTION
        longLeg.symbol = 'SPYX1517C310000'
        longLeg.orderSide = OrderLeg.side.BUY
        longLeg.quantityRatio = 1

        order.price = 0.01
        order.quantity = 1
        order.instrumentType = TradeMonsterConstants.INSTRUMENTS.OPTION
        order.timeInForce = LimitOrder.timeInForceEnum.DAY
        order.marketSession = LimitOrder.marketSessionEnum.REG
        order.orderLegs = []
        order.orderLegs.append(shortLeg)
        order.orderLegs.append(longLeg)
        order.spreadName = TradeMonsterConstants.OrderRequests.ORDER_SPREAD_TYPES.PUT_VERTICAL

        #send a live order with a silly price
        result = self.orderService.sendOrderAndGetParsedResponse(self.accounts[ACCOUNT_NUMBER], order)

        status = result.status
        print 'Status of order is {0}'.format(status)

        self.assertTrue(status in OrderStatus.status.__dict__.keys())



    def testCancelSingleOrder(self):
        order = self.createSimpleLimitOrder()
        orderResponse = self.orderService.sendOrderAndGetParsedResponse(self.accounts[ACCOUNT_NUMBER], order)
        print 'Going to cancel order',orderResponse.orderId,'...'
        time.sleep(1)
        result = self.orderService.sendCancelOrder(orderResponse.orderId)
        self.assertTrue(TradeMonsterConstants.ResponseRoots.RETRIEVE_ORDER_CANCELLED_ROOT in result)


    def testCancelAllOrders(self):
        order = self.createSimpleLimitOrder()
        orderResponse = self.orderService.sendOrderAndGetParsedResponse(self.accounts[ACCOUNT_NUMBER], order)
        print 'Going to cancel all orders',orderResponse.orderId,'...'
        time.sleep(1)
        result = self.orderService.sendCancelAllOrders(self.accounts[ACCOUNT_NUMBER].accountNumber)
        self.assertTrue(TradeMonsterConstants.ResponseRoots.RETRIEVE_ALL_CANCELLED_ROOT in result)


    def testCancelDayOrder(self):
        order = self.createSimpleLimitOrder()
        orderResponse = self.orderService.sendOrderAndGetParsedResponse(self.accounts[ACCOUNT_NUMBER], order)
        print 'Going to cancel day order',orderResponse.orderId,'...'
        time.sleep(1)
        result = self.orderService.sendCancelDayOrders(self.accounts[ACCOUNT_NUMBER].accountNumber)
        self.assertTrue(TradeMonsterConstants.ResponseRoots.RETRIEVE_DAY_CANCELLED_ROOT in result)


    def testCountAllOrders(self):
        order = self.createSimpleLimitOrder()
        self.orderService.sendOrderAndGetParsedResponse(self.accounts[ACCOUNT_NUMBER], order)
        order = self.createSimpleLimitOrder()
        self.orderService.sendOrderAndGetParsedResponse(self.accounts[ACCOUNT_NUMBER], order)
        print 'Going to count all orders...'
        time.sleep(1)
        result = self.orderService.sendCountAllOpenOrders(self.accounts[ACCOUNT_NUMBER].accountNumber)
        print 'Counted', result, 'orders total'
        self.assertEquals(result,2)

    def testCountDayOrders(self):
        self.orderService.sendCancelAllOrders(self.accounts[ACCOUNT_NUMBER].accountNumber) #cancel everything first just in case
        order = self.createSimpleLimitOrder()
        self.orderService.sendOrderAndGetParsedResponse(self.accounts[ACCOUNT_NUMBER], order)
        print 'Going to count day orders...'
        time.sleep(1)
        result = self.orderService.sendCountDayOrders(self.accounts[ACCOUNT_NUMBER].accountNumber)
        print 'Counted', result, 'day orders'
        self.assertEquals(result,1)

    def testGetOrderHistory(self):
        order = self.createSimpleLimitOrder()
        orderResponse = self.orderService.sendOrderAndGetParsedResponse(self.accounts[ACCOUNT_NUMBER], order)
        result = self.orderService.sendGetOrderHistory(orderResponse.orderId)
        self.fail('TradeMonster call getOrderHistory not yet working - followup with them...')

    def testGetOrderDetails(self):
        order = self.createSimpleLimitOrder()
        orderResponse = self.orderService.sendOrderAndGetParsedResponse(self.accounts[ACCOUNT_NUMBER], order)
        result = self.orderService.sendGetOrderDetail(orderResponse.orderId)
        self.assertTrue(TradeMonsterConstants.ResponseRoots.RETRIEVE_ORDER_DETAILS_ROOT in result)

if __name__ == '__main__':
    unittest.main()
