__author__ = 'adamsherman'


def enum(**enums):
    return type('Enum', (), enums)

class TradeMonsterConstants(object):
    '''
    Misc constants for interacting with TradeMonsters' service

    URLS are specific endpoints to make requests to

    Request classes (AccountRequests etc) contain the default xml payload requests as per TradeMonster documentation
    '''

    class Environments():
        QA = 'https://www.qa.monstersecurities.com'
        PROD = 'https://www.trademonster.com'


    ISO_TIME = '%Y%m%dT%H:%M:%S'
    TRANSACTION_TIME = '%Y-%m-%dT%H:%M:%S'
    PERFORMANCE_TIME = '%a %b %d %H:%M:%S GMT-0500 %Y'
    INSTRUMENTS = enum(EQUITY = 'Equity', OPTION = 'Option')
    CALL_PUT = enum(CALL = 'call', PUT = 'put')
    OPTION_LOOKUP_SERIVCE = Environments.PROD + '/detailedOptionLookUpLite.action'


    class URLS():
        LOGIN = '/j_acegi_security_check'
        LOGOUT = '/j_acegi_logout'

        SERVICES = '/services'

        ACCOUNT_HISTORY_SERVICE = SERVICES + '/accountHistoryService'
        ACCOUNT_PERFORMANCE_SERVICE = SERVICES + '/accountPerformanceService'
        ACCOUNT_PERSON_SERVICE = SERVICES + '/personService'
        ACCOUNT_GROUP_SERVICE = SERVICES + '/customerAccountGroupingService'
        ACCOUNT_BALANCES_SERVICE = SERVICES + '/customerWidgetService'
        ACCOUNT_CASH_TRANSFER_SERVICE = SERVICES + '/cashTransferService'

        POSITION_SERVICE = SERVICES + '/clientPositionService'

        ORDER_PLACEMENT_SERVICE = SERVICES + '/orderStockService'
        ORDER_BOOK_SERVICE = SERVICES + '/orderBookService'

        QUOTES_OPTION_SERVICE = SERVICES + '/quotesOptionService'
        QUOTES_SYMBOL_SERVICE = SERVICES + '/quotesService'



    class AccountRequests():
        FETCH_ALL_GROUPS = 'fetchAllGroupsForAUser'
        CREATE_ACCOUNT_GROUP = 'createAccountGroup'

        TRANSACTION_TYPES = enum(   ALL_NA = 'ALL N/A' ,
                                    ALL = 'ALL',
                                    ACH_OUT = 'ACH OUT',
                                    ALLOCATION = 'ALLOCATION',
                                    ASSIGNMENT = 'ASSIGNMENT',
                                    CA_Corporate_Action = 'CA Corporate Action',
                                    CHECK_OUT_Check_Withdrawal = 'CHECK OUT Check Withdrawal',
                                    CLOSURE = 'CLOSURE',
                                    DEPOSIT = 'DEPOSIT',
                                    DEPOSIT_ACH_ACH_Deposit = 'DEPOSIT ACH ACH Deposit',
                                    DEPOSIT_CHECK = 'DEPOSIT CHECK',
                                    DEPOSIT_DELIVERY_Delivery = 'DEPOSIT DELIVERY Delivery',
                                    DEPOSIT_INTEREST = 'DEPOSIT INTEREST',
                                    DEPOSIT_RECEIPT = 'DEPOSIT RECEIPT',
                                    DEPOSIT_WIRE_Wire_Deposit = 'DEPOSIT WIRE Wire Deposit',
                                    DIV_Dividend = 'DIV Dividend',
                                    EXERCISE = 'EXERCISE',
                                    FEE_Fees = 'FEE Fees',
                                    FUNDS_PLEDGED = 'FUNDS PLEDGED',
                                    INTEREST = 'INTEREST',
                                    JOURNAL = 'JOURNAL',
                                    LEAPS = 'LEAPS',
                                    MANUAL_ADJUSTMENT = ' MANUAL ADJUSTMENT',
                                    MONEY_ROLL_UP = 'MONEY ROLL UP',
                                    OPT_EXPIRATION_Option_Expiration = 'OPT_EXPIRATION Option Expiration',
                                    REVERSED_Reversal = 'REVERSED Reversal',
                                    SUB_JOURNAL = 'SUB JOURNAL ',
                                    SWEEP = 'SWEEP',
                                    TRADE = 'TRADE',
                                    TRANSFER = 'TRANSFER',
                                    WIRE_OUT = 'WIRE OUT',
                                    WITHDRAWAL = 'WITHDRAWAL',
                                    WITHHOLDING = 'WITHHOLDING'
        )

        PERFORMANCE_CATEGORY = enum( SYMBOL = 'SYMBOL', ASSET_CLASS = 'ASSET_CLASS', ACCOUNT_HISTORY = "ACCOUNT_HISTORY",
                                     TAGS = 'TAGS', TRADE_LOTS = 'TRADE_LOTS')

        ACCOUNT_TYPES = enum(MARGIN = 'MARGIN', OPTION = 'OPTION' )

        DEFAULT_FETCH_ACCOUNTS = '<retrieveCustomerAccounts/>'

        DEFAULT_FETCH_GROUPS = '<fetchAllGroupsForAUser/>'

        DEFAULT_DELETE_GROUPS = """ <deleteGroups>
                                        <groupIds></groupIds>
                                    </deleteGroups> """

        DEFAULT_ACCOUNT_HISTORY = """<getAccountHistory>
                                        <userId></userId>
                                        <timeRange>RANGE</timeRange> <!-- Can also be TODAY -->
                                        <numOfTransactions>1000</numOfTransactions>
                                        <accountIds></accountIds>
                                        <startTime> <!-- Time tags are not sent if timeRange is TODAY -->
                                            <year>2012</year>
                                            <month>01</month>
                                            <date>01</date>
                                            <hours>00</hours>
                                            <minutes>00</minutes>
                                            <seconds>00</seconds>
                                        </startTime>
                                        <endTime>
                                            <year>2012</year>
                                            <month>01</month>
                                            <date>22</date>
                                            <hours>23</hours>
                                            <minutes>59</minutes>
                                            <seconds>59</seconds>
                                            </endTime>
                                        <transactionTypes>ALL</transactionTypes> <!-- See list below -->
                                    </getAccountHistory> """

        DEFAULT_CUST_WIDGET = """<getCustomerWidgetData>
                                        <accountNumber></accountNumber>
                                        <streaming>true</streaming>
                                        <suppressHoldings>true</suppressHoldings>
                                        <suppressPnL>false</suppressPnL>
                                    </getCustomerWidgetData> """

        DEFAULT_ACCOUNT_PERFORMANCE = """<getAccountPerformance>
                                            <toDate>1337859125829</toDate>
                                            <accountNumber>2HC10320</accountNumber>
                                            <openOrClose />
                                            <fromDateVO>
                                                <dateObj>Thu May 24 00:00:00 GMT-0500 2012</dateObj> <date>24</date>
                                                <hours>0</hours>
                                                <year>2012</year>
                                                <seconds>0</seconds>
                                                <month>5</month>
                                                <minutes>0</minutes>
                                            </fromDateVO>
                                            <accountIds>1000000094122</accountIds>
                                            <toDateVO>
                                                <dateObj>Thu May 24 06:32:05 GMT-0500 2012</dateObj> <date>24</date>
                                                <hours>6</hours>
                                                <year>2012</year>
                                                <seconds>5</seconds>
                                                <month>5</month>
                                                <minutes>32</minutes>
                                            </toDateVO>
                                            <category>ACCOUNT_HISTORY</category>
                                            <timeFrame>RANGE</timeFrame>
                                            <fromDate>1337835600000</fromDate>
                                        </getAccountPerformance>"""


        DEFAULT_CASH_TRANSFER = """<getCashTransfers>
                                        <status>PENDING</status>
                                         <accountId></accountId>
                                    </getCashTransfers>"""


    class PositionRequests():

        DEFAULT_POSITIONS_DETAIL = """<getPositionsDetailNew>
                                        <accountIds></accountIds>
                                        <accountId></accountId>
                                        <loadSimulated>true</loadSimulated>
                                        <requireStrategy>false</requireStrategy>
                                        <suppressOpenPnL>true</suppressOpenPnL>
                                        <suppressDefaults>true</suppressDefaults>
                                        <filter />
                                    </getPositionsDetailNew>"""

        DEFAULT_POSITIONS_BASIC = """<getBasicPositionDetails>
                                        <symbol></symbol>
                                        <underlyer></underlyer>
                                    </getBasicPositionDetails>"""

        DEFAULT_POSITIONS_SELECTED = """<getSelectedPosition>
                                            <subscriptionIds>NaN</subscriptionIds>
                                            <accountIds></accountIds>
                                            <accountId></accountId>
                                            <symbol></symbol>
                                            <instrumentType></instrumentType>
                                            <loadSimulated>true</loadSimulated>
                                            <requireStrategy>true</requireStrategy>
                                            <filter />
                                        </getSelectedPosition>"""

        DEFAULT_POSITIONS_UNDERLIERS = """<getHeldUnderlyers>
                                                <accountId></accountId>
                                                <includeClosed>true</includeClosed>
                                           </getHeldUnderlyers> """

        DEFAULT_POSITIONS_TRANSACTIONS = """<getTxHistoryForInstrument>
                                                <accountId></accountId>
                                                <positionType></positionType>
                                                <symbol></symbol>
                                                <instrumentType></instrumentType>
                                                <userId></userId>
                                            </getTxHistoryForInstrument> """

    class OrderRequests():

        ORDER_SPREAD_TYPES = enum(BACKSPREAD = 'Backspread',
                                    BUTTERFLY = 'Butterfly',
                                    CALENDAR = 'Calendar',
                                    CALL_BACKSPREAD = 'Call Backspread',
                                    CALL_CALENDAR = 'Call Calendar',
                                    CALL_DIAGONAL = 'Call Diagonal',
                                    CALL = 'Call',
                                    CALL_BUTTERFLY = 'Call Butterfly',
                                    CALL_CONDOR = 'Call Condor',
                                    CALL_VERTICAL = 'Call Vertical',
                                    COMBINATION = 'Combination',
                                    CONDOR = 'Condor',
                                    COVERED = 'Covered',
                                    COVERED_CALL = 'Covered Call',
                                    CUSTOM_SPREAD  = 'Custom Spread',
                                    IRON_CONDOR = 'Iron Condor',
                                    IRON_BUTTERFLY = 'Iron Butterfly',
                                    PUT = 'Put',
                                    PUT_BUTTERFLY = 'Put Butterfly',
                                    PUT_CONDOR = 'Put Condor',
                                    PROTECTIVE_PUT = 'Protective Put',
                                    PUT_BACKSPREAD = 'Put Backspread',
                                    PUT_CALENDAR = 'Put Calendar',
                                    PUT_DIAGONAL = 'Put Diagonal',
                                    PUT_VERTICAL = 'Put Vertical',
                                    SINGLE_OPTION = 'SingleOption',
                                    STOCK = 'Stock',
                                    SHARES = 'Shares',
                                    STRADDLE = 'Straddle',
                                    STRANGLE = 'Strangle',
                                    SYNTHETIC_STOCK = 'Synthetic Stock',
                                    VERTICAL = 'Vertical',
                                    VERTICAL_COLLAR = 'VerticalCollar',
                                    VERTICAL_SPREAD = 'Vertical Spread')

        DEFAULT_SINGLE_LEG_ORDER = """<sendOrder>
                                        <accountType>OPTION</accountType>
                                        <modifyOrder>false</modifyOrder>
                                        <originalOrderId>NaN</originalOrderId>
                                        <combineLikeLegs>false</combineLikeLegs>
                                        <accountNumber>A0000019</accountNumber>
                                        <userId>1000000009867</userId>
                                        <limitPrice>2.74</limitPrice>
                                        <stopTriggerPrice>NaN</stopTriggerPrice> <!-- = Stop Price if Client selected Stop order -->
                                        <trailingAmount>NaN</trailingAmount> <!-- = Trailing Amount if Client selected Trail Stop -->
                                        <source>___</source>
                                        <orderId>NaN</orderId>
                                        <priceType>LM</priceType>
                                        <quantity>1000</quantity>
                                        <holdOrder>false</holdOrder>
                                        <duplicateOrder>false</duplicateOrder>
                                        <discretionFlag>false</discretionFlag>
                                        <solicitedFlag>false</solicitedFlag>
                                        <instrumentType>Equity</instrumentType>
                                        <orderLegEntries>
                                            <symbol>COOL</symbol>
                                            <orderSide>BUY</orderSide>
                                            <quantityRatio>1</quantityRatio>
                                            <instrumentType>Equity</instrumentType>
                                        </orderLegEntries>
                                        <timeInForce>DAY</timeInForce>
                                        <marketSession>REG</marketSession>
                                        <gtdDate></gtdDate>
                                        <noteVo>
                                            <userId></userId>
                                            <objectType>null</objectType>
                                            <noteText />
                                            <objectIds>NaN</objectIds>
                                        </noteVo>
                                        </sendOrder>"""

        DEFAULT_MULTI_LEG_ORDER = """<sendOrder>
                                        <accountType>OPTION</accountType>
                                        <modifyOrder>false</modifyOrder>
                                        <originalOrderId>NaN</originalOrderId>
                                        <combineLikeLegs>false</combineLikeLegs>
                                        <accountNumber>2HC08522</accountNumber>
                                        <displayQuantity>NaN</displayQuantity>
                                        <gtdDate>NaN</gtdDate>
                                        <userId>1000000000966</userId>
                                        <limitPrice>0.03</limitPrice>
                                        <stopTriggerPrice>NaN</stopTriggerPrice>
                                        <trailingAmount>NaN</trailingAmount>
                                        <discretionAmount>NaN</discretionAmount>
                                        <offSetAmount>NaN</offSetAmount>
                                        <source> </source> <!-- Required to be filled in with TM-assigned value --> <orderId>NaN</orderId>
                                        <priceType>LM</priceType>
                                        <quantity>10</quantity>
                                        <holdOrder>false</holdOrder>
                                        <duplicateOrder>false</duplicateOrder>
                                        <discretionFlag>false</discretionFlag>
                                        <solicitedFlag>false</solicitedFlag>
                                        <instrumentType>Option</instrumentType>
                                        <spreadName>Call Vertical</spreadName>
                                        <orderSide>BUY</orderSide>
                                        <orderLegEntries>
                                            <!-- Intentionally left blank -->
                                        </orderLegEntries>

                                        <timeInForce>DAY</timeInForce>
                                        <marketSession>REG</marketSession>
                                        <noteVo>
                                            <userId>1000000000966</userId>
                                            <objectType>null</objectType>
                                            <noteText />
                                            <objectIds>NaN</objectIds>
                                        </noteVo>
                                        </sendOrder>
                                        """


        DEFAULT_ORDER_CONFIRMATION = """<populateConfirmation>
                                            <accountType>OPTION</accountType>
                                            <modifyOrder>false</modifyOrder>
                                            <originalOrderId>NaN</originalOrderId>
                                            <combineLikeLegs>false</combineLikeLegs>
                                            <accountNumber>67110437</accountNumber>
                                            <displayQuantity>NaN</displayQuantity>
                                            <gtdDate>NaN</gtdDate>
                                            <userId>1000000000876</userId>
                                            <limitPrice>100.05</limitPrice>
                                            <stopTriggerPrice>NaN</stopTriggerPrice>
                                            <trailingAmount>NaN</trailingAmount>
                                            <discretionAmount>NaN</discretionAmount>
                                            <offSetAmount>NaN</offSetAmount>
                                            <source></source>
                                            <orderId>NaN</orderId>
                                            <priceType>LM</priceType>
                                            <quantity>100</quantity>
                                            <holdOrder>false</holdOrder>
                                            <duplicateOrder>false</duplicateOrder>
                                            <discretionFlag>false</discretionFlag>
                                            <solicitedFlag>false</solicitedFlag>
                                            <instrumentType>Equity</instrumentType>
                                            <orderLegEntries>
                                                <!-- intentionally left blank -->
                                            </orderLegEntries>
                                            <timeInForce>DAY</timeInForce>
                                            <marketSession>REG</marketSession>
                                            <noteVo>
                                                <userId>1000000000876</userId>
                                                <objectType>null</objectType>
                                                <noteText/>
                                                <objectIds>NaN</objectIds>
                                            </noteVo>
                                        </populateConfirmation> """

        DEFAULT_MUTUAL_FUND_ORDER = """<sendMFOrder>
                                            <orderSide>BUY</orderSide>
                                            <accountNumber>2HC08522</accountNumber>
                                            <instrumentType>MutualFund</instrumentType>
                                            <symbol>PRNEX</symbol>
                                            <dividendType>Cash</dividendType>
                                            <accountType>Cash</accountType>
                                            <userId>1000000000966</userId>
                                            <source> </source> <!-- Required to be filled in with TM-assigned value -->
                                            <amount>5000</amount>
                                            <noteVo>
                                                <userId>1000000000966</userId>
                                                <objectType>null</objectType>
                                                <noteText />
                                                <objectIds>NaN</objectIds>
                                            </noteVo>
                                        </sendMFOrder>"""

        DEFAULT_ORDER_CANCEL = """<cancelOrder></cancelOrder>"""

        DEFAULT_ORDER_CANCEL_ALL = """<cancelAllOrders></cancelAllOrders>"""

        DEFAULT_ORDER_CANCEL_DAY = """<cancelDayOrders></cancelDayOrders>"""

        DEFAULT_ALL_OPEN_ORDERS_COUNT = """<getCancelAllOrdersCount></getCancelAllOrdersCount>"""

        DEFAULT_DAY_ORDERS_COUNT = """<getCancelDayOrdersCount></getCancelDayOrdersCount>"""

        DEFAULT_LOAD_ORDER_BOOK = """<loadOrderBook>
                                        <dateRange>1</dateRange>
                                        <accountNumber></accountNumber>
                                        <statusList></statusList> <!-- create a new tag for each status -->
                                    </loadOrderBook>"""

        DEFAULT_LOAD_SPECIFIC_ORDERS = """<loadSpecifiedOrders>
                                            <orderIds></orderIds> <!-- create a new tag for each orderIds -->
                                            <filtersOn>false</filtersOn>
                                        </loadSpecifiedOrders>"""

        DEFAULT_GET_ORDER_HISTORY = """<getOrderHistory></getOrderHistory>"""

        DEFAULT_GET_ORDER_DETAIL = """<getOrderDetail></getOrderDetail>"""


    class QuotesRequests():
        DEFAULT_OPTION_CHAIN_REQUEST = """<getOptionChain>
                                        <symbol></symbol>
                                    </getOptionChain> """

        DEFAULT_QUOTE_REQUEST = """<getQuotes>
                                        <blank></blank>
                                    </getQuotes>"""


    class ResponseRoots():
        RETRIEVE_ACCT_ROOT = 'ns2:retrieveCustomerAccountsResponse'
        RETRIEVE_ACCT_HISTORY_ROOT = 'ns2:getAccountHistoryResponse'
        RETRIEVE_ACCT_PERFORMANCE_ROOT = 'ns2:getAccountPerformanceResponse'
        RETRIEVE_ORDER_PLACED_ROOT = 'ns2:sendOrderResponse'
        RETRIEVE_ORDER_CONFIRMATION_ROOT = 'ns2:populateConfirmationResponse'
        RETRIEVE_ORDER_CANCELLED_ROOT = 'ns1:cancelOrder'
        RETRIEVE_ORDER_DETAILS_ROOT = 'ns2:getOrderDetailResponse'
        RETRIEVE_ALL_CANCELLED_ROOT = 'ns2:cancelAllOrdersResponse'
        RETRIEVE_DAY_CANCELLED_ROOT = 'ns2:cancelDayOrdersResponse'
        RETRIVE_ALL_CANCELLED_COUNT_ROOT = 'ns2:getCancelAllOrdersCountResponse'
        RETRIVE_DAY_CANCELLED_COUNT_ROOT = 'ns2:getCancelDayOrdersCountResponse'
        RETRIEVE_QUOTE_CHAIN_ROOT = 'ns2:getOptionChainResponse'
        RETRIEVE_QUOTE_SYMBOL_ROOT = 'ns2:getQuotesResponse'


