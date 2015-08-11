__author__ = 'adam'

import xmltodict

from pytrademonster.constants import TradeMonsterConstants
from pytrademonster.objects import PositionItem


class PositionRequests(object):
    '''
    Class for creating the request strings for the position service
    '''
    def createPositionsBasicPayload(self, symbol, underlier):
        xmlStr = TradeMonsterConstants.PositionRequests.DEFAULT_POSITIONS_BASIC
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['getBasicPositionDetails']['symbol'] = symbol
        xmlObj['getBasicPositionDetails']['underlyer'] = underlier
        return xmltodict.unparse(xmlObj)

    def createPositionsDetailPayload(self,accountId):
        xmlStr = TradeMonsterConstants.PositionRequests.DEFAULT_POSITIONS_DETAIL
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['getPositionsDetailNew']['accountIds'] = accountId
        xmlObj['getPositionsDetailNew']['accountId'] = accountId
        return xmltodict.unparse(xmlObj)

    def createPositionsSelectedPayload(self,accountId, symbol, instrumentType):
        xmlStr = TradeMonsterConstants.PositionRequests.DEFAULT_POSITIONS_SELECTED
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['getSelectedPosition']['accountIds'] = accountId
        xmlObj['getSelectedPosition']['accountId'] = accountId
        xmlObj['getSelectedPosition']['symbol'] = symbol
        xmlObj['getSelectedPosition']['instrumentType'] = instrumentType
        return xmltodict.unparse(xmlObj)

    def createPositionsUnderliersPayload(self,accountId):
        xmlStr = TradeMonsterConstants.PositionRequests.DEFAULT_POSITIONS_UNDERLIERS
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['getHeldUnderlyers']['accountId'] = accountId
        return xmltodict.unparse(xmlObj)

    def createTransactionHistoryPayload(self, accountId, positionType, symbol, instrumentType, userId):
        xmlStr = TradeMonsterConstants.PositionRequests.DEFAULT_POSITIONS_TRANSACTIONS
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['getTxHistoryForInstrument']['positionType'] = positionType
        xmlObj['getTxHistoryForInstrument']['accountId'] = accountId
        xmlObj['getTxHistoryForInstrument']['symbol'] = symbol
        xmlObj['getTxHistoryForInstrument']['instrumentType'] = instrumentType
        xmlObj['getTxHistoryForInstrument']['userId'] = userId
        return xmltodict.unparse(xmlObj)


class PositionServices(object):
    '''
    Class for invoking various position specific services
    '''

    def __init__(self, pyTradeMonster):
        self.pyTradeMonster = pyTradeMonster
        self.positionRequests = PositionRequests()
        self.url = TradeMonsterConstants.URLS.POSITION_SERVICE

    def getPositionsDetail(self,accountId):       
        payload = self.positionRequests.createPositionsDetailPayload(accountId)
        return self.pyTradeMonster.doCall(self.url,payload)

    def getPositionsBasic(self,symbol, underlyer):       
        payload = self.positionRequests.createPositionsBasicPayload(symbol, underlyer)
        return self.pyTradeMonster.doCall(self.url,payload)

    def getPositionsSelected(self,accountId, symbol, insturmentType):      
        payload = self.positionRequests.createPositionsSelectedPayload(accountId, symbol, insturmentType)
        return self.pyTradeMonster.doCall(self.url,payload)

    def getPositionsUnderliers(self, accountId):     
        payload = self.positionRequests.createPositionsUnderliersPayload(accountId)
        return self.pyTradeMonster.doCall(self.url,payload)

    def getPositionsTransactions(self, accountId, positionType, symbol, instrumentType, userId):    
        payload = self.positionRequests.createTransactionHistoryPayload(accountId, positionType, symbol, instrumentType, userId)
        return self.pyTradeMonster.doCall(self.url,payload)

    def getParsedPositionsDetail(self, accountId):
        '''
        Populate a dictionary of PositionsDetail
        :return: list of all the positions
        '''
        positionDetailedResponse = self.getPositionsDetail(accountId)
        items = positionDetailedResponse[TradeMonsterConstants.ResponseRoots.RETRIEVE_POSITIONS_DETAILED_ROOT]['item']
        
        positions = []
        for item in items:
            if item['description'] == 'multiple':
                # TODO FIXME following loop is not tested; not sure if this is how we could iterate through multiple tags
                for Position in item['positions']:
                    position = PositionItem()
                    position.UnderlierBeta = item['beta']
                    position.UnderlierDescription = item['description']
                    position.UnderlierInstrumentId = item['instrumentId']
                    position.UnderlierInstrumentType = item['instrumentType']
                    position.UnderlierMargin = item['margin']
                    position.UnderlierPmMargin = item['pmMargin']
                    position.UnderlierSymbol = item['symbol']
                    self.parseSignlePositionQuote(position, Position)
                    positions.append(position)
            else:
                position = PositionItem()
                Position = item['positions']
                position.UnderlierBeta = item['beta']
                position.UnderlierDescription = item['description']
                position.UnderlierInstrumentId = item['instrumentId']
                position.UnderlierInstrumentType = item['instrumentType']
                position.UnderlierMargin = item['margin']
                position.UnderlierPmMargin = item['pmMargin']
                position.UnderlierSymbol = item['symbol']
                self.parseSignlePositionQuote(position, Position)
                positions.append(position)
        return positions

    def parseSignlePositionQuote(self, position, xmlPosition):
                position.accountId = xmlPosition['accountId']
                position.costOpen = xmlPosition['costOpen']
                position.costTotal = xmlPosition['costTotal']
                position.day = xmlPosition['day']
                position.dayCostOpen = xmlPosition['dayCostOpen']
                position.dayCostTotal = xmlPosition['dayCostTotal']
                position.daysToExpiry = xmlPosition['daysToExpiry']
                position.description = xmlPosition['description']
                position.exerciseStyle = xmlPosition['exerciseStyle']
                position.expirationDate = xmlPosition['expirationDate']
                position.holdingType = xmlPosition['holdingType']
                position.instrumentId = xmlPosition['instrumentId']
                position.instrumentType = xmlPosition['instrumentType']
                position.month = xmlPosition['month']
                position.mtdCostOpen = xmlPosition['mtdCostOpen']
                position.mtdCostTotal = xmlPosition['mtdCostTotal']
                position.opraCode = xmlPosition['opraCode']
                position.optionType = xmlPosition['optionType']
                position.positionId = xmlPosition['positionId']
                position.positionType = xmlPosition['positionType']
                position.quantity = xmlPosition['quantity']
                position.shortDescription = xmlPosition['shortDescription']
                position.strategyName = xmlPosition['strategyName']
                position.strikePrice = xmlPosition['strikePrice']
                position.symbol = xmlPosition['symbol']
                position.symbolLongName = xmlPosition['symbolLongName']
                position.valueMultiplier = xmlPosition['valueMultiplier']
                position.year = xmlPosition['year']
                position.ytdCostOpen = xmlPosition['ytdCostOpen']
                position.ytdCostTotal = xmlPosition['ytdCostTotal']