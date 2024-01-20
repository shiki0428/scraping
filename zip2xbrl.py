#! python3
# zipファイルをXBRLファイルに展開する

import zipfile, os


os.chdir("C:/Users/金城諒洋/OneDrive/DB/zip")  # zipファイルが存在するディレクトリに移動する

for i in os.listdir("C:/Users/金城諒洋/OneDrive/DB/zip"):
    try:
        print(i)
        example_zip = zipfile.ZipFile(i)
        folder_name = i.replace('.zip', '') # フォルダの名称
        locate = "C:/Users/金城諒洋/OneDrive/DB/xbrl/" + folder_name  # 移動先のパス
        example_zip.extractall(locate) # 新しくフォルダをつくり，そこに展開する
        example_zip.close()
    except Exception:
        pass
