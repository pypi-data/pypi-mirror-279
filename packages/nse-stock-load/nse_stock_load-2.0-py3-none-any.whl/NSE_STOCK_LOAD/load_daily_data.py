# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 14:09:11 2020

@author: kiran
"""

from nse_stock_load.variables import local_root,time_stamp,connect
import pandas as pd
import numpy as np

def nse_daily_data(path=local_root,filename="sec_bhavdata_full.csv"):

    df=pd.read_csv(path+filename)
    df.STOCK_DATE=pd.to_datetime(df.STOCK_DATE)
    min_date=df['STOCK_DATE'].min().strftime("%Y-%m-%d")
    max_date=df['STOCK_DATE'].max().strftime("%Y-%m-%d")
    del_query="DELETE FROM NSE_DAILY_DATA WHERE STOCK_DATE BETWEEN '"+min_date+"' and '"+max_date+"'"
    sel_query="SELECT SYMBOL,COMPANY_NAME,SECTOR FROM STOCKCODE"

    df_table=pd.read_sql(sel_query,connect)
    df_table.columns=df_table.columns.str.upper()

    df_main=df.set_index('SYMBOL')                          # set index
    df_table=df_table.set_index('SYMBOL')

    df_merge=pd.merge(df_main,df_table,how="left",left_on="SYMBOL", right_on="SYMBOL")      # merge tables
    df_merge=df_merge.reset_index(drop=False)

    df_merge['SERIES'].replace(np.nan,"NA",inplace=True)
    df_merge.loc[df_merge['SERIES']!='EQ','COMPANY_NAME']=df_merge.loc[df_merge['SERIES']!='EQ','SYMBOL']           # IF series!="EQ" company_name=symbol
    df_merge.loc[df_merge['SERIES']!='EQ','SECTOR']=df_merge.loc[df_merge['SERIES']!='EQ','SERIES']                 # IF series!="EQ" sector=symbol
    df_merge.loc[:,['LAST_PRICE','DELIVERABLE_QTY','PERCENT_DLY_QT_TO_TRADED_QTY']].replace("-","",inplace=True)
    df_merge.loc[:,['LAST_PRICE','DELIVERABLE_QTY','PERCENT_DLY_QT_TO_TRADED_QTY']].replace("",np.nan,inplace=True)
    df_merge['LOAD_DT_TIME']=pd.to_datetime(time_stamp)                        # load_Dt_timestamp
    df_merge['COMPANY_NAME']=df_merge['COMPANY_NAME'].str.strip()
    df_merge['TURNOVER']=df_merge['TURNOVER'].round(2)
    #df_merge.loc[df_merge['TURNOVER']>0.5,['TURNOVER']]=df_merge['TURNOVER'].round(2)
    df_merge.drop_duplicates(inplace=True)
    df_merge=df_merge[['COMPANY_NAME','SYMBOL','SERIES','STOCK_DATE','PREV_CLOSE_PRICE','OPEN_PRICE','HIGH_PRICE','LOW_PRICE','LAST_PRICE',
       'CLOSE_PRICE','AVERAGE_PRICE','TOTAL_TRADED_QUANTITY','TURNOVER','NO_OF_TRADES','DELIVERABLE_QTY',
       'PERCENT_DLY_QT_TO_TRADED_QTY','LOAD_DT_TIME','SECTOR']]

    connect.execute(del_query)                                                                                      # delete data if exist
    df_merge.to_sql('nse_daily_data',connect,if_exists='append',index=False,chunksize=100)                          # insert data again

    connect.execute("UPDATE nse_daily_data t1 INNER JOIN nse_index_daily_data as t2  on t2.index_date=t1.stock_date SET t1.Open_Index_Value=t2.Open_Index_Value, t1.Closing_Index_Value=t2.Closing_Index_Value where t2.Index_name='Nifty 50' and DATE_FORMAT(index_date,'%%y-%%m')=(select DATE_FORMAT(max(index_date),'%%y-%%m') from NSE_INDEX_DAILY_DATA) and T1.SERIES='EQ'")