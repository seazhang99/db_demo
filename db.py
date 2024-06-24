from hdbcli import dbapi
import json
import pandas as pd
from decimal import Decimal

from config import HC


#Does quasi the same things as json.loads from here: https://pypi.org/project/dynamodb-json/. 
#To ensure the decimal type data be converted correct. 
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
    
def format_data(rows, cursor_descriptions, output_format = 'raw'):
    results = []
    for row in rows:
        result = {}
        for index in range(len(row)):
            result[cursor_descriptions[index][0]] = row[index]
        results.append(result)
    ret = results
    if output_format == 'json':
        ret = json.dumps(results, cls=JSONEncoder)
    elif output_format == 'dataframe':
        ret = pd.DataFrame(results)
    return ret

def get_connection():
    address = HC['endpoint'] 
    port = HC['port']
    user = HC['user']
    password = HC['password']
    
    conn = dbapi.connect(
        address = address,
        port = port,
        user = user,
        password = password,
        encrypt = True,
        sslValidateCertificate = False
    )
    return conn

def update_sql(sql):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()
    conn.close()

def execute_sql(sql):
    print(sql)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    results = rows
    cursor_descriptions = cursor.description
    cursor.close()
    conn.close()
    return cursor_descriptions, results

def db_query(sql, outputformat = 'raw'):
    cursor_descriptions, rows = execute_sql(sql)
    return format_data(rows, cursor_descriptions, outputformat)

#sql = "SELECT DISTINCT SCHEMA_NAME, TABLE_NAME, COLUMN_NAME, DATA_TYPE_NAME, LENGTH, SCALE FROM SYS.TABLE_COLUMNS WHERE SCHEMA_NAME = 'DATMOK'"
#sql = "SELECT DISTINCT * FROM DATMOK.BUSINESS_PARTNERS"
#data = query(sql)
#print(data)
#sql = 'SELECT TOP 10 bp.PARTNERID AS "BP ID", bp.COMPANYNAME AS "BP Name", SUM(soi.NETAMOUNT) AS "Total Net Amount" FROM DATMOK.SALES_ORDERS so INNER JOIN DATMOK.SALES_ORDER_ITEMS soi ON so.SALESORDERID = soi.SALESORDERID INNER JOIN DATMOK.BUSINESS_PARTNERS bp ON so.PARTNERID = bp.PARTNERID WHERE YEAR(so.CREATEDAT) = 2015 AND so.SALESORG = \'APJ\' GROUP BY bp.PARTNERID, bp.COMPANYNAME ORDER BY SUM(soi.NETAMOUNT) DESC'
#print(query(sql, outputformat='json'))