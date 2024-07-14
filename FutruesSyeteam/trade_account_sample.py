#載入 tcoreapi
from tcoreapi_mq import * 
#載入我們提供的交易 function
from trade_functions import *
import threading
import json

global g_TradeZMQ
global g_TradeSession

#登入
g_TradeZMQ = TradeAPI("ZMQ","8076c9867a372d2a9a814ae710c256e2")

#設定連接 Port，通常不用改 3.0 = 51207, 4.0 = 50744。
#如果無法連線，可能是 port 被占用，可以到 TC安裝路徑\APPs\TCoreRelease\Logs 找日期最新的 TradeZMQService-xxxxxx-0.log
#搜尋  RepPort: ，即可取得連線 Port
t_data = g_TradeZMQ.Connect("50744")

if t_data["Success"] != "OK":
    #連線失敗。
    print("[trade]connection failed")
    print('連線失敗!\n可能是 port 被占用，請到 TC安裝路徑\\APPs\\TCoreRelease\\Logs \n找日期最新的 TradeZMQService-xxxxxx-0.log,搜尋  RepPort: ，即可取得連線 Port')
else:

    g_TradeSession = t_data["SessionKey"]

    #登出
    #t_logout= g_TradeZMQ.Logout(t_data["SessionKey"])
    #print(t_logout)

    #創建一個交易線程處理交易與帳務相關的請求
    thread_stop = False
    t1 = threading.Thread(target = trade_sub_th,args=(g_TradeZMQ, g_TradeSession,t_data["SubPort"], lambda: thread_stop))
    t1.start()

    #設定合約代碼，測試時請注意範例的合約是否已經下市。
    #使用 HOT 可以取得最新的合約月份
    testSymbol = "TC.F.TWF.MXF.HOT"

    #查詢已登入資金賬戶
    accountInfo = g_TradeZMQ.QryAccount(g_TradeSession)
    strAccountMask=""

    if accountInfo != None:
        arrInfo = accountInfo["Accounts"]
        if len(arrInfo) != 0:
            #print("@@@@@@@@@@@:",arrInfo[0],"\n")
            strAccountMask = arrInfo[0]["AccountMask"]
            
            #查詢委託記錄
            reportData = g_TradeZMQ.QryReport( g_TradeSession,"" )
            ShowEXECUTIONREPORT(g_TradeZMQ, g_TradeSession, reportData)
            print("")
            fillReportData = g_TradeZMQ.QryFillReport( g_TradeSession,"" )
            ShowFillReport( g_TradeZMQ, g_TradeSession, fillReportData )
            print("")

            #查詢資金
            if strAccountMask !="":
                res = g_TradeZMQ.QryMargin( g_TradeSession, strAccountMask )
                print( "資金查詢結果：")
                print( type( res ))
                print( res )
                print("")
            
            #查詢持倉
            positionData = g_TradeZMQ.QryPosition( g_TradeSession , strAccountMask,"" )
            print( "持倉查詢結果：")
            print( type( positionData ))
            print( positionData['Positions'] )
            print("")
            # ShowPOSITIONS( g_TradeZMQ, g_TradeSession, strAccountMask, positionData )
            # print("")

            #下單（限價單範例）
            # Side          
            ##    1 : Buy
            ##    2:Sell
            # TimeInForce   
            ##    1 : ROD,
            ##    2 : IOC/FAK
            ##    3 : FOK
            # OrderType
            ##    1 : Market order
            ##    2 : Limit order 
            ##    3 : Stop order 
            ##    4 : Stop limit order 
            ##    5 : Trailing Stop
            ##    6 : Trailing StopLimit
            ##    7 : Market if Touched Order
            ##    8 : Limit if Touched Order
            ##    9 : Trailing Limit
            ##    10 : 對方價(HIT)
            ##    11 : 本方價(JOIN)
            ##    15 : 中間價(MID)
            ##    20 : 最優價 (BST)
            ##    21 : 最優價轉限價 (BSTL)
            ##    22 : 五檔市價 (5LvlMKT)
            ##    23 : 五檔市價轉限價 (5LvlMTL)
            ##    24 : 市價轉限價 (MTL)
            ##    25 : 一定範圍市價(MWP)
            # PositionEffect
            ##    0 : 開倉  Open position
            ##    1 : 平倉  Close position
            ##    2 : 平今
            ##    3 : 平昨
            ##    4 : 自動   Auto select Open/Cloe position
            ##    10 : 備兌開倉
            ##    11 : 備兌平倉

            orders_obj = {
                "Symbol": testSymbol,
                "BrokerID":arrInfo[0]['BrokerID'],
                "Account":arrInfo[0]['Account'],
                "Price":"18400",
                "TimeInForce":"1",
                "Side":"1",
                "OrderType":"2",
                "OrderQty":"1",
                "PositionEffect":"4"
            }

            #打開注解會下單，請特別小心！
            #s_order = g_TradeZMQ.NewOrder( g_TradeSession, orders_obj )
            s_order = json.loads( '{"Reply": "NEWORDER", "Success": "OK"}' )
            print( s_order )

            if s_order['Success']=="OK":
                print("下單成功")
            elif s_order['ErrCode']=="-10":
                print("unknow error")
            elif s_order['ErrCode']=="-11":
                print("買賣別錯誤")
            elif s_order['ErrCode']=="-12":
                print("覆式單商品代碼解晰錯誤 ")
            elif s_order['ErrCode']=="-13":
                print("下單賬號, 不可下此交易所商品")
            elif s_order['ErrCode']=="-14":
                print("下單錯誤, 不支持的價格 或 OrderType 或 TimeInForce ")
            elif s_order['ErrCode']=="-15":
                print("不支援證券下單")
            elif s_order['ErrCode']=="-20":
                print("聯機未建立")
            elif s_order['ErrCode']=="-22":
                print("價格的 TickSize 錯誤")
            elif s_order['ErrCode']=="-23":
                print("下單數量超過該商品的上下限 ")
            elif s_order['ErrCode']=="-24":
                print("下單數量錯誤 ")
            elif s_order['ErrCode']=="-25":
                print("價格不能小於和等於 0 (市價類型不會去檢查) ")
            elif s_order['sample_message']=='988':
                print("打開注解才能下單")
            
            #改單
            # ReportID
            ##    請帶入回報編號
            # ReplaceExecType
            ##    0:改價
            ##    1:改量
            ##    2:改價改量
            # Price
            ##    期望的委託價格
            # OrderQty
            ##    期望減少的數量
            # StopPrice
            ##    期望的停損價格

            reporders_obj={
                "ReportID":"2144112706C",
                "ReplaceExecType":"0",
                "Price":"18350"
            }

            reorder=g_TradeZMQ.ReplaceOrder( g_TradeSession, reporders_obj )
            print("%%%%%%%%%%%%%%%%%%%%%%%%%",reorder)

            #刪單
            # ReportID
            ##    請帶入回報編號
            canorders_obj={
                "ReportID":"2144112706C",
            }

            canorder=g_TradeZMQ.CancelOrder( g_TradeSession ,canorders_obj )
            print("%%%%%%%%%%%%%%%%%%%%%%%%%",canorder)

    #查詢持倉監控
    QryPositionTracker( g_TradeZMQ, g_TradeSession )

    print("展示完成....")
    thread_stop = True
    #斷開連線
    g_TradeZMQ.Logout(g_TradeSession)
    print("中斷連線中...")