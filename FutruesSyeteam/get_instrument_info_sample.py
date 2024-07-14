#載入 tcoreapi
from tcoreapi_mq import * 
#載入我們提供的行情 function
from quote_functions import *
import pandas as pd


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

    #連綫成功后，將取得的 Session Key 儲存下來，後面調用指令需要帶入。
    g_QuoteSession = q_data["SessionKey"]

    #建立一個執行緒用來處理即時行情與歷史資料
    thread_stop = False
    t1 = threading.Thread(target = quote_sub_th,args=(g_QuoteZMQ,q_data["SubPort"], lambda: thread_stop))
    t1.start()

    #設定合約代碼，測試時請注意範例的合約是否已經下市。
    testSymbol = "TC.F.TWF.MXF.202403"

    #查詢指定合約資訊
    print( "" )
    print( "查詢指定合約：", testSymbol )

    res = g_QuoteZMQ.QueryInstrumentInfo(g_QuoteSession, testSymbol )
    print( type( res ) )
    print( res )

    print("------------------")
    #查詢全部期貨合約
    #查詢指定類型合約列表
    #期貨：Fut
    #期權：Opt
    #證券：Stock

    print( "" )
    print( "查詢全部期貨合約：" )
    res = g_QuoteZMQ.QueryAllInstrumentInfo(g_QuoteSession,"Fut")
    print( type( res ) )
    print( res )

    print("展示完成....")
    thread_stop = True

    #斷開連線
    g_QuoteZMQ.Logout(g_QuoteSession)
    print("中斷連線中...")