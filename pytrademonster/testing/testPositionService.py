# -*- coding: utf-8 -*-
__author__ = 'adam'

import unittest
from pytrademonster import PyTradeMonster
from pytrademonster.services import AccountServices, PositionServices


"""
########################################################################
IMPORTANT: set this to a real account number to make the tests run
########################################################################
"""
ACCOUNT_NUMBER = 'xxxxxx'
class TestPositionService(unittest.TestCase):
    """
    Test parsing of positions
    """

    @classmethod
    def setUpClass(self):
        self.pyTradeMonster = PyTradeMonster('../cred.dat')
        self.positionService = PositionServices(self.pyTradeMonster)
        self.accountsService = AccountServices(self.pyTradeMonster)
        self.accounts = self.accountsService.getParsedAccountObjects()


    def testGetSinglePosition(self):
        positions = self.positionService.getParsedPositionsDetail(self.accounts[ACCOUNT_NUMBER].accountId)
        if len(positions) > 0:
            print 'Found positions'
        else :
            self.fail('No positions found or unable to parse, please have a live position in the account first!')



if __name__ == '__main__':
    unittest.main()
