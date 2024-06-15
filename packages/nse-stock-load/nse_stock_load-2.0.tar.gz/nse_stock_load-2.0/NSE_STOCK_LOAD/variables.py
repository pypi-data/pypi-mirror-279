# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:57:54 2020

@author: kiran
"""

from datetime import datetime
import sqlalchemy as sqla
import pandas as pd

dates=list("%02i" % x for x in range(1,32))
time_stamp=datetime.now().strftime('%d-%b-%y %H:%M:%S.%f')

url_path="https://www1.nseindia.com/content/historical/EQUITIES/"                                #https://www1.nseindia.com/content/historical/EQUITIES/2020/APR/cm13APR2020bhav.csv.zip

#engine=sqla.create_engine("oracle+cx_oracle://sys:root@localhost:1521/test?mode=SYSDBA&events=true",max_identifier_length=128)      # db connection
engine=sqla.create_engine('mysql+pymysql://root:admin@/mysql')
connect=engine.connect()

query="SELECT date_format(date_add(LAST_DAY(stock_date),interval 1 DAY),'%%Y%%m%%d') STOCK_DATE FROM (SELECT MAX(STOCK_DATE) STOCK_DATE FROM NSE_DAILY_DATA)A"


data=pd.read_sql(query,connect)

current_year  = datetime.today().year              # 2020
current_month = "%02i" % datetime.today().month    # 05
current_day   = "%02i" % datetime.today().day      # 15
last_month    = "%02i" % (int(current_month)-1)    # 03

email_id=''

try:
    start_year    = data.iloc[0,0][0:4]              # 2020
except:
    start_year    = current_year

try:
    start_month   = data.iloc[0,0][4:6]              # 04
except:
    start_month   = last_month

try:
    mon           = datetime.strptime(str(data.iloc[0,0]),'%Y%m%d').strftime("%b").upper()                   # APR
except:
    mon           = datetime.today().strftime("%b").upper()


backup_root="/mnt/data/nse/load/"
reports_path=backup_root+"Reports/"
stop_loss_path=backup_root+"STOP_LOSS_Trigger/"
data_backup_path=backup_root+"Daily_Data_Backup/"
metadata_path=backup_root+"Oracle_Table_Metadata/"
backup_path=backup_root+"Scheduled_Processedfile_Backup/"

local_root="/mnt/data/nse/load/"
mail_path=local_root+"Mail/"
index_path=local_root+"nse_indices/"
local_path=local_root+"monthly_dump/"
index_final_path=local_root+"nse_indices/final/"