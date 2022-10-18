#! python3
# html2sql.py - フォルダからhtmlファイルをスクレイピングしてSQLに保存する

import os, re
import bs4
from bs4 import BeautifulSoup
import pandas as pd # 消してもいいかも
import sqlite3

from dotenv import load_dotenv
import os
load_dotenv()
directory_zip = os.getenv('DIRCTORY_ZIP_PATH')
directory_path = os.getenv('DIRCTORY_PATH')

conn = sqlite3.connect("EDINET.db", isolation_level=None)
cur = conn.cursor()

sql = '''INSERT INTO company_composition (
    docID,
    Government_and_local_governments,
    financial_institution,
    Financia_Instruments_Business_Operator,
    Other_legal_entities,
    Non_individual,
    individual,
    Individual_Other,
    total) VALUES (?,?,?,?,?,?,?,?,?);'''


select_sql = '''
    select 
        total 
    from company_composition
    where
        docID = ?
'''
# 正規表現をつくる(htmで終わる)

pattern = re.compile(r'^0104010.*htm')
pattern_h4 = re.compile(r'.*?【所有者別状況】.*?')
is_shareholder = False
#MD＆A情報を持つ章を抽出
# 必要な部分に絞る

full_list = []
company_list = []
tmp = 0

def isfloat(s):  # 浮動小数点数値かどうかを判定
    try:
        float(s)  # 試しにfloat関数で文字列を変換
    except ValueError:
        return False  # 失敗すれば False
    else:
        return True 

for foldername, subfolders, filenames in os.walk(directory_zip):
    is_value = False

    # テキストを保存するための空の箱を用意する（ループ毎に空になる）
    b = ""
    
    dir_len = len(directory_zip)
    if (len(foldername) != (dir_len + 23)):
        continue

    doc_id = foldername[dir_len : dir_len + 8]
    cur.execute(select_sql,[doc_id])
    is_col = cur.fetchone()
    if  is_col:
        # print(is_col)
        continue
    # カレントディレクトリの全ファイルをループする
    for edi_filename in os.listdir(foldername):

        mo = pattern.search(edi_filename)
        # htmlファイル以外はスキップする
        if mo == None:
            continue

        # print(foldername+'/'+edi_filename)


        directory = foldername+'/'+edi_filename


        # スクレイピングの処理をいれる(引数にedi_filenameを使えばよい)(foldernameも使える)


        htm = open(directory, 'r',encoding="utf-8" )

        sp = BeautifulSoup(htm, "html.parser")


        #list型でMD&Aの見出し以下を子要素にもつモノ

        htm_contents = sp.find_all(True)
        # print(len(htm_contents))#所有
        num = 0
        for tag in htm_contents:

            value_list = []
            num += 1
            # print(i)
            # print(num,"--------------------")
            if tag.name == 'h4' and '【所有者別状況】' in tag.text:
                # print(tag.text)
                # print('【所有者別状況】' in tag.text)
                is_shareholder = True
            if tag.name == 'div' and is_shareholder:
                is_shareholder = False
                # print(tag)
                for table in tag:
                    if table.name == 'table':
                        # print(table)     
                        for td in table:
                            # print(td)
                            for p in td:
                                for value in p:
                                    # print(value)
                                    # if value.find('p') and value.find('p') != -1:
                                    #     # print(value.find('p').text)
                                    #     # print("-----------")
                                    #     value_list.append(value.find('p').text)

                                    # if value.find('ix:nonfraction') and value.find('ix:nonfraction') != -1:
                                    #     # print(value.find('ix:nonfraction').text)
                                    #     # print("-----------")
                                    #     val = value.find('ix:nonfraction').text.replace(",","") or "0"
                                    #     value_list.append( float(val) )

                                    if value.find('span') and value.find('span') != -1:
                                        # print(value)
                                        # print(value.find('span').text)
                                        # print("-----------")
                                        val = value.find('span').text.replace(",","") or "0"
                                        
                                        if not isfloat(val):
                                            val = 0

                                    
                                        value_list.append(float(val))
            if value_list:
                tmp += 1
                
                if len(value_list) < 3:
                    is_shareholder = True
                    continue
                print(len(value_list))
                company_list.append(doc_id)
                full_list.append(value_list)
                is_value = True
                # if tmp == 100:
                #     for l,i in enumerate(full_list):
                #         print(company_list[l])
                #         print(i)
                #         print("------------------")
                #     exit()
                # exit()

        # if ("S100NXKY" in foldername ):
        #     print(full_list[-1][-6:])
        #     exit()         
    # if not is_value and 'PublicDoc/' in foldername[8:] :        
    #     company_list.append(foldername)

count = 0    
for l,i in enumerate(full_list) :
    if len(i) == 42:
        count += 1
        print([company_list[l]],len(i),i[-9:-1])
    # print([company_list[l]]+i[-7:]+[100])
    try:
        cur.execute(sql,[company_list[l]]+i[-9:-1])
    except:
        pass 

print(count)
print(len(full_list))

conn.close()


# print(len(company_list))  
# for i in company_list:     
#     print(i)


"""
.headers on
.mode csv
.once export2.csv

select * from company
left outer join company_composition on company.docID = company_composition.docID
order by total desc;

"""