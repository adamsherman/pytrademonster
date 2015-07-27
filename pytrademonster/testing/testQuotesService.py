from pytrademonster.pyTradeMonster import PyTradeMonster

__author__ = 'adam'

import unittest

import xmltodict

from pytrademonster import PyTradeMonster
from pytrademonster.services import QuotesService
from pytrademonster.constants import TradeMonsterConstants


class TestQuotesService(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.pyTradeMonster = PyTradeMonster('../cred.dat')
        self.quotesService = QuotesService(self.pyTradeMonster)
        self.symbolDict = {'SPY' : TradeMonsterConstants.INSTRUMENTS.EQUITY, 'SPYX1517C300000' : TradeMonsterConstants.INSTRUMENTS.OPTION}


    def testQuoteRetrieval(self):
        results = self.quotesService.getParsedOptionChain('SPY')
        self.assertGreater(len(results), 1)

    def testQuotePayload(self):
        xmlStr = self.quotesService.quoteRequests.createQuotesPayload(self.symbolDict)
        xmlObj = xmltodict.parse(xmlStr)
        self.assertEqual(xmlObj['getQuotes']['item'][0]['symbol'],'SPY')


    def testQuoteSymbol(self):
        results = self.quotesService.getParsedQuotes(self.symbolDict)
        self.assertTrue(len(results) == 2)
        spyEquity = results['SPY'].instrumentType
        self.assertEquals(spyEquity,TradeMonsterConstants.INSTRUMENTS.EQUITY)



if __name__ == '__main__':
    unittest.main()
