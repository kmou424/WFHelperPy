import hashlib
import os
import random
import time
from urllib import request

import cv2
import numpy
import requests
from adbutils import adb

from lib.config import ConfigManager
from lib.timer import Timer
from lib.times import Time


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


class Hash:
    @staticmethod
    def getFileHash(filename: str) -> str:
        with open(filename, 'rb') as f:
            sha1obj = hashlib.sha1()
            sha1obj.update(f.read())
            return sha1obj.hexdigest()


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def loadZoom(self, zoom: float):
        if zoom > 1.0:
            self.x = self.x * zoom
            self.y = self.y * zoom


class Rect:
    def __init__(self, left_top: Point, right_bottom: Point):
        self.left_top = left_top
        self.right_bottom = right_bottom


class Rgb:
    def __init__(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b

    @staticmethod
    def point2rgb(img: cv2.cv2, point: Point):
        return Rgb.pixel2rgb(img[point.y, point.x])

    @staticmethod
    def pixel2rgb(pixel: numpy.ndarray):
        return Rgb(pixel[2], pixel[1], pixel[0])


class Color:
    def __init__(self, left: Rgb, right: Rgb):
        self.left = left
        self.right = right

    def isMatch(self, src: Rgb):
        return (self.left.red <= src.red <= self.right.red) and \
               (self.left.green <= src.green <= self.right.green) and \
               (self.left.blue <= src.blue <= self.right.blue)


class Boss:
    BossLevels = {
        'prim': '初级',
        'mid': '中级',
        'high': '高级',
        'highp': '高级+',
        'super': '超级'
    }

    def __init__(self, item: dict):
        self.item = item

    def isAvailable(self) -> bool:
        end_time = Time.getTimeStampByStandardFormat(self.item['end'])
        now_time = Time.getTimeStampForNow()
        return end_time > now_time

    def getName(self) -> str:
        return self.item['name']

    def getId(self) -> str:
        return self.item['id']

    def getType(self) -> str:
        return self.item['type']

    def getLevels(self) -> str:
        return self.item['levels']

    def getMinLevel(self):
        return self.getLevels().split(' ')[0]


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


class AdbTools:
    device = None
    height = None
    width = None
    zoom = None

    def __init__(self, address: str):
        if address.__contains__(':'):
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
        img = cv2.imdecode(numpy.frombuffer(screenshot, numpy.uint8), cv2.IMREAD_COLOR)
        if img is None:
            screenshot = screenshot.replace(b'\r\n', b'\n')
            img = cv2.imdecode(numpy.frombuffer(screenshot, numpy.uint8), cv2.IMREAD_COLOR)
        if isGray:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        return img

    def getTopProcess(self):
        s = self.device.shell("dumpsys activity top | grep ACTIVITY").split('\n')
        return s[len(s) - 1]


class AircvRect:
    def __init__(self, found: bool, has_info: bool, allow_enter: bool, rect=None):
        self.text = None
        self.found = found
        self.has_info = has_info
        self.allow_enter = allow_enter
        self.rect = rect

    def setImageText(self, text: str):
        self.text = text


class _GuestData:
    def __init__(self, mTrackBell: bool, mTrackBossList: bool):
        self.TrackBellSwitch = mTrackBell
        self.TrackBossListSWitch = mTrackBossList


class _RoomCreatorData:
    def __init__(self, mMinBossTemplate: str, mRoomCreatorEnabled: bool, mRoomCreatorRecruitmentMode: str,
                 mIsStartFightWhileFull: bool, mRoomCreatorGhostMode: str, mRoomCreatorGhostEscapeTime: int):
        self.MinBossTemplate = mMinBossTemplate
        self.Enabled = mRoomCreatorEnabled
        self.RecruitmentMode = mRoomCreatorRecruitmentMode
        self.isStartWhileFull = mIsStartFightWhileFull
        self.GhostMode = mRoomCreatorGhostMode
        self.GhostEscapeTime = mRoomCreatorGhostEscapeTime


class Args:
    def __init__(self, mAdb: AdbTools, cfgMan: ConfigManager, timer: Timer,
                 mGameServer: str,
                 mTrackBell: bool, mTrackBossList: bool,
                 mMinBossTemplate: str, mRoomCreatorEnabled: bool, mRoomCreatorRecruitmentMode: str,
                 mIsStartFightWhileFull: bool, mRoomCreatorGhostMode: str, mRoomCreatorGhostEscapeTime: int,
                 mScreenshot: cv2.cv2):
        self.adb = mAdb
        self.cfgMan = cfgMan
        self.timer = timer

        self.GameServer = mGameServer
        self.GuestData = _GuestData(mTrackBell, mTrackBossList)
        self.RoomCreatorData = _RoomCreatorData(
            mMinBossTemplate, mRoomCreatorEnabled, mRoomCreatorRecruitmentMode,
            mIsStartFightWhileFull, mRoomCreatorGhostMode, mRoomCreatorGhostEscapeTime
        )

        self.Screenshot = mScreenshot
