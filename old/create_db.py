import sqlite3

# TEST.dbを作成する
# すでに存在していれば、それにアスセスする。
dbname = 'EDINET.db'
conn = sqlite3.connect(dbname)

# データベースへのコネクションを閉じる。(必須)



cur = conn.cursor()

cur.execute(
    """
CREATE TABLE IF NOT EXISTS company(
    docID text,
    company_name text,
    PRIMARY KEY (docID)
);    
    """
)
#   Government and local governments   financial_institution   Financial_Instruments Business_Operator   Other_legal_entities
cur.execute(
    """
CREATE TABLE IF NOT EXISTS company_composition(
    docID text,
    Government_and_local_governments NUMERIC(9,3),
    financial_institution NUMERIC(9,3),
    Financia_Instruments_Business_Operator NUMERIC(9,3),
    Other_legal_entities NUMERIC(9,3),
    Non_individual NUMERIC(9,3),
    individual NUMERIC(9,3),
    Individual_Other NUMERIC(9,3),
    total NUMERIC(9,3),

    PRIMARY KEY (docID)
);    
    """
)



conn.close()