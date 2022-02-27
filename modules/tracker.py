import threading
import time

import cv2

from lib.config import ConfigManager
from lib.constants import CheckColor, CheckPoint, CheckTemplate, \
    ConfigOptions, ConfigSections, ResultCode, Task, StatusCode, CheckRect
from lib.utils import AdbTools, Args
from modules.checker import Checker
from lib.resource import Resource
from modules.trackers.bell import Bell
from modules.trackers.fight import Fight
from modules.trackers.login import Login
from modules.trackers.room import Room
from modules.trackers.timer import Timer


class TrackerThread(threading.Thread):
    def __init__(self, adb):
        threading.Thread.__init__(self)
        self.running = False
        self.mTask = Task.NO_TASK
        self.mStatus = StatusCode.NO_ERROR
        cfgMan = ConfigManager('config.ini', writable=False)
        mGameServer = cfgMan \
            .selectSection(ConfigSections.SECTION_SETTINGS.get()) \
            .getString(ConfigOptions.GAME_SERVER.get())
        self.mArgs = Args(adb, cfgMan, mGameServer, None)
        self.mTrackBell = self.mArgs.cfgMan \
            .selectSection(ConfigSections.SECTION_MAIN.get()) \
            .getBoolean(ConfigOptions.TRACK_BELL_SWITCH.get())
        self.mEscapeDelay = -1
        self.timer = Timer()
        self.mStartTime = 0

    def run(self):
        threading.Thread.run(self)
        self.running = True
        self.mStatus = StatusCode.NO_ERROR
        self.timer.resetClock()
        while True:
            # 检查adb
            if not self.mArgs.adb.check():
                print("ADB 连接错误, 运行中断")
                self.running = False
                self.mTask = Task.NO_TASK
                self.mStatus = StatusCode.ADB_CONNECT_INTERRUPT
                break
            # 执行完本次任务再停止
            if not self.running and self.mTask == Task.NO_TASK:
                print('停止运行')
                break
            # 判断前台应用
            if Resource.getGamePackageName(self.mArgs.mGameServer) not in self.mArgs.adb.getTopProcess():
                time.sleep(1)
                continue
            # 截图
            self.mArgs.mScreenshot = self.mArgs.adb.takeScreenShot(False)
            # 若分辨率太大则需要缩放
            if self.mArgs.adb.zoom > 1.0:
                self.mArgs.mScreenshot = cv2.resize(self.mArgs.mScreenshot, (720, 1280), interpolation=cv2.INTER_NEAREST)
            print(self.mTask.name)
            # 意外弹窗检测
            self.__unexpected_dialog()
            # 意外回到登录界面检测
            self.__unexpected_login_interface()
            # 回到主页事件检测
            self.__back_to_home()
            # 监听铃铛
            self.mTask = Login.track(self.mArgs, self.mTask)
            if self.mTrackBell:
                self.mTask = Bell.track(self.mArgs, self.mTask)
            self.mTask = Room.track(self.mArgs, self.mTask)
            if self.mTask == Task.GO_FIGHT_AS_OWNER:
                self.mEscapeDelay = 5
                self.mStartTime = time.perf_counter()
            else:
                self.mEscapeDelay = -1
            self.mTask = Fight.track(self.mArgs, self.mTask, self.mStartTime, self.mEscapeDelay)
            time.sleep(1)
        # 意外退出处理
        self.mTask = Task.NO_TASK

    def __unexpected_dialog(self):
        if Checker.checkImageWithTemplate(self.mArgs, CheckTemplate.DIALOG_CONTINUE_TASK):
            self.mTask = Task.GO_CONTINUE_AFTER_LOGIN
        if Checker.checkImageWithTemplate(self.mArgs, CheckTemplate.DIALOG_SINGLE_OK):
            print("检测到了意外的弹窗，回到首页")
            self.mArgs.adb.random_click(CheckTemplate.DIALOG_SINGLE_OK.getRect(self.mArgs.mGameServer))
            if self.mTask.code < Task.GO_LOGIN.code:
                self.mTask = Task.GO_BACK_TO_HOME

    def __unexpected_login_interface(self):
        if Checker.checkImageWithTemplate(self.mArgs, CheckTemplate.LOGIN_INTERFACE_SIGN):
            print("意外回到了登录界面，前往重新登录")
            self.mTask = Task.GO_LOGIN

    def __back_to_home(self):
        if self.mTask != Task.GO_BACK_TO_HOME:
            return
        if not Checker.checkBottomBar(self.mArgs.mScreenshot,
                                      CheckColor.BOTTOM_BAR_ACTIVE_COLOR,
                                      CheckPoint.BOTTOM_BAR_HOME_POINT):
            if Checker.checkBottomBar(self.mArgs.mScreenshot,
                                      CheckColor.BOTTOM_BAR_INACTIVE_COLOR,
                                      CheckPoint.BOTTOM_BAR_HOME_POINT):
                self.mArgs.adb.random_click(CheckRect.BOTTOM_BAR_HOME_RECT)
                self.mTask = Task.NO_TASK


class Tracker:
    def __init__(self):
        self.adb_tools = None
        self.trackerThread = TrackerThread(None)

    def run(self, address: str):
        self.adb_tools = AdbTools(address)
        if not self.adb_tools.check():
            print("设备连接失败")
            self.trackerThread.mStatus = StatusCode.ADB_CONNECT_FAILED
            return ResultCode.START_FAILED
        if not self.adb_tools.initZoom():
            print("不支持的分辨率")
            self.trackerThread.mStatus = StatusCode.UNSUPPORTED_RESOLUTION
            return ResultCode.START_FAILED
        # 开始运行线程
        if not self.running():
            self.trackerThread = TrackerThread(adb=self.adb_tools)
            self.trackerThread.start()
        return ResultCode.START_SUCCEED

    def stop(self):
        self.trackerThread.running = False
        if self.running():
            return ResultCode.WAITING_TASK
        else:
            return ResultCode.STOP_SUCCEED

    def running(self):
        if self.trackerThread is None:
            return False
        if not self.trackerThread.running and self.trackerThread.mTask == Task.NO_TASK:
            return False
        else:
            return True

    def status(self):
        if self.trackerThread is None:
            return 0
        ret = self.trackerThread.mStatus
        if ret < 0 or ret == StatusCode.HAD_ERROR:
            self.trackerThread.mStatus = StatusCode.HAD_ERROR
        else:
            self.trackerThread.mStatus = StatusCode.NO_ERROR
        return ret
