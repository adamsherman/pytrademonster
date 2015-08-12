__author__ = 'adam'
"""
Various classes related to an order to TradeMonster.

Order: the actual order sent to market
OrderLeg: component of an order that is sent to market

OrderResponse: class for storing all results returned from a placed order
NewOrderLeg: class for storing result of a leg that is returned from a placed order
OrderPreview: the preview portion of an order response from a placed order
"""
from pytrademonster.constants import enum

class OrderType(object):
    types = enum(LIMIT = 'LM', MARKET='MK', STOP_ORDER = 'SP', TRAILING_STOP = 'TS',
                STOP_LIMIT = 'SL', TRAILING_STOP_LIMIT = 'TSL')

class OrderStatus(object):
     status = enum(SAVED = 'SAVED', EXPIRED = 'EXPIRED', QUEUED = 'QUEUED', PENDING = 'PENDING',
                   OPEN = 'OPEN', FILLED = 'FILLED', REJECTED = 'REJECTED',
                   CANCEL_QUEUED = 'CANCEL QUEUED', OTHER = 'OTHER')

class OrderLeg(object):
    '''
    Class used to create an individual leg when placing orders
    '''
    side = enum(BUY = 'BUY', SELL = 'SELL')
    openClose = enum(OPEN = 'OPEN', CLOSE = 'CLOSE')

    def __init__(self):
        self.orderSide = OrderLeg.side.BUY #default
        self.symbol = None
        self.openOrClose = None
        self.quantityRatio = 1
        self.instrumentType = None



class NewOrderLeg(object):
    '''
    Class that is used to store the result returned when placing an order - i.e., each individual leg
    '''
    def __init__(self):
         #specific fields for 'newOrderLeg' that is returned when sending an order
        self.exchange = None
        self.expirationDate = None
        self.holdingType = None #long or short
        self.positionType = None
        self.strikePrice = None
        self.price = None
        self.symbol = None
        self.quantity = None

class OrderResponse():
    '''
    Class for the storing the results retrieved back immediately when an order is placed
    '''

    def __init__(self):
        self.date = None
        self.status = None
        self.orderId = None
        self.actualOrderId = None #only named this to conform with their data model - somewhat confusing
        self.accountNumber = None
        self.orderPreview = None

class OrderPreview(object):
    '''
    Class for storing the order preview results that is retrieved upon placing an order
    '''
    def __init__(self):
        self.cost = None
        self.commnAndFees = None
        self.possibleFreeTradeCredit = None
        self.totalCost = None
        #self.cashBpEffect = None
        self.buyingPowerEffect = None
        self.resultingBuyingPower = None
        self.resultingCashBuyingPower = None
        self.resultingMarginBuyingPower = None
        self.resultingDayTradeBuyingPower = None
        self.netLiquidationValue = None
        self.negativeOrderImpact = None
        self.isReviewRequired = None
        self.isProhibitedOptionPairPresent = None
        self.isNetLiquidationLess = None
        self.marginRequirement = None
        self.currentInitialOptionReq = None
        self.currentMaintenanceOptionReq = None
        self.equityLegCost = None
        self.optionLegCost = None
        self.maintenanceMarginRequirement = None
        self.resultingCash = None
        self.openOrderReserve = None
        self.openOrderRequirement = None
        self.smaBuyingPower = None
        self.unadjustedBuyingPower = None
        self.discountingFactor = None
        self.cashInLieu = None
        self.regTEquity = None
        self.isIndexOptionExercise = None
        self.isBpConsumed = None
        self.indexSettlementAmount = None
        self.isProceedsConsidered = None
        self.displayErrorToCustomer = None
        self.newOrderLegs = []


class Order(object):
    '''
    Class for creating an order to send to the market
    '''
    timeInForceEnum = enum(CLO='CLO', DAY='DAY', EXT='EXT', FOK='FOK', GTC='GTC', GTD='GTD', IOC='IOC')
    marketSessionEnum = enum(REG='REG', EXT='EXT')
    def __init__(self):
        self.type = None
        self.price = None
        self.quantity = None
        self.instrumentType = None
        self.timeInForce = None
        self.modifyOrder = False
        self.originalOrderId = None
        self.combineLikeLegs = False
        self.holdOrder = False
        self.discretionFlag = False
        self.solicitedFlag = False
        self.marketSession = None
        self.goodToCancelDate = None
        self.spreadName = None
        self.orderLegs = []


class LimitOrder(Order):
    def __init__(self):
        super(LimitOrder, self).__init__()
        self.type = OrderType.types.LIMIT

class MarketOrder(Order):
    def __init__(self):
        super(MarketOrder, self).__init__()
        self.type = OrderType.types.MARKET

class StopOrder(Order):
    def __init__(self):
        super(StopOrder, self).__init__()
        self.type = OrderType.types.STOP

class TrailingStopOrder(Order):
    def __init__(self):
        super(TrailingStopOrder, self).__init__()
        self.type = OrderType.types.TRAILING_STOP

class StopLimit(Order):
    def __init__(self):
        super(StopLimit, self).__init__()
        self.type = OrderType.types.STOP_LIMIT
        self.stopTriggerPrice = None

class TrailingStopLimitOrder(Order):
    def __init__(self):
        super(TrailingStopLimitOrder, self).__init__()
        self.type = OrderType.types.TRAILING_STOP_LIMIT
        self.trailingAmount = None