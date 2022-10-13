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

# 正規表現をつくる(htmで終わる)

pattern = re.compile(r'^0104010.*htm')
pattern_h4 = re.compile(r'.*?【所有者別状況】.*?')
is_shareholder = False
#MD＆A情報を持つ章を抽出

def extract_md_a_contents(htm_contents: list) -> list:
    
    md_a_contents = []
    
    for content in htm_contents :

        #bs4.element.Tag型ではないとfindメソッドでtypeエラーを起こすため判定
        if not isinstance(content, bs4.element.Tag) :
            continue

        found = content.find(class_=re.compile("smt_head"))
        #findしたけどデータがない場合.textプロパティを呼び出す際にtypeエラーを起こすため判定
        if not found :
            continue

        title = found.text
        #md_aの章番号を指定
            # "1【経営方針、経営環境及び対処すべき課題等】",
            # "3【経営者による財政状態、経営成績及びキャッシュ・フローの状況の分析】"
        #企業によって全角と半角か別れる可能性があるためどちらも判定
        if title[0] in ['１', '1','３', '3']  :
             md_a_contents.append(content)
            
    return md_a_contents


# 必要な部分に絞る

def insert_df(md_a_contents: list) -> list:
    
    md_a_df = list()

    for content in  md_a_contents : 
        # テキスト情報を持つbs4.element.Tag型のみ取得
        found_values = content.find_all(class_=re.compile("smt_head3"))
         # テキストを取得
        md_a_df = list(map(lambda val: val.text,found_values))
        
    return md_a_df


full_list = []
company_list = []
for foldername, subfolders, filenames in os.walk(directory_zip):
    is_value = False

    # テキストを保存するための空の箱を用意する（ループ毎に空になる）
    b = ""

    # カレントディレクトリの全ファイルをループする
    for edi_filename in os.listdir(foldername):

        mo = pattern.search(edi_filename)
        # htmlファイル以外はスキップする
        if mo == None:
            continue
        print(mo)
        print(foldername+'/'+edi_filename)

        directory = foldername+'/'+edi_filename


        # スクレイピングの処理をいれる(引数にedi_filenameを使えばよい)(foldernameも使える)
        htm = open(directory, 'r',encoding="utf-8" )

        sp = BeautifulSoup(htm, "html.parser")


        #list型でMD&Aの見出し以下を子要素にもつモノ

        htm_contents = sp.find_all(True)
        print(len(htm_contents))#所有
        num = 0
        for tag in htm_contents:

            value_list = []
            num += 1
            # print(i)
            # print(num,"--------------------")
            if tag.name == 'h4' and '【所有者別状況】' in tag.text:
                print(tag.text)
                print('【所有者別状況】' in tag.text)
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
                                    #     print(value.find('p').text)
                                    #     print("-----------")
                                    #     value_list.append(value.find('p').text)

                                    if value.find('ix:nonfraction') and value.find('ix:nonfraction') != -1:
                                        print(value.find('ix:nonfraction').text)
                                        print("-----------")
                                        value_list.append(value.find('ix:nonfraction').text)

                                    # if value.find('span') and value.find('span') != -1:
                                    #     print(value.find('span').text)
                                    #     print("-----------")
                                    #     value_list.append(value.find('span').text)
            if value_list:
                company_list.append(foldername)
                full_list.append(value_list)
                is_value = True
                # exit()
            
    # if not is_value and 'PublicDoc/' in foldername[8:] :        
    #     company_list.append(foldername)
    
for l,i in enumerate(full_list) :
    print(l,len(i))
    print(i)

print(len(full_list))
# print(len(company_list))  
# for i in company_list:     
#     print(i)