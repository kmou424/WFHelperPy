import os
import sys
from pathlib import Path

from lib.logger import Logger

VENV_PYTHON_PATH = 'tools/Scripts/python.exe'
RUNNER_DIR = 'runners/'
WIN_SCRIPT_NAME = '.bat'
LINUX_SCRIPT_NAME = '.sh'

if len(sys.argv) == 3:
    if not 0 <= int(sys.argv[1]) <= 65536:
        Logger.displayLog("端口号无效", Logger.LOG_LEVEL_ERROR, -1)
    WIN_SCRIPT_NAME = sys.argv[2] + WIN_SCRIPT_NAME
    LINUX_SCRIPT_NAME = sys.argv[2] + LINUX_SCRIPT_NAME
else:
    print("Usage: {filename} [port] [session_name]"
          .format(filename=os.path.basename(sys.argv[0])))
    exit(-1)

if not Path(RUNNER_DIR).exists():
    os.makedirs(RUNNER_DIR)


def generateRunScript(name):
    if 'win' in sys.platform:
        with open(RUNNER_DIR + WIN_SCRIPT_NAME, 'w') as run_bat:
            run_bat.writelines('@title {name}\n'.format(name=name))
            run_bat.writelines('{python_path} wfhelper.py {port} {config_path}\n'
                               .format(
                                    python_path=VENV_PYTHON_PATH.replace('/', '\\'),
                                    port=sys.argv[1],
                                    config_path='configs/{name}.ini'.format(name=name)
                                ))
            Logger.displayLog("会话已创建，请执行 .\\{path} 来启动会话".format(path=RUNNER_DIR.replace('/', '\\') + WIN_SCRIPT_NAME), Logger.LOG_LEVEL_INFO)
    if 'linux' in sys.platform or 'mac' in sys.platform:
        with open(RUNNER_DIR + LINUX_SCRIPT_NAME, 'w') as run_sh:
            run_sh.writelines('#!/bin/bash\n')
            run_sh.writelines('{python_path} wfhelper.py {port} {config_path}\n'
                              .format(
                               python_path=VENV_PYTHON_PATH,
                               port=sys.argv[1],
                               config_path='configs/{name}.ini'.format(name=name)
                                ))
            Logger.displayLog("会话已创建，请执行 ./{path} 来启动会话".format(path=RUNNER_DIR + LINUX_SCRIPT_NAME), Logger.LOG_LEVEL_INFO)


def removeOldRunScript(name):
    if Path(WIN_SCRIPT_NAME).exists():
        os.remove(WIN_SCRIPT_NAME)
    if Path(LINUX_SCRIPT_NAME).exists():
        os.remove(LINUX_SCRIPT_NAME)


removeOldRunScript(sys.argv[2])
generateRunScript(sys.argv[2])
