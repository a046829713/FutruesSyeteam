import sys
sys.path.append("../")
from datetime import time
import pandas as pd
import pandas_market_calendars as mcal


all_name =  mcal.get_calendar_names()



cme = mcal.get_calendar('CMES')

holidays = cme.holidays()



print(cme.valid_days(start_date='2024-05-01', end_date='2024-05-31'))




# Hot

# 03/20

# TC 03/15 


# 回測 最後交易日 商品資料(TC熱門月)
# 實際交易 TC熱門月砍倉


# TC 202403 202404 202405 202406 