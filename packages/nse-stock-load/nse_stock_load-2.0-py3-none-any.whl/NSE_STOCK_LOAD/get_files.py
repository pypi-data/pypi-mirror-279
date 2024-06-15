# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 20:46:50 2020

@author: kiran

"""

import pandas as pd
import numpy as np
import requests
import zipfile
import glob
import os

class files():
    
    def __init__(self):
    
        from nse_stock_load.variables import backup_path,url_path,local_path,local_root,dates,start_year,mon,start_month            # Importing variables
        
        self.backup_path=backup_path
        self.url_path=url_path
        self.local_path=local_path
        self.local_root=local_root
        self.dates=dates
        self.start_year=start_year
        self.mon=mon
        self.start_month=start_month

    def download_files(self):                # Download files, unzip and delete the zip files
        
        
        y=self.start_year
        mon=self.mon
        url_path=self.url_path+str(y)+'/'+str(mon)+'/'

        for d in self.dates:
            
            curSession = requests.Session()
            cookies = dict(cookies_are='working')
            filename='cm'+str(d)+str(mon)+str(y)+'bhav.csv.zip'
            url=url_path+filename
            #print(curSession.cookies.get_dict())
            
            try:
                #cookies = dict(cookies_are='working')
                myfile=curSession.get(url,timeout=5,stream=True,cookies=cookies)
                #print(session.cookies.get_dict())
                #r.cookies
                #print(url)
                if myfile.status_code == 200 :
                    open(self.local_path+filename,'wb').write(myfile.content)

                    with zipfile.ZipFile(self.local_path+filename,'r') as zip:
                        zip.extractall(path=self.local_path)

                    os.remove(self.local_path+filename)
            except:
                pass

    def concatenate(self):                  # Concatenate the downloaded month files

        files=glob.glob(self.local_path+"cm*")
        df=pd.concat(pd.read_csv(file,header=0,index_col=0) for file in files) #with header
        df.to_csv(self.local_root+"sec_bhavdata_full.csv")
        print("\nDaily files concatenated")


    def format_and_backup(self):

        data=pd.read_csv(self.local_root+"sec_bhavdata_full.csv",header=0)
        data=data[['SYMBOL','SERIES', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'LAST', 'PREVCLOSE', 'TOTTRDQTY', 'TOTTRDVAL', 'TIMESTAMP', 'TOTALTRADES']]
        data.rename({ 'OPEN':'OPEN_PRICE' ,'HIGH':'HIGH_PRICE' ,'LOW':'LOW_PRICE' ,'CLOSE':'CLOSE_PRICE' ,'LAST':'LAST_PRICE' ,'PREVCLOSE':'PREV_CLOSE_PRICE','TOTTRDQTY':'TOTAL_TRADED_QUANTITY','TOTTRDVAL':'TURNOVER' ,'TIMESTAMP':'STOCK_DATE' ,'TOTALTRADES':'NO_OF_TRADES' },axis=1,inplace=True)
        data['AVERAGE_PRICE']=np.nan
        data['DELIVERABLE_QTY']=np.nan
        data['PERCENT_DLY_QT_TO_TRADED_QTY']=np.nan
        data=data[['SYMBOL', 'SERIES','STOCK_DATE','PREV_CLOSE_PRICE', 'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE','LAST_PRICE',
       'CLOSE_PRICE', 'AVERAGE_PRICE','TOTAL_TRADED_QUANTITY', 'TURNOVER',  'NO_OF_TRADES','DELIVERABLE_QTY', 'PERCENT_DLY_QT_TO_TRADED_QTY']]
        data['TURNOVER']=data['TURNOVER']/100000
        data.to_csv(self.backup_path+"sec_bhavdata_full_"+str(self.start_year)+str(self.start_month)+".csv",index_label=True,index=0)
        data.to_csv(self.local_root+"sec_bhavdata_full.csv",index_label=True,index=0)
        print("\nIntial cleansing completed")


def file_main():
    run=files()
    run.download_files()
    run.concatenate()
    run.format_and_backup()
    
if __name__ == "__main__":
   file_main()