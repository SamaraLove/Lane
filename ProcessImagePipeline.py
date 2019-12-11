# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 13:45:30 2019

@author: LOVESA
"""

#importing relevant packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os
import cv2
import math
from os.path import isfile, join

import Helper as Functions

#Parameters definition
low_threshold = 50
high_threshold = 150
kernel_size = 7
# Define the Hough transform parameters
# Make a blank the same size as our image to draw on
rho = 2 # distance resolution in pixels of the Hough grid
theta = np.pi/180 # angular resolution in radians of the Hough grid
threshold = 160     # minimum number of votes (intersections in Hough grid cell)
min_line_len = 10 #minimum number of pixels making up a line
max_line_gap = 20    # maximum gap in pixels between connectable line segments


# image processing pipeline function
def pipeline(image):
    plt.imshow(image)  #plot original image
    initial_img = np.copy(image)*0 # creating a blank to draw lines on

    #from PipelineFunctions import grayscale, gaussian blur and canny functions on the whole image
    gray = Functions.grayscale(image)
    plt.imshow(gray, cmap='gray')  #grayscale image
    gaussian_blur = Functions.gaussian_blur(gray, kernel_size)
    plt.imshow(gaussian_blur)
    edges = Functions.canny(gaussian_blur, low_threshold, high_threshold)
    plt.imshow(edges)   #plots binary image 

    # dilate()ing edge image. 
    #This will make the lines thicker which will help fit the Hough lines better
    dilated = cv2.dilate(edges, np.ones((3,3), dtype=np.uint8))
    plt.imshow(dilated)

    #Cropping the image to within the region of interest
    #imshape = image.shape
    #vertices = np.array([[(140,imshape[0]),(440, 325), (520, 325), (960,imshape[0])]], dtype=np.int32)
    vertices = np.array([[(140,550),(440, 325), (550, 325), (920,550)]], dtype=np.int32)
    #the co-ordinate origin in the image is top-left corner of image
    
    # create a masked edges image
    masked_image = Functions.region_of_interest(dilated, vertices)
    plt.imshow(masked_image)    #plots binary image with lines within boundary    
    #Shows the region
    #x, y = vertices.T
    #plt.plot(x, y, 'b--', lw=4)
    
    #Detecting shape edges in the remaining (cropped) image data
    #Applying the hough transform
    hough_img = Functions.hough_lines(masked_image, rho, theta, threshold, min_line_len, max_line_gap)

    #Testing output of hough_img
    #print(hough_img.shape)
    #print(hough_img)
    #for i in range(hough_img.shape[0]):
    #    for j in range(hough_img.shape[1]):
    #        for k in range(3):
    #            if hough_img[i,j,k] > 1e-4:
    #                print(i,j,k,hough_img[i,j,k])
    
    plt.imshow(hough_img)       #Prints full binary image with red lines only
    weighted_img = Functions.weighted_img(hough_img,image, α=0.8, β=1.,γ=0.)
    plt.imshow(weighted_img)    #Prints original image with lines highlighted red 
    
    return weighted_img