# -*- coding: utf-8 -*-
"""
Created on Sun May 10 16:44:08 2020

@author: kiran
"""

import os,nse_stock_load
from nse_stock_load.variables import backup_root
from variables import email_id
from loghandler import logger
import importlib
import sys

class env_check_n_setup:

   
    if email_id == None:
        
        logger.INFO("Email Id not existing mail communication")
        email=input("Enter Email ID")
        
        if email == None:
            
            logger.INFO("Do you want to continue without email id?")
            ignore_email_confirm=input("Y/n")
            
            
            
            if ignore_email_confirm == None:
                pass
        
    if os.path.lexists(backup_root)==True:

        from nse_stock_load.variables import backup_root,backup_path,reports_path,data_backup_path,metadata_path,local_root,local_path,mail_path,index_path,index_final_path,stop_loss_path

        dir_list=[backup_root,backup_path,reports_path,data_backup_path,metadata_path,local_root,local_path,mail_path,index_path,index_final_path,stop_loss_path]
        for dir_name in dir_list:
            try:
                os.mkdir(dir_name)
            except:
                continue
        logger.INFO("\nAll requried directories are available/created")
        
    else:
        os.chdir("/")
        for x in os.listdir():
            if os.path.isdir(x):
                logger.INFO(x)
                
        while True:

            backup_root=input("input directory for nse backups : ")

            if os.path.lexists(backup_root):

                path=os.path.dirname(nse_stock_load.__file__)                   #path="C:\\Users\\kiran\\Desktop\\app\\nse_stock_load"
                file=open(path+"/variables.py",'r')
                file_read=file.read()
                file.close()
                

                new_text=file_read.replace('G:/MY STUFF/Dropbox/Code&ETL/Stock_Exchange/',backup_root)
                new_text=new_text.replace('C:/Users/kiran/Downloads/NSE DATA/',backup_root)

                file_write=open(path+"/variables.py",'w+')
                file_write.write(new_text)
                file_write.close()

                logger.INFO("\nupdated the root directory for nse backups,downloads")
                break

            else:
                logger.INFO(backup_root,"doesn't exist, input correct path")

        importlib.reload(sys.modules['nse_stock_load.variables'])

        from nse_stock_load.variables import backup_root,backup_path,reports_path,data_backup_path,metadata_path,local_root,local_path,mail_path,index_path,index_final_path,stop_loss_path

        dir_list=[backup_root,backup_path,reports_path,data_backup_path,metadata_path,local_root,local_path,mail_path,index_path,index_final_path,stop_loss_path]
        for dir_name in dir_list:
            try:
                os.mkdir(dir_name)
            except:
                continue
        
        logger.INFO("\nAll requried directories are available/created from base path "+backup_root)