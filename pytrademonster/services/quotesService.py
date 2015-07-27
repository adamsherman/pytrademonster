from collections import OrderedDict

__author__ = 'adam'

from pytrademonster.constants import TradeMonsterConstants
from pytrademonster.objects import QuoteChain, QuoteOptionItem, QuoteItem
import xmltodict

class QuoteRequests(object):
    '''
    Create payload items for quote requests
    '''
    def createOptionChainPayload(self, symbol):
        xmlStr = TradeMonsterConstants.QuotesRequests.DEFAULT_OPTION_CHAIN_REQUEST
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['getOptionChain']['symbol'] = symbol
        return xmltodict.unparse(xmlObj)

    def createQuotesPayload(self, symbolTypeDict):
        xmlStr = TradeMonsterConstants.QuotesRequests.DEFAULT_QUOTE_REQUEST
        xmlObj = xmltodict.parse(xmlStr)
        itemObj = xmlObj['getQuotes']
        itemObj['item'] = []
        del itemObj['blank']
        for symbol,instrumentType in symbolTypeDict.iteritems():
            itemDict = OrderedDict()
            itemDict['symbol'] = symbol
            itemDict['instrumentType'] = instrumentType
            itemObj['item'].append(itemDict)
        return xmltodict.unparse(xmlObj)





class QuotesService(object):

    def __init__(self, pyTradeMonster):
        self.pyTradeMonster = pyTradeMonster
        self.quoteRequests = QuoteRequests()

    def getOptionChain(self, symbol):
        url = TradeMonsterConstants.URLS.QUOTES_OPTION_SERVICE
        payload = self.quoteRequests.createOptionChainPayload(symbol)
        return self.pyTradeMonster.doCall(url, payload)

    def createQuoteOptionItem(self, strike, side):
        option = QuoteOptionItem()
        option.exchange = strike['exchange']
        option.expiryDay = strike['instrument']['expireDayET']
        option.expiryMonth = strike['instrument']['month']
        option.expiryYear = strike['instrument']['year']
        option.minTickValue = strike['minimumTickValue1']
        option.multiplier = strike['multiplier']
        option.opraRoot = strike['instrument']['opraCode']
        option.reutersCode = strike['reutersInstrumentCode']
        option.sharesPerContract = strike['sharesPerContract']
        option.instrumentId = strike['instrumentId']
        option.strike = strike['strikePrice']
        option.symbol = strike['symbol']
        option.side = side
        option.tradeable = strike['instrument']['tradable']
        return option


    def getParsedOptionChain(self, symbol):
        '''
        Return a list of option chains for various strikes/expirations for a given symbol
        :param symbol:
        :return:
        '''
        optionChainResponse = self.getOptionChain(symbol)
        items = optionChainResponse[TradeMonsterConstants.ResponseRoots.RETRIEVE_QUOTE_CHAIN_ROOT]['item']
        optionChain = []
        for item in items:
            quoteChain = QuoteChain()
            quoteChain.rootTicker = symbol
            quoteChain.daysToExpire = item['daysToExpire']
            quoteChain.deliveryType = item['deliverableType']
            quoteChain.exerciseStyle = item['exerciseStyle']
            quoteChain.expirationType = item['expirationType']
            quoteChain.expiryLabel = item['expiryLabel']
            quoteChain.expiryType = item['expiryType']
            allStrikes = item['option_Collection']

            #iterate through each strike and append to the option dictionary
            for strike in allStrikes:
                strikeVal = strike['strike']
                callOption = self.createQuoteOptionItem(strike['call'], TradeMonsterConstants.CALL_PUT.CALL)
                putOption = self.createQuoteOptionItem(strike['put'], TradeMonsterConstants.CALL_PUT.PUT)
                callKey = (strikeVal, TradeMonsterConstants.CALL_PUT.CALL)
                putKey = (strikeVal, TradeMonsterConstants.CALL_PUT.PUT)
                quoteChain.options[callKey] = callOption
                quoteChain.options[putKey] = putOption

            optionChain.append(quoteChain)

        return optionChain





    def getQuotes(self, symbolTypeDict):
        '''
        Retrieve multiple quotes from Trademonster
        :param symbolTypeDict:
        :return:
        '''
        url = TradeMonsterConstants.URLS.QUOTES_SYMBOL_SERVICE
        payload = self.quoteRequests.createQuotesPayload(symbolTypeDict)
        return self.pyTradeMonster.doCall(url, payload)



    def getParsedQuotes(self, symbolTypeDict):
        '''
        Convenience method for returning a dictionary of Quote Objects from various symbols
        :param symbolTypeDict:
        :return:
        '''
        quotesResponse = self.getQuotes(symbolTypeDict)
        items = quotesResponse[TradeMonsterConstants.ResponseRoots.RETRIEVE_QUOTE_SYMBOL_ROOT]['item']
        quoteDict = {}
        for item in items:
            quote = QuoteItem()
            quote.symbol = item['symbol']
            quote.askPrice = item['askPrice']['amount']
            quote.askSize = item['askSize']
            quote.bidPrice = item['bidPrice']['amount']
            quote.bidSize = item['bidSize']
            quote.closingMark = item['closingMark']['amount']
            quote.currency = item['bidPrice']['currency']
            quote.dividendType = item['divType'] if 'divType' in item else None
            quote.dividend = item['dividend']['amount'] if 'dividend' in item else None
            quote.dividendDate = item['dividendDate'] if 'dividendDate' in item else None
            quote.highPrice = item['highPrice']['amount']
            quote.impliedVolatility = item['impliedVolatility']
            quote.instrumentType = item['instrumentType']
            quote.lastTradedSize = item['lastSize']
            quote.lastPrice = item['lastTradedPrice']['amount']
            quote.lastTradedTimeMs = item['lastTradeTimeMillis'] if 'lastTradeTimeMillis' in item else None
            quote.lowPrice = item['lastTradedPrice']
            quote.openPrice = item['openPrice']['amount']
            quote.previousClosePrice = item['previousClosePrice']['amount']
            quote.volume = item['volume']
            quote.yearHigh = item['yearHighPrice']['amount'] if 'yearHighPrice' in item else None
            quote.yearLow = item['yearLowPrice']['amount'] if 'yearLowPrice' in item else None

            quoteDict[quote.symbol] = quote

        return quoteDict

