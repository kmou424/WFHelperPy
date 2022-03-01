import os
import sys
from pathlib import Path

from lib.logger import Logger
from lib.utils import FileCtrl

PATH_DELIMITER = FileCtrl.getPathDelimiter()

TEMPLATE_PATH = 'template'
TEMPLATE_MIRROR = "https://gitee.com/kmou424/wfhelperpy_template"
VENV_PATH = 'tools'
VENV_BIN_DIR = 'tools/Scripts'
VENV_PIP_PATH = 'tools/Scripts/pip.exe'
VENV_PYTHON_PATH = 'tools/Scripts/python.exe'

if 'linux' in sys.platform or 'mac' in sys.platform:
    VENV_BIN_DIR = VENV_BIN_DIR.replace('Scripts', 'bin')
    VENV_PIP_PATH = VENV_PIP_PATH.replace('.exe', '').replace('Scripts', 'bin')
    VENV_PYTHON_PATH = VENV_PYTHON_PATH.replace('.exe', '').replace('Scripts', 'bin')


def cloneTemplateRepo():
    Logger.displayLog("正在拉取模板文件")
    os.system("git clone {repo_url} {template_path}".format(repo_url=TEMPLATE_MIRROR, template_path=TEMPLATE_PATH))


def createToolsVenv():
    Logger.displayLog("正在创建虚拟环境")
    os.system('python -m venv tools')


def generateRunScript():
    if 'win' in sys.platform:
        with open('run.bat', 'w') as run_bat:
            run_bat.writelines('@title WFHelperPy\n')
            run_bat.writelines('{python_path} wfhelper.py\n'
                               .format(python_path=VENV_PYTHON_PATH.replace('/', '\\')))
    if 'linux' in sys.platform or 'mac' in sys.platform:
        with open('run.sh', 'w') as run_sh:
            run_sh.writelines('#!/bin/bash\n')
            run_sh.writelines('{python_path} wfhelper.py\n'
                              .format(python_path=VENV_PYTHON_PATH))
    Logger.displayLog("生成新的启动脚本", quit_code=0)


def removeOldRunScript():
    if Path('run.bat').exists():
        os.remove('run.bat')
    if Path('run.sh').exists():
        os.remove('run.sh')
    Logger.displayLog("清除旧的启动脚本")


def installRequirements():
    Logger.displayLog("检查并安装依赖")
    ret = os.system(
        '{pip_path} install -r requirements.txt'.format(pip_path=VENV_PIP_PATH.replace('/', PATH_DELIMITER)))
    removeOldRunScript()
    if ret == 0:
        Logger.displayLog("安装依赖成功")
        generateRunScript()
    else:
        Logger.displayLog("安装依赖失败", Logger.LOG_LEVEL_ERROR, quit_code=ret)


Logger.displayLog("正在检查模板文件")
if Path(TEMPLATE_PATH).exists():
    Logger.displayLog("检测到旧的模板文件")
    Logger.displayLog("更新上游文件")
    os.system('git -C {template_path} pull'.format(template_path=TEMPLATE_PATH))
else:
    cloneTemplateRepo()

Logger.displayLog("正在检查虚拟环境")
if Path(VENV_PATH).exists():
    if Path(VENV_BIN_DIR).exists() and Path(VENV_PIP_PATH).exists() and Path(VENV_PYTHON_PATH).exists():
        Logger.displayLog("虚拟环境正常")
    else:
        Logger.displayLog("虚拟环境异常, 将开始重建", Logger.LOG_LEVEL_WARNING)
        FileCtrl.rmtree(VENV_PATH)
        createToolsVenv()
else:
    Logger.displayLog("虚拟环境不存在")
    createToolsVenv()
installRequirements()
