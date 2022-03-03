import base64
import os
from pathlib import Path

from lib.utils import Downloader, Hash
from lib.file import FileCtrl

DEFAULT_MIRROR = 'https://gitee.com/kmou424/wfhelperpy_template/raw/main/'
PWD = os.getcwd()
TEMPLATE_PATH = PWD + '\\template'
TEMPLATE_HASH_FILENAME = 'template_hash.txt'
TEMPLATE_HASH_FILEPATH = TEMPLATE_PATH + '\\' + TEMPLATE_HASH_FILENAME

FileCtrl.checkDir(TEMPLATE_PATH)
if Path(TEMPLATE_HASH_FILEPATH).exists():
    os.remove(TEMPLATE_HASH_FILEPATH)

Downloader.downloadFile(
    url=DEFAULT_MIRROR + '/' + TEMPLATE_HASH_FILENAME,
    filepath=TEMPLATE_HASH_FILEPATH
)

cnt = 0

with open(TEMPLATE_HASH_FILEPATH, 'r') as file:
    all_lines = file.readlines()
    for line in all_lines:
        if line != '' and line is not None:
            line = base64.b64decode(line.encode('utf-8')).decode('utf-8')
            cnt += 1
            name_hash = line.split(' ')
            path = TEMPLATE_PATH + '\\' + name_hash[0]
            print('[{cnt}] Checking file {filename}'.format(cnt=cnt, filename=name_hash[0]))
            if not Path(path).exists():
                print('[Error] File is missing, will download it for now')
                FileCtrl.checkDir(os.path.dirname(path))
                Downloader.downloadFile(DEFAULT_MIRROR + name_hash[0].replace('\\', '/'), path)
            else:
                if name_hash[1] != Hash.getFileHash(path):
                    print('[Warning] This file has an update, will download it for now')
                    os.remove(path)
                    Downloader.downloadFile(DEFAULT_MIRROR + name_hash[0].replace('\\', '/'), path)
                else:
                    print('[Info] OK')
