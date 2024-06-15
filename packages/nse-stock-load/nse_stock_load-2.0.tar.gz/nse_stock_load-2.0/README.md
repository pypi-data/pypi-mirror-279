Python code to download NSE stock data from NSE website, transform and load data into Oracle DB.

Below are the setup to install the Package.

1) Download StockCode and setup.py files to your local pc.

2) Install all prerequisite modules by running below command from StockCode folder
   
   pip install -r requirements.txt
    
3) Run below command to install module.
  
   python setup.py install

4) Create Tables in Oracle as in "TablesMetadata.txt".

5) Insert data into "stockcode" table as in "stockcode.txt".

6) Import python module and run as below to download NSE data and load data into ORACLE.

      from nse_stock_load import sequence
      
      sequence.load_till_date()
