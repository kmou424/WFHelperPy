import json

import cv2

from lib.constants import ConfigSections, ConfigOptions
from lib.utils import Rect, Boss, Args


class Resource:
    __package_name = {
        'cn': 'com.leiting.wf',
        'tw': 'air.com.gamania.worldflipper'
    }

    @staticmethod
    def getGamePackageName(server: str):
        return Resource.__package_name.get(server)

    @staticmethod
    def getBellBossList(mArgs: Args):
        bell_selector_mode = mArgs.cfgMan\
            .selectSection(ConfigSections.SECTION_CUSTOM.get())\
            .getString(ConfigOptions.BELL_SELECTOR_MODE.get(), default='no')
        ret = None
        if bell_selector_mode == 'boss_selector':
            ret = mArgs.cfgMan\
                .selectSection(ConfigSections.SECTION_CUSTOM.get())\
                .getString(ConfigOptions.BOSS_SELECTOR.get())
        if bell_selector_mode == 'bell_boss_selector_advanced':
            ret = mArgs.cfgMan\
                .selectSection(ConfigSections.SECTION_CUSTOM.get())\
                .getString(ConfigOptions.BELL_BOSS_SELECTOR_ADVANCED.get())
        if ret is not None:
            ret = ret.split(',')
        return ret

    @staticmethod
    def getTemplate(server: str, template_img_name: str):
        target = "template/{server}/{tin}.png"\
            .format(server=server, tin=template_img_name)
        return cv2.imread(target)

    @staticmethod
    def getBossTemplate(server: str, boss_id: str):
        target = "template/{server}/boss/Boss_{boss_id}.png"\
            .format(server=server, boss_id=boss_id)
        return cv2.imread(target)

    @staticmethod
    def cropImg(img: cv2.cv2, rect: Rect):
        return img[rect.left_top.y:rect.right_bottom.y, rect.left_top.x:rect.right_bottom.x]


class ResourceJson:
    @staticmethod
    def getBossInfo(server: str):
        target = "template/{server}/boss/index.json"\
            .format(server=server)
        with open(target, encoding='utf-8') as file:
            res = json.load(file)
        ret = []
        for i in res:
            boss = Boss(i)
            if (boss.getType() == 'special' and boss.isAvailable())\
                    or boss.getType() == 'normal':
                ret.append(i)
        return ret
