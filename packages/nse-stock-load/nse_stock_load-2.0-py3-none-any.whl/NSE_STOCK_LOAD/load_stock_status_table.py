# -*- coding: utf-8 -*-
"""
Created on Tue May  5 18:12:05 2020

@author: kiran
"""
import pandas as pd

class stock_status:

    from nse_stock_load.variables import connect,time_stamp

    def load_active_inactive(self):

        nseactive_stock_query="SELECT trim(COMPANY_NAME) COMPANY_NAME,STOCK_EXCHANGE,STOCK_DATE,SERIES, SECTOR FROM NSE_ACTIVESTOCK"
        stockcode_query="SELECT trim(COMPANY_NAME) COMPANY_NAME,SYMBOL FROM STOCKCODE"


        nseactive_stock_df=pd.read_sql(nseactive_stock_query,self.connect)
        stockcode_df=pd.read_sql(stockcode_query,self.connect)
        
        nseactive_stock_df.columns=nseactive_stock_df.columns.str.lower()
        stockcode_df.columns=stockcode_df.columns.str.lower()
        
        group_df=nseactive_stock_df.groupby(['company_name','series','stock_exchange','sector'])

        df=group_df.max().loc[:,['stock_date']]
        df.reset_index(drop=False,inplace=True)
        merge_df=pd.merge(df,stockcode_df,on=['company_name'],how='left')
        merge_df.loc[(merge_df['series']!='EQ') & (merge_df['symbol'].isnull()),'symbol']=merge_df.loc[(merge_df['series']!='EQ') & (merge_df['symbol'].isnull()),'series']
        merge_df.drop_duplicates(inplace=True)
        #print(merge_df.loc[(merge_df['series']!='EQ') & (merge_df['symbol'].isnull()),['symbol']])
        merge_df['stock_date']=pd.to_datetime(merge_df['stock_date'])
        
        merge_df['comments']=merge_df.apply(lambda x : " Last Traded on : "+str(x['stock_date'].strftime("%B-%Y")),axis=1)
        merge_df['trade_ind']=merge_df.apply(lambda x : "N" if (pd.to_datetime(self.time_stamp)-x['stock_date']).days > 90 else "Y",axis=1)

        merge_df=merge_df[['company_name','stock_exchange','stock_date','trade_ind','comments','symbol','series','sector']]
        merge_df.columns=merge_df.columns.str.upper()
        load_active_df=merge_df[merge_df['TRADE_IND']=='Y']
        load_inactive_df=merge_df[merge_df['TRADE_IND']=='N']

        self.connect.execute("delete from activestock_list")
        load_active_df.to_sql('activestock_list',self.connect,if_exists='append',index=False)

        load_inactive_df.to_sql('inactivestock_list',self.connect,if_exists='append',index=False)

    def delete_inactive(self):

        # delete records from INACTIVESTOCK_LIST if found to be active i.e., if stock becomes active again
        
        df_query="select * from INACTIVESTOCK_LIST"
        df=pd.read_sql(df_query,self.connect)
        df.drop_duplicates(inplace=True)
        self.connect.execute("delete from inactivestock_list")
        df.to_sql('inactivestock_list',self.connect,if_exists='append',index=False)

        active_stock_query="SELECT COMPANY_NAME,STOCK_EXCHANGE,trim(SERIES) SERIES FROM ACTIVESTOCK_LIST"
        inactive_stock_query="SELECT COMPANY_NAME,STOCK_EXCHANGE,trim(SERIES) SERIES FROM INACTIVESTOCK_LIST"
        
        active_stock_df=pd.read_sql(active_stock_query,self.connect)
        inactive_stock_df=pd.read_sql(inactive_stock_query,self.connect)
        
        active_stock_df.columns=active_stock_df.columns.str.lower()
        inactive_stock_df.columns=inactive_stock_df.columns.str.lower()
        
        list_update_df=pd.merge(inactive_stock_df,active_stock_df,right_on=['company_name','stock_exchange','series'],left_on=['company_name','stock_exchange','series'],how='inner')
        list_update_df.drop_duplicates(inplace=True)
        series=list_update_df.values
        #print(series)
        for record in series :
            #self.connect.execute("delete from INACTIVESTOCK_LIST where company_name=:company_name and stock_exchange=:stock_exchange and series=:series" , {"company_name": record[0], "stock_exchange": record[1], "series": record[2]})
            self.connect.execute("delete from INACTIVESTOCK_LIST where company_name='"+record[0]+"' and stock_exchange='"+record[1]+"' and series='"+record[2]+"';" )

def status_main():

    run=stock_status()
    run.load_active_inactive()
    run.delete_inactive()