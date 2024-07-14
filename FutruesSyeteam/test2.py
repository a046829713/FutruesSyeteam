import datetime

from dateutil.relativedelta import relativedelta
import time

def get_data_range(sD="2010010100"):
    begin_date = datetime.datetime.strptime(sD, "%Y%m%d%H")
    end_date = begin_date + timedelta(days=150)

    if end_date > datetime.datetime.now():
        end_date = datetime.datetime.now().date()

    return begin_date.strftime("%Y%m%d%H"),end_date.strftime("%Y%m%d%H")

begin_date = "2010010100"
NO_data_list = []
while True:
    begin_date , end_date = get_data_range(begin_date)
    print(begin_date , end_date)
    time.sleep(5)
    begin_date = end_date