import glob
import requests
import numpy as np
import pandas as pd
from loghandler import logger

class index_load:
     
    def __init__(self):
        
        from nse_stock_load.variables import connect,index_path,start_month,start_year,current_month,current_year,dates
        
        self.m=start_month
        self.y=start_year
        self.till_month=current_month
        self.till_year=current_year
        
        self.local_path=index_path
        #new : https://archives.nseindia.com/content/indices/ind_close_all_27012020.csv
        #old : url="https://nseindia.com/content/indices/"+filename
        self.url_path="https://archives.nseindia.com/content/indices/"
        self.connect=connect
        self.index_path=index_path
        self.start_month=start_month
        self.start_year=start_year
        self.current_month=current_month
        self.current_year=current_year
        self.dates=dates
 
    def download_file(self):
              
        for d in self.dates:

            filename="ind_close_all_"+str(d)+str(self.m)+str(self.y)+".csv"
            url=self.url_path+filename

            try:
                myfile=requests.get(url,timeout=5)

                if myfile.status_code == 200 :
                    open(self.local_path+filename,'wb').write(myfile.content)

            except:
                #logger.INFO(filename,"not found passing")
                pass

    def files_concat(self):
    
        try:
            #logger.INFO("concatinated files for the month,year will be ind_close_all_"+str(y)+str(m))
            files=glob.glob(self.local_path+"ind_close_all_*"+str(self.m)+str(self.y)+"*")
            df=pd.concat(pd.read_csv(file,header=0,index_col=0) for file in files) #with header
            df.to_csv(self.local_path+"final/ind_close_all_"+str(self.y)+str(self.m)+".csv")
            logger.INFO("\nMonth files concatenated")

        except:
            pass

    def table_loading(self):
    
        try:

            df=pd.read_csv(self.local_path+"final/ind_close_all_"+str(self.y)+str(self.m)+".csv")

            df=df.rename(columns=lambda x:x.lower().replace(' ','_').replace('change(%)','percent_change').replace('/','_').replace('(rs.','in').replace('.)','ores').replace('volume','volum'))

            df['index_date']=pd.to_datetime(df['index_date'],format='%d-%m-%Y')

            df.replace({'-':np.nan},inplace=True)
            df.replace({np.nan:''},inplace=True)
            min_date=df['index_date'].min().strftime("%Y-%m-%d")
            max_date=df['index_date'].max().strftime("%Y-%m-%d")
            self.connect.execute("delete from nse_index_daily_data where index_date between '"+min_date+"' and '"+max_date+"'" )
            df.to_sql('nse_index_daily_data',self.connect,if_exists='append',index=False,chunksize=100)

            logger.INFO("\nindex table Loaded for {} , {} month ".format(self.y,self.m))

        except:
            pass


def index_main():

    run=index_load()
    run.download_file()
    run.files_concat()
    run.table_loading()