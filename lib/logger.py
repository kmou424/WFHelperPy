from lib.times import Time


class Logger:

    LOG_LEVEL_DEBUG = 'D'
    LOG_LEVEL_INFO = 'I'
    LOG_LEVEL_WARNING = 'W'
    LOG_LEVEL_ERROR = 'E'

    @staticmethod
    def quit(code: int):
        lvl = Logger.LOG_LEVEL_INFO
        if code != 0:
            lvl = Logger.LOG_LEVEL_ERROR
        Logger.__displayLog("Quited @ {code}".format(code=code), lvl)
        exit(code)

    @staticmethod
    def displayLog(log_content: str, log_lvl=LOG_LEVEL_INFO, quit_code=None):
        Logger.__displayLog(log_content, log_lvl)
        if quit_code is not None:
            Logger.quit(quit_code)

    @staticmethod
    def __displayLog(log_content: str, log_lvl: str):
        print("[{time_str}] [{log_lvl}] {content}"
              .format(time_str=Time.getTimeByStandardFormat(), log_lvl=log_lvl, content=log_content))
