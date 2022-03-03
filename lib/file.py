import shutil
import stat
from pathlib import Path
import os
import sys


class FileCtrl:
    @staticmethod
    def checkDir(dirname: str, isCreate=True):
        isExist = True
        if not Path(dirname).exists():
            isExist = False
            if isCreate:
                os.makedirs(dirname)
        return isExist

    @staticmethod
    def getPathDelimiter():
        if 'win' in sys.platform:
            return '\\'
        elif 'mac' in sys.platform or 'linux' in sys.platform:
            return '/'
        else:
            print("error: Unrecognized platform " + sys.platform + " or not support")
            exit(1)

    @staticmethod
    def getAllFilesList(directory: str) -> list:
        _files = []
        file_list = os.listdir(directory)
        for _i in range(0, len(file_list)):
            path = os.path.join(directory, file_list[_i])
            if os.path.isdir(path):
                _files.extend(FileCtrl.getAllFilesList(path))
            if os.path.isfile(path):
                _files.append(path)
        return _files

    @staticmethod
    def isExist(filename: str) -> bool:
        return Path(filename).exists()

    @staticmethod
    def rmtree(path: str):
        if 'linux' in sys.platform or 'mac' in sys.platform:
            os.system('rm -rf {path}'.format(path=path))
        else:
            return shutil.rmtree(path, onerror=FileCtrl.__onRmtreeError)

    @staticmethod
    def __onRmtreeError(func, path, execinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)
