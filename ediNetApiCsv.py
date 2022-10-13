#! python3
# EDINET APIから情報取得する，リストをcsvで出力する


import requests, datetime, os, csv, sqlite3

# データベースを作成する場所を指定する

os.chdir('/Users/shikishiki/Desktop/PythonDB')


# Sample.dbに接続する（自動的にコミットするようにする）
conn = sqlite3.connect("Sample.db", isolation_level=None)

# テーブルを作成する
# code text

# sql="""
# CREATE TABLE LIST(
#  docID VARCHAR(20),
#  filerName TEXT,
#  docDescription TEXT
# );
# """
# conn.execute(sql)


# day_listの作成（関数）

def make_day_list(start_date, end_date):
    print('start_date: ', start_date)
    print('end_date: ', end_date)

    period = end_date - start_date
    period =int(period.days)
    day_list = []
    for d in range(period):
        day = start_date + datetime.timedelta(days = d)
        day_list.append(day)

    day_list.append(end_date)

    return day_list

# 書類取得のためにdocID(書類管理番号)のリストを作成（関数）

def make_doc_id_list(day_list):
    securities_report_doc_list= []
    output_file = open('D:\\trial\\Data\\list.csv', 'w', newline='')    # Fileオブジェクトの生成
    output_writer = csv.writer(output_file)                  # Writerオブジェクトを生成
    output_writer.writerow(["docID", "filerName", "docDescription"]) # 項目の作成
    for index, day in enumerate(day_list):
        url = 'https://disclosure.edinet-fsa.go.jp/api/v1/documents.json' # 書類一覧APIのエンドポイント
        params = {'date' : day, 'type': 2}

        res = requests.get(url, params = params)
        json_data = res.json()                                    # resはResponseオブジェクトなので，resからjsonデータを格納する
        print(day)
        

        for num in range(len(json_data["results"])):

            ordinance_code = json_data["results"][num]["ordinanceCode"] # 府令コードを格納
            form_code = json_data["results"][num]["formCode"] # 様式コードを格納

            if ordinance_code == "010" and form_code == "030000":   # 有価証券報告書(030000)に絞る
                print(json_data["results"][num]["docID"], json_data["results"][num]["filerName"],
                      json_data["results"][num]["docDescription"])
                output_writer.writerow([json_data["results"][num]["docID"], json_data["results"][num]["filerName"],
                      json_data["results"][num]["docDescription"]])
                securities_report_doc_list.append(json_data["results"][num]["docID"])
                # SQLに保存する("docID", "filerName", "docDescription")を保存する

                a = json_data["results"][num]["docID"]

                b = json_data["results"][num]["filerName"]

                c = json_data["results"][num]["docDescription"]

                conn.execute(f'INSERT INTO LIST VALUES("{a}", "{b}", "{c}")')
              

    output_file.close()

    return securities_report_doc_list

# 書類をdocID(書類管理番号)に基づいてダウンロードする（関数）

def download_xbrl_in_zip(securities_report_doc_list, number_of_lists):
    for index, doc_id in enumerate(securities_report_doc_list):
        print(doc_id, ":", index + 1, "/", number_of_lists)
        url = "https://disclosure.edinet-fsa.go.jp/api/v1/documents/" + doc_id  # エンドポイントには，docID(書類管理番号)も入る
        params = {"type" : 1}  # リクエストパラメーターは，XBRLファイルを指定する
        filename = "/Users/shikishiki/dev/XBRL/zip/" + doc_id + ".zip"                                       # 保存場所を指定する（フォルダは必要）
        res = requests.get(url, params=params, stream = True)
        # 指定したパスのファイルを新規作成する。withでブロック終わりに閉じる
        if res.status_code == 200:
            with open(filename, 'wb') as file:
                for chunk in res.iter_content(chunk_size=1024):
                    file.write(chunk)

# 実行するmain()

def main():
    start_date = datetime.date(2022, 5, 1)   # 開始日を決める
    end_date = datetime.date(2022, 5, 31)    # 終了日を決める
    day_list = make_day_list(start_date, end_date) # day_listの作成
    securities_report_doc_list = make_doc_id_list(day_list)
    number_of_lists = len(securities_report_doc_list)
    print("number_of_lists：", len(securities_report_doc_list))
    print("get_list：", securities_report_doc_list)

    download_xbrl_in_zip(securities_report_doc_list, number_of_lists)
    print("download finish")

    c=conn.cursor()
    c.execute("SELECT * FROM LIST")
    for row in c:
        print(row[0], row[1], row[2])
    conn.close()    


main()

        

            
        




