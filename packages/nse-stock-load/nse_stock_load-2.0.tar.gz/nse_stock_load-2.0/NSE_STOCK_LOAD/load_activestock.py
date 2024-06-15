# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 14:09:23 2020

@author: kiran
"""

from nse_stock_load.variables import connect,time_stamp
import pandas as pd

def nse_active_stock():
    
    #open_close_query="SELECT COMPANY_NAME,SYMBOL,SERIES,DATE_FORMAT(STOCK_DATE,'%%m-%%Y') STOCK_DATE,OPEN_PRICE,CLOSE_PRICE,SECTOR,STOCK_DATE as 'STOCK_DATE1' FROM NSE_DAILY_DATA WHERE DATE_FORMAT(STOCK_DATE,'%%m-%%Y') = (SELECT DATE_FORMAT(MAX(STOCK_DATE),'YYYY-MM') FROM NSE_DAILY_DATA) AND SERIES='EQ' ORDER BY COMPANY_NAME,SERIES,STOCK_DATE1"
    #high_low_query="SELECT COMPANY_NAME, SYMBOL, SERIES, DATE_FORMAT(STOCK_DATE,'%%m-%%Y') STOCK_DATE, HIGH_PRICE, LOW_PRICE, SECTOR, STOCK_DATE as 'STOCK_DATE1' FROM NSE_DAILY_DATA WHERE DATE_FORMAT(STOCK_DATE,'%%m-%%Y') = (SELECT DATE_FORMAT(MAX(STOCK_DATE),'YYYY-MM') FROM NSE_DAILY_DATA) AND SERIES='EQ' ORDER BY COMPANY_NAME,SERIES,STOCK_DATE1"

    open_close_query="SELECT COMPANY_NAME,SYMBOL,SERIES,DATE_FORMAT(STOCK_DATE,'%%m-%%Y') STOCK_DATE,OPEN_PRICE,CLOSE_PRICE,SECTOR,STOCK_DATE as 'STOCK_DATE1' FROM NSE_DAILY_DATA WHERE DATE_FORMAT(STOCK_DATE,'%%m-%%Y') = (SELECT DATE_FORMAT(MAX(STOCK_DATE),'%%m-%%Y') FROM NSE_DAILY_DATA) AND SERIES='EQ' ORDER BY COMPANY_NAME,SERIES,STOCK_DATE1"
    high_low_query="SELECT COMPANY_NAME, SYMBOL, SERIES, DATE_FORMAT(STOCK_DATE,'%%m-%%Y') STOCK_DATE, HIGH_PRICE, LOW_PRICE, SECTOR, STOCK_DATE as 'STOCK_DATE1' FROM NSE_DAILY_DATA WHERE DATE_FORMAT(STOCK_DATE,'%%m-%%Y') = (SELECT DATE_FORMAT(MAX(STOCK_DATE),'%%m-%%Y') FROM NSE_DAILY_DATA) AND SERIES='EQ' ORDER BY COMPANY_NAME,SERIES,STOCK_DATE1"

    open_close_df=pd.read_sql(open_close_query,connect)
    high_low_df=pd.read_sql(high_low_query,connect)
    
    open_close_df.columns=open_close_df.columns.str.lower()
    high_low_df.columns=high_low_df.columns.str.lower()
    
    open_close_groupby=open_close_df.groupby(['symbol'])
    high_low_groupby=high_low_df.groupby(['symbol'])

    join_df=open_close_groupby.first().loc[:,['company_name', 'series', 'stock_date', 'sector']]

    open_df=open_close_groupby.first().loc[:,['open_price']]
    close_df=open_close_groupby.last().loc[:,['close_price']]
    high_df=high_low_groupby.max().loc[:,['high_price']]
    low_df=high_low_groupby.min().loc[:,['low_price']]

    final_df=join_df.join([close_df,open_df,high_df,low_df])
    final_df['STOCK_EXCHANGE']='NSE'
    final_df.reset_index(drop=False,inplace=True)
    final_df.columns=final_df.columns.str.upper()
    final_df['LOAD_DT_TIME']=pd.to_datetime(time_stamp)
    final_df['STOCK_DATE']="01-"+final_df['STOCK_DATE']
    final_df['STOCK_DATE']=pd.to_datetime(final_df['STOCK_DATE'],format="%d-%m-%Y")

    final_df=final_df[['COMPANY_NAME','SYMBOL','SERIES','STOCK_DATE','OPEN_PRICE','HIGH_PRICE','LOW_PRICE','CLOSE_PRICE','LOAD_DT_TIME','STOCK_EXCHANGE','SECTOR']]

    date=final_df['STOCK_DATE'].min().strftime("%Y-%m-%d")
    del_query="delete from nse_activestock where stock_date='"+str(date)+"'"

    connect.execute(del_query)
    final_df.to_sql('nse_activestock',connect,if_exists='append',index=False)