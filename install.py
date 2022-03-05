import os
import sys
from pathlib import Path

from lib.logger import Logger
from lib.file import FileCtrl

PATH_DELIMITER = FileCtrl.getPathDelimiter()

WIN_WHEEL_LIST = ['prebuilt/wheel/python_Levenshtein-0.12.2-cp37-cp37m-win_amd64.whl']

TEMPLATE_PATH = 'template'
TEMPLATE_MIRROR = "https://gitee.com/kmou424/wfhelperpy_template"
PREBUILT_PATH = "prebuilt"
PREBUILT_MIRROR = "https://gitee.com/kmou424/wfhelperpy_prebuilt"
VENV_PATH = 'tools'
VENV_BIN_DIR = 'tools/Scripts'
VENV_PIP_PATH = 'tools/Scripts/pip.exe'
VENV_PYTHON_PATH = 'tools/Scripts/python.exe'

if 'linux' in sys.platform or 'mac' in sys.platform:
    VENV_BIN_DIR = VENV_BIN_DIR.replace('Scripts', 'bin')
    VENV_PIP_PATH = VENV_PIP_PATH.replace('.exe', '').replace('Scripts', 'bin')
    VENV_PYTHON_PATH = VENV_PYTHON_PATH.replace('.exe', '').replace('Scripts', 'bin')


def clonePrebuiltRepo():
    Logger.displayLog("正在拉取Prebuilt文件")
    os.system("git clone {repo_url} {prebuilt_path}".format(repo_url=PREBUILT_MIRROR, prebuilt_path=PREBUILT_PATH))


def cloneTemplateRepo():
    Logger.displayLog("正在拉取模板文件")
    os.system("git clone {repo_url} {template_path}".format(repo_url=TEMPLATE_MIRROR, template_path=TEMPLATE_PATH))


def createToolsVenv():
    Logger.displayLog("正在创建虚拟环境")
    os.system('python -m venv tools')


def installRequirements():
    Logger.displayLog("检查并安装依赖")
    os.system('{pip_path} install wheel'.format(pip_path=VENV_PIP_PATH.replace('/', PATH_DELIMITER)))
    if 'win' in sys.platform:
        Logger.displayLog("安装预编译wheel")
        for whl in WIN_WHEEL_LIST:
            os.system('{pip_path} install {whl}'.format(pip_path=VENV_PIP_PATH.replace('/', PATH_DELIMITER), whl=whl))
    _ret = os.system(
        '{pip_path} install -r requirements.txt'.format(pip_path=VENV_PIP_PATH.replace('/', PATH_DELIMITER)))
    if _ret == 0:
        Logger.displayLog("安装依赖成功")
    else:
        Logger.displayLog("安装依赖失败", Logger.LOG_LEVEL_ERROR, quit_code=_ret)


# 控制台返回值
ret = 0
Logger.displayLog("正在检查模板文件")
if Path(TEMPLATE_PATH).exists():
    Logger.displayLog("检测到旧的模板文件")
    Logger.displayLog("更新上游...")
    ret = os.system('git -C {template_path} pull'.format(template_path=TEMPLATE_PATH))
    if ret != 0:
        Logger.displayLog("更新上游失败", Logger.LOG_LEVEL_WARNING)
        Logger.displayLog("尝试删除现有模板文件并重新拉取")
        FileCtrl.rmtree(TEMPLATE_PATH)
        cloneTemplateRepo()
else:
    cloneTemplateRepo()

Logger.displayLog("正在检查Prebuilt文件")
if Path(PREBUILT_PATH).exists():
    Logger.displayLog("检测到旧的Prebuilt文件")
    Logger.displayLog("更新上游...")
    ret = os.system('git -C {prebuilt_path} pull'.format(prebuilt_path=PREBUILT_PATH))
    if ret != 0:
        Logger.displayLog("更新上游失败", Logger.LOG_LEVEL_WARNING)
        Logger.displayLog("尝试删除现有Prebuilt文件并重新拉取")
        FileCtrl.rmtree(PREBUILT_PATH)
        clonePrebuiltRepo()
else:
    clonePrebuiltRepo()

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
