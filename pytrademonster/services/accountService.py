__author__ = 'adam'

from datetime import datetime

import xmltodict

from pytrademonster.constants import TradeMonsterConstants
from pytrademonster.objects import AccountTransaction, Account


class AccountRequests(object):

    def createAccountHistoryPayload(self, userId, numTransactions, accountId, transactionType, start=None, end=None ):
        '''
        start and end are in iso8601 YYYYMMDDThh:mm:ss format
        '''

        xmlStr = TradeMonsterConstants.AccountRequests.DEFAULT_ACCOUNT_HISTORY
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['getAccountHistory']['userId'] = userId
        if start != None and end != None:
            startDatetime = datetime.strptime(start, TradeMonsterConstants.ISO_TIME)
            endDatetime = datetime.strptime(end, TradeMonsterConstants.ISO_TIME)
            xmlObj['getAccountHistory']['startTime']['year'] = startDatetime.year
            xmlObj['getAccountHistory']['startTime']['month'] = startDatetime.month
            xmlObj['getAccountHistory']['startTime']['date'] = startDatetime.day
            xmlObj['getAccountHistory']['startTime']['minutes'] = startDatetime.minute
            xmlObj['getAccountHistory']['startTime']['seconds'] = startDatetime.second
            xmlObj['getAccountHistory']['endTime']['year'] = endDatetime.year
            xmlObj['getAccountHistory']['endTime']['month'] = endDatetime.month
            xmlObj['getAccountHistory']['endTime']['date'] = endDatetime.day
            xmlObj['getAccountHistory']['endTime']['minutes'] = endDatetime.minute
            xmlObj['getAccountHistory']['endTime']['seconds'] = endDatetime.second
        else:
            xmlObj['getAccountHistory']['timeRange'] = 'TODAY'
        xmlObj['getAccountHistory']['numOfTransactions'] = numTransactions
        xmlObj['getAccountHistory']['accountIds'] = accountId
        xmlObj['getAccountHistory']['transactionTypes'] = transactionType
        return xmltodict.unparse(xmlObj)

    def createAccountBalancePayload(self, accountNumber):
        xmlStr = TradeMonsterConstants.AccountRequests.DEFAULT_CUST_WIDGET
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['getCustomerWidgetData']['accountNumber'] = accountNumber
        return xmltodict.unparse(xmlObj)


    def createDeleteGroupPayload(self, groupId):
        xmlStr = TradeMonsterConstants.AccountRequests.DEFAULT_DELETE_GROUPS
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['deleteGroups']['groupIds'] = groupId
        return xmltodict.unparse(xmlObj)

    def createNewGroupPayload(self, groupNameToUse, accountIds):
        xmlStr = TradeMonsterConstants.AccountRequests.CREATE_ACCOUNT_GROUP
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['createAccountGroup']['groupName'] = groupNameToUse
        xmlObj['createAccountGroup']['groupId'] = ''
        xmlObj['createAccountGroup']['accountIds'] = accountIds
        return xmltodict.unparse(xmlObj)


    def createAccountPerformancePayload(self, accountNumber,accountId, fromDate, toDate, category=TradeMonsterConstants.AccountRequests.PERFORMANCE_CATEGORY.SYMBOL ):
        xmlStr = TradeMonsterConstants.AccountRequests.DEFAULT_ACCOUNT_PERFORMANCE
        xmlObj = xmltodict.parse(xmlStr)
        startDatetime = datetime.strptime(fromDate, TradeMonsterConstants.ISO_TIME)
        endDatetime = datetime.strptime(toDate, TradeMonsterConstants.ISO_TIME)
        xmlObj['getAccountPerformance']['fromDateVO']['dateObj'] = startDatetime.strftime(TradeMonsterConstants.PERFORMANCE_TIME)
        xmlObj['getAccountPerformance']['fromDateVO']['date'] = startDatetime.day
        xmlObj['getAccountPerformance']['fromDateVO']['hours'] = startDatetime.hour
        xmlObj['getAccountPerformance']['fromDateVO']['year'] = startDatetime.year
        xmlObj['getAccountPerformance']['fromDateVO']['seconds'] = startDatetime.second
        xmlObj['getAccountPerformance']['fromDateVO']['month'] = startDatetime.month
        xmlObj['getAccountPerformance']['fromDateVO']['minutes'] = startDatetime.minute
        xmlObj['getAccountPerformance']['toDateVO']['dateObj'] = endDatetime.strftime(TradeMonsterConstants.PERFORMANCE_TIME)
        xmlObj['getAccountPerformance']['toDateVO']['date'] = endDatetime.day
        xmlObj['getAccountPerformance']['toDateVO']['hours'] = endDatetime.hour
        xmlObj['getAccountPerformance']['toDateVO']['year'] = endDatetime.year
        xmlObj['getAccountPerformance']['toDateVO']['seconds'] = endDatetime.second
        xmlObj['getAccountPerformance']['toDateVO']['month'] = endDatetime.month
        xmlObj['getAccountPerformance']['toDateVO']['minutes'] = endDatetime.minute

        xmlObj['getAccountPerformance']['accountIds'] = accountId
        xmlObj['getAccountPerformance']['accountNumber'] = accountNumber
        xmlObj['getAccountPerformance']['category'] = category
        xmlObj['getAccountPerformance']['toDate'] = int(endDatetime.strftime('%s'))
        xmlObj['getAccountPerformance']['fromDate'] = int(startDatetime.strftime('%s'))

        return xmltodict.unparse(xmlObj)

    def createCashTransferPayload(self, accountId):
        xmlStr = TradeMonsterConstants.AccountRequests.DEFAULT_CASH_TRANSFER
        xmlObj = xmltodict.parse(xmlStr)
        xmlObj['getCashTransfers']['accountId'] = accountId
        return xmltodict.unparse(xmlObj)




class AccountServices(object):
    '''
    Class for invoking various account specific services
    '''

    def __init__(self, pyTradeMonster):
        self.pyTradeMonster = pyTradeMonster
        self.accountRequests = AccountRequests()

    def getParsedAccountObjects(self):
        '''
        Populate a dictionary of Account objects
        Key is AccountNumber - i.e., '5PDXXXXX
        :return:
        '''
        xmlObj = self.getAccounts()
        accountDict = {}

        root = xmlObj[TradeMonsterConstants.ResponseRoots.RETRIEVE_ACCT_ROOT]
        for acct in root['accountList']:
            account = Account()
            account.accountId = acct['accountId']
            account.accountNumber = acct['accountNumber']
            account.accountDisplayName = acct['accountDisplayName']
            account.accountType = acct['accountType']
            account.accountInceptionDate = acct['accountInceptionDate']
            account.accountRegistrationType = acct['accountRegistrationType']
            account.accountStatus = acct['accountStatus']
            account.alertEmail = acct['alertEmail']
            account.ownerFirstName = acct['primaryAccountHolderFirstName']
            account.ownerLastName = acct['primaryAccountHolderLastName']
            account.userId = root['userProfile']['userId']
            accountDict[account.accountNumber] = account
        return accountDict

    def getParsedAccountHistory(self, account, numTransactions, transactionType, start=None, end=None):
        '''
        Return a list of account history objects
        :param userId:
        :param numTransactions:
        :param accountId:
        :param transactionType:
        :param start:
        :param end:
        :return: trnasactionList
        '''

        xmlObj = self.getAccountHistory(account.userId, numTransactions, account.accountId, transactionType, start, end)
        transactionList = []

        root = xmlObj[TradeMonsterConstants.ResponseRoots.RETRIEVE_ACCT_HISTORY_ROOT]
        for item in root['accountHistoryVO']:
            transaction = AccountTransaction()
            transaction.accountId = item['accountId']
            transaction.currency = item['amount']['currency']
            transaction.amount = item['amount']['amount']
            transaction.transactionDescription = item['transactionDescription']
            transaction.transactionDate = item['transactionDate']
            transaction.transactionType = item['transactionType']
            if 'acType' in item:
                transaction.accountType = item['acType']
            if 'fee' in item:
                transaction.fee = item['fee']['amount']
            if 'instrumentType' in item :
                transaction.instrumentType = item['instrumentType']
            if 'side' in item :
                transaction.buyOrSell = item['side']
            if 'quantity' in item :
                transaction.quantity = item['quantity']
            if 'status' in item :
                transaction.status = item['status']
            if 'symbol' in item :
                transaction.symbol = item['symbol']
            if 'commission' in item :
                transaction.commissionAmount = item['commission']['amount']
            transactionList.append(transaction)
        return transactionList



    def getAccounts(self):
        url = TradeMonsterConstants.URLS.ACCOUNT_PERSON_SERVICE
        payload = TradeMonsterConstants.AccountRequests.DEFAULT_FETCH_ACCOUNTS
        return self.pyTradeMonster.doCall(url,payload)

    def getAccountHistory(self,userId, numTransactions, accountId, transactionType, start=None, end=None):
        url = TradeMonsterConstants.URLS.ACCOUNT_HISTORY_SERVICE
        payload = self.accountRequests.createAccountHistoryPayload(userId,numTransactions,accountId, transactionType, start, end)
        return self.pyTradeMonster.doCall(url,payload)

    def getAllGroups(self):
        url = TradeMonsterConstants.URLS.ACCOUNT_GROUP_SERVICE
        payload = TradeMonsterConstants.AccountRequests.DEFAULT_FETCH_GROUPS
        return self.pyTradeMonster.doCall(url,payload)

    def getBalanceForAccount(self, accountNumber):
        url = TradeMonsterConstants.URLS.ACCOUNT_BALANCES_SERVICE
        payload = self.accountRequests.createAccountBalancePayload(accountNumber)
        return self.pyTradeMonster.doCall(url,payload)

    def getAccountPerformance(self, accountNumber, accountId, fromDate, toDate, category):
        url = TradeMonsterConstants.URLS.ACCOUNT_PERFORMANCE_SERVICE
        payload = self.accountRequests.createAccountPerformancePayload(accountNumber, accountId, fromDate, toDate, category)
        return self.pyTradeMonster.doCall(url, payload)

    def getCashTransfers(self, accountId):
        url = TradeMonsterConstants.URLS.ACCOUNT_CASH_TRANSFER_SERVICE
        payload = self.accountRequests.createCashTransferPayload(accountId)
        return self.pyTradeMonster.doCall(url,payload)

    def doCreateAccountGroup(self, groupNameToUse, accountIds):
        '''
        Create a new group with a list of accountIds
        :param groupNameToUse:
        :param accountIds: list of account ids
        :return:
        '''
        url = TradeMonsterConstants.URLS.GROUP_SERVICE
        payload =self.accountRequests.createNewGroupPayload(groupNameToUse, accountIds)
        self.pyTradeMonster.doCall(url,payload)


