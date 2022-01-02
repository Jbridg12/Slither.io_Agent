#   file:           decisionmaker.py
#   author:         alex williams
#   description:
#       this file implements the DecisionMaker class for COSC494's Project 4 assignment.
#       the class facilitates decision-making by applying Hough transforms to identify 
#       orbs in Slither.io game screen. The class'es primary use is the "generate_decision"
#       method that takes an image as input to generate a navigational decision (e.g., "N" 
#       for North).
#
#   usage:
#       this class can be used as follows:
#
#           d = DecisionMaker([250,250]) // (250,250) is the location of the snake in your screenshot.
#           decision = d.generate_decision(img)
#
#   note:
#       you cannot modify this file for Project 4.

import cv2
import math

#Needed to import numpy
import numpy as np

class DecisionMaker():
    def __init__(self, center):
        '''The constructor requires an x,y coordinate in a list or tuple that
        represents the center point of the screen, i.e. where the snake is located.'''
        self.center = center

    def calculate_quadrant_counts(self, circles):
        '''This function calculates perceived orb counts for each quadrant, given a list of circles.'''
        
        # define a dictionary for counting based on predetermined weights.
        #   - these weights counteract the presence of the leaderboard + other UI elements that are false positives
        quad_counts = {
            'N': 0,
            'NW': -10,
            'W': 0,
            'SW': -25,
            'S': -25,
            'SE': -25,
            'E': -10,
            'NE': -10,
        }

        # iteate over all the circle objects, and tally the direction counts.
        for circle in circles[0,:]:
            print(circle)
            # Determine which direction the circle is, relative to our target.
            deltaX = circle[0] - self.center[0]
            deltaY = circle[1] - self.center[1]

            # Calculated the degree between points.
            degrees_temp = math.atan2(deltaX, deltaY)/math.pi*180
            if degrees_temp < 0:
                degrees_final = 360 + degrees_temp
            else:
                degrees_final = degrees_temp
            
            # Perform a look-up with compass directions.
            compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
            direction = compass_brackets[round(degrees_final / 45)]
        
            # Increment
            quad_counts[direction]+=1

        print(quad_counts)

        # Return the direction with the largest number of counted orbs
        return max(quad_counts, key=quad_counts.get)

    def generate_decision(self, img):
        '''This funciton generates a navigational decision provided an OpenCV image object.
        Navigational decisions are returned as a string, based on the following mapping:
        
            N --> North
            NW --> Northwest
            W --> West
            SW --> Southwest
            S --> South
            SE --> Southeast
            E --> East
            NE --> Northeast
        '''

        # Run the
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2GRAY)
        gray_blur = cv2.medianBlur(img, 5)
        gray_lap = cv2.Laplacian(gray_blur, cv2.CV_8UC1, ksize=3)
        dilate_lap = cv2.dilate(gray_lap, (3, 3))
        lap_blur = cv2.bilateralFilter(dilate_lap, 5, 9, 9)
        circles = cv2.HoughCircles(lap_blur, cv2.HOUGH_GRADIENT, 5, 5, param2=25, minRadius=1, maxRadius=5)
        
        #Removed draw_circles call
        #cimg = draw_circles(img, circles)

        # Feed the image into our counter, and return the direction with the 
        # largest number of orbs.
        return self.calculate_quadrant_counts(circles)