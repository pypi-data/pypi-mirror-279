# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 22:16:32 2020

@author: kiran
"""

from nse_stock_load.variables import local_root,local_path,mail_path
import os

def purge():

    index_path=local_root+"nse_indices/"

    for root,path,files in os.walk(mail_path):
        for file in files:
            os.remove(os.path.join(root+file))

    for root,path,files in os.walk(local_path):
        for file in files:
            os.remove(os.path.join(root+file))

    for root,path,files in os.walk(index_path,topdown=False):
        if 'final' not in root:
            try:
                for file in files:
                    os.remove(os.path.join(root+file))
            except:
                pass


if "__name__" == "__main__":
    purge()