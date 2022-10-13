#ディレクトリ作成　ダウンロード
directory_path = "/Users/shikishiki/dev/XBRL/companies/"
#ここに保存んしたいフォルダー名とpath を書く　path は調べて！！

import datetime
import requests
import pandas as pd
import os
start_date = datetime.date(2022, 5, 1)
end_date = datetime.date(2022, 5,30)

period = end_date - start_date
period = int(period.days)
day_list = []
for d in range(period):
    day = start_date + datetime.timedelta(days=d)
    day_list.append(day)
    
day_list.append(end_date)

#結果を格納するための空のリストを用意します
report_list =[]
#日付リストの期間に提出された書類のメタデータを取得してjson形式に変換します
for day in day_list:
    url = "https://disclosure.edinet-fsa.go.jp/api/v1/documents.json"
    params = {"date": day, "type": 2}
    res = requests.get(url, params=params)
    json_data = res.json()

    for num in range(len(json_data["results"])):
        ordinance_code= json_data["results"][num]["ordinanceCode"]
        form_code= json_data["results"][num]["formCode"]
        
	#ordinance_code=010かつform_code=030000が有価証券報告書になります
        if ordinance_code == "010" and  form_code =="030000" :
            company_name=json_data["results"][num]["filerName"]
            edi={ '会社名':company_name,
                        '書類名':json_data["results"][num]["docDescription"],           
                        'docID':json_data["results"][num]["docID"],
                        '証券コード':json_data["results"][num]["secCode"],
                        '日付': day             }

            dir_path = directory_path + "{}/".format(edi['会社名'])
            if not os.path.exists(dir_path): 
                os.mkdir(dir_path)
            url = "https://disclosure.edinet-fsa.go.jp/api/v1/documents/" + json_data["results"][num]["docID"]
            params = {"type": 1}
            filename =  dir_path + json_data["results"][num]["docID"] + ".zip"
            res = requests.get(url, params=params ,stream=True)

            if res.status_code == 200:
                with open(filename, 'wb') as file:
                    for chunk in res.iter_content(chunk_size=1024):
                        file.write(chunk)

            # exit()
            report_list.append(edi)

# df = pd.DataFrame(report_list)
# print(df)

# docid =df[df['証券コード'] == '83160']['docID']
# print(docid)



