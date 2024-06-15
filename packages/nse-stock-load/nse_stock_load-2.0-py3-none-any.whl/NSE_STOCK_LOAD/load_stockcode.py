# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 19:30:01 2020

@author: kiran
"""

from nse_stock_load.variables import mail_path,connect
from loghandler import logger
import pandas as pd

def stock_code_table_load(path=mail_path,file="NSE_New_Symbol.csv"):

    #connect=engine.connect()
    df=pd.read_csv(path+file,header=None,names=['SYMBOL','COMPANY_NAME','SECTOR'])
    df['SYMBOL1']=df['SYMBOL']
    df=df[['COMPANY_NAME','SYMBOL','SYMBOL1','SECTOR']]
    df.to_sql('stockcode',connect,index=False,if_exists='append')
    logger.INFO("\nSTOCKCODE table loading completed")