import json
import pandas as pd
import datetime
import time


class DataTransformer():
    def __init__(self) -> None:
        pass



    def paser_AllInstrumentInfo(self):
        """
            用來解析所有的交易所期貨商品
        """

        with open("AllInstrumentInfo.txt" ,'r') as file:
            data = json.loads(file.read())
        
        
        
        if data['Success'] != "OK":
            raise ValueError("the something wrong with TC")
        
        for exchange_info  in data['Instruments']['Node']:
            # 優先解析CME
            if exchange_info['ENG'] == 'CME':
                print(exchange_info)
                print('*'*120)

    def time_price_check(self,history_file:str,price:float):
        df = pd.read_csv(history_file)
        error_df = df[(df['High'] > price) | (df['Low'] > price) |(df['Close'] > price) | (df['Open'] > price)]
        print(error_df)
        error_df.to_csv("異常資料區間.csv")

    def cut_off_MC_need(self, history_file:str, local_file:str):
        """
            history_file = 'TC.F.CME.QG.HOT.csv',
            local_file = 'CME.QG HOT-Minute-Trade.txt'
        """
        df = pd.read_csv(history_file)
        df.rename(columns={
            "Volume":"TotalVolume",
            "UpTick":"UpTicks",
            "DownTick":"DownTicks",
                        },inplace=True)

        df ['TotalTicks'] = df['UpTicks'] + df['DownTicks']
        df = df[['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'UpVolume','DownVolume', 'TotalVolume', 'UpTicks', 'DownTicks', 'TotalTicks']]
        df['NewDatetime'] = df['Date'] + ' ' + df['Time']
        df['NewDatetime'] = pd.to_datetime(df['NewDatetime'])


        local_data = pd.read_csv(local_file)
        local_datetimefisrt = datetime.datetime.strptime(local_data.iloc[0]['Date'] + ' ' + local_data.iloc[0]['Time'],"%Y/%m/%d %H:%M:%S")
        df = df[df['NewDatetime'].apply(lambda x : True if x < local_datetimefisrt else False)]

        df = df[['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'UpVolume',
            'DownVolume', 'TotalVolume', 'UpTicks', 'DownTicks', 'TotalTicks']]
        df.set_index('Date',inplace =True)
        df.to_csv(f'MC_{history_file}')


# DataTransformer().time_price_check( history_file = 'TC.F.CME.QG.HOT.csv',
#             local_file = 'CME.QG HOT-Minute-Trade.txt')



DataTransformer().cut_off_MC_need(history_file='TC.F.CME.ES.HOT.csv',local_file='CME.ES HOT-Minute-Trade.txt')