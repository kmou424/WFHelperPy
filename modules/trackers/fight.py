from lib.constants import CheckTemplate, Task, ConfigValues
from lib.resource import Resource
from lib.utils import Args
from modules.checker import Checker


class Fight:
    @staticmethod
    def track(mArgs: Args, task: Task):
        if task == Task.GO_FIGHT_AS_GUEST or \
                task == Task.GO_FIGHT_AS_OWNER:
            # 开始战斗计时
            mArgs.timer.reset()
            task = Task.GO_FIGHT
        # 前往战斗
        if task == Task.GO_FIGHT:
            # 判定灵车模式并跳车
            if Resource.getGamingModeMain(mArgs) == ConfigValues.GAMING_MODE_MAIN_OWNER and \
                    mArgs.RoomCreatorData.Enabled and \
                    mArgs.RoomCreatorData.GhostMode == ConfigValues.COMMON_ENABLE.get() and \
                    mArgs.RoomCreatorData.GhostEscapeTime >= 0:
                pass_time = mArgs.timer.getPassTime()
                if pass_time >= mArgs.RoomCreatorData.GhostEscapeTime:
                    return Task.GO_FIGHT_ESCAPE
                else:
                    print("即将跳车，当前战斗时长%.2f秒，还有%.2f秒跳车" %
                          (pass_time, mArgs.RoomCreatorData.GhostEscapeTime - pass_time))
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
            if mArgs.GameServer == 'tw':
                if Checker.checkImageWithTemplate(mArgs, CheckTemplate.RESULT_OFFLINE_EXIT_ROOM_BUTTON):
                    mArgs.adb.random_click(CheckTemplate.RESULT_OFFLINE_EXIT_ROOM_BUTTON.getRect(mArgs.GameServer))
                    return Task.GO_BACK_TO_HOME_FORCE
            # TODO: 提供离开房间和返回房间两种不同的选项
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.RESULT_BOTTOM_EXIT_ROOM_BUTTON) or \
                    Checker.checkImageWithTemplate(mArgs, CheckTemplate.RESULT_BOTTOM_DISBAND_ROOM_BUTTON):
                mArgs.adb.random_click(CheckTemplate.RESULT_BOTTOM_EXIT_ROOM_BUTTON.getRect(mArgs.GameServer))
                return Task.GO_BACK_TO_HOME_FORCE
            # 如果已经出现底栏了，则直接回到主城
            if Checker.hasBottomBar(mArgs.Screenshot):
                return Task.GO_BACK_TO_HOME
            # 没有检测到继续按钮就点空白位置 (无脑一直点可以用来跳过一些特殊事件，例如升级等)
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.RESULT_BOTTOM_CONTINUE_BUTTON):
                mArgs.adb.random_click(CheckTemplate.RESULT_BOTTOM_CONTINUE_BUTTON.getRect(mArgs.GameServer))
            else:
                mArgs.adb.random_click(CheckTemplate.RESULT_BOTTOM_BLANK_SPACE.getRect(mArgs.GameServer))
        if task == Task.GO_FIGHT_ESCAPE:
            # 检查确认放弃对话框并点击确认
            # 优先级最高
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.FIGHT_PAUSE_UI_ESCAPE_DIALOG):
                mArgs.adb.random_click(CheckTemplate.DIALOG_DOUBLE_OK.getRect(mArgs.GameServer))
                return Task.GO_BACK_TO_HOME_FORCE
            # 检查暂停按钮并点击
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.FIGHT_PAUSE_BUTTON_RECT):
                mArgs.adb.random_click(CheckTemplate.FIGHT_PAUSE_BUTTON_RECT.getRect(mArgs.GameServer))
                return task
            # 检查放弃按钮并点击
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.FIGHT_PAUSE_UI_ESCAPE_BUTTON):
                mArgs.adb.random_click(CheckTemplate.FIGHT_PAUSE_UI_ESCAPE_BUTTON.getRect(mArgs.GameServer))
                return task
        return task
