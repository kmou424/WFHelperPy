import os
import sys

import cv2

from lib.config import ConfigManager
from lib.constants import ConfigOptions, ConfigSections, StatusCode
from lib.file import FileCtrl
from lib.utils import AdbTools


def printHelp():
    print("{filename} [release_game_version] [template_img_name]"
          "[left-top-x] [left-top-y] [right-bottom-x] [right-bottom-y]"
          .format(filename=os.path.basename(sys.argv[0])))


if __name__ == "__main__":
    cfgMan = ConfigManager('config.ini', writable=False)
    address = cfgMan.selectSection(ConfigSections.SECTION_SETTINGS.get())\
        .getString(ConfigOptions.DEVICE_ADB_SERIAL.get())
    adb = AdbTools(address)
    if not adb.check():
        print("connect failed")
        exit(StatusCode.ADB_CONNECT_FAILED)
    if not adb.initZoom():
        print("不支持的分辨率")
        exit(StatusCode.UNSUPPORTED_RESOLUTION)
    if len(sys.argv) == 7:
        release_game_version = sys.argv[1]
        template_img_name = sys.argv[2]
        left_top_x = int(sys.argv[3])
        left_top_y = int(sys.argv[4])
        right_bottom_x = int(sys.argv[5])
        right_bottom_y = int(sys.argv[6])
        save_dir = "template/{rgv}"\
            .format(rgv=release_game_version)
        FileCtrl.checkDir(save_dir)
        save_file = "{basedir}/{tin}.png"\
            .format(basedir=save_dir, tin=template_img_name)
        p = adb.takeScreenShot(True)
        # 若分辨率太大则需要缩放
        if adb.zoom > 1.0:
            p = cv2.resize(p, (720, 1280), interpolation=cv2.INTER_NEAREST)
        p = p[left_top_y:right_bottom_y, left_top_x:right_bottom_x]
        cv2.imwrite(save_file, p)
    else:
        printHelp()
