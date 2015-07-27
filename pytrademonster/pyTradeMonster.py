__author__ = 'adamsherman'

import logging
import os
import getpass

from requests import Session,adapters
import xmltodict
from simplecrypt import encrypt,decrypt

from pytrademonster.services import LoginService
from pytrademonster.constants import TradeMonsterConstants


log = logging.getLogger(__name__)
ECP = '#ecp'

class PyTradeMonster(object):
    '''
    Main interface to TradeMonster.
    Maintains an open session, and handles making requests.
    '''

    HEADERS = {'content-type':'application/xml'}

    def __init__(self, pwFile = 'cred.dat', environment = TradeMonsterConstants.Environments.PROD):
        self.environment = environment
        login = LoginService(self.environment)
        user,password = self.getUserAndPass(pwFile)
        login.doLogin(user,password)
        self.headers =  {'content-type':'application/xml', 'JSESSIONID' : login.sessionId, 'token' : login.token, 'sourceapp':login.userId}
        self.session = self.createSession(login.cookies)


    def getUserAndPass(self, pwFile):
        '''
        Try and retrieve the username and password from the encrypted user file - 'cred.dat'
        If no file exists, prompt the user for a login/password and create a file with encrypted contents
        :return: user and pass tuple
        '''
        log.info('Retrieving username and password....')
        if os.path.isfile(pwFile):
            with open(pwFile) as f:
                tokens = decrypt(ECP,f.read()).split('\n')
                user,passwd = tokens[0],tokens[1]
        else:
            user = raw_input('Enter your username: ')
            passwd = getpass.getpass('Enter your password: ')
            log.info('Encrypting user/pass to {0}....'.format(pwFile))
            userPassEncrypted = encrypt(ECP,user + '\n' + passwd)
            with open(pwFile, mode='w') as f:
                f.write(userPassEncrypted)
        log.info('Sucessfully retrieved username and password')
        return (user,passwd)

    def createSession(self, cookies):
        '''
        Creates a global session to be used by all requests
        :param cookies:
        :return:
        '''
        session = Session()
        adapter = adapters.HTTPAdapter(pool_connections = 1000, pool_maxsize = 5000)
        session.mount('https://', adapter)
        session.headers = self.headers
        session.cookies = cookies
        return session


    def doCall(self, url, payload):
        '''
        Make a request to a given url with given payload data and return a python object from a parsed xml response
        Either QA or PROD environment, as defined in constants
        :param url:
        :param payload:
        :return: python object created from parsed xml
        '''
        log.debug("Making request to {0}".format(self.environment + url))
        response = self.session.post(self.environment + url,payload)
        xmlObj = xmltodict.parse(response.text)
        log.debug("Got response: {0}".format(xmlObj))
        return xmlObj


