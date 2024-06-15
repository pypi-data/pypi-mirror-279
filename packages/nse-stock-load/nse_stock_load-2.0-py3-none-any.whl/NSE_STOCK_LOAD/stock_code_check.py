# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:56:21 2020

@author: kiran
"""

import pandas as pd

class validation:

    from nse_stock_load.variables import local_root,connect

    def csv_dataframe(self):
        
        self.csv_df=pd.read_csv(self.local_root+"sec_bhavdata_full.csv",index_col=False)
        self.csv_df=self.csv_df[self.csv_df['SERIES']=='EQ']
        self.csv_df=self.csv_df[['SYMBOL','SERIES']]
        self.csv_df=self.csv_df.sort_values('SYMBOL')
        self.csv_df.drop_duplicates(inplace=True)
        self.csv_df.reset_index(inplace=True,drop=True)

    def databse_dataframe(self):
        
        query="SELECT SYMBOL AS 'KEY', SYMBOL FROM STOCKCODE"
        self.db_df=pd.read_sql(query,self.connect)
        self.db_df.columns=self.db_df.columns.str.upper()

    def merge_df(self):
        
        merge_df=pd.merge(self.csv_df,self.db_df,how='left',left_on='SYMBOL',right_on='SYMBOL')
        merge_df=merge_df[merge_df['KEY'].isnull()]
        merge_df=merge_df[['SYMBOL', 'SERIES']]
        merge_df.to_csv(self.local_root+"NSE_New_Symbol.csv",index=False,header=False)
        self.validation_file_wc=merge_df['SYMBOL'].count()


def validation_main():

    run=validation()
    run.csv_dataframe()
    run.databse_dataframe()
    run.merge_df()
    return run.validation_file_wc

if "__name__" == "__main__":
    validation_main()