
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

""" References """
# https://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui
# https://nanonets.com/blog/ocr-with-tesseract/

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
custom_config = r'--oem 0 --psm 6' # Define the settings for pytesseract


""" Actual code for capturing screen and checking condition """
def main():
    while True:
        with mss.mss() as sct:
            screen_capture()
            # Stop the program on button press (Must be done locally. Does not work if focus is on background app.)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

# Function that captures a specific window (does not need to be visible) instead of a screen.


def screen_capture():  # Credits to hazzey on StackOverFlow.
    hwnd = win32gui.FindWindow(None, 'Minecraft 1.12.2')
    left, top, right, bot = win32gui.GetClientRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)

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

    if result == 1:         # PrintWindow Succeeded
        # Original Code
        # Define an area of the window to focus on.
        screen = np.array(im)
        crop = screen[670:870, 0:160] # Will need to change these values based off the resolution of the window.

        # Apply some image preprocessing
        gray = get_grayscale(crop)
        noise = remove_noise(gray)
        thresh = thresholding(noise)
        cv2.imshow('test', thresh)
        checkString = pytesseract.image_to_string(thresh, config=custom_config)
        if "Pixelmon" in checkString:
            playsound('Suction.mp3')
            time.sleep(5)
main()
