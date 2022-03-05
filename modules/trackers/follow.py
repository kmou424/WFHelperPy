import time

from lib.base import Point
from lib.constants import Task, CheckTemplate, Const, Locate
from lib.logger import Logger
from lib.utils import Random, Args
from modules.checker import Checker


class Follow:
    @staticmethod
    def track(mArgs: Args, mTask: Task):
        if mTask == Task.NO_TASK:
            # 检查主城界面领主战按钮
            if not Checker.checkImageWithTemplate(mArgs, CheckTemplate.HOME_BOSS_LIST_BUTTON):
                return Task.GO_BACK_TO_HOME_FORCE
            else:
                mArgs.adb.random_click(CheckTemplate.HOME_BOSS_LIST_BUTTON.getRect(mArgs.GameServer))
                # 等待过渡动画
                time.sleep(0.8)
                return Task.GO_FOLLOW_CHECK_BOSS_LIST
        if mTask == Task.GO_FOLLOW_CHECK_BOSS_LIST:
            # 检查检索中对话框 (应对较慢网络)
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.BOSS_LIST_LOADING_TEXT):
                # 为避免过于频繁刷新，最好是边休眠边检测
                time.sleep(0.5)
                return mTask
            # 检查是否在Boss列表界面
            if not Checker.checkImageWithTemplate(mArgs, CheckTemplate.BOSS_LIST_REFRESH_BUTTON) \
                    and not Checker.checkImageWithTemplate(mArgs, CheckTemplate.BOSS_LIST_REFRESH_UNAVAILABLE_BUTTON):
                return mTask
            aircv_rect = Checker.getAircvRectWithTemplate(mArgs)
            # 没有找到房间
            if not aircv_rect.found:
                # 刷新列表
                Follow.__refreshList(mArgs)
                return mTask
            else:  # 已找到房间
                # 这张卡片是一个房间
                if aircv_rect.has_info:
                    if not aircv_rect.allow_enter:
                        # 房间不允许进入，向下滑动一张卡片，继续查找
                        Follow.__swipeDownFirstCard(mArgs)
                        return mTask
                    else:  # 房间允许进入
                        text = aircv_rect.getImageText()
                        if text is []:
                            Logger.displayLog("OCR时出现问题", Logger.LOG_LEVEL_ERROR, -1)
                        # 查找OCR结果
                        if mArgs.GuestData.FollowFriendSelect and not str(aircv_rect.getImageText()[0]).__contains__(
                                mArgs.GuestData.FollowFriendSelectName + Locate.BOSS_LIST_CARD_TITLE_ROOM_SUFFIX[mArgs.GameServer]
                        ):
                            Follow.__swipeDownFirstCard(mArgs)
                            Logger.displayLog("Not found, original str: " + str(aircv_rect.getImageText()[0]), Logger.LOG_LEVEL_INFO)
                            return mTask
                        # TODO: 判断体力消耗
                        # 点击房间并进入
                        mArgs.adb.random_click(aircv_rect.rect)
                        return Task.GO_ROOM_AS_GUEST
        return mTask

    @staticmethod
    def __refreshList(mArgs):
        if Checker.checkImageWithTemplate(mArgs, CheckTemplate.BOSS_LIST_REFRESH_BUTTON):
            mArgs.adb.random_click(CheckTemplate.BOSS_LIST_REFRESH_BUTTON.getRect(mArgs.GameServer))

    @staticmethod
    def __swipeDownFirstCard(mArgs):
        # 随机生成两个x用来竖直滑动
        random_vertical_swipe_x_fir = Random.genFloat(0, mArgs.adb.width, seed=123)
        random_vertical_swipe_x_sec = Random.genFloat(0, mArgs.adb.width, seed=321)
        random_swipe = Random.genInt(400, 800)
        mArgs.adb.swipe(
            # 滑动3张卡片的距离
            Point(
                random_vertical_swipe_x_fir,
                Const.BOSS_LIST_HEADER_BOTTOM_Y +
                # 第一张卡片底部到头图底部的距离
                Const.BOSS_LIST_FIRST_CARD_BOTTOM_Y - Const.BOSS_LIST_HEADER_BOTTOM_Y
            ),
            Point(random_vertical_swipe_x_sec, Const.BOSS_LIST_HEADER_BOTTOM_Y),
            # 随机生成一个滑动时间
            random_swipe
        )
        # 等待滑动动作完成
        time.sleep(float(random_swipe) / 1000)
