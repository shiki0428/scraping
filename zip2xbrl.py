#! python3
# zipファイルをXBRLファイルに展開する

import zipfile
from dotenv import load_dotenv
import os
load_dotenv()
directory_zip = os.getenv('DIRCTORY_ZIP_PATH')
directory_path = os.getenv('DIRCTORY_PATH')

os.chdir(directory_path)  # zipファイルが存在するディレクトリに移動する

for i in os.listdir(directory_path):
    print(i)
    example_zip = zipfile.ZipFile(i)
    folder_name = i.replace('.zip', '') # フォルダの名称
    locate = directory_zip + folder_name  # 移動先のパス
    example_zip.extractall(locate) # 新しくフォルダをつくり，そこに展開する
    example_zip.close()
