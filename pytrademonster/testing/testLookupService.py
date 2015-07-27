__author__ = 'adam'

import unittest

from pytrademonster.services import lookupService


class TestLookupService(unittest.TestCase):
    '''
    Test the simple lookup for a list of option codes from TradeMonster given an equity underlier and strike
    '''
    def testLookupService(self):
        underlier = 'SPY'
        strike = 200

        options = lookupService.lookupOption(strike, underlier)
        optionsListLength = len(options)

        print 'Found', optionsListLength, 'options'
        for index, option in enumerate(options):
            print index,'\t',option

        self.assertGreaterEqual(optionsListLength, 1)