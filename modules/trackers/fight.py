import time


from lib.constants import CheckTemplate, Task
from lib.utils import Args
from modules.checker import Checker


class Fight:
    @staticmethod
    def track(mArgs: Args, task: Task, start_time: float, escape_time: int):
        if task == Task.GO_FIGHT_AS_GUEST or \
                task == Task.GO_FIGHT_AS_OWNER:
            return Task.GO_FIGHT
        # 前往战斗
        if task == Task.GO_FIGHT:
            if escape_time >= 0:
                if time.perf_counter() - start_time >= escape_time:
                    return Task.GO_FIGHT_ESCAPE
            # 判断续战
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.FIGHT_REBORN_BUTTON_TEXT):
                print("战败了...")
                return Task.GO_BACK_TO_HOME
            # 判断结算
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.RESULT_BOTTOM_CONTINUE_BUTTON):
                task = Task.GO_FIGHT_RESULT
        # 结算
        if task == Task.GO_FIGHT_RESULT:
            # 台服设定，掉线后结算时的两个按钮会变成一个按钮，所以特判一下
            if mArgs.mGameServer == 'tw':
                if Checker.checkImageWithTemplate(mArgs, CheckTemplate.RESULT_OFFLINE_EXIT_ROOM_BUTTON):
                    mArgs.adb.random_click(CheckTemplate.RESULT_OFFLINE_EXIT_ROOM_BUTTON.getRect(mArgs.mGameServer))
                    return Task.GO_BACK_TO_HOME
            # TODO: 提供离开房间和返回房间两种不同的选项
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.RESULT_BOTTOM_EXIT_ROOM_BUTTON):
                mArgs.adb.random_click(CheckTemplate.RESULT_BOTTOM_EXIT_ROOM_BUTTON.getRect(mArgs.mGameServer))
                return Task.GO_BACK_TO_HOME
            # 没要到最后一步，点击继续(无脑一直点可以用来跳过一些特殊事件，例如升级等)
            mArgs.adb.random_click(CheckTemplate.RESULT_BOTTOM_CONTINUE_BUTTON.getRect(mArgs.mGameServer))
        if task == Task.GO_FIGHT_ESCAPE:
            # 检查确认放弃对话框并点击确认
            # 优先级最高
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.FIGHT_PAUSE_UI_ESCAPE_DIALOG):
                mArgs.adb.random_click(CheckTemplate.DIALOG_DOUBLE_OK.getRect(mArgs.mGameServer))
                return Task.GO_BACK_TO_HOME
            # 检查暂停按钮并点击
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.FIGHT_PAUSE_BUTTON_RECT):
                mArgs.adb.random_click(CheckTemplate.FIGHT_PAUSE_BUTTON_RECT.getRect(mArgs.mGameServer))
                return task
            # 检查放弃按钮并点击
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.FIGHT_PAUSE_UI_ESCAPE_BUTTON):
                mArgs.adb.random_click(CheckTemplate.FIGHT_PAUSE_UI_ESCAPE_BUTTON.getRect(mArgs.mGameServer))
                return task
        return task
