import time

from lib.base import Point
from lib.constants import Task, CheckTemplate, Const, ConfigSections, ConfigOptions
from lib.logger import Logger
from lib.resource import Resource
from lib.utils import Random, Args
from modules.checker import Checker


class Creator:
    @staticmethod
    def track(mArgs: Args, mTask: Task):
        if mTask == Task.NO_TASK:
            # 检查主城界面领主战按钮
            if not Checker.checkImageWithTemplate(mArgs, CheckTemplate.HOME_BOSS_LIST_BUTTON):
                Logger.displayLog("不在主城，请求返回首页")
                return Task.GO_BACK_TO_HOME_FORCE
            else:
                mArgs.adb.random_click(CheckTemplate.HOME_BOSS_LIST_BUTTON.getRect(mArgs.GameServer))
                # 等待过渡动画
                time.sleep(0.8)
                # 重置定时器
                mArgs.timer.reset()
                return Task.GO_CREATOR_CHECK_BOSS_LIST
        if mTask == Task.GO_CREATOR_CHECK_BOSS_LIST:
            # 检查检索中对话框 (应对较慢网络)
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.BOSS_LIST_LOADING_TEXT):
                # 为避免过于频繁刷新，最好是边休眠边检测
                time.sleep(0.5)
                return mTask
            # 检查是否在Boss列表界面
            if not Checker.checkImageWithTemplate(mArgs, CheckTemplate.BOSS_LIST_REFRESH_BUTTON):
                return mTask
            # 检查定时器(判断超时)
            # 如果已经在此界面停止了20s以上，刷新Boss列表
            if mArgs.timer.getPassTime() > 20:
                Logger.displayLog("操作超时，刷新列表")
                mArgs.adb.random_click(CheckTemplate.BOSS_LIST_REFRESH_BUTTON.getRect(mArgs.GameServer))
                # 再次重置定时器
                mArgs.timer.reset()
                return mTask
            # 找Boss头像对应的卡片，返回是否找到，卡片是否包含"i"图标以及卡片的Rect
            aircv_rect = Checker.getAircvRectWithTemplate(mArgs, mArgs.RoomCreatorData.MinBossTemplate)
            # 随机生成两个x用来竖直滑动
            random_vertical_swipe_x_fir = Random.genFloat(0, mArgs.adb.width, seed=123)
            random_vertical_swipe_x_sec = Random.genFloat(0, mArgs.adb.width, seed=321)
            # 找到Boss头像对应的卡片
            if aircv_rect.found:
                # 检测到这个Boss的卡片是一个房间
                if aircv_rect.has_info:
                    random_swipe = Random.genInt(400, 800)
                    mArgs.adb.swipe(
                        # 从"i"图标底部开始向上滑动至头图底部
                        Point(random_vertical_swipe_x_fir, aircv_rect.rect.right_bottom.y),
                        Point(random_vertical_swipe_x_sec, Const.BOSS_LIST_HEADER_BOTTOM_Y),
                        # 随机生成一个滑动时间
                        random_swipe
                    )
                    # 等待滑动动作完成
                    time.sleep(float(random_swipe) / 1000)
                else:  # 这张卡片不是一个房间
                    # 点进去，前往下一步骤
                    mArgs.adb.random_click(aircv_rect.rect)
                    # 重置定时器，为下一个步骤准备计时
                    mArgs.timer.reset()
                    return Task.GO_CREATOR_CHECK_BOSS_LEVEL
            else:  # 没有找到头像对应的卡片(说明Boss在列表下面，继续向下翻)
                random_swipe = Random.genInt(550, 1000)
                mArgs.adb.swipe(
                    # 滑动3张卡片的距离
                    Point(
                        random_vertical_swipe_x_fir,
                        Const.BOSS_LIST_HEADER_BOTTOM_Y +
                        # 3 * 第一张卡片底部到头图底部的距离
                        3 * (Const.BOSS_LIST_FIRST_CARD_BOTTOM_Y - Const.BOSS_LIST_HEADER_BOTTOM_Y)
                    ),
                    Point(random_vertical_swipe_x_sec, Const.BOSS_LIST_HEADER_BOTTOM_Y),
                    # 随机生成一个滑动时间
                    random_swipe
                )
                # 等待滑动动作完成
                time.sleep(float(random_swipe) / 1000)
        if mTask == Task.GO_CREATOR_CHECK_BOSS_LEVEL:
            # 检测是否已经到了选择Boss难度的界面
            if not Checker.checkImageWithTemplate(mArgs, CheckTemplate.BOSS_INFO_EXCHANGE_BUTTON):
                return mTask
            # 检查定时器(判断超时)
            if mArgs.timer.getPassTime() > 10:
                Logger.displayLog("操作超时，回到主城")
                return Task.GO_BACK_TO_HOME_FORCE
            # 获取目标Boss的ID
            creator_boss_id = mArgs.cfgMan \
                .checkoutSection(ConfigSections.SECTION_CUSTOM.get()) \
                .getString(ConfigOptions.ROOM_CREATOR_BOSS_SELECTOR.get())
            # 扫描图片
            aircv_rect = Checker.getAircvRectWithTemplate(mArgs, Resource.getBossTemplate(mArgs.GameServer, creator_boss_id))
            # 找到就点击
            if aircv_rect.found:
                mArgs.adb.random_click(aircv_rect.rect)
                return Task.GO_CREATOR_CREATE_ROOM
        if mTask == Task.GO_CREATOR_CREATE_ROOM:
            # 点击多人游戏按钮
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.COMMON_MULTI_PLAY_BUTTON):
                mArgs.adb.random_click(CheckTemplate.COMMON_MULTI_PLAY_BUTTON.getRect(mArgs.GameServer))
                return Task.GO_ROOM_AS_OWNER
        return mTask
