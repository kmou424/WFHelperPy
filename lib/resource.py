import json

import cv2

from lib.base import Rect, Boss
from lib.config import ConfigManager
from lib.constants import ConfigSections, ConfigOptions, ConfigValues


class ResourceJson:
    @staticmethod
    def getBossInfo(server: str):
        target = "template/{server}/boss/index.json" \
            .format(server=server)
        with open(target, encoding='utf-8') as file:
            res = json.load(file)
        ret = []
        for i in res:
            boss = Boss(i)
            if (boss.getType() == 'special' and boss.isAvailable()) \
                    or boss.getType() == 'normal':
                ret.append(i)
        return ret


class Resource:
    __package_name = {
        'cn': 'com.leiting.wf',
        'tw': 'air.com.gamania.worldflipper'
    }

    @staticmethod
    def getGamePackageName(server: str):
        return Resource.__package_name.get(server)

    @staticmethod
    def getGamingModeMain(cfgMan: ConfigManager):
        gaming_mode_main = cfgMan \
            .selectSection(ConfigSections.SECTION_MAIN.get()) \
            .getString(ConfigOptions.GAMING_MODE_MAIN.get(), default=ConfigValues.GAMING_MODE_MAIN_GUEST.get())
        if gaming_mode_main == ConfigValues.GAMING_MODE_MAIN_GUEST.get():
            return ConfigValues.GAMING_MODE_MAIN_GUEST
        if gaming_mode_main == ConfigValues.GAMING_MODE_MAIN_OWNER.get():
            return ConfigValues.GAMING_MODE_MAIN_OWNER

    @staticmethod
    def getBellBossList(cfgMan: ConfigManager):
        bell_selector_mode = cfgMan \
            .selectSection(ConfigSections.SECTION_CUSTOM.get()) \
            .getString(ConfigOptions.BELL_SELECTOR_MODE.get(), default='no')
        ret = None
        if bell_selector_mode == ConfigValues.BELL_SELECTOR_MODE_COMMON.get():
            ret = cfgMan \
                .selectSection(ConfigSections.SECTION_CUSTOM.get()) \
                .getString(ConfigOptions.COMMON_BOSS_SELECTOR.get())
        if bell_selector_mode == ConfigValues.BELL_SELECTOR_MODE_ADVANCED.get():
            ret = cfgMan \
                .selectSection(ConfigSections.SECTION_CUSTOM.get()) \
                .getString(ConfigOptions.BELL_BOSS_SELECTOR_ADVANCED.get())
        if ret is not None:
            ret = ret.split(',')
        return ret

    @staticmethod
    def getTemplate(server: str, template_img_name: str):
        target = "template/{server}/{tin}.png" \
            .format(server=server, tin=template_img_name)
        return cv2.imread(target)

    @staticmethod
    def getBossTemplate(server: str, boss_id: str):
        target = "template/{server}/boss/Boss_{boss_id}.png" \
            .format(server=server, boss_id=boss_id)
        return cv2.imread(target)

    @staticmethod
    def getMinBossTemplate(cfgMan: ConfigManager, GameServer: str) -> cv2.cv2:
        boss_id = cfgMan \
            .checkoutSection(ConfigSections.SECTION_CUSTOM.get()) \
            .getString(ConfigOptions.ROOM_CREATOR_BOSS_SELECTOR.get()) \
            .split('_')[0]
        for boss_info in ResourceJson.getBossInfo(GameServer):
            boss = Boss(boss_info)
            if boss.getId() == boss_id:
                return Resource.getBossTemplate(
                                GameServer,
                                "{id}_{level}".format(id=boss_id, level=boss.getMinLevel())
                )

    @staticmethod
    def cropImg(img: cv2.cv2, rect: Rect, isGray=False):
        img = img[rect.left_top.y:rect.right_bottom.y, rect.left_top.x:rect.right_bottom.x]
        if isGray:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        return img
