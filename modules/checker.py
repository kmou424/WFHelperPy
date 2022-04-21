import aircv
import cv2

from lib.base import Color, Rgb, Point, Rect
from lib.constants import Template, CheckTemplate, Const, CheckColor, CheckPoint
from lib.logger import Logger
from lib.resource import Resource
from lib.utils import AircvRect, Args


class Checker:
    @staticmethod
    def checkBottomBar(img: cv2.cv2, color: Color, point: Point):
        return color.isMatch(Rgb.point2rgb(img, point))

    @staticmethod
    def hasBottomBar(img: cv2.cv2):
        if Checker.checkBottomBar(img, CheckColor.BOTTOM_BAR_ACTIVE_COLOR, CheckPoint.BOTTOM_BAR_CITY_POINT) or \
                Checker.checkBottomBar(img, CheckColor.BOTTOM_BAR_ACTIVE_COLOR, CheckPoint.BOTTOM_BAR_HOME_POINT) or \
                Checker.checkBottomBar(img, CheckColor.BOTTOM_BAR_ACTIVE_COLOR,
                                       CheckPoint.BOTTOM_BAR_CHARACTER_POINT) or \
                Checker.checkBottomBar(img, CheckColor.BOTTOM_BAR_ACTIVE_COLOR, CheckPoint.BOTTOM_BAR_STORE_POINT) or \
                Checker.checkBottomBar(img, CheckColor.BOTTOM_BAR_ACTIVE_COLOR, CheckPoint.BOTTOM_BAR_PICKUP_POINT) or \
                Checker.checkBottomBar(img, CheckColor.BOTTOM_BAR_ACTIVE_COLOR, CheckPoint.BOTTOM_BAR_MENU_POINT):
            return True
        return False

    @staticmethod
    def checkImageWithTemplate(mArg: Args, mTemplate: Template, accuracy=0.85):
        if str(Checker.checkImage(
            Resource.cropImg(mArg.Screenshot, mTemplate.getRect(mArg.GameServer)),
            Resource.getTemplate(mArg.GameServer, mTemplate.getName()),
            accuracy
        )) != 'None':
            Logger.displayLog('Checker: ' + mTemplate.getName(), log_lvl=Logger.LOG_LEVEL_DEBUG)
            return True
        else:
            return False

    @staticmethod
    def checkImage(img1: cv2.cv2, img2: cv2.cv2, accuracy=0.85) -> dict:
        return aircv.find_template(img1, img2, accuracy)

    @staticmethod
    def extractPointFromAircv(aircv_ret) -> dict:
        rect_points = str(aircv_ret['rectangle']).replace('))', '').replace('((', '').split('), (')
        left_top = rect_points[0].split(', ')
        left_bottom = rect_points[1].split(', ')
        right_top = rect_points[2].split(', ')
        right_bottom = rect_points[3].split(', ')

        return {
            'lt': left_top,
            'lb': left_bottom,
            'rt': right_top,
            'rb': right_bottom
        }

    @staticmethod
    def getAircvRectWithTemplate(mArgs: Args, template=None) -> AircvRect:
        # 在截图中查找模板并获取结果
        if template is not None:
            img_info = Checker.checkImage(
                mArgs.Screenshot,
                template,
                accuracy=0.86
            )
        else:
            img_info = Checker.checkImage(
                mArgs.Screenshot,
                Resource.getTemplate(mArgs.GameServer, 'Common_card_info_icon'),
                accuracy=0.86
            )
        # 初始化 返回值 AircvRect 类
        ret = AircvRect(False, False, False)
        if str(img_info) != 'None':
            # 查找结果不为None时，设置返回结果"是否找到"为True
            ret.found = True
            # 获取结果中的左上角与右下角的点
            points = Checker.extractPointFromAircv(img_info)
            left_top = points['lt']
            right_bottom = points['rb']
            if template is not None:
                # 使用这两点生成一个Rect
                target_rect = Rect(Point(int(left_top[0]), int(left_top[1])),
                                   Point(int(right_bottom[0]), int(right_bottom[1])))
                # 扩展Rect为整个卡片
                target_rect.left_top.x = Const.BOSS_LIST_CARD_LEFT_X
                target_rect.right_bottom.x = Const.BOSS_LIST_CARD_RIGHT_X
                # 查找卡片中是否有房间特有的标志
                # 如果有，将"此卡片为房间"设置为True
                ret.has_info = str(Checker.checkImage(
                    Resource.cropImg(mArgs.Screenshot, target_rect),
                    Resource.getTemplate(mArgs.GameServer, CheckTemplate.COMMON_CARD_INFO_ICON.getName())
                )) != 'None'
                # 缩减卡片右边x，防止点到"i"按钮
                target_rect.right_bottom.x = Const.BOSS_LIST_CARD_RIGHT_X_NO_INFO
                # 最后把卡片Rect赋值给返回值的Rect
                ret.rect = target_rect
            else:
                ret.has_info = True
                room_status_color_point = Point(int(left_top[0]) - Const.BOSS_LIST_CARD_INFO_MARGIN_LEFT_ROOM_STATUS,
                                                int(left_top[1]))
                ret.allow_enter = CheckColor.PREPARE_ACTIVE_COLOR.isMatch(
                    Rgb.point2rgb(mArgs.Screenshot, room_status_color_point))
                left_top[0] = str(Const.BOSS_LIST_CARD_TEXT_LEFT)
                left_top[1] = str(int(left_top[1]) - Const.BOSS_LIST_CARD_INFO_MARGIN_TOP)
                right_bottom[0] = str(Const.BOSS_LIST_CARD_TEXT_RIGHT)
                right_bottom[1] = str(int(right_bottom[1]) + Const.BOSS_LIST_CARD_INFO_MARGIN_BOTTOM)
                ret.rect = Rect(Point(int(left_top[0]), int(left_top[1])),
                                Point(int(right_bottom[0]), int(right_bottom[1])))
                re2 = []
                for r in mArgs.ocr.ocr(Resource.cropImg(mArgs.Screenshot, ret.rect)):
                    re2.append(''.join(r[0]))
                ret.setImageText(re2)

        return ret
