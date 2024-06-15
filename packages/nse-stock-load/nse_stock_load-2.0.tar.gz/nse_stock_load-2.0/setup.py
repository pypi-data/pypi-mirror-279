# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 22:59:19 2020

@author: kiran
"""

from setuptools import setup,find_packages

setup(
      name='nse_stock_load',
    version='2.0',
    description='Package of load end to end nse data into mysql Database, corrected to_char to DATE_FORMAT',
    author='kiran nanduri',
    author_email='kirannanduri@outlook.com',
    packages=find_packages(include=['NSE_STOCK_LOAD']),
    include_package_data=True,
    license='kiran',
    zip_safe=False,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt"],
    },

    entry_points={
        "setuptools.installation": [
            "env_check_n_setup = nse_stock_load.env_setup:env_check_n_setup"
        ],
    },
    install_requires=
    [ 
    'requests==2.25.1',
    'pandas',
    'numpy',
    'SQLAlchemy==1.4.14'
    ]
   
)
