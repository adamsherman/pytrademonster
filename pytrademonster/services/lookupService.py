__author__ = 'adam'

import json

import requests

from pytrademonster.constants import TradeMonsterConstants


def lookupOption(strike, underlier, expiryDate = None, rowsPerPage = 10000, optionType = None, ):
    '''

    :param strike: None for all expiries, otherwise a specific strike, i.e. 200
    :param underlier: underlying equity
    :param expiryDate: MM/DD/YYYY format, i.e. 08/12/2016
    :param rowsPerPage:
    :param optionType: Nnne for put and calls, or PUT or CALL for a specific side
    :return: A list of dictionaries with valid option symbols, i.e. 'SPYS1715C191500'
    '''
    strike = float(strike) if strike != None else None
    jsonObj = {'jsonObject' : {"remoteClassName":'com.om.dh.sm.vo.DetailedLookUpReqVO',
                               'expirationDate':  expiryDate 
                                ,'optionType':  optionType
                                ,'strikePrice':  strike
                                ,'pagination':{'sortBy':None,'startRow':0,'totalPages':0,'rowsPerPage':rowsPerPage,
                                                        'currentPage':1,'results':[],'endRow':0,'totalRows':0,
                                                        'remoteClassName': 'com.om.dh.dao.pagination.PaginationResult',
                                                        'previousPage':False,'nextPage':False},
                                'underlier':   underlier  }
               }
    jsonStr = json.dumps(jsonObj)
    jsonStr = jsonStr[1:-1]
    colon = jsonStr.find(':')
    jsonStr =jsonStr[1:colon-1] + '=' + jsonStr[colon+2:]


    postedResult = requests.post(TradeMonsterConstants.OPTION_LOOKUP_SERIVCE, data = jsonStr, headers = {'Content-type': 'application/x-www-form-urlencoded'})
    resultJson = json.loads(postedResult.text)

    return resultJson


