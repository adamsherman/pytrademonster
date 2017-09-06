**IMPORTANT**

*As of September 2017, Optionshouse has been fully integrated into eTrade
and as such this API is no longer valid for eTrade's own API. For reference only at this point*

====



*Pytrademonster* is a simple, pythonic interface to TradeMonster/Optionhouses' https://www.optionshouse.com/ XML based API. It attempts to cover
most of the functionality that their API provides. Optionshouse uses an xml schema which can be requested from them or by using a tool such as Charles Proxy to figure out.

Admittedly, their API documentation is a bit shoddy, but this project
accounts for that where possible. In order to trade systematically with them there is an account minumum that you must maintain.

*Tested against their API Version 2.5*

*Intended for Python 2.7*

Getting Started
===============
::

    Choose one:
         1. Checkout the project here and run 'python setup.py install'
         2. 'pip install pytrademonster' (use sudo if needed)

|
Examples (for more, see the unit tests)
========

**Create an instance of PyTradeMonster and log in**

The first time this is done, you'll be prompted for your user/pass
and it will be encrypted and saved into a default file, 'cred.dat' or one of your choice

.. code-block:: python

    from pytrademonster import PyTradeMonster
    pyTradeMonster = PyTradeMonster()

**Get a quote**

.. code-block:: python

    from pytrademonster import PyTradeMonster
    from pytrademonster.services import QuotesService
    from pytrademonster.constants import TradeMonsterConstants

    pyTradeMonster = PyTradeMonster()
    quotesService = QuotesService(pyTradeMonster)

    #add any number of 'ticker:instrumentType' pairs
    symbolDict = {'SPY' : TradeMonsterConstants.INSTRUMENTS.EQUITY}
    quoteResult = quotesService.getParsedQuotes(symbolDict)

**Get an option chain**

.. code-block:: python

    from pytrademonster import PyTradeMonster
    from pytrademonster.services import QuotesService
    from pytrademonster.constants import TradeMonsterConstants
    
    pyTradeMonster = PyTradeMonster()
    quotesService = QuotesService(pyTradeMonster)
    
    #get a list of option strikes for various expirations for a single security
    results = quotesService.getParsedOptionChain('SPY')
    
**Get account information**

.. code-block:: python

    from pytrademonster import PyTradeMonster
    from pytrademonster.services import AccountServices

    pyTradeMonster = PyTradeMonster()
    accountsService = AccountServices(pyTradeMonster)
    
    # return a dictionary of Account objects that contain useful account information
    accounts = accountsService.getParsedAccountObjects()


**Place an equity order**

.. code-block:: python

    from pytrademonster import PyTradeMonster
    from pytrademonster.services import OrderServices, AccountServices
    from pytrademonster.objects import LimitOrder, OrderLeg
    from pytrademonster.constants import TradeMonsterConstants
    
    pyTradeMonster = PyTradeMonster()

    orderService = OrderServices(pyTradeMonster)
    accountsService = AccountServices(pyTradeMonster)
    
    # get our list of accounts
    accounts = accountsService.getParsedAccountObjects()
    
    ACCOUNT_NUMBER = 'your account number'
    
    # create a simple limit order with a silly price
    order = LimitOrder()
    orderLeg = OrderLeg()
    orderLeg.instrumentType = TradeMonsterConstants.INSTRUMENTS.EQUITY
    orderLeg.symbol = 'SPY'
    orderLeg.orderSide = OrderLeg.side.BUY
    order.price = 0.01
    order.quantity = 1
    order.orderLegs = [orderLeg]
    order.instrumentType = TradeMonsterConstants.INSTRUMENTS.EQUITY
    order.timeInForce = LimitOrder.timeInForceEnum.DAY
    order.marketSession = LimitOrder.marketSessionEnum.REG

    # send the order to the trademonster
    orderResponse = orderService.sendOrderAndGetParsedResponse(self.accounts[ACCOUNT_NUMBER], order)
    
    orderId = orderResponse.orderId
    orderStatus = orderResponse.status
    print 'Order {0} status is {1}'.format(orderId,status)

**Place a multi-leg option order**

.. code-block:: python
    
    from pytrademonster import PyTradeMonster
    from pytrademonster.services import OrderServices, AccountServices
    from pytrademonster.objects import LimitOrder, OrderLeg
    from pytrademonster.constants import TradeMonsterConstants
    
    pyTradeMonster = PyTradeMonster()

    orderService = OrderServices(pyTradeMonster)
    accountsService = AccountServices(pyTradeMonster)
    
    # get our list of accounts
    accounts = accountsService.getParsedAccountObjects()
    
    ACCOUNT_NUMBER = 'your account number'
    
    # Create a simple buy (debit) spread, by creating each individual leg   
    # The symbol and spread name fields should be changed depending on the ticker
    order = LimitOrder()
    shortLeg = OrderLeg()
    longLeg = OrderLeg()

    shortLeg.instrumentType = TradeMonsterConstants.INSTRUMENTS.OPTION
    shortLeg.symbol = 'TickerSymbol' #you can look up the ticker using a service or their GUI
    shortLeg.orderSide = OrderLeg.side.SELL
    shortLeg.quantityRatio = 1

    longLeg.instrumentType = TradeMonsterConstants.INSTRUMENTS.OPTION
    longLeg.symbol = 'TickerSymbol' #you can look up the ticker using a service or their GUI
    longLeg.orderSide = OrderLeg.side.BUY
    longLeg.quantityRatio = 1

    order.price = 0.01
    order.quantity = 1
    order.instrumentType = TradeMonsterConstants.INSTRUMENTS.OPTION
    order.timeInForce = LimitOrder.timeInForceEnum.DAY
    order.marketSession = LimitOrder.marketSessionEnum.REG
    order.orderLegs = []
    order.orderLegs.append(shortLeg)
    order.orderLegs.append(longLeg)
    order.spreadName = TradeMonsterConstants.OrderRequests.ORDER_SPREAD_TYPES.PUT_VERTICAL #if it's a put spread

    #send a live order with a silly price
    orderResult = orderService.sendOrderAndGetParsedResponse(self.accounts[ACCOUNT_NUMBER], order)

    status = orderResult.status
    print 'Status of order is {0}'.format(status)
    
  
**Cancel an order**

.. code-block:: python
    
    from pytrademonster import PyTradeMonster
    from pytrademonster.services import OrderServices

    pyTradeMonster = PyTradeMonster()
    orderService = OrderServices(pyTradeMonster)
    
    # get the orderId from a recent order first
    # i.e., orderId = orderService.sendOrderAndGetParsedResponse(self.accounts[ACCOUNT_NUMBER], order).orderId
    
    result = orderService.sendCancelOrder(orderId)
    
    
**Get detailed position information**

.. code-block:: python
    
    from pytrademonster import PyTradeMonster
    from pytrademonster.services import PositionService
    
    pyTradeMonster = PyTradeMonster()
    positionService = PositionService(pyTradeMonster)
    
    # get account id from the account service first if needed
    # this will return a list of existing positions by type and their associated information
    result = positionService.getPositionsDetail(accountId)
    

**Plot your pnl**

.. code-block:: python
    
    from pytrademonster import PyTradeMonster
    from pytrademonster.visualizer import plotAccountPnl
    
    pyTradeMonster = PyTradeMonster()
    accountNumber = 'xxxxxxx' # your account number
    startTime = '20100101T00:00:00'
    endTime = '20150730T00:00:00'
    plotAccountPnl(pyTradeMonster, TradeMonsterConstants.AccountRequests.TRANSACTION_TYPES.TRADE, accountNumber, startTime, endTime, 'AAPL')



Functions provided
==================
This tries to be as consistent with their API as possible, but some functions just don't work as described. 
The coverage is fairly robust, but not a complete representation of their entire API. 

::
    
    For more details, look at the XML mappings in *constants.py* as well as the function calls in the services.
    


Future development
==================

This is certainly a work in progress, and no guarantees, but feel free to shoot me a note here for anything you'd like to see.
