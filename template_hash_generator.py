import base64
import os
from pathlib import Path

from lib.file import FileCtrl
from lib.utils import HashUtils

FILE_EXT = ['png', 'json']
PWD = os.getcwd()
TEMPLATE_PATH = PWD + '\\template'
TEMPLATE_HASH_FILEPATH = TEMPLATE_PATH + '\\template_hash.txt'
FileCtrl.checkDir(TEMPLATE_PATH)
if Path(TEMPLATE_HASH_FILEPATH).exists():
    os.remove(TEMPLATE_HASH_FILEPATH)

files = FileCtrl.getAllFilesList(TEMPLATE_PATH)
with open(TEMPLATE_HASH_FILEPATH, mode='w') as file:
    for i in files:
        for ext in FILE_EXT:
            if str(i).endswith(ext):
                line = "{filename} {hash}".format(
                    filename=str(i).replace(TEMPLATE_PATH + '\\', ''),
                    hash=HashUtils.getFileHash(i)
                )
                file.write(base64.b64encode(line.encode('utf-8')).decode('utf-8') + '\n')
