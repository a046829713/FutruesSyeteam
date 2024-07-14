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

    #查詢全部選擇權合約
    # print( "" )
    # print( "查詢全部選擇權合約：" )
    # res = g_QuoteZMQ.QueryAllInstrumentInfo(g_QuoteSession,"Opt")
    # print( type( res ) )
    # print( res )

    #實時行情訂閱
    #設定合約代碼，測試時請注意範例的合約是否已經下市。
    testSymbol = "TC.O.TWF.TXO.202403.C.19500"

    #實時Greeks訂閱
    g_QuoteZMQ.SubGreeks(g_QuoteSession, testSymbol)

    print("即時 Greeks 數據展示中....")

    for i in range(50):
        time.sleep( 0.5 )

    print("展示完成....")
    thread_stop = True


    #解除訂閱
    g_QuoteZMQ.UnsubGreeks(g_QuoteSession, testSymbol)

    #斷開連線
    g_QuoteZMQ.Logout(g_QuoteSession)
    print("中斷連線中...")

############################
#    Greeks 即時行情欄位表  #
############################

# 實時Greeks {
# 	'UnderlyingAsset': '', 
# 	'Symbol': 'TC.O.TWF.TXO.202201.C.18400', 
# 	'GreeksType': 'REAL', 
# 	'TradingDay': '20220104', 
# 	'TradingHours': '25923', 
# 	'Last': '', 
# 	'Vol': '', 
# 	'Bid': '', 
# 	'Ask': '', 
# 	'ImpVol': '12.6', 
# 	'BIV': '12.57', 
# 	'SIV': '12.7', 
# 	'Delta': '55.19', 
# 	'Gamma': '0.0008', 
# 	'Vega': '15.5378', 
# 	'Theta': '-8.7793', 
# 	'Rho': '-9.4395', 
# 	'TheoVal': '228.036', 
# 	'ExtVal': '170', 
# 	'Margin': '', 
# 	'OI': '', 
# 	'PreOI': '', 
# 	'IntVal': '58', 
# 	'PreImpVol': '12.19', 
# 	'UndVol': '', 
# 	'UndOI': '', 
# 	'VIX': '', 
# 	'HV_W4': '', 
# 	'HV_W8': '', 
# 	'HV_W13': '', 
# 	'HV_W26': '', 
# 	'HV_W52': '', 
# 	'PreciseTime': '25923', 
# 	'us': '', 
# 	'us_d': '', 
# 	'us_t': '', 
# 	'us_p': '', 
# 	'us_bp1': '', 
# 	'us_sp1': '', 
# 	'uf': '', 
# 	'uf_d': '', 
# 	'uf_t': '', 
# 	'uf_p': '', 
# 	'uf_bp1': '', 
# 	'uf_sp1': '', 
# 	'usf': '', 
# 	'usf_d': '', 
# 	'usf_t': '', 
# 	'usf_p': '', 
# 	'E0_ImpVol': '', 
# 	'E0_PreImpVol': '', 
# 	'E0_Delta': '', 
# 	'E0_Gamma': '', 
# 	'E0_Vega': '', 
# 	'E0_Theta': '', 
# 	'E0_Rho': '', 
# 	'E0_Charm': '', 
# 	'E0_Vanna': '', 
# 	'E0_Vomma': '', 
# 	'E0_Speed': '', 
# 	'E0_Zomma': '', 
# 	'E0_CPIV': '', 
# 	'E0_MIV': '', 
# 	'E0_Calld': '', 
# 	'E0_Putd': '', 
# 	'E0_FIV': ''
# }