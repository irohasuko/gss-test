# DB接続用定数
DRIVER = '{SQL Server}'
SERVER = 'HP-ENVY'
DATABASE = 'SCH_INFO'
TRUSTED_CONNECTION ='yes'
SQL_SELECT = "SELECT SHC_CD, DEP_CD, CLS_CD, SHC_NAME, DEP_NAME, CLS_NAME, CONCAT(SHC_CD, DEP_CD, CLS_CD) AS 比較用コード FROM SCHOOL_INFO"
    
URL = 'DRIVER='+DRIVER+';SERVER='+SERVER+';DATABASE='+DATABASE+';PORT=1433;Trusted_Connection='+TRUSTED_CONNECTION+';'

# エクセル保存用ヘッダー行
HEADER = 'SHC_CD, DEP_CD, CLS_CD, SHC_NAME, DEP_NAME, CLS_NAME, 比較用コード'

# 処理用
## 大学と専門学校のコード境界(7までが大学、8からが専門)
BORDER_UNV_VOC = 8

## 学校名の列番目
ROW_SCH_NAME = 3
## 学科名の列番目
ROW_DEP_NAME = 4
## 比較用コードの列番目
ROW_COMPARE_CD = 6

## エクセルシート名
ADD_UNV = '大学追加'
DEL_UNV = '大学削除'
DIF_UNV = '大学差分'
ADD_VOC = '専門追加'
DEL_VOC = '専門削除'
DIF_VOC = '専門差分'
