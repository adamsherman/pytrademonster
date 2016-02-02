__author__ = 'adam'

"""
Objects to represent an options' quote chain
"""


class QuoteChain(object):

    def __init__(self):
        self.rootTicker = None
        self.daysToExpire = None
        self.deliveryType = None
        self.exerciseStyle = None
        self.expirationType = None
        self.expiryDeliverable = None
        self.expiryLabel = None
        self.expiryType = None
        self.options = {} # strike and side is the key, value is a QuoteOptionItem

class QuoteOptionItem(object):
    '''
    Representation of a single strike of an options.
    Contains indicative information.
    '''

    def __init__(self):
        self.strike = None
        self.exchange = None
        self.side = None
        self.minTickValue = None
        self.multiplier = None
        self.opraRoot = None
        self.instrumentId = None
        self.reutersCode = None
        self.sharesPerContract = None
        self.symbol = None
        self.expiryYear = None
        self.expiryMonth = None
        self.expiryDay = None
        self.tradeable = None


class QuoteItem(object):
    '''
    Representation of an actual price quote for any asset Trademonster trades
    '''

    def __init__(self):
        self.askPrice = 0
        self.bidPrice = 0
        self.askSize = 0
        self.bidSize = 0
        self.currency = None
        self.closingMark = 0
        self.dividendType = None
        self.dividend = 0
        self.dividendDate = 0
        self.highPrice = 0
        self.impliedVolatility = 0
        self.instrumentType = None
        self.lastPrice = 0
        self.lastTradedSize = 0
        self.lastTradedTimeMs = 0
        self.lowPrice = 0
        self.openInterest = 0
        self.openPrice = 0
        self.previousClosePrice = 0
        self.symbol = None
        self.volume = 0
        self.yearHigh = 0
        self.yearLow = 0