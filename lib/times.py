import time


class Time:
    @staticmethod
    def getTimeStampForNow():
        return int(time.time() * 1000)

    @staticmethod
    def getTimeStampByStandardFormat(tm: str):
        return int(time.mktime(time.strptime(tm, "%Y-%m-%d %H:%M:%S")) * 1000)

    @staticmethod
    def getTimeByStandardFormat():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    @staticmethod
    def getTimeByCustomFormat(fmt: str):
        return time.strftime(fmt, time.localtime(time.time()))
