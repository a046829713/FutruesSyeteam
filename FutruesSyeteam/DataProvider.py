# 載入 tcoreapi
from tcoreapi_mq import QuoteAPI
import re
import datetime
import time
import threading
import json
# 載入我們提供的行情 function
from quote_functions import quote_sub_th, GetHistory
from dateutil.relativedelta import relativedelta
import pandas as pd
from datetime import timedelta

class DataProvider():
    def __init__(self) -> None:
        # 建立 ZMQ 聯綫

        # 設定連綫授權碼，通常不用改。
        self.g_QuoteZMQ = QuoteAPI("ZMQ", "8076c9867a372d2a9a814ae710c256e2")

        self.q_data = self.g_QuoteZMQ.Connect("51237")

        while self.q_data["Success"] != "OK":
            # 連線失敗。
            print("[ quote ]connection failed - 連線失敗")
            time.sleep(5)
            this_port = self.checkLogPort()
            self.q_data = self.g_QuoteZMQ.Connect(this_port)
        else:
            # 連綫成功后，將取得的 Session Key 儲存下來，後面調用指令需要帶入。
            self.g_QuoteSession = self.q_data["SessionKey"]
            print(f"連線成功-連線金鑰:{self.g_QuoteSession}")
    
    def logout(self):        
        print("展示完成....")        
        #斷開連線
        self.g_QuoteZMQ.Logout(self.g_QuoteSession)
        print("中斷連線中...")
    
    def checkLogPort(self):
        # 設定連接 Port，通常不用改 3.0 = 51237, 4.0 = 50774。
        # 如果無法連線，可能是 port 被占用，可以到 TC安裝路徑\APPs\TCoreRelease\Logs 找日期最新的 QuoteZMQService-xxxxxx-0.log
        # 搜尋  RepPort: ，即可取得連線 Port
        # 20240406
        today_str = datetime.datetime.now().date().strftime("%Y%m%d")
        TCLOGPATH = r'C:\TOUCHANCE\APPs\TCoreRelease\Logs' + \
            f'\QuoteZMQService-{today_str}-0.log'
        with open(TCLOGPATH, 'r+') as file:
            results = re.findall('RepPort:(\d+)', file.read())

        finally_port = results[-1]
        return finally_port

    def GetQueryAllInstrumentInfo(self,save=False):
        AllInstrumentInfo = self.g_QuoteZMQ.QueryAllInstrumentInfo(
            self.g_QuoteSession, type='Fut')        

        if save:
            data = json.dumps(AllInstrumentInfo)
            
            with open('AllInstrumentInfo.txt', 'w+') as file:
                file.write(data)
        else:
            return AllInstrumentInfo
        

    def get_traget_symbol(self, traget_symbol):
        """
            input:
                like this EMD
            取得熱門月的完整代碼
            ['TC.F.CME.EMD.HOT']
        """
        # 輸入代碼取得相關資料
        data = self.GetQueryAllInstrumentInfo()

        # with open("AllInstrumentInfo.txt",'r') as file:
        #     data = json.loads(file.read())
            
        all_output = []
        all_instruments = data['Instruments']['Node']
        for each_maket_info in all_instruments:
            for key,value in each_maket_info.items():
                if key == 'Node' and value:
                    all_output.extend(value[0]['Contracts'])
   
        out_put = []
        for each_symbol in all_output:
            if traget_symbol in each_symbol:
                out_put.append(each_symbol)

        print(out_put)
        return out_put

        
    def get_data_range(self,sD="2010010100"):
        begin_date = datetime.datetime.strptime(sD, "%Y%m%d%H")
        end_date = begin_date + timedelta(days=150)

        if end_date > datetime.datetime.now():
            end_date = datetime.datetime.now().date()

        return begin_date.strftime("%Y%m%d%H"),end_date.strftime("%Y%m%d%H")
    
    def changeDatetime(self, x):
        if len(x) != 14:
            output = x[:8] + '0' * (14 - len(x) )+ x[8:]
            output = datetime.datetime.strptime(output, "%Y%m%d%H%M%S").strftime("%Y/%m/%d %H:%M:%S")
            return output
        else:
            return datetime.datetime.strptime(x, "%Y%m%d%H%M%S").strftime("%Y/%m/%d %H:%M:%S")
    
    def reload(self,Symbol:str):
        """
            Symbol:str:
                "TC.F.TWF.TXF.HOT"
            # 設定合約代碼，測試時請注意範例的合約是否已經下市。
            # 使用 HOT 可以取得連續月資料
            

            # 訂閱歷史數據
            # message["DataType"]="TICKS"   ticks
            # message["DataType"]="1K"   1K
            # message["DataType"]="DK"   日K
            # message["DataType"]="DOGSS"   Greeks 秒數據
            # message["DataType"]="DOGSK"   Greeks 分鐘數據
            
            # 回補區間設定
            # yyyymmddHH, HH 00-23
            # 請特別注意，我們提供的是 +0 的時間，所以如果你需要取得台灣 +8 的時間
            # 例如：下午 1500 - 1700，請自己先減 8，HH 07-09
            # 取得的資料，請再自己 +8，轉換為台灣時區
        """
        # 建立一個執行緒用來處理即時行情與歷史資料
        thread_stop = False
        # TC 好似有個訂閱port
        t1 = threading.Thread(target=quote_sub_th, args=(
            self.g_QuoteZMQ, self.q_data["SubPort"], lambda: thread_stop))
        t1.start()

        ktype = '1K'        
        begin_date = "2010010100"
        all_df = pd.DataFrame()

        NO_data_list = []
        while True:
            begin_date , end_date = self.get_data_range(begin_date)
            print("開始日期:",begin_date,"結束日期:",end_date)
            if begin_date == end_date:break
            df = GetHistory(self.g_QuoteZMQ, self.g_QuoteSession, Symbol, ktype, begin_date, end_date)
            print(df)
            if df.empty:
                NO_data_list.append((begin_date,end_date))
            all_df = pd.concat([all_df,df])
            begin_date = end_date
            time.sleep(1)
 
        print("本次回補沒有資料的日期:",NO_data_list)
        # 20130718220100
        all_df['NewDatetime'] = all_df['Date'].astype(str) + all_df['Time'].astype(str)
        all_df['NewDatetime'] = all_df['NewDatetime'].apply(self.changeDatetime)
        all_df = all_df.drop_duplicates(subset=['NewDatetime'])# 回補完要拋棄重複的部分


        all_df['Date'] = all_df['NewDatetime'].apply(lambda x : x.split(' ')[0])
        all_df['Time'] = all_df['NewDatetime'].apply(lambda x : x.split(' ')[1])

        
        
        all_df = all_df.drop(columns=['OI','QryIndex','NewDatetime','UnchVolume'])
        all_df.set_index('Date',inplace=True)
        # 列印下載完成的歷史資料
        all_df.to_csv(Symbol + '.csv')
        print("下載完成")        
        thread_stop = True

if __name__ == '__main__':
    app = DataProvider()
    app.reload('TC.F.CME.QG.HOT')
    # app.get_traget_symbol('QG')
