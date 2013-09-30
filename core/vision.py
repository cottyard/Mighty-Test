from cv2 import cv
import numpy # need to explicitly import this for pyinstaller to detect dependency
from PIL import ImageGrab

def findInScreen(path):
    screen = ImageGrab.grab()
    screen_path = path.replace('.png', '_screen.png')
    screen.save(screen_path)

    template = cv.LoadImage(path)
    screen = cv.LoadImage(screen_path)

    w_m, h_m = cv.GetSize(screen)
    w_t, h_t = cv.GetSize(template)

    width = w_m - w_t + 1
    height = h_m - h_t + 1

    result = cv.CreateImage((width, height), 32, 1)

    cv.MatchTemplate(screen, template, result, cv.CV_TM_SQDIFF)

    minVal, maxVal, minLoc, maxLoc = cv.MinMaxLoc(result)

    if float(minVal)/maxVal < 0.2:
        return minLoc
