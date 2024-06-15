# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 19:30:22 2020

@author: kiran
"""

import os
import pandas as pd
from datetime import date
from zipfile import ZipFile,ZIP_DEFLATED

class report_generation():

    from nse_stock_load.variables import reports_path,connect

    qurey_n_filename=[
            ("EOD_PRICE_CHANGE_REPORT","select COMPANY_NAME, SYMBOL, SERIES, STOCK_DATE, PREV_CLOSE_PRICE, OPEN_PRICE, HIGH_PRICE, CLOSE_PRICE, (((CLOSE_PRICE-OPEN_PRICE)*100)/CLOSE_PRICE) as 'PERCENT_CHANGE'  from NSE_DAILY_DATA where STOCK_DATE=(select max(stock_date) from NSE_DAILY_DATA) and (((CLOSE_PRICE-OPEN_PRICE)*100)/CLOSE_PRICE)>=4.5 and Open_Price > 25 order by PERCENT_CHANGE desc"),
            ("BOD_PRICE_STATUS","select COMPANY_NAME,SYMBOL,SERIES,STOCK_DATE,PREV_CLOSE_PRICE,OPEN_PRICE,(OPEN_PRICE-PREV_CLOSE_PRICE) PRICE_CHANGE, ((OPEN_PRICE-PREV_CLOSE_PRICE)*100)/PREV_CLOSE_PRICE PERCENT_CHANGE from NSE_DAILY_DATA where STOCK_DATE=(select max(stock_date) from NSE_DAILY_DATA) and (((OPEN_PRICE-PREV_CLOSE_PRICE)*100)/PREV_CLOSE_PRICE)>=4.5 and Open_Price > 25 order by PERCENT_CHANGE desc"),
            ("HIGHEST_GAINERS_TODAY","select COMPANY_NAME,SYMBOL,SERIES,STOCK_DATE,(CLOSE_PRICE-OPEN_PRICE) PRICE_CHANGE,OPEN_PRICE,CLOSE_PRICE,HIGH_PRICE, Total_Traded_Quantity,No_Of_Trades,PREV_CLOSE_PRICE from NSE_DAILY_DATA where STOCK_DATE=(select max(stock_date) from NSE_DAILY_DATA) AND (CLOSE_PRICE-OPEN_PRICE)>5 order by PRICE_CHANGE desc"),
            ("BIGGEST_LOOSERS_TODAY","select COMPANY_NAME,SYMBOL,SERIES,STOCK_DATE,PREV_CLOSE_PRICE,OPEN_PRICE,HIGH_PRICE,CLOSE_PRICE,(CLOSE_PRICE-OPEN_PRICE) PRICE_CHANGE from NSE_DAILY_DATA where STOCK_DATE=(select max(stock_date) from NSE_DAILY_DATA) AND (CLOSE_PRICE-OPEN_PRICE)<-5 order by PRICE_CHANGE"),
            ("LAST6MONTHS_RAISING_STOCKS","select a.Company_Name, A.SERIES,A.SYMBOL, B.STOCK_DATE START_MONTH, a.STOCK_DATE TILL_MONTH,b.OPEN_PRICE PREV_PRICE, a.CLOSE_PRICE CURR_PRICE,(a.OPEN_PRICE-b.OPEN_PRICE) PRICE_CHANGE,(a.OPEN_PRICE-b.OPEN_PRICE)*100/b.OPEN_PRICE RET from nse_activestock a,nse_activestock b where a.Company_Name=b.Company_Name and a.Stock_Exchange=b.Stock_Exchange and a.SERIES=b.SERIES and b.stock_date=date_format(date_add((sysdate())-((date_format(sysdate(),'%%d')) - 1),interval 6 month),'%%Y-%%m-%%d') and a.Stock_Date=date_format((sysdate())-((date_format(sysdate(),'%%d')) - 1),'%%Y-%%m-%%d') and (a.OPEN_PRICE-b.OPEN_PRICE)*100/b.OPEN_PRICE > 10 ORDER BY RET DESC"),
            ("LAST3MONTHS_FALLING_STOCKS","select a.Company_Name,a.SYMBOL,a.series,B.STOCK_DATE START_DT,a.STOCK_DATE TILL_DT,b.OPEN_PRICE PREV_PRICE, a.CLOSE_PRICE CURR_PRICE , (a.OPEN_PRICE-b.OPEN_PRICE) PRICE_CHANGE, (a.OPEN_PRICE-b.OPEN_PRICE)*100/b.OPEN_PRICE PERCENT_CHANGE  from nse_activestock a,nse_activestock b where a.Company_Name=b.Company_Name and a.Stock_Exchange=b.Stock_Exchange and a.SERIES=b.SERIES and b.stock_date=date_format(date_add((sysdate())-((date_format(sysdate(),'%%d')) - 1),interval 6 month),'%%Y-%%m-%%d') and a.Stock_Date=date_format(sysdate()-((date_format(sysdate(),'%%d')) - 1),'%%Y-%%m-%%d') and (a.OPEN_PRICE-b.OPEN_PRICE)*100/b.OPEN_PRICE < -10 ORDER BY PRICE_CHANGE desc"),
            ("CURRENT_MONTH_STOCK_STATUS","select A.COMPANY_NAME,B.SYMBOL,A.SERIES,a.CLOSE_PRICE CURR,B.CLOSE_PRICE PREV,a.CLOSE_PRICE-B.CLOSE_PRICE CHNG, ((a.CLOSE_PRICE-B.CLOSE_PRICE)/A.CLOSE_PRICE)*100 MNTH_CHANGE from NSE_ACTIVESTOCK a,NSE_ACTIVESTOCK b where a.COMPANY_NAME=b.COMPANY_NAME and a.SYMBOL=b.SYMBOL and a.SERIES=b.SERIES AND (A.SYMBOL,A.STOCK_DATE) IN (SELECT SYMBOL,MAX(STOCK_DATE) FROM NSE_ACTIVESTOCK GROUP BY SYMBOL) AND (B.SYMBOL,B.STOCK_DATE) IN (SELECT SYMBOL,MAX(STOCK_DATE) FROM NSE_ACTIVESTOCK WHERE (STOCK_DATE)<(SELECT DISTINCT MAX(STOCK_DATE) FROM NSE_ACTIVESTOCK) GROUP BY SYMBOL) ORDER BY CHNG DESC")
            ]

    csv_files=[]

    def db_fetch(self,query="select * from dual",path=reports_path,to_file="dual.txt"):

        os.chdir('/mnt/data/')
        self.root_dir=os.getcwd()+"/"
        full_path=self.root_dir+to_file
        data=pd.read_sql(query,self.connect)
        data.to_csv(full_path,index=False)

    def generate_reports(self):

        for q in self.qurey_n_filename:
            self.db_fetch(query=q[1],to_file=q[0]+"_"+date.today().strftime("%Y%m%d")+".csv")
            self.csv_files.append(q[0]+"_"+date.today().strftime("%Y%m%d")+".csv")

    def zip_reports(self,path=reports_path):

        os.chdir(self.reports_path)
        zf = ZipFile("reports_archive_"+date.today().strftime("%Y%m%d")+".zip", "w",compression=ZIP_DEFLATED)

        for files in self.csv_files:
            zf.write(os.path.join(self.root_dir,files))
        zf.close()
        
        for files in self.csv_files:   
            try:
                os.remove(self.root_dir+files)
            except:
                continue

def report_generation_main():
    run=report_generation()
    run.generate_reports()
    run.zip_reports()
    print("\nReports Generated and archived to mail")
    

if "__name__"=="__main__":
    report_generation_main()