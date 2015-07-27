__author__ = 'adamsherman'

import sys
import logging

import requests

from pytrademonster.constants import TradeMonsterConstants


log = logging.getLogger(__name__)

class LoginService(object):
    '''
    Class to handle logging in/out of trademonster and storing individual session information
    '''
    PAYLOAD_USER = 'j_username'
    PAYLOAD_PASSWORD = 'j_password'

    def __init__(self, environment):
        self.userId = None
        self.sessionId = None
        self.token = None
        self.cookies = None
        self.loginUrl = environment + TradeMonsterConstants.URLS.LOGIN
        self.logoutUrl = environment + TradeMonsterConstants.URLS.LOGOUT

    def doLogin(self, user, password):
        '''
        Send a login request to trademonster. Upon success, set instance variables for credentials.
        :param user:
        :param password:
        :return:
        '''
        payload = {LoginService.PAYLOAD_USER : user, LoginService.PAYLOAD_PASSWORD : password}
        loginRequest = requests.post(self.loginUrl, payload)
        loginDict = loginRequest.json()
        if 'token' in loginDict:
            self.token = loginDict['token']
            self.sessionId = loginDict['sessionId']
            self.userId = loginDict['userId']
            self.cookies = loginRequest.cookies
            log.info('Successfully logged in!')
        else:
            log.warn('Unable to login. Exiting.')
            sys.exit()

    def doLogout(self):
        if  self.sessionId is not None:
            payload = {'JSESSIONID' : self.sessionId}
            logoutRequest = requests.post(self.logoutUrl, payload)


