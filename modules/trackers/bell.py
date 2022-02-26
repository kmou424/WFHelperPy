from lib.constants import CheckTemplate, Task
from lib.utils import Args
from modules.checker import Checker
from lib.resource import Resource


class Bell:
    @staticmethod
    def track(mArgs: Args, task: Task):
        if task == Task.NO_TASK:
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.HOME_BELL_ACTIVE):
                mArgs.adb.random_click(CheckTemplate.HOME_BELL_ACTIVE.getRect(mArgs.mGameServer))
                return Task.GO_BELL_CLICKED
        # 点击铃铛后
        if task == Task.GO_BELL_CLICKED:
            if Checker.checkImageWithTemplate(mArgs, CheckTemplate.BELL_DIALOG_TITLE_RECT):
                bell_boss_list = Resource.getBellBossList(mArgs)
                if bell_boss_list is None:
                    mArgs.adb.random_click(CheckTemplate.BELL_DIALOG_JOIN_RECT.getRect(mArgs.mGameServer))
                    return Task.GO_ROOM_AS_GUEST
                bell_dialog_boss_info_img = Resource.cropImg(
                    mArgs.mScreenshot,
                    CheckTemplate.BELL_DIALOG_BOSS_INFO_IMG.getRect(mArgs.mGameServer)
                )
                for boss_id in bell_boss_list:
                    if Checker.checkImage(
                            bell_dialog_boss_info_img,
                            Resource.getBossTemplate(mArgs.mGameServer, boss_id),
                            accuracy=0.95
                    ):
                        mArgs.adb.random_click(CheckTemplate.BELL_DIALOG_JOIN_RECT.getRect(mArgs.mGameServer))
                        # TODO: 日志打印Boss名字，单独在一个线程执行，以免占用过多资源
                        print('Boss ID: ' + boss_id)
                        return Task.GO_ROOM_AS_GUEST
                print('这不是咱要打的Boss，润了润了')
                mArgs.adb.random_click(CheckTemplate.BELL_DIALOG_DISJOIN_RECT.getRect(mArgs.mGameServer))
                return Task.GO_BACK_TO_HOME
        return task
