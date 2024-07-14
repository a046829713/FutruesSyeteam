#載入 tcoreapi
from tcoreapi_mq import * 
#載入我們提供的行情 function
from quote_functions import *
import threading

#建立 ZMQ 連線

#設定連線授權碼，通常不用改。
g_QuoteZMQ = QuoteAPI("ZMQ","8076c9867a372d2a9a814ae710c256e2")

#設定連接 Port，通常不用改 3.0 = 51237, 4.0 = 50774。
#如果無法連線，可能是 port 被占用，可以到 TC安裝路徑\APPs\TCoreRelease\Logs 找日期最新的 QuoteZMQService-xxxxxx-0.log
#搜尋  RepPort: ，即可取得連線 Port
q_data = g_QuoteZMQ.Connect("50774")

if q_data["Success"] != "OK":
    #連線失敗。
    print("[ quote ]connection failed")
    print("連線失敗!\n可能是 port 被占用，請到 TC安裝路徑\\APPs\\TCoreRelease\\Logs \n找日期最新的 QuoteZMQService-xxxxxx-0.log 搜尋  RepPort: ，即可取得連線 Port")
else:

    #連線成功后，將取得的 Session Key 儲存下來，後面調用指令需要帶入。
    g_QuoteSession = q_data["SessionKey"]

    #建立一個執行緒用來處理即時行情與歷史資料
    thread_stop = False
    t1 = threading.Thread(target = quote_sub_th,args=(g_QuoteZMQ,q_data["SubPort"], lambda: thread_stop))
    t1.start()
    
    #實時行情訂閱
    #設定合約代碼，測試時請注意範例的合約是否已經下市。
    #使用 HOT 可以取得最新合約即時數據
    testSymbol = "TC.F.TWF.MXF.HOT"


    #訂閱實時行情
    g_QuoteZMQ.SubQuote(g_QuoteSession, testSymbol)

    print("即時 Greeks 數據展示中....")

    for i in range(10):
        time.sleep( 0.5 )

    print("展示完成....")
    thread_stop = True

    #解除訂閱
    g_QuoteZMQ.UnsubGreeks(g_QuoteSession, testSymbol)

    #斷開連線
    g_QuoteZMQ.Logout(g_QuoteSession)
    print("中斷連線中...")

#####################
#    即時行情欄位表  #
#####################

# {
# 	'Symbol': 'TC.F.TWF.MXF.202201', 
# 	'Exchange': 'TWF', 
# 	'ExchangeName': '台灣期交所', 
# 	'Security': 'FIMTX', 
# 	'SecurityName': '小臺', 
# 	'SecurityType': '6', 
# 	'TradeQuantity': '1', 
# 	'FilledTime': '23305', 
# 	'TradeDate': '20220104', 
# 	'FlagOfBuySell': '2', 
# 	'OpenTime': '84500', 
# 	'CloseTime': '50000', 
# 	'BidVolume': '14', 
# 	'BidVolume1': '29', 
# 	'BidVolume2': '34', 
# 	'BidVolume3': '29', 
# 	'BidVolume4': '22', 
# 	'BidVolume5': '0', 
# 	'BidVolume6': '0', 
# 	'BidVolume7': '0', 
# 	'BidVolume8': '0', 
# 	'BidVolume9': '0', 
# 	'AskVolume': '20', 
# 	'AskVolume1': '37', 
# 	'AskVolume2': '30', 
# 	'AskVolume3': '38', 
# 	'AskVolume4': '60', 
# 	'AskVolume5': '0', 
# 	'AskVolume6': '0', 
# 	'AskVolume7': '0', 
# 	'AskVolume8': '0', 
# 	'AskVolume9': '0', 
# 	'TotalBidCount': '57880', 
# 	'TotalBidVolume': '93622', 
# 	'TotalAskCount': '56531', 
# 	'TotalAskVolume': '89091', 
# 	'BidSize': '58369', 
# 	'AskSize': '61200', 
# 	'FirstDerivedBidVolume': '2', 
# 	'FirstDerivedAskVolume': '3', 
# 	'BuyCount': '57880', 
# 	'SellCount': '56531', 
# 	'EndDate': '20220119', 
# 	'BestBidVolume': '14', 
# 	'BestAskVolume': '20', 
# 	'BeginDate': '20211021', 
# 	'YTradeDate': '0', 
# 	'ExpiryDate': '16', 
# 	'TradingPrice': '18461', 
# 	'Change': '189', 
# 	'TradeVolume': '85581', 
# 	'OpeningPrice': '18350', 
# 	'HighPrice': '18497', 
# 	'LowPrice': '18350', 
# 	'ClosingPrice': '', 
# 	'ReferencePrice': '18272', 
# 	'UpperLimitPrice': '20099', 
# 	'LowerLimitPrice': '16445', 
# 	'YClosedPrice': '18365', 
# 	'YTradeVolume': '44762', 
# 	'Bid': '18459', 
# 	'Bid1': '18458', 
# 	'Bid2': '18457', 
# 	'Bid3': '18456', 
# 	'Bid4': '18455', 
# 	'Bid5': '', 
# 	'Bid6': '', 
# 	'Bid7': '', 
# 	'Bid8': '', 
# 	'Bid9': '', 
# 	'Ask': '18461', 
# 	'Ask1': '18462', 
# 	'Ask2': '18463', 
# 	'Ask3': '18464', 
# 	'Ask4': '18465', 
# 	'Ask5': '', 
# 	'Ask6': '', 
# 	'Ask7': '', 
# 	'Ask8': '', 
# 	'Ask9': '', 
# 	'PreciseTime': '23305406000', 
# 	'FirstDerivedBid': '18456', 
# 	'FirstDerivedAsk': '18463', 
# 	'SettlementPrice': '', 
# 	'BestBid': '18459', 
# 	'BestAsk': '18461', 
# 	'Deposit': '', 
# 	'TickSize': '', 
# 	'TradeStatus': '', 
# 	'OpenInterest': '0'
# }