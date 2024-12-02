# 標準ライブラリ
import datetime
import csv

# 外部ライブラリ
import pyodbc

# 定数ファイル
import constants
import util

def get_current_data():
    """現在のDBデータを取得して配列で返却する
    """
    connect= pyodbc.connect(constants.URL)
    cursor = connect.cursor()
    cursor.execute(constants.SQL_SELECT)
    rows = cursor.fetchall()

    cursor.close()
    connect.close()
    
    return rows

def store_csv(db_data):
    """DBから取得したリストをtsv形式でファイルに保存
    出力ファイル名は現在日付+時間とする
    """

    current_date = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    with open("./dbdata/" + current_date + ".csv", "w", encoding="utf_8", newline="") as f:
        writer = csv.writer(f)
        for db_row in db_data:
            writer.writerow(util.remove_blank(db_row))
    
def compare_unv_add(former="", current=""):
    """追加された大学情報をExcelで出力
    """
    
    # 最新2つのファイル名を取得
    if former=="" or current=="":
        file_names = util.extract_file_name()
        former = file_names[0]
        current = file_names[1]
    
    # それぞれのファイル読み込み
    former_data = []
    with open("./dbdata/" + former, "r", encoding="utf_8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            former_data.append(tuple(row))
    
    former_data_set = util.extract_unv_data(former_data)
    
    current_data = []
    with open("./dbdata/" + current, "r", encoding="utf_8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            current_data.append(tuple(row))
            
    current_data_set = util.extract_unv_data(current_data)
    
    # 現在データで追加された要素を抽出
    add_data = util.extract_dif_by_compare_cd(current_data_set, former_data_set)
    
    util.to_excel(add_data, constants.ADD_UNV, False)
    
def compare_unv_del(former="", current=""):
    """削除された大学情報をExcelで出力
    """
    
    # 最新2つのファイル名を取得
    if former=="" or current=="":
        file_names = util.extract_file_name()
        former = file_names[0]
        current = file_names[1]
    
    # それぞれのファイル読み込み
    former_data = []
    with open("./dbdata/" + former, "r", encoding="utf_8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            former_data.append(tuple(row))
    
    former_data_set = util.extract_unv_data(former_data)
    
    current_data = []
    with open("./dbdata/" + current, "r", encoding="utf_8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            current_data.append(tuple(row))
            
    current_data_set = util.extract_unv_data(current_data)
    
    # 現在データで削除された要素を抽出
    del_data = util.extract_dif_by_compare_cd(former_data_set, current_data_set)
    
    util.to_excel(del_data, constants.DEL_UNV, True)

def compare_unv_dif(former="", current=""):
    """差分のある大学情報をExcelで出力
    """
    
    # 最新2つのファイル名を取得
    if former=="" or current=="":
        file_names = util.extract_file_name()
        former = file_names[0]
        current = file_names[1]
    
    # それぞれのファイル読み込み
    former_data = []
    with open("./dbdata/" + former, "r", encoding="utf_8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            former_data.append(tuple(row))
    
    former_data_set = util.extract_unv_data(former_data)
    
    current_data = []
    with open("./dbdata/" + current, "r", encoding="utf_8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            current_data.append(tuple(row))
            
    current_data_set = util.extract_unv_data(current_data)
    
    # 現在データで差分のあるされた要素を抽出
    del_data = util.extract_dif(current_data_set, former_data_set)
    
    util.to_excel(del_data, constants.DIF_UNV, True)


if __name__ == '__main__':
    # current_data = get_current_data()
    # exp_name = store_csv(current_data)
    compare_unv_add()
    compare_unv_del()
    compare_unv_dif()
