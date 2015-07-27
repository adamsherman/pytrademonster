__author__ = 'adam'

import xmltodict

from pytrademonster.constants import TradeMonsterConstants


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