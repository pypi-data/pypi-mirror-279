# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 19:31:19 2020

@author: kiran
"""

from nse_stock_load.variables import data_backup_path,metadata_path,time_stamp,connect
import pandas as pd
from zipfile import ZipFile,ZIP_DEFLATED
from datetime import datetime
import os

TablesQuery="SELECT concat('show create table ',TABLE_NAME,':',TABLE_NAME) tbl   FROM information_schema.tables where  TABLE_TYPE='BASE TABLE' and Table_schema='mysql' and table_collation='utf8mb4_general_ci'"

def backup_main():

    metadata_df=pd.read_sql(TablesQuery,connect)

    cnt=1

    for i in metadata_df.iloc[:,0]:

        df=pd.read_sql(i.split(":")[0],connect)

        if cnt==1:
            df.to_csv(metadata_path+"TablesMetadata.txt",header=False,index=None,quotechar=' ',line_terminator=';\n')
            f=open(metadata_path+"tables_list.txt",'w')
            f.write(i.split(":")[1])
            f.close()
        else:
            df.to_csv(metadata_path+"TablesMetadata.txt",header=False,index=None,mode='a',quotechar=' ',line_terminator=";\n")
            f=open(metadata_path+"tables_list.txt",'a')
            f.write("\n"+i.split(":")[1])
            f.close()
        cnt+=1


    os.chdir('/mnt/data/')
    root_dir=os.getcwd()+"/"
    date=datetime.strptime(time_stamp[:9],"%d-%b-%y").strftime("%Y%m%d")
    files=[]
    
    with open(metadata_path+"tables_list.txt",'r') as doc:
        files=doc.read()
        files=list(files.split("\n"))
     
    for table in files:
        df=pd.read_sql("select * from "+table,connect)
        df.to_csv(root_dir+table+".txt",header=None,index=None,chunksize=100,)

    zf = ZipFile(data_backup_path+"archive_"+str(date)+".zip", "w",compression=ZIP_DEFLATED)

    for file in files:
        zf.write(os.path.join(root_dir,file+".txt"))
        os.remove(root_dir+file+".txt")

    zf.close()