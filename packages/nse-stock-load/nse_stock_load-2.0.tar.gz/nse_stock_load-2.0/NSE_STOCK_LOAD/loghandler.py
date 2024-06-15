#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 01:42:18 2021

@author: kiran
"""

from datetime import date
import logging

def logger(logfile='nse_load'):
    
    logfile=logfile+date.today()+'.log'
    logger = logging.getLogger("__name__")
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s -5s- %(funcName)s - 25s - %(levelname)s - 5s - (process)d - 5s - %(message)s')
    
    fh = logging.FileHandler(logfile)
    fh.setFormatter(formatter)
    
    sh = logging.StreamHandler(setLevel=logging.INFO)
    sh.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(sh)