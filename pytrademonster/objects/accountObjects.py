__author__ = 'adam'

"""
Container objects for an account
"""

class Account(object):
    '''
    Container class for a an Account
    '''
    def __init__(self):
        self.accountNumber = None
        self.accountStatus = None
        self.accountType = None
        self.accountDisplayName = None
        self.accountInceptionDate = None
        self.accountRegistrationType = None
        self.accountId = None
        self.ownerFirstName = None
        self.ownerLastName = None
        self.alertEmail = None
        self.userId = None

    def __repr__(self):
        return 'AccountName: {0}, AccountNumber: {1}, AccountType: {2}'.format(self.accountDisplayName, self.accountNumber,self.accountType)


class AccountTransaction(object):
    '''
    Container class for an Account History item
    '''
    def __init__(self):
        self.accountId = None
        self.accountType = None
        self.currency = None
        self.amount = 0
        self.commissionAmount = 0
        self.fee = 0
        self.instrumentType = None
        self.quantity = None
        self.buyOrSell = None
        self.status = None
        self.symbol = None
        self.transactionDescription = None
        self.transactionDate = None
        self.transactionType = None

    def __repr__(self):
        return 'AccountId: {0} \t Date: {1} \t Amount: {2} \t Type: {3} \t Description: {4}'.format(self.accountId,self.transactionDate, self.amount, self.transactionType, self.transactionDescription)

