import threading
import time

import cv2
from cnocr import CnOcr

from lib.config import ConfigManager
from lib.constants import CheckColor, CheckPoint, CheckTemplate, \
    ConfigOptions, ConfigSections, ResultCode, Task, StatusCode, CheckRect, ConfigValues
from lib.resource import Resource
from lib.timer import Timer
from lib.utils import AdbTools, Args, GuestData, RoomCreatorData
from modules.checker import Checker
from modules.trackers.bell import Bell
from modules.trackers.creator import Creator
from modules.trackers.fight import Fight
from modules.trackers.follow import Follow
from modules.trackers.login import Login
from modules.trackers.room import Room


class TrackerThread(threading.Thread):
    def __init__(self, adb, config_file):
        threading.Thread.__init__(self)
        self.mTask = Task.NO_TASK
        self.mStatus = StatusCode.NO_ERROR
        cfgMan = ConfigManager(config_file, writable=False)
        mGameServer = cfgMan \
            .selectSection(ConfigSections.SECTION_SETTINGS.get()) \
            .getString(ConfigOptions.GAME_SERVER.get(), default='cn')
        mOcr = CnOcr(root='prebuilt/cnocr_model')
        self.mArgs = Args(
            isRunning=False,
            mAdb=adb,
            cfgMan=cfgMan,
            timer=Timer(),
            mOcr=mOcr,
            mGameServer=mGameServer,
            mScreenshot=None,
            mGuestData=GuestData(cfgMan),
            mRoomCreatorData=RoomCreatorData(cfgMan, mGameServer))
        self.mEscapeDelay = -1
        self.mStartTime = 0

    def run(self):
        threading.Thread.run(self)
        self.mArgs.running = True
        self.mStatus = StatusCode.NO_ERROR
        self.mArgs.timer.reset()
        while True:
            # 检查adb
            if not self.mArgs.adb.check():
                print("ADB 连接错误, 运行中断")
                self.mArgs.running = False
                self.mTask = Task.NO_TASK
                self.mStatus = StatusCode.ADB_CONNECT_INTERRUPT
                break
            # 判断前台应用
            if Resource.getGamePackageName(self.mArgs.GameServer) not in self.mArgs.adb.getTopProcess():
                time.sleep(1)
                continue
            # 截图
            self.mArgs.Screenshot = self.mArgs.adb.takeScreenShot(False)
            # 若分辨率太大则需要缩放
            if self.mArgs.adb.zoom > 1.0:
                self.mArgs.Screenshot = cv2.resize(self.mArgs.Screenshot, (720, 1280), interpolation=cv2.INTER_NEAREST)
            print(self.mTask.name)
            # 意外弹窗检测
            self.__unexpected_dialog()
            # 意外回到登录界面检测
            self.__unexpected_login_interface()
            # 回到主页事件检测
            self.__back_to_home()
            # 意外主页事件检测
            self.__check_is_home()
            # 执行完本次任务再停止
            if not self.mArgs.running and self.mTask == Task.NO_TASK:
                print('停止运行')
                break
            # 登录类 追踪器
            self.mTask = Login.track(self.mArgs, self.mTask)
            if Resource.getGamingModeMain(self.mArgs.cfgMan) == ConfigValues.GAMING_MODE_MAIN_GUEST:
                # 铃铛类 追踪器
                if self.mArgs.GuestData.TrackBellSwitch:
                    self.mTask = Bell.track(self.mArgs, self.mTask)
                # 好友类 追踪器
                if self.mArgs.GuestData.TrackFollowSWitch:
                    self.mTask = Follow.track(self.mArgs, self.mTask)
            if Resource.getGamingModeMain(self.mArgs.cfgMan) == ConfigValues.GAMING_MODE_MAIN_OWNER:
                # 开车类 追踪器
                if self.mArgs.RoomCreatorData.Enabled:
                    self.mTask = Creator.track(self.mArgs, self.mTask)
            self.mTask = Room.track(self.mArgs, self.mTask)
            if self.mArgs.RoomCreatorData.Enabled and \
                    self.mTask == Task.GO_FIGHT_AS_OWNER and \
                    self.mArgs.RoomCreatorData.GhostMode == ConfigValues.COMMON_ENABLE.get():
                self.mEscapeDelay = self.mArgs.RoomCreatorData.GhostEscapeTime
            else:
                self.mEscapeDelay = -1
            self.mTask = Fight.track(self.mArgs, self.mTask)
            time.sleep(1)
        # 意外退出处理
        self.mTask = Task.NO_TASK

    def __check_is_home(self):
        # 如果意外到了主城
        # 通过检测首页的领主战按钮来检测是否在主页
        # (摒弃掉了旧的颜色检测方法，因为会和其他任务出现冲突)
        if Checker.checkImageWithTemplate(self.mArgs, CheckTemplate.HOME_BOSS_LIST_BUTTON):
            self.mTask = Task.NO_TASK

    def __unexpected_dialog(self):
        # TODO: 增加可选择使用或者不使用领主加成点数的选项 (当前默认选是)
        if Checker.checkImageWithTemplate(self.mArgs, CheckTemplate.DIALOG_INCOME_BUFF):
            self.mArgs.adb.random_click(CheckTemplate.DIALOG_DOUBLE_OK.getRect(self.mArgs.GameServer))
        # 检测日期改变对话框
        if Checker.checkImageWithTemplate(self.mArgs, CheckTemplate.DIALOG_DATE_CHANGED):
            self.mArgs.adb.random_click(CheckTemplate.DIALOG_SINGLE_OK.getRect(self.mArgs.GameServer))
            self.mTask = Task.GO_LOGIN
        # 检测继续任务对话框
        if Checker.checkImageWithTemplate(self.mArgs, CheckTemplate.DIALOG_CONTINUE_TASK):
            self.mTask = Task.GO_CONTINUE_AFTER_LOGIN
        # 普通意外弹窗
        if Checker.checkImageWithTemplate(self.mArgs, CheckTemplate.DIALOG_SINGLE_OK):
            print("检测到了意外的弹窗，回到首页")
            self.mArgs.adb.random_click(CheckTemplate.DIALOG_SINGLE_OK.getRect(self.mArgs.GameServer))
            # 如果房间被自动解散
            if Checker.checkImageWithTemplate(self.mArgs, CheckTemplate.DIALOG_ROOM_DISBAND):
                self.mTask = Task.GO_BACK_TO_HOME_FORCE
                return
            if self.mTask.code < Task.GO_LOGIN.code:
                self.mTask = Task.GO_BACK_TO_HOME

    def __unexpected_login_interface(self):
        if Checker.checkImageWithTemplate(self.mArgs, CheckTemplate.LOGIN_INTERFACE_SIGN):
            print("意外回到了登录界面，前往重新登录")
            self.mTask = Task.GO_LOGIN

    def __back_to_home(self):
        isActive = Checker.checkBottomBar(self.mArgs.Screenshot,
                                          CheckColor.BOTTOM_BAR_ACTIVE_COLOR,
                                          CheckPoint.BOTTOM_BAR_HOME_POINT)
        isInactive = Checker.checkBottomBar(self.mArgs.Screenshot,
                                            CheckColor.BOTTOM_BAR_INACTIVE_COLOR,
                                            CheckPoint.BOTTOM_BAR_HOME_POINT)

        if self.mTask == Task.GO_BACK_TO_HOME:
            if not isActive and isInactive:
                self.mArgs.adb.random_click(CheckRect.BOTTOM_BAR_HOME_RECT)
                self.mTask = Task.NO_TASK
        if self.mTask == Task.GO_BACK_TO_HOME_FORCE:
            if not Checker.checkImageWithTemplate(self.mArgs, CheckTemplate.HOME_BOSS_LIST_BUTTON):
                if isActive or isInactive:
                    self.mArgs.adb.random_click(CheckRect.BOTTOM_BAR_HOME_RECT)
                    self.mTask = Task.NO_TASK
            else:
                self.mTask = Task.NO_TASK


class Tracker:
    def __init__(self, config_file):
        self.adb_tools = None
        self.trackerThread = TrackerThread(None, config_file)
        self.__config_file = config_file

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
            self.trackerThread = TrackerThread(self.adb_tools, self.__config_file)
            self.trackerThread.start()
        return ResultCode.START_SUCCEED

    def stop(self):
        self.trackerThread.mArgs.running = False
        if self.running():
            return ResultCode.WAITING_TASK
        else:
            return ResultCode.STOP_SUCCEED

    def running(self):
        if self.trackerThread is None:
            return False
        if not self.trackerThread.mArgs.running and self.trackerThread.mTask == Task.NO_TASK:
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
