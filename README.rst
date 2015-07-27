**Pytrademonster** is a simple, pythonic interface to TradeMonster/Optionhouses' XML based API. It attempts to cover
most of the functionality that their API provides. Admittedly, their API documentation is a bit shoddy, but this project
accounts for that where possible.

Tested against their API Version 2.5

Getting Started
===============
::

    Choose one:
         1. Checkout the project here and run 'python setup.py install'
         2. 'pip install pytrademonster' (use sudo if needed)


Examples
========

**Create an instance of PyTradeMonster and log in**

The first time this is done, you'll be prompted for your user/pass
and it will be saved into a default file, 'cred.dat' or one of your choice

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

**Place and order**

**Query an order**

**Modify an order**

**Plot your pnl**


Functions provided
==================
This tries to be as consistent with their API as possible




