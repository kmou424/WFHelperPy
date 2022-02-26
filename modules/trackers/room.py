import cv2

from lib.constants import CheckColor, CheckPoint, CheckTemplate, Task, CheckRect
from lib.utils import Rgb, Args
from modules.checker import Checker


class Room:
    @staticmethod
    def track(mArgs: Args, task: Task):
        # 乘客模式 进房
        if task == Task.GO_ROOM_AS_GUEST:
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.PREPARE_BOTTOM_CARD_INFO_BUTTON):
                return Task.GO_ROOM_PREPARE_AS_GUEST
        if task == Task.GO_ROOM_AS_OWNER:
            # TODO: 房主模式-进入
            return task
        # 乘客模式 准备
        if task == Task.GO_ROOM_PREPARE_AS_GUEST:
            # TODO: 检查准备人数
            player_cnt = Room.__preparedPlayerCnt(mArgs.mScreenshot)
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.PREPARE_CHECKBOX_INACTIVE):
                mArgs.adb.random_click(CheckRect.PREPARE_CHECKBOX_BUTTON_RECT)
                return Task.GO_ROOM_WAITING_FIGHT
        if task == Task.GO_ROOM_PREPARE_AS_OWNER:
            # TODO: 房主模式-准备
            return task
        # 准备完成 等待进入战斗
        if task == Task.GO_ROOM_WAITING_FIGHT:
            # 判断开战后等待其他人
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.FIGHT_WAITING_FOR_OTHERS_TEXT_RECT):
                return task
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.FIGHT_PAUSE_BUTTON_RECT):
                return Task.GO_FIGHT_AS_GUEST
        return task

    @staticmethod
    def __preparedPlayerCnt(screenshot: cv2.cv2):
        cnt = 0
        if CheckColor.PREPARE_ACTIVE_COLOR.isMatch(Rgb.point2rgb(screenshot, CheckPoint.PREPARE_PLAYER1_STATUS)):
            cnt += 1
        if CheckColor.PREPARE_ACTIVE_COLOR.isMatch(Rgb.point2rgb(screenshot, CheckPoint.PREPARE_PLAYER2_STATUS)):
            cnt += 1
        if CheckColor.PREPARE_ACTIVE_COLOR.isMatch(Rgb.point2rgb(screenshot, CheckPoint.PREPARE_PLAYER3_STATUS)):
            cnt += 1
        return cnt
