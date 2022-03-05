import cv2
import numpy

from lib.times import Time


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def loadZoom(self, zoom: float):
        if zoom > 1.0:
            self.x = self.x * zoom
            self.y = self.y * zoom


class Rect:
    def __init__(self, left_top: Point, right_bottom: Point):
        self.left_top = left_top
        self.right_bottom = right_bottom


class Rgb:
    def __init__(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b

    @staticmethod
    def point2rgb(img: cv2.cv2, point: Point):
        return Rgb.pixel2rgb(img[point.y, point.x])

    @staticmethod
    def pixel2rgb(pixel: numpy.ndarray):
        return Rgb(pixel[2], pixel[1], pixel[0])


class Color:
    def __init__(self, left: Rgb, right: Rgb):
        self.left = left
        self.right = right

    def isMatch(self, src: Rgb):
        return (self.left.red <= src.red <= self.right.red) and \
               (self.left.green <= src.green <= self.right.green) and \
               (self.left.blue <= src.blue <= self.right.blue)


class Boss:
    BossLevels = {
        'prim': '初级',
        'mid': '中级',
        'high': '高级',
        'highp': '高级+',
        'super': '超级'
    }

    def __init__(self, item: dict):
        self.item = item

    def isAvailable(self) -> bool:
        end_time = Time.getTimeStampByStandardFormat(self.item['end'])
        now_time = Time.getTimeStampForNow()
        return end_time > now_time

    def getName(self) -> str:
        return self.item['name']

    def getId(self) -> str:
        return self.item['id']

    def getType(self) -> str:
        return self.item['type']

    def getLevels(self) -> str:
        return self.item['levels']

    def getMinLevel(self):
        return self.getLevels().split(' ')[0]
