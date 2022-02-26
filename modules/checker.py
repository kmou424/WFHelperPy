import aircv
import cv2

from lib.constants import Template
from lib.resource import Resource
from lib.utils import Color, Point, Rgb, Args


class Checker:
    @staticmethod
    def checkBottomBar(img: cv2.cv2, color: Color, point: Point):
        return color.isMatch(Rgb.point2rgb(img, point))

    @staticmethod
    def checkImageWithTemplate(mArg: Args, mTemplate: Template):
        return Checker.checkImage(
            Resource.cropImg(mArg.mScreenshot, mTemplate.getRect(mArg.mGameServer)),
            Resource.getTemplate(mArg.mGameServer, mTemplate.getName())
        )

    @staticmethod
    def checkImage(img1: cv2.cv2, img2: cv2.cv2, accuracy=0.85):
        return str(aircv.find_template(img1, img2, accuracy)) != 'None'

