#! python3
# html2sql.py - フォルダからhtmlファイルをスクレイピングしてSQLに保存する

import os, re
import bs4
from bs4 import BeautifulSoup
import pandas as pd # 消してもいいかも
import sqlite3

# データベースを作成する場所を指定する

os.chdir("E:/ゼミ/companies/")


# Sample.dbに接続する（自動的にコミットするようにする）
conn = sqlite3.connect("Sample.db", isolation_level=None)

# テーブルを作成する
# code text

# sql="""
# CREATE TABLE MD(
#  docID VARCHAR(20),
#  md TEXT
# );
# """
# conn.execute(sql)

# 正規表現をつくる(htmで終わる)

htm_pattern = re.compile(r'htm$')

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
        found_values = content.find_all(class_=re.compile("smt_text"))
         # テキストを取得
        md_a_df = list(map(lambda val: val.text,found_values))

    return md_a_df


for foldername, subfolders, filenames in os.walk('/Users/shikishiki/Desktop/xbrl'):

    # テキストを保存するための空の箱を用意する（ループ毎に空になる）

    b = ""

    # カレントディレクトリの全ファイルをループする

    for edi_filename in os.listdir(foldername):

        mo = htm_pattern.search(edi_filename)

        # htmlファイル以外はスキップする
        if mo == None:
            continue

        # スクレイピングの処理をいれる(引数にedi_filenameを使えばよい)(foldernameも使える)

        htm = open(foldername+'/'+edi_filename, 'r',encoding="utf-8" )

        sp = BeautifulSoup(htm, "html.parser")

        #list型でMD&Aの見出し以下を子要素にもつモノ

        htm_contents = sp.find('body').div.contents
        print(htm_contents)
        md_a_contents = extract_md_a_contents(htm_contents)
        print(md_a_contents)
        exit()

        md_a_df = insert_df(md_a_contents)


        # md_a_dfがemptydataならばスキップする
        if not md_a_df:
            continue


        md_a_df_text = ':'.join(md_a_df)        # listになっているので結合して文字列にする


        b= b +  md_a_df_text.replace('"', '')      # テキストの中に(")が入っていると文字列の認識が上手くできないため除いた上で加える


    # データを登録する

    # bがemptydataならばスキップする

    if not b:
            continue

    test = foldername.lstrip('E:/ゼミ/companies/xbrl')

    code = test.rsplit('E:/ゼミ/companies/PublicDoc') # listになっているので，１つ目を取り出す

    a = code[0]

    print(a)

    conn.execute(f'INSERT INTO MD VALUES("{a}","{b}")') 


conn.close()

