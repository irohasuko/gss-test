# 標準ライブラリ
import datetime
import csv
import struct

# 外部ライブラリ
import requests 
import pyodbc

def get_token():
    identity_endpoint = "http://169.254.169.254/metadata/identity/oauth2/token"
    resource_uri="https://database.windows.net/"
    token_auth_uri = f"{identity_endpoint}?resource={resource_uri}&api-version=2019-08-01"
    head_msi = {"Metadata": "true"}
    resp = requests.get(token_auth_uri, headers=head_msi)
    access_token = resp.json()['access_token']
    
    SQL_COPT_SS_ACCESS_TOKEN = 1256

    byte_access_token = bytes(access_token, 'utf-8')
    exptoken = b''
    for i in byte_access_token:
            exptoken += bytes({i})
            exptoken += bytes(1)
    tokenstruct = struct.pack("=i", len(exptoken)) + exptoken

    token_dict = {SQL_COPT_SS_ACCESS_TOKEN: tokenstruct}
    
    return token_dict    

def get_current_data(token_dict):
    """現在のDBデータを取得して配列で返却する
    """
    conn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=tcp:python-auth-test.database.windows.net,1433;Database=python-bat;", attrs_before = token_dict)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Employees')
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return rows

def store_csv(db_data):
    """DBから取得したリストをtsv形式でファイルに保存
    出力ファイル名は現在日付+時間とする
    """

    current_date = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    with open("./dbdata/" + current_date + ".csv", "w", encoding="utf_8", newline="") as f:
        writer = csv.writer(f)
        for db_row in db_data:
            writer.writerow(remove_blank(db_row))

def remove_blank(list):
    """リストの各項目の末尾にある空白文字を削除
    """
    return [element.rstrip() if isinstance(element, str) else element for element in list]

if __name__ == '__main__':
    # current_data = get_current_data()
    # exp_name = store_csv(current_data)
    token = get_token()
    rows = get_current_data(token)
    store_csv(rows)
