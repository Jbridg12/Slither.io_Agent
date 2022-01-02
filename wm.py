#   file:           wm.py
#   author:         Josh Bridges
#   description:
#       this file implements the window manager class using selenium to
#       to open a chrome browser. The class allows taking a screenshot of
#       a certain space on the screen and extractText uses pytesseract to
#       draw text from a screenshot 
#
#   usage:
#       this class can be used as follows:
#           window = wm.WindowManager() //create instance
#           image = window.takeScreenshot(200, 200, 300, 300) // take a 200x200 screenshot starting at psition (300, 300)
#           text = window.extractText(image) // get the text from the passed image 

from selenium import webdriver
import cv2
try:     
    import Image
except ImportError:    
    from PIL import Image
import numpy as np
import mss
import mss.tools
import pytesseract
from PIL import Image
import PIL.ImageOps 

#Windows support for pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class WindowManager():
    #Constructor creates and starts a 600x600 chrome window on the slither.io website
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
        self.driver = webdriver.Chrome("./chromedriver.exe", options=chrome_options)
        
        self.driver.set_window_size(600, 600)
        self.driver.set_window_position(0, 0)
        self.driver.get("http://slither.io")
        
        #Instantiate threshold variables for text extraction
        self.threshold = 190
        self.var = 10
        
    #Takes a screenshot of the specified area of the screen
    def takeScreenshot(self, width=600, height=600, x=0, y=0):
        with mss.mss() as sct:
            region = {'left': x, 'top': y, 'width': width, 'height': height}
            
            img = sct.grab(region)
            mss.tools.to_png(img.rgb, img.size, output="screenshot.png")
            
            result = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
            img = result[::1, ::1]
            return img
    
    #Extract text as a string from the image passed using pytesseract
    def extractText(self, img):
        for rows in range(0, len(img)):    
            for cols in range(0, len(img[0])):        
                x = img[rows][cols]        
                if x[0] > self.threshold and x[1] > self.threshold and x[2] > self.threshold and max(x) - min(x) < self.var:            
                    img[rows][cols] = [0, 0, 0]       
                else:            
                    img[rows][cols] = [255,255,255]
                    
        text = pytesseract.image_to_string(img)
        return text
