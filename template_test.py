import os
import sys
import time

import aircv
import cv2

from lib.config import ConfigManager
from lib.constants import ConfigOptions, ConfigSections, StatusCode
from lib.file import FileCtrl
from lib.utils import AdbTools


def printHelp():
    print("{filename} [adb_serial] [release_game_version] [template_img_name]"
          .format(filename=os.path.basename(sys.argv[0])))


if __name__ == "__main__":
    if len(sys.argv) == 4:
        address = sys.argv[1]
        adb = AdbTools(address)
        if not adb.check():
            print("connect failed")
            exit(StatusCode.ADB_CONNECT_FAILED)
        if not adb.initZoom():
            print("不支持的分辨率")
            exit(StatusCode.UNSUPPORTED_RESOLUTION)
        release_game_version = sys.argv[2]
        template_img_name = sys.argv[3]
        save_file = "template/{rgv}/{tin}.png"\
            .format(rgv=release_game_version, tin=template_img_name)
        start_ss = time.perf_counter()
        p = adb.takeScreenShot(False)
        if FileCtrl.isExist(save_file):
            # 若分辨率太大则需要缩放
            if adb.zoom > 1.0:
                p = cv2.resize(p, (720, 1280), interpolation=cv2.INTER_NEAREST)
            end_ss = time.perf_counter()
            print('Screenshot: %s Seconds' % (end_ss - start_ss))

            p2 = cv2.imread(save_file)

            start = time.perf_counter()
            s = str(aircv.find_template(p, p2))
            print(s)
            end = time.perf_counter()
            print('Match image: %s Seconds' % (end - start))
        else:
            print("Error: {filename} not found!".format(filename=save_file))
    else:
        printHelp()
