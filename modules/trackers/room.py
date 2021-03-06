import cv2

from lib.base import Rgb
from lib.constants import CheckColor, CheckPoint, CheckTemplate, Task, CheckRect
from lib.resource import Resource
from lib.utils import Args
from modules.checker import Checker


class Room:
    @staticmethod
    def track(mArgs: Args, task: Task):
        # 乘客模式 进房
        if task == Task.GO_ROOM_AS_GUEST:
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.BOSS_LIST_REFRESH_BUTTON) or \
                    Checker.checkImageWithTemplate(mArgs, CheckTemplate.BOSS_LIST_REFRESH_UNAVAILABLE_BUTTON):
                return Task.GO_FOLLOW_CHECK_BOSS_LIST
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.COMMON_CARD_INFO_ICON):
                return Task.GO_ROOM_PREPARE_AS_GUEST
        # 房主模式 进房
        if task == Task.GO_ROOM_AS_OWNER:
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.COMMON_CARD_INFO_ICON):
                if Checker.checkImageWithTemplate(mArgs, CheckTemplate.RECRUITMENT_BUTTON):
                    mArgs.adb.random_click(CheckTemplate.RECRUITMENT_BUTTON.getRect(mArgs.GameServer))
                    return Task.GO_ROOM_PREPARE_AS_OWNER
        # 乘客模式 准备
        if task == Task.GO_ROOM_PREPARE_AS_GUEST:
            # TODO: 检查准备人数
            # player_cnt = Room.__preparedPlayerCnt(mArgs.Screenshot)
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.COMMON_CHECKBOX_INACTIVE):
                mArgs.adb.random_click(CheckRect.PREPARE_CHECKBOX_BUTTON_RECT)
                return Task.GO_ROOM_WAITING_FIGHT_GUEST
        # 房主模式 准备
        if task == Task.GO_ROOM_PREPARE_AS_OWNER:
            # 招募
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.DIALOG_RECRUITMENT_TITLE):
                Room.__checkRecruitment(mArgs)
                mArgs.adb.random_click(CheckTemplate.DIALOG_RECRUITMENT_OK.getRect(mArgs.GameServer))
                return task
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.COMMON_CARD_INFO_ICON):
                # TODO: 使用两种模式来确认募集以保证准确
                return Task.GO_ROOM_WAITING_FIGHT_OWNER
        # 准备完成 等待进入战斗
        if task == Task.GO_ROOM_WAITING_FIGHT_GUEST:
            # 判断开战后等待其他人
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.FIGHT_WAITING_FOR_OTHERS_TEXT_RECT):
                return task
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.FIGHT_PAUSE_BUTTON_RECT):
                return Task.GO_FIGHT_AS_GUEST
        if task == Task.GO_ROOM_WAITING_FIGHT_OWNER:
            # 检查界面是否还在准备界面
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.COMMON_CARD_INFO_ICON):
                # 判断"挑战"按钮是否已经亮起
                if CheckColor.PREPARE_ACTIVE_COLOR \
                        .isMatch(Rgb.point2rgb(mArgs.Screenshot, CheckPoint.PREPARE_START_FIGHT)):
                    # 需要满员且已满员
                    if (mArgs.RoomCreatorData.isStartWhileFull and Room.__preparedPlayerCnt(mArgs.Screenshot) == 3) or \
                            not mArgs.RoomCreatorData.isStartWhileFull:  # 不需要满员 立即开始
                        mArgs.adb.random_click(CheckTemplate.COMMON_START_FIGHT_BUTTON.getRect(mArgs.GameServer))
                return task
            # 判断开战后等待其他人
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.FIGHT_WAITING_FOR_OTHERS_TEXT_RECT):
                return task
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.FIGHT_PAUSE_BUTTON_RECT):
                return Task.GO_FIGHT_AS_OWNER
        return task

    @staticmethod
    def __checkRecruitment(mArgs: Args):
        # TODO: 使用两种模式来确认募集以保证准确
        recruitment_mode = mArgs.RoomCreatorData.RecruitmentMode.split('_')
        # 互关
        double_follow = Checker.checkImage(
            Resource.cropImg(mArgs.Screenshot,
                             CheckTemplate.RECRUITMENT_DOUBLE_FOLLOW_CHECKBOX.getRect(mArgs.GameServer)),
            Resource.getTemplate(mArgs.GameServer, CheckTemplate.COMMON_CHECKBOX_ACTIVE.getName())
        )
        if (double_follow and recruitment_mode[0] == 'false') or \
                (not double_follow and recruitment_mode[0] == 'true'):
            mArgs.adb.random_click(CheckTemplate.RECRUITMENT_DOUBLE_FOLLOW_CHECKBOX.getRect(mArgs.GameServer))
        # 关注者
        single_follow = Checker.checkImage(
            Resource.cropImg(mArgs.Screenshot,
                             CheckTemplate.RECRUITMENT_SINGLE_FOLLOW_CHECKBOX.getRect(mArgs.GameServer)),
            Resource.getTemplate(mArgs.GameServer, CheckTemplate.COMMON_CHECKBOX_ACTIVE.getName())
        )
        if (single_follow and recruitment_mode[1] == 'false') or \
                (not single_follow and recruitment_mode[1] == 'true'):
            mArgs.adb.random_click(CheckTemplate.RECRUITMENT_SINGLE_FOLLOW_CHECKBOX.getRect(mArgs.GameServer))
        # 随机
        random_recruitment = Checker.checkImage(
            Resource.cropImg(mArgs.Screenshot,
                             CheckTemplate.RECRUITMENT_RANDOM_CHECKBOX.getRect(mArgs.GameServer)),
            Resource.getTemplate(mArgs.GameServer, CheckTemplate.COMMON_CHECKBOX_ACTIVE.getName())
        )
        if (random_recruitment and recruitment_mode[2] == 'false') or \
                (not random_recruitment and recruitment_mode[2] == 'true'):
            mArgs.adb.random_click(CheckTemplate.RECRUITMENT_RANDOM_CHECKBOX.getRect(mArgs.GameServer))

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
