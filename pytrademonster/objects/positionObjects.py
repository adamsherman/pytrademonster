__author__ = 'rohit'

"""
Objects to represent an positions within an account
"""



class PositionItem(object):
    '''
    Representation of a single position.
    Contains indicative information.
    There are fields which may be applicable to certain instrumentType only
    e.g. expirationDate is only applicable to options and not to Equities.
    '''

    def __init__(self):
        self.UnderlierBeta = None
        self.UnderlierDescription = None
        self.UnderlierInstrumentId = None
        self.UnderlierInstrumentType = None
        self.UnderlierMargin = None
        self.UnderlierPmMargin = None
        self.UnderlierSymbol = None
        self.accountId = None
        self.CAndFCurrent = None
        self.CAndFOpen = None
        self.costOpen = None
        self.costTotal = None
        self.day = None
        self.dayCAndFOpen = None
        self.dayCostOpen = None
        self.dayCostTotal = None
        self.daysToExpiry = None
        self.description = None
        self.exerciseStyle = None
        self.expirationDate = None
        self.holdingType = None
        self.instrumentId = None
        self.instrumentType = None
        self.month = None
        self.mtdCAndFOpen = None
        self.mtdCostOpen = None
        self.mtdCostTotal = None
        self.opraCode = None
        self.optionType = None
        self.positionId = None
        self.positionType = None
        self.quantity = None
        self.shortDescription = None
        self.strategyName = None
        self.strikePrice = None
        self.symbol = None
        self.symbolLongName = None
        self.valueMultiplier = None
        self.year = None
        self.ytdCAndFOpen = None
        self.ytdCostOpen = None
        self.ytdCostTotal = None
