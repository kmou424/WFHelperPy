from lib.constants import Task, CheckTemplate, CheckRect
from lib.utils import Args
from modules.checker import Checker


class Login:
    @staticmethod
    def track(mArgs: Args, task: Task):
        # 前往登录: 点一下屏幕来登录
        if task == Task.GO_LOGIN:
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.LOGIN_INTERFACE_SIGN):
                mArgs.adb.random_click(CheckTemplate.LOGIN_INTERFACE_SIGN.getRect(mArgs.GameServer))
                return Task.GO_CONTINUE_AFTER_LOGIN
        # 点击登录后
        if task == Task.GO_CONTINUE_AFTER_LOGIN:
            # 如果现在还在登录界面，爬回去重新点
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.LOGIN_INTERFACE_SIGN):
                return Task.GO_LOGIN
            # 如果登录后遇到了继续进行之前任务的弹窗
            # TODO: 用户选择重新登录后是否继续之前的任务
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.DIALOG_CONTINUE_TASK):
                mArgs.adb.random_click(CheckTemplate.DIALOG_DOUBLE_OK.getRect(mArgs.GameServer))
                return Task.GO_CHECK_INTERFACE
            # 点击关闭公告位置(日期改变)
            # 无脑点击来跳过签到/公告/活动提示等
            # 检测到底栏时停止并返回主城
            if Checker.hasBottomBar(mArgs.Screenshot):
                if Checker.checkImageWithTemplate(mArgs, CheckTemplate.HOME_BOSS_LIST_BUTTON):
                    return Task.GO_BACK_TO_HOME
                else:
                    return Task.GO_BACK_TO_HOME
            else:
                mArgs.adb.random_click(CheckRect.DIALOG_ANNOUNCEMENT_CLOSE_BUTTON_RECT)
        # 继续上次任务: 前往检测当前界面是否在战斗中
        if task == Task.GO_CHECK_INTERFACE:
            # 判定正在战斗中
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.FIGHT_PAUSE_BUTTON_RECT):
                return Task.GO_FIGHT
            # 判定战斗结束
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.RESULT_BOTTOM_CONTINUE_BUTTON):
                return Task.GO_FIGHT_RESULT
        return task
