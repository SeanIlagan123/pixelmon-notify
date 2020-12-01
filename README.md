This is a small script that will notify a user via sound if a legendary pokemon spawns in pixelmon.
-> Lets a user have other apps open without having to pay attention to Minecraft 1.12.2

To use this Tesseract OCR needs to be installed on your computer.
Useful instructions can be found here: https://nanonets.com/blog/ocr-with-tesseract/#installingtesseract. NOTE: Will need to configure pathing for it to work there are useful tutorials online that show you how to do that.
Unfortunately the script is not quite optimised for running on all window resolutions. So you will need to change the values of line 149 in order for it to work. See screen_focus_example.png to find the ideal cropped positions.
The window size should be small when viewing the cv2 output and should only focus on the text not the entire screen.

An example of the app being used can be found here: 
https://youtu.be/lR7ioIf_OuY


NOTE: Minimising minecraft will stop the code from running, to use this effectively just place another window ontop of it.
