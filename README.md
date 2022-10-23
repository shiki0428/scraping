# scraping

## 環境ファイルの設定  
.env    
DIRCTORY_PATH = #apiでダウンロードした情報格納ディレクトリpath 
DIRCTORY_ZIP_PATH = zip解凍先path  
#FORMAT:YYYY-MM-DD  
START_DATE = '2021-05-01'  
END_DATE = '2022-05-01'  

## 必要ライブラリインストール
```
python -m venv venv
source venv/bin/activate
pip install -r requiremnt.txt
```


## 実行ファイル
1. create_db.py  #sqlite テーブル作成
2. docid_download_from_edinet.py #edinetからzipダウンロード
3. zip2xbrl.py　#zipを解凍
4. shareholderComposition.py #【所有者別状況】の表の情報をDBに登録
5. shareholderComposition_2.py #【所有者別状況】の表の情報をDBに登録 取得できなかったできなかった約100社を追加取得


## sqlite操作　csvに書き出しなど
```
sqlite3 EDINET.db #dbにアクセス

.headers on
.mode csv
.once　export.csv

select company.company_name,
company_composition.docID, 
company_composition.Government_and_local_governments, 
company_composition.financial_institution, 
company_composition.Financia_Instruments_Business_Operator, 
company_composition.Other_legal_entities, 
company_composition.Non_individual, 
company_composition.individual, 
company_composition.Individual_Other, 
company_composition.total
from company
left outer join company_composition on company.docID = company_composition.docID
order by total desc;

```

## 課題
- shareholderComposition.py を実行しても取得したいデータの1割は欠損が生じる  
  edinetに公開しているファイルのうちformatに従っていない会社がある
- テーブルに年度を保存するcolumnを追加かつpkにも追加した方が良い　