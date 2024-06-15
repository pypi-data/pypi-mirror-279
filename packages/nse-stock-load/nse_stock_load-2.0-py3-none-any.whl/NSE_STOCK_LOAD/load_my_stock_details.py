# -*- coding: utf-8 -*-
"""
Created on Tue May  5 08:06:10 2020

@author: kiran
"""

from nse_stock_load.mail import mailing
from loghandler import logger
from datetime import datetime
import pandas as pd

class stock_load_and_mail:
    
    from nse_stock_load.variables import mail_path,time_stamp,connect,stop_loss_path

    def STOCK_DETAILS_SNAPSHOT(self):
        
        mail=mailing()
        mail.read_mail(search="Get",download_attach="Yes",file_check="Get.csv",path=self.mail_path)
        df=pd.read_csv(self.mail_path+"Get.csv")
        query="SELECT SYMBOL,COMPANY_NAME FROM STOCKCODE"
        stockcode_df=pd.read_sql(query,self.connect)
        stockcode_df.columns=stockcode_df.columns.str.upper()
        final_df=pd.merge(df,stockcode_df,how="inner",left_on="SYMBOL", right_on="SYMBOL")
        final_df['LOAD_DT_TIME']=self.time_stamp
        final_df['PRICE_OF_STOCK']=final_df['TOTAL_PURCHASE_PRICE']/final_df['QUANTITY']
        final_df['LOAD_DT_TIME']=pd.to_datetime(final_df['LOAD_DT_TIME'])
        final_df['DATE_OF_PURCHASE']=pd.to_datetime(final_df['DATE_OF_PURCHASE'])
        final_df=final_df[['COMPANY_NAME','SYMBOL','SERIES','DATE_OF_PURCHASE','PRICE_OF_STOCK','QUANTITY','TOTAL_PURCHASE_PRICE','ORDER_TYPE','STOCK_EXCHANGE','LOAD_DT_TIME']]
        #logger.INFO(final_df.T)
        final_df.to_sql('stock_details_snapshot',self.connect,if_exists='append',index=False)

    def STOCK_DETAILS(self):
        
        del_query="delete from stock_details_master"
        master_load_query="SELECT DISTINCT X.COMPANY_NAME, X.SYMBOL, X.SERIES, if(X.QUANTITY=0,'N','Y') as 'ACTIVE_STOCK_IND', X.DATE_OF_PURCHASE, X.FIRST_PURCHASE_DATE, X.LAST_PURCHASE_DATE, X.QUANTITY as 'QUANTITY_AVAILABLE', X.PRICE_OF_STOCK as 'PURCHASE_PRICE_OF_STOCK', X.CURRENT_PRICE as 'CURRENT_PRICE_OF_STOCK', X.PRICE_OF_STOCK*0.9 as 'STOP_LOSS_TRIGGER_AMT', (X.CURRENT_PRICE-X.PRICE_OF_STOCK) as 'CNG_SINCE_BOUGHT', X.MNTH_CHANGE as 'CNG_LAST_1_MONTHS', (X.CURRENT_PRICE-a.CLOSE_PRICE) as 'CNG_LAST_6_MONTHS', if((X.CURRENT_PRICE-X.PRICE_OF_STOCK)<=0,'GAIN','LOSS') as 'STATUS', a.STOCK_EXCHANGE, x.LOAD_DT_TIME LOAD_DT_TIME  FROM nse_activestock A INNER JOIN (SELECT A.COMPANY_NAME,A.SYMBOL,A.SERIES,A.DATE_OF_PURCHASE,B.FIRST_PURCHASE_DATE,a.PRICE_OF_STOCK,C.LAST_PURCHASE_DATE,D.QUANTITY,E.CURRENT_PRICE,F.MNTH_CHANGE,a.LOAD_DT_TIME FROM STOCK_DETAILS_SNAPSHOT a LEFT OUTER JOIN (SELECT COMPANY_NAME,SYMBOL,MIN(DATE_OF_PURCHASE) FIRST_PURCHASE_DATE FROM STOCK_DETAILS_SNAPSHOT GROUP BY COMPANY_NAME,SYMBOL)B ON A.COMPANY_NAME=B.COMPANY_NAME AND A.SYMBOL=B.SYMBOL LEFT OUTER JOIN (SELECT COMPANY_NAME,SYMBOL,MAX(DATE_OF_PURCHASE) LAST_PURCHASE_DATE FROM STOCK_DETAILS_SNAPSHOT GROUP BY COMPANY_NAME,SYMBOL)C ON A.COMPANY_NAME=C.COMPANY_NAME AND A.SYMBOL=C.SYMBOL LEFT OUTER JOIN (SELECT A.COMPANY_NAME,A.SYMBOL,(A.QUANTITY-NVL(B.SELL,0)) QUANTITY  FROM STOCK_DETAILS_SNAPSHOT  A LEFT OUTER JOIN (SELECT COMPANY_NAME,SYMBOL,QUANTITY SELL FROM STOCK_DETAILS_SNAPSHOT WHERE ORDER_TYPE='SELL') B ON A.COMPANY_NAME=B.COMPANY_NAME  AND A.SYMBOL=B.SYMBOL WHERE A.ORDER_TYPE='BUY' ) D  ON A.COMPANY_NAME=D.COMPANY_NAME AND A.SYMBOL=D.SYMBOL  LEFT OUTER JOIN  (SELECT COMPANY_NAME,SYMBOL,CLOSE_PRICE CURRENT_PRICE FROM NSE_ACTIVESTOCK WHERE (SYMBOL,STOCK_DATE) IN (SELECT SYMBOL,MAX(STOCK_DATE) FROM NSE_ACTIVESTOCK GROUP BY SYMBOL)) E  ON A.COMPANY_NAME=E.COMPANY_NAME AND A.SYMBOL=E.SYMBOL LEFT OUTER JOIN (select A.COMPANY_NAME,B.SYMBOL,A.SERIES,(a.CLOSE_PRICE-B.CLOSE_PRICE) MNTH_CHANGE from NSE_ACTIVESTOCK a,NSE_ACTIVESTOCK b where a.COMPANY_NAME=b.COMPANY_NAME and a.SYMBOL=b.SYMBOL and a.SERIES=b.SERIES AND (A.SYMBOL,A.STOCK_DATE) IN (SELECT SYMBOL,MAX(STOCK_DATE) FROM NSE_ACTIVESTOCK GROUP BY SYMBOL) AND (B.SYMBOL,B.STOCK_DATE) IN (SELECT SYMBOL,MAX(STOCK_DATE) FROM NSE_ACTIVESTOCK WHERE (STOCK_DATE)<(SELECT DISTINCT MAX(STOCK_DATE) FROM NSE_ACTIVESTOCK) GROUP BY SYMBOL) )F ON A.COMPANY_NAME=F.COMPANY_NAME AND A.SYMBOL=F.SYMBOL GROUP BY A.COMPANY_NAME,A.SYMBOL,A.SERIES,A.DATE_OF_PURCHASE,B.FIRST_PURCHASE_DATE,a.PRICE_OF_STOCK,C.LAST_PURCHASE_DATE,D.QUANTITY,E.CURRENT_PRICE,F.MNTH_CHANGE,a.LOAD_DT_TIME) X ON A.COMPANY_NAME=X.COMPANY_NAME AND A.SYMBOL=X.SYMBOL where (A.SYMBOL,A.STOCK_DATE) IN (SELECT SYMBOL,MIN(STOCK_DATE) FROM NSE_ACTIVESTOCK  GROUP BY SYMBOL)"
        df=pd.read_sql(master_load_query,self.connect)
        df.columns=df.columns.str.upper()
        df.rename(columns={'CNG_LAST_1_MONTHS':'CNG_IN_LAST_1MONTHS','CNG_LAST_6_MONTHS':'CNG_IN_LAST_6MONTHS'},inplace=True)
        df['LOAD_DT_TIME']=pd.to_datetime(self.time_stamp)

        self.connect.execute(del_query)
        df.to_sql('stock_details_master',self.connect,if_exists='append',index=None)


    def check_and_mail(self):
        
        query="select COUNT(*) as 'CNT'  from STOCK_DETAILS_MASTER  where CURRENT_PRICE_OF_STOCK<=STOP_LOSS_TRIGGER_AMT and active_stock_ind='Y'"
        df=pd.read_sql(query,self.connect)
        if df.iloc[0,0] > 0:

            filename="SLTriggger_"+datetime.strptime(self.time_stamp[:9],"%d-%b-%y").date().strftime("%Y%m%d")+".csv"
            path=self.stop_loss_path
            subject="STOP LOSS Triggered"
            message="STOP LOSS Triggered for "+datetime.strptime(self.time_stamp[:9],"%d-%b-%y").date().strftime("%Y%m%d")

            sel_query="select COMPANY_NAME,SYMBOL,STOCK_EXCHANGE,SERIES, QUANTITY_AVAILABLE,PURCHASE_PRICE_OF_STOCK, CURRENT_PRICE_OF_STOCK,CNG_SINCE_BOUGHT, STOP_LOSS_TRIGGER_AMT,STATUS  from STOCK_DETAILS_MASTER where CURRENT_PRICE_OF_STOCK<=STOP_LOSS_TRIGGER_AMT"
            df=pd.read_sql(sel_query,self.connect)
            df.drop_duplicates()
            df.columns=df.columns.str.upper()
            df=df.sort_values(by='COMPANY_NAME')
            df.to_csv(path+filename,index=None)
            mail=mailing()
            mail.send_mail(files=[filename],path=path,mail_to=['swathikirannanduri@gmail.com'],subject=subject,body=message)


def my_stock_main():

    run=stock_load_and_mail()

    try :
        run.STOCK_DETAILS_SNAPSHOT()
        run.STOCK_DETAILS()
        run.check_and_mail()
    except:
        logger.INFO("\nNo new mails are found for new stocks, sending updated price values for the date")
    run.STOCK_DETAILS()
    run.check_and_mail()