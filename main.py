
import numpy as np
import pytesseract
import cv2
import mss
import mss.tools
import keyboard
from playsound import playsound
import pyautogui

# To capture minimised images
import win32gui
import win32ui
from ctypes import windll
from PIL import Image
import time


# Sending a message
import discord
from discord.ext import commands

# https://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui

""" Defining the preprocessing functions. """

# Set image to grayscale


def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal


def remove_noise(image):
    return cv2.medianBlur(image, 5)

# thresholding


def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# dilation


def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)

# erosion


def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)

# opening - erosion followed by dilation


def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# canny edge detection


def canny(image):
    return cv2.Canny(image, 100, 200)

# skew correction


def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# template matching


def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


# Definging a the config
custom_config = r'--oem 0 --psm 6'


""" Actual code for capturing screen and checking condition """

""" # The initial values of TOP and LEFT.
# Can be changed under certain conditions
top_value = 800
left_value = 1920 """

""" def main(image_captures):
    while True:
        with mss.mss() as sct:
            # The screen part to capture
            monitor = {"top": top_value, "left": left_value, "width": 160, "height": 135}

            # Grab the data
            sct_img = sct.grab(monitor)
            cv2.imshow('test', np.array(sct_img))

            gray = get_grayscale(np.array(sct_img))
            noise = remove_noise(gray)
            thresh = thresholding(noise)
            checkString = pytesseract.image_to_string(thresh, config=custom_config)
            # print("Using Thresh: " + checkString)
            if "Pixelmon" in checkString:
                playsound('Suction.mp3')
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            # Save to the picture file """


def main():
    while True:
        with mss.mss() as sct:
            # The screen part to capture
            # monitor = {"top": top_value, "left": left_value, "width": 160, "height": 135}
            # Grab the data
            # sct_img = sct.grab(monitor)
            if (screen_capture()):
                break
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            # Save to the picture file

# Function that captures a specific window (does not need to be visible) instead of a screen.


def screen_capture():
    hwnd = win32gui.FindWindow(None, 'Minecraft 1.12.2')

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    # left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left  # 750
    h = bot - top
    # h = 500

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    """ print(result) """

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        # PrintWindow Succeeded
        screen = np.array(im)
        crop = screen[670:870, 0:160]
        # cv2.imshow('test', screen)
        gray = get_grayscale(crop)
        noise = remove_noise(gray)
        thresh = thresholding(noise)
        cv2.imshow('test', thresh)
        checkString = pytesseract.image_to_string(thresh, config=custom_config)
        if "Pixelmon" in checkString:
            playsound('Suction.mp3')
            time.sleep(5)
        # main(new_capture)
        # im.save("test.png")
main()
