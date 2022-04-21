import hashlib
import os
import random
import re
import time
from urllib import request

import cv2
import numpy
import requests
from adbutils import adb
from cnocr import CnOcr

from lib.base import Rect, Point
from lib.config import ConfigManager
from lib.constants import ConfigSections, ConfigOptions, ConfigValues
from lib.logger import Logger
from lib.resource import Resource
from lib.timer import Timer


class Downloader:
    @staticmethod
    def downloadFile(url: str, filepath: str):
        opener = request.build_opener()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/98.0.4758.102 '
                          'Safari/537.36 '
                          'Edg/98.0.1108.56',
        }
        opener.addheaders = headers
        print('Download File: ' + filepath.replace(os.getcwd() + '\\', ''))
        content = requests.get(url, headers=headers).content
        with open(filepath, 'wb') as file:
            file.write(content)
        print('Completed')


class HashUtils:
    @staticmethod
    def getFileHash(filename: str) -> str:
        with open(filename, 'rb') as f:
            sha1obj = hashlib.sha1()
            sha1obj.update(f.read())
            return sha1obj.hexdigest()


class Random:
    @staticmethod
    def __getSeed():
        return int(time.time() * 1000000)

    # 生成随机浮点数
    @staticmethod
    def genFloat(left: float, right: float, seed=0):
        random.seed(Random.__getSeed() + seed)
        return random.uniform(left, right)

    # 生成随机整数
    @staticmethod
    def genInt(left: int, right: int, seed=0):
        random.seed(Random.__getSeed() + seed)
        return random.randint(left, right)

    # 根据Rect生成随机点
    @staticmethod
    def genPoint(rect: Rect, seed=0):
        random.seed(Random.__getSeed() + seed)
        return Point(random.uniform(rect.left_top.x, rect.right_bottom.x),
                     random.uniform(rect.left_top.y, rect.right_bottom.y))


class connection:
    @staticmethod
    def get_bluestacks5_hyperv(serial):
        from winreg import ConnectRegistry, OpenKey, QueryInfoKey, EnumValue, CloseKey, HKEY_LOCAL_MACHINE

        if serial == "bluestacks5-hyperv":
            parameter_name = "bst.instance.Nougat64.status.adb_port"
        else:
            parameter_name = f"bst.instance.Nougat64_{serial[19:]}.status.adb_port"

        reg_root = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        sub_dir = f"SOFTWARE\\BlueStacks_nxt"
        bs_keys = OpenKey(reg_root, sub_dir)
        bs_keys_count = QueryInfoKey(bs_keys)[1]
        for i in range(bs_keys_count):
            key_name, key_value, key_type = EnumValue(bs_keys, i)
            if key_name == "UserDefinedDir":
                with open(f"{key_value}\\bluestacks.conf", 'r', encoding='utf-8') as f:
                    content = f.read()
                    port = re.findall(rf'{parameter_name}="(.*?)"\n', content, re.S)
                    if len(port) > 0:
                        serial = f"127.0.0.1:{port[0]}"
                break

        CloseKey(bs_keys)
        CloseKey(reg_root)
        return serial


class AdbTools:
    device = None
    height = None
    width = None
    zoom = None

    def __init__(self, address: str):
        if address.__contains__('bluestacks'):
            address = connection.get_bluestacks5_hyperv(address)
        if address.__contains__(':'):
            Logger.displayLog("ADB Address: " + address)
            msg = adb.connect(address, timeout=3.0)
            if msg.__contains__("connected"):
                self.device = adb.device(serial=address)
        else:
            self.device = adb.device(serial=address)

    def initZoom(self):
        window = self.device.window_size()
        self.height = window.height
        self.width = window.width
        if self.__checkWindowSize():
            self.zoom = float(self.width) / 720.0
            if self.zoom < 1.0:
                return False
            return True
        else:
            return False

    def check(self):
        if self.device is not None and self.device.serial is not None:
            for de in adb.devices():
                if str(de).__contains__(self.device.serial):
                    return True
        return False

    def __checkWindowSize(self):
        return float(self.width) / float(self.height) == 720.0 / 1280.0

    def click(self, zoom: float, point: Point):
        point.loadZoom(zoom)
        self.device.click(point.x, point.y)

    def random_click(self, mRandomRect: Rect):
        self.click(self.zoom, Random.genPoint(mRandomRect))

    def swipe(self, start_point: Point, end_point: Point, duration_ms: float):
        start_point.loadZoom(self.zoom)
        end_point.loadZoom(self.zoom)
        self.device.swipe(
            start_point.x, start_point.y,
            end_point.x, end_point.y,
            duration_ms / 1000
        )

    def takeScreenShot(self, isGray: bool) -> cv2.cv2:
        if not self.check():
            return None
        stream = self.device.shell("screencap -p", stream=True)
        screenshot = b""
        while True:
            chunk = stream.read(4096)
            if not chunk:
                break
            screenshot += chunk
        buffer = numpy.frombuffer(screenshot, numpy.uint8)
        if buffer.size == 0:
            return None
        img = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
        if img is None:
            screenshot = screenshot.replace(b'\r\n', b'\n')
            buffer = numpy.frombuffer(screenshot, numpy.uint8)
            img = cv2.imdecode(screenshot, cv2.IMREAD_COLOR)
        if isGray:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        return img

    def getTopProcess(self):
        s = self.device.shell("dumpsys activity top | grep ACTIVITY").split('\n')
        return s[len(s) - 1]


class AircvRect:
    def __init__(self, found: bool, has_info: bool, allow_enter: bool, rect=None):
        self.__text = None
        self.found = found
        self.has_info = has_info
        self.allow_enter = allow_enter
        self.rect = rect

    def setImageText(self, text: list):
        self.__text = text

    def getImageText(self) -> list:
        if self.__text is None:
            return []
        return self.__text


class GuestData:
    def __init__(self, cfgMan: ConfigManager):
        self.TrackBellSwitch = cfgMan \
            .checkoutSection(ConfigSections.SECTION_MAIN.get()) \
            .getBoolean(ConfigOptions.TRACK_BELL_SWITCH.get())
        self.TrackFollowSWitch = cfgMan \
            .checkoutSection(ConfigSections.SECTION_MAIN.get()) \
            .getBoolean(ConfigOptions.TRACK_FOLLOW_SWITCH.get())
        self.FollowFriendSelect = cfgMan \
            .checkoutSection(ConfigSections.SECTION_CUSTOM.get()) \
            .getString(ConfigOptions.FOLLOW_FRIEND_SELECT.get(), 'disable') == ConfigValues.COMMON_ENABLE.get()
        self.FollowFriendSelectName = cfgMan \
            .checkoutSection(ConfigSections.SECTION_CUSTOM.get()) \
            .getString(ConfigOptions.FOLLOW_FRIEND_SELECT_NAME.get())


class RoomCreatorData:
    def __init__(self, cfgMan: ConfigManager, mGameServer: str):
        self.MinBossTemplate = Resource.getMinBossTemplate(cfgMan, mGameServer)
        self.Enabled = cfgMan \
            .selectSection(ConfigSections.SECTION_MAIN.get()) \
            .getBoolean(ConfigOptions.ROOM_CREATOR_SWITCH.get())
        self.RecruitmentMode = cfgMan \
            .selectSection(ConfigSections.SECTION_CUSTOM.get()) \
            .getString(ConfigOptions.RECRUITMENT_MODE.get(), 'true_false_false')
        self.isStartWhileFull = cfgMan \
            .selectSection(ConfigSections.SECTION_CUSTOM.get()) \
            .getString(ConfigOptions.ROOM_CREATOR_START_FIGHT_MODE.get(), 'full') == 'full'
        self.GhostMode = cfgMan \
            .checkoutSection(ConfigSections.SECTION_CUSTOM.get()) \
            .getString(ConfigOptions.ROOM_CREATOR_GHOST_MODE.get())
        self.GhostEscapeTime = cfgMan \
            .checkoutSection(ConfigSections.SECTION_CUSTOM.get()) \
            .getInt(ConfigOptions.ROOM_CREATOR_GHOST_ESCAPE_TIME.get())


class Args:
    def __init__(self, isRunning: bool, isPaused: bool,
                 mAdb: AdbTools, cfgMan: ConfigManager, timer: Timer, mOcr: CnOcr,
                 mGameServer: str, mScreenshot: cv2.cv2,
                 mGuestData: GuestData, mRoomCreatorData: RoomCreatorData):
        self.running = isRunning
        self.paused = isPaused
        self.adb = mAdb
        self.cfgMan = cfgMan
        self.timer = timer
        self.ocr = mOcr

        self.GameServer = mGameServer
        self.GuestData = mGuestData
        self.RoomCreatorData = mRoomCreatorData

        self.Screenshot = mScreenshot
