
__author__ = 'adamsherman'

from datetime import datetime
from collections import OrderedDict

import xmltodict

from pytrademonster.constants import TradeMonsterConstants
from pytrademonster.objects import LimitOrder, OrderType, OrderResponse, NewOrderLeg, OrderPreview


class OrderRequests(object):
    '''
    Create payloads for order requests
    '''

    def createSingleLegOrderPayload(self,account, order):
        '''
        Create a single leg payload
        Used primarily by equity trades, or single options
        :param account:
        :param order:
        :return:
        '''
        xmlStr = TradeMonsterConstants.OrderRequests.DEFAULT_SINGLE_LEG_ORDER
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['sendOrder']['accountType'] = account.accountType
        xmlObj['sendOrder']['accountNumber'] = account.accountNumber
        xmlObj['sendOrder']['accountId'] = account.accountId
        xmlObj['sendOrder']['userId'] = account.userId
        xmlObj['sendOrder']['priceType'] = order.type
        xmlObj['sendOrder']['quantity'] = order.quantity
        xmlObj['sendOrder']['instrumentType'] = order.instrumentType
        xmlObj['sendOrder']['timeInForce'] = order.timeInForce
        xmlObj['sendOrder']['marketSession'] = order.marketSession
        xmlObj['sendOrder']['orderLegEntries']['symbol'] = order.orderLegs[0].symbol
        xmlObj['sendOrder']['orderLegEntries']['instrumentType'] = order.orderLegs[0].instrumentType
        xmlObj['sendOrder']['orderLegEntries']['orderSide'] = order.orderLegs[0].orderSide

        if isinstance(order, LimitOrder):
             xmlObj['sendOrder']['limitPrice'] = order.price

        return xmltodict.unparse(xmlObj)


    def createMultiLegOrderPayload(self,account, order):
        '''
        Create a single leg payload
        Used primarily by equity trades, or single options
        :param account:
        :param order:
        :return:
        '''
        xmlStr = TradeMonsterConstants.OrderRequests.DEFAULT_MULTI_LEG_ORDER
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['sendOrder']['accountType'] = account.accountType
        xmlObj['sendOrder']['accountNumber'] = account.accountNumber
        xmlObj['sendOrder']['userId'] = account.userId
        xmlObj['sendOrder']['priceType'] = order.type
        xmlObj['sendOrder']['quantity'] = order.quantity
        xmlObj['sendOrder']['instrumentType'] = order.instrumentType
        xmlObj['sendOrder']['spreadName'] = order.spreadName
        xmlObj['sendOrder']['timeInForce'] = order.timeInForce
        xmlObj['sendOrder']['marketSession'] = order.marketSession
        xmlObj['sendOrder']['orderLegEntries'] = []
        for orderLeg in order.orderLegs:
            orderLegDict = OrderedDict()
            orderLegDict['symbol'] = orderLeg.symbol
            orderLegDict['quantityRatio'] = orderLeg.quantityRatio
            orderLegDict['instrumentType'] = orderLeg.instrumentType
            orderLegDict['orderSide'] = orderLeg.orderSide
            orderLegDict['openOrClose'] = orderLeg.openOrClose
            xmlObj['sendOrder']['orderLegEntries'].append(orderLegDict)

        if isinstance(order, LimitOrder):
             xmlObj['sendOrder']['limitPrice'] = order.price

        return xmltodict.unparse(xmlObj, pretty='True')



    def createPopulateConfirmation(self, account, originalOrder, orderResponse):
        '''

        :param account:
        :param order:
        :return:
        '''
        xmlStr = TradeMonsterConstants.OrderRequests.DEFAULT_ORDER_CONFIRMATION
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['populateConfirmation']['accountType'] = account.accountType
        xmlObj['populateConfirmation']['modifyOrder'] = originalOrder.modifyOrder
        xmlObj['populateConfirmation']['originalOrderId'] = orderResponse.actualOrderId
        xmlObj['populateConfirmation']['combineLikeLegs'] = originalOrder.combineLikeLegs
        xmlObj['populateConfirmation']['accountNumber'] = account.accountNumber
        xmlObj['populateConfirmation']['gtdDate'] = originalOrder.goodToCancelDate
        xmlObj['populateConfirmation']['userId'] = account.userId
        if originalOrder.type == OrderType.types.LIMIT:
            xmlObj['populateConfirmation']['limitPrice'] = originalOrder.price
        elif originalOrder.type == OrderType.types.STOP_ORDER:
            xmlObj['populateConfirmation']['stopTriggerPrice'] = originalOrder.price
        elif originalOrder.type == OrderType.types.TRAILING_STOP:
            xmlObj['populateConfirmation']['trailingAmount'] = originalOrder.price
        xmlObj['populateConfirmation']['orderId'] = orderResponse.orderId
        xmlObj['populateConfirmation']['priceType'] = originalOrder.type
        xmlObj['populateConfirmation']['quantity'] = originalOrder.quantity
        xmlObj['populateConfirmation']['holdOrder'] = originalOrder.holdOrder
        xmlObj['populateConfirmation']['discretionOrder'] = originalOrder.discretionFlag
        xmlObj['populateConfirmation']['solicitedFlag'] = originalOrder.solicitedFlag
        xmlObj['populateConfirmation']['instrumentType'] = originalOrder.instrumentType
        xmlObj['populateConfirmation']['timeInForce'] = originalOrder.timeInForce
        xmlObj['populateConfirmation']['marketSession'] = originalOrder.marketSession
        xmlObj['populateConfirmation']['noteVo']['userId'] = account.userId

        xmlObj['populateConfirmation']['orderLegEntries'] = []
        for orderLeg in originalOrder.orderLegs:
            orderLegDict = OrderedDict()
            orderLegDict['symbol'] = orderLeg.symbol
            orderLegDict['quantityRatio'] = orderLeg.quantityRatio
            orderLegDict['instrumentType'] = orderLeg.instrumentType
            orderLegDict['orderSide'] = orderLeg.orderSide
            orderLegDict['openOrClose'] = orderLeg.openOrClose
            xmlObj['populateConfirmation']['orderLegEntries'].append(orderLegDict)

        return xmltodict.unparse(xmlObj, pretty = 'True')


    def createCancelOrderPayload(self,orderId):
        '''
        :param orderId:
        :return:
        '''
        xmlStr = TradeMonsterConstants.OrderRequests.DEFAULT_ORDER_CANCEL
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['cancelOrder'] = orderId
        return xmltodict.unparse(xmlObj)

    def createCancelAllOrdersPayload(self, accountId):
        '''
        :param orderId:
        :return:
        '''
        xmlStr = TradeMonsterConstants.OrderRequests.DEFAULT_ORDER_CANCEL_ALL
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['cancelAllOrders'] = accountId
        return xmltodict.unparse(xmlObj)

    def createCancelDayOrdersPayload(self, accountId):
        '''
        :param orderId:
        :return:
        '''
        xmlStr = TradeMonsterConstants.OrderRequests.DEFAULT_ORDER_CANCEL_DAY
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['cancelDayOrders'] = accountId
        return xmltodict.unparse(xmlObj)

    def createCountAllOpenOrdersPayload(self, accountId):
        '''
        :param orderId:
        :return:
        '''
        xmlStr = TradeMonsterConstants.OrderRequests.DEFAULT_ALL_OPEN_ORDERS_COUNT
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['getCancelAllOrdersCount'] = accountId
        return xmltodict.unparse(xmlObj)

    def createCountOpenDayOrdersPayload(self, accountId):
        '''
        :param orderId:
        :return:
        '''
        xmlStr = TradeMonsterConstants.OrderRequests.DEFAULT_DAY_ORDERS_COUNT
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['getCancelDayOrdersCount'] = accountId
        return xmltodict.unparse(xmlObj)

    def createLoadOrderbookPayload(self, accountId, numberOfDays, statusList):
        '''
        Create the payload for loading the entire orderbook
        :param account:
        :param statusList:
        :param numberOfDays
        :return:
        '''
        xmlStr = TradeMonsterConstants.OrderRequests.DEFAULT_LOAD_ORDER_BOOK
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['accountNumber'] = accountId
        xmlObj['dateRange'] = numberOfDays
        xmlObj['statusList'] = []
        for status in statusList:
            statusDict = OrderedDict()
            statusDict['symbol'] = status
            xmlObj['statusList'].append(statusDict)
        return xmltodict.unparse(xmlObj)


    def createLoadSpecificOrdersPayload(self, accountId, numberOfDays, orderIds):
        '''
        Create the payload for loading specific orders
        :param accountId:
        :param numberOfDays:
        :param orderIds:
        :return:
        '''
        xmlStr = TradeMonsterConstants.OrderRequests.DEFAULT_LOAD_SPECIFIC_ORDERS
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['orderIds'] = []
        for orderId in orderIds:
            orderIdDict = OrderedDict()
            orderIdDict['orderIds'] = orderId
            xmlObj['orderIds'].append(orderIdDict)
        return xmltodict.unparse(xmlObj)

    def createOrderHistoryPayload(self, orderId):
        '''
        Create payload for retrieving an order
        :param orderId:
        :return:
        '''
        xmlStr = TradeMonsterConstants.OrderRequests.DEFAULT_GET_ORDER_HISTORY
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['getOrderHistory'] = orderId
        return xmltodict.unparse(xmlObj)

    def createOrderDetailPayload(self, orderId):
        '''
        Create payload for retrieving order details
        :param orderId:
        :return:
        '''
        xmlStr = TradeMonsterConstants.OrderRequests.DEFAULT_GET_ORDER_DETAIL
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['getOrderDetail'] = orderId
        return xmltodict.unparse(xmlObj)

class OrderServices(object):

    def __init__(self,pyTradeMonster):
        self.pyTradeMonster = pyTradeMonster
        self.orderRequests = OrderRequests()

    def sendSingleLegOrder(self,account,order):
        '''
        Send a single leg order, i.e. buy a put etc
        :param account:
        :param order:
        :return:
        '''
        url = TradeMonsterConstants.URLS.ORDER_PLACEMENT_SERVICE
        payload = self.orderRequests.createSingleLegOrderPayload(account,order)
        return self.pyTradeMonster.doCall(url,payload)

    def sendMultiLegOrder(self,account,order):
        '''
        Send a multi leg order, i.e. a spread etc
        :param account:
        :param order:
        :return:
        '''
        url = TradeMonsterConstants.URLS.ORDER_PLACEMENT_SERVICE
        payload = self.orderRequests.createMultiLegOrderPayload(account,order)
        return self.pyTradeMonster.doCall(url,payload)

    def sendOrderAndGetParsedResponse(self, account, order):
        '''
        Helper method
        Sends and order, then parses an order response received from trademonster and create an OrderResponse object
        :param account:
        :param order:
        :return: OrderResponse object
        '''
        if len(order.orderLegs) == 1:
            xmlObj = self.sendSingleLegOrder(account, order)
            multiLeg = False
        elif len(order.orderLegs) > 1:
            multiLeg = True
            xmlObj = self.sendMultiLegOrder(account, order)

        root = xmlObj[TradeMonsterConstants.ResponseRoots.RETRIEVE_ORDER_PLACED_ROOT]

        orderResponse = OrderResponse()
        orderResponse.actualOrderId = root['actualOrderId']
        orderResponse.accountNumber = root['accountNumber']
        orderResponse.orderId = root['actualOrderId']
        orderResponse.date = root['orderSentDate']
        orderResponse.status = root['orderStatus']

        # add OrderPreview object

        orderPreview = OrderPreview()
        orderPreviewRoot = root['orderPreviewVO']
        orderPreview.buyingPowerEffect = float(orderPreviewRoot['buyingPowerEffect']['amount'])
        orderPreview.cashBpEffect = float(orderPreviewRoot['cashBpEffect']['amount'])
        orderPreview.cashInLieu =  float(orderPreviewRoot['cashInLieu']['amount'])
        orderPreview.cost = float(orderPreviewRoot['cost']['amount'])
        orderPreview.commnAndFees = float(orderPreviewRoot['commnAndFees']['amount'])
        orderPreview.currentInitialOptionReq = float(orderPreviewRoot['currentInitialOptionReq']['amount'])
        orderPreview.currentMaintenanceOptionReq = float(orderPreviewRoot['currentMaintenanceOptionReq']['amount'])
        orderPreview.discountingFactor = float(orderPreviewRoot['discountingFactor']['amount'])
        orderPreview.equityLegCost = float(orderPreviewRoot['equityLegCost']['amount'])
        orderPreview.displayErrorToCustomer = orderPreviewRoot['displayErrorToCustomer']
        orderPreview.indexSettlementAmount = float(orderPreviewRoot['indexSettlementAmount']['amount'])
        orderPreview.isIndexOptionExercise = orderPreviewRoot['isIndexOptionExercise']
        orderPreview.isNetLiquidationLess = orderPreviewRoot['isNetLiquationLess']
        orderPreview.isProceedsConsidered = orderPreviewRoot['isProceedsConsidered']
        orderPreview.isProhibitedOptionPairPresent = orderPreviewRoot['isProhibitedOptionPairPresent']
        orderPreview.isReviewRequired = orderPreviewRoot['isReviewRequired']
        orderPreview.marginRequirement = float(orderPreviewRoot['marginRequirement']['amount'])
        orderPreview.netLiquidationValue = float(orderPreviewRoot['netLiquidationValue']['amount'])
        orderPreview.openOrderRequirement = float(orderPreviewRoot['openOrderRequirement']['amount'])
        orderPreview.openOrderReserve = float(orderPreviewRoot['openOrderReserve']['amount'])
        orderPreview.optionLegCost = float(orderPreviewRoot['optionLegCost']['amount'])
        orderPreview.regTEquity = float(orderPreviewRoot['regTEquity']['amount'])
        orderPreview.resultingBuyingPower = float(orderPreviewRoot['resultingBuyingPower']['amount'])
        orderPreview.resultingCash = float(orderPreviewRoot['resultingCash']['amount'])
        orderPreview.resultingCashBuyingPower = float(orderPreviewRoot['resultingCashBuyingPower']['amount'])
        orderPreview.resultingDayTradeBuyingPower = float(orderPreviewRoot['resultingDayTradeBuyingPower']['amount'])
        orderPreview.resultingMarginBuyingPower = float(orderPreviewRoot['resultingMarginBuyingPower']['amount'])
        orderPreview.smaBuyingPower = float(orderPreviewRoot['smaBuyingPower']['amount'])
        orderPreview.totalCost = float(orderPreviewRoot['totalCost']['amount'])
        orderPreview.unadjustedBuyingPower = float(orderPreviewRoot['unadjustedBuyingPower']['amount'])

        numOfOrderLegs = orderPreviewRoot['newOrderLegs']
        if multiLeg is True:
            for leg in numOfOrderLegs:
                orderLeg = NewOrderLeg()
                orderLeg.exchange = leg['exchange']
                expiration = leg['expirationDateVO']
                orderLeg.expirationDate = datetime(int(expiration['year']), int(expiration['month']), int(expiration['date']))
                orderLeg.instrumentType = leg['instrumentType']
                orderLeg.quantity = int(leg['qty'])
                orderLeg.strikePrice = float(leg['strikePrice']['amount'])
                orderLeg.symbol = leg['symbol']
                orderLeg.price = float(leg['price']['amount'])
                orderLeg.holdingType = leg['holdingType']
                orderLeg.positionType = leg['positionType']
                orderPreview.newOrderLegs.append(orderLeg)
        else:
            orderLeg = NewOrderLeg()
            orderLeg.exchange = numOfOrderLegs['exchange']
            orderLeg.instrumentType = numOfOrderLegs['instrumentType']
            orderLeg.quantity = int(numOfOrderLegs['qty'])
            orderLeg.symbol = numOfOrderLegs['symbol']
            orderLeg.price = float(numOfOrderLegs['price']['amount'])
            orderLeg.holdingType = numOfOrderLegs['holdingType']
            orderLeg.positionType = numOfOrderLegs['positionType']
            orderPreview.newOrderLegs.append(orderLeg)

        orderResponse.orderPreview = orderPreview
        return orderResponse



    def getOrderConfirmation(self,account, originalOrder, orderResponse):
        '''
        Return an object that 'confirm' an order
        Generally contains most of the fields found in OrderPreview
        :param account:
        :param order:
        :return:
        '''
        url = TradeMonsterConstants.URLS.ORDER_PLACEMENT_SERVICE
        payload = self.orderRequests.createPopulateConfirmation(account,originalOrder,orderResponse)
        return self.pyTradeMonster.doCall(url,payload)

    def sendCancelOrder(self, orderId):
        '''
        Simply cancels an existing order based on it's orderId
        :param orderId:
        :return:
        '''
        url = TradeMonsterConstants.URLS.ORDER_BOOK_SERVICE
        payload = self.orderRequests.createCancelOrderPayload(orderId)
        return self.pyTradeMonster.doCall(url,payload)

    def sendCancelAllOrders(self, accountId):
        '''
        Cancel all outstanding orders for an accountId
        :param accountId:
        :return:
        '''
        url = TradeMonsterConstants.URLS.ORDER_BOOK_SERVICE
        payload = self.orderRequests.createCancelAllOrdersPayload(accountId)
        return self.pyTradeMonster.doCall(url,payload)

    def sendCancelDayOrders(self, accountId):
        '''
        Cancel all outstanding day orders for an accountId
        :param accountId:
        :return:
        '''
        url = TradeMonsterConstants.URLS.ORDER_BOOK_SERVICE
        payload = self.orderRequests.createCancelDayOrdersPayload(accountId)
        return self.pyTradeMonster.doCall(url,payload)

    def sendCountAllOpenOrders(self, accountId):
        '''
        Count number of outstanding orders
        :param accountId:
        :return: A count of all open orders
        '''
        url = TradeMonsterConstants.URLS.ORDER_BOOK_SERVICE
        payload = self.orderRequests.createCountAllOpenOrdersPayload(accountId)
        result = self.pyTradeMonster.doCall(url,payload)
        if TradeMonsterConstants.ResponseRoots.RETRIVE_ALL_CANCELLED_COUNT_ROOT in result:
            return int(result[TradeMonsterConstants.ResponseRoots.RETRIVE_ALL_CANCELLED_COUNT_ROOT]['#text'])
        return None

    def sendCountDayOrders(self, accountId):
        '''
        Cancel all outstanding orders for an accountId
        :param accountId:
        :return: A count of all open day orders
        '''
        url = TradeMonsterConstants.URLS.ORDER_BOOK_SERVICE
        payload = self.orderRequests.createCountOpenDayOrdersPayload(accountId)
        result = self.pyTradeMonster.doCall(url,payload)
        if TradeMonsterConstants.ResponseRoots.RETRIVE_DAY_CANCELLED_COUNT_ROOT in result:
            return int(result[TradeMonsterConstants.ResponseRoots.RETRIVE_DAY_CANCELLED_COUNT_ROOT]['#text'])
        return None

    def sendGetOrderHistory(self, orderId):
        '''
        Get the history for a single order
        :param orderId:
        :return:
        '''
        url = TradeMonsterConstants.URLS.ORDER_BOOK_SERVICE
        payload = self.orderRequests.createOrderHistoryPayload(orderId)
        return self.pyTradeMonster.doCall(url,payload)

    def sendGetOrderDetail(self, orderId):
        '''
        Get the order details for a single order
        :param orderId:
        :return:
        '''
        url = TradeMonsterConstants.URLS.ORDER_BOOK_SERVICE
        payload = self.orderRequests.createOrderDetailPayload(orderId)
        return self.pyTradeMonster.doCall(url,payload)

