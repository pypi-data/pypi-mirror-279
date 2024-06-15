# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 19:29:03 2020

@author: kiran
"""

from nse_stock_load.variables import reports_path,mail_path,start_year,start_month
#,current_year,current_month,current_day,backup_root
from nse_stock_load.load_stock_status_table import status_main
from nse_stock_load.load_activestock import nse_active_stock
from nse_stock_load.load_daily_data import nse_daily_data
from nse_stock_load.load_nse_indices import index_main
from nse_stock_load.Data_backup import backup_main
from nse_stock_load import load_my_stock_details
from nse_stock_load import stock_code_check
from nse_stock_load import load_stockcode
from nse_stock_load.mail import mailing
from nse_stock_load import purge_files
from nse_stock_load import get_files
from nse_stock_load import reports
from loghandler import logger
from datetime import date
import time
import os

#from nse_stock_load.env_setup import env_check_n_setup
from importlib import reload
import sys


#env_check_n_setup()

def complete_load():
    
    reload(sys.modules['nse_stock_load.variables'])
    

    
    purge_files.purge()                             # Purging files at start
    
    logger.INFO("\nsequence started for year {} month {}".format(start_year,start_month))
    
    index_main()            # index table load

    get_files.file_main()

    filcount=stock_code_check.validation_main()

    mail=mailing()

    if filcount!=0:

        mail.send_mail(files=["../NSE_New_Symbol.csv"])
        logger.INFO("\nNew stock codes sent in mail")

        while True:

            if os.path.exists(mail_path+"NSE_New_Symbol.csv")==False:

                time.sleep(120)

                try:
                    mail.read_mail(search="Start",download_attach="Yes",file_check="NSE_New_Symbol.csv")
                except:
                    pass
            else:
                logger.INFO("\nFile received with company names will proceed to load stock table")
                load_stockcode.stock_code_table_load()
                break

    else:
        logger.INFO("\nAll stock codes present in database. Proceeding to load.....")

    nse_daily_data()

    logger.INFO("\nDaily data loading completed")

    nse_active_stock()

    logger.INFO("\nMonthly data loading completed")

    status_main()           # load activelist table

    reports.report_generation_main()

    report_body="Loading completed for today, Attached the daily reports"
    report_subject="Load,Archival and Backup Completed"
    archival_file=["reports_archive_"+date.today().strftime("%Y%m%d")+".zip"]

    mail.send_mail(files=archival_file,path=reports_path,body=report_body,subject=report_subject,mail_to=["swathikirannanduri@gmail.com"])
    logger.INFO("\nArchived Reports sent in mail as zip")

    load_my_stock_details.my_stock_main()
    logger.INFO("\nStop Loss triggered")
    
    logger.INFO("\nTable backup going on")
    backup_main()
    logger.INFO("\nBackup's completed")
    
    purge_files.purge()                             # Purging files at end
    logger.INFO("\nfiles purged")
        
    logger.INFO("\nsequence completed")

def load_till_date():

    while True:
        
        reload(sys.modules['nse_stock_load.variables'])
        from nse_stock_load.variables import start_year,start_month,current_year,current_month,current_day
               
        if int(start_year) != int(current_year):
            complete_load()

        elif int(current_month) != int(start_month):
            complete_load()

        elif int(current_day) > 25:
            complete_load()
            logger.INFO("\nAll loadings completed till this month")
            break
            
        else:
            logger.INFO("\nAll loadings completed till date")
            break