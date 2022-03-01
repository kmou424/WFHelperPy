import aircv
import cv2

from lib.constants import Template, CheckTemplate, Const, CheckColor, CheckPoint
from lib.resource import Resource
from lib.utils import Color, Point, Rgb, Args, AircvRect, Rect


class Checker:
    @staticmethod
    def checkBottomBar(img: cv2.cv2, color: Color, point: Point):
        return color.isMatch(Rgb.point2rgb(img, point))

    @staticmethod
    def hasBottomBar(img: cv2.cv2):
        if Checker.checkBottomBar(img, CheckColor.BOTTOM_BAR_ACTIVE_COLOR, CheckPoint.BOTTOM_BAR_CITY_POINT) or \
                Checker.checkBottomBar(img, CheckColor.BOTTOM_BAR_ACTIVE_COLOR, CheckPoint.BOTTOM_BAR_HOME_POINT) or \
                Checker.checkBottomBar(img, CheckColor.BOTTOM_BAR_ACTIVE_COLOR, CheckPoint.BOTTOM_BAR_CHARACTER_POINT) or \
                Checker.checkBottomBar(img, CheckColor.BOTTOM_BAR_ACTIVE_COLOR, CheckPoint.BOTTOM_BAR_STORE_POINT) or \
                Checker.checkBottomBar(img, CheckColor.BOTTOM_BAR_ACTIVE_COLOR, CheckPoint.BOTTOM_BAR_PICKUP_POINT) or \
                Checker.checkBottomBar(img, CheckColor.BOTTOM_BAR_ACTIVE_COLOR, CheckPoint.BOTTOM_BAR_MENU_POINT):
            return True
        return False

    @staticmethod
    def checkImageWithTemplate(mArg: Args, mTemplate: Template, accuracy=0.85):
        return str(Checker.checkImage(
            Resource.cropImg(mArg.Screenshot, mTemplate.getRect(mArg.GameServer)),
            Resource.getTemplate(mArg.GameServer, mTemplate.getName()),
            accuracy
        )) != 'None'

    @staticmethod
    def checkImage(img1: cv2.cv2, img2: cv2.cv2, accuracy=0.85) -> dict:
        return aircv.find_template(img1, img2, accuracy)

    @staticmethod
    def getAircvRectWithTemplate(mArgs: Args, template: cv2.cv2) -> AircvRect:
        # 在截图中查找模板并获取结果
        img_info = Checker.checkImage(
            mArgs.Screenshot,
            template,
            accuracy=0.87
        )
        # 初始化 返回值 AircvRect 类
        ret = AircvRect(False, False)
        if str(img_info) != 'None':
            # 查找结果不为None时，设置返回结果"是否找到"为True
            ret.found = True
            # 获取结果中的左上角与右下角的点
            rect_points = str(img_info['rectangle']).removesuffix('))').removeprefix('((').split('), (')
            left_top = rect_points[0].split(', ')
            right_bottom = rect_points[3].split(', ')
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
        return ret
