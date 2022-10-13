# scraping

.env
DIRCTORY_PATH = apiでダウンロードした情報格納ディレクトリpath
DIRCTORY_ZIP_PATH = zip解凍先path

python -m venv venv
source venv/bin/activate
pip install -r requiremnt.txt

1. docid_download_from_edinet.py
2. python zip2xbrl.py
3. shareholderComposition.py