#! python3
# zipファイルをXBRLファイルに展開する

import zipfile, os


os.chdir('/Users/shikishiki/dev/XBRL/zip')  # zipファイルが存在するディレクトリに移動する

for i in os.listdir('/Users/shikishiki/dev/XBRL/zip'):
    print(i)
    example_zip = zipfile.ZipFile(i)
    folder_name = i.replace('.zip', '') # フォルダの名称
    locate = '/Users/shikishiki/dev/XBRL/xbrl/' + folder_name  # 移動先のパス
    example_zip.extractall(locate) # 新しくフォルダをつくり，そこに展開する
    example_zip.close()
