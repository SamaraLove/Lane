# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 12:11:19 2019

@author: LOVESA
"""

#%matplotlib inline
#%nteractive debugger using the magic command %pdb
#Terminal to convert ojupyter to HTML
#jupyter nbconvert --to html notebook.ipynb

#importing relevant packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os
from os.path import isfile, join

import PipelineFunctions as Functions

#Parameters definition
low_threshold = 50
high_threshold = 150
kernel_size = 7
# Define the Hough transform parameters
# Make a blank the same size as our image to draw on
rho = 2 # distance resolution in pixels of the Hough grid
theta = np.pi/180 # angular resolution in radians of the Hough grid
threshold = 15     # minimum number of votes (intersections in Hough grid cell)
min_line_len = 20 #minimum number of pixels making up a line
max_line_gap = 20    # maximum gap in pixels between connectable line segments


#'/path/to/folder'
#inputpath='C:/Users/lovesa/Desktop/Roadline/test_images'
#outputpath = 'C:/Users/lovesa/Desktop/Roadline/test_images/test_images_output'
inputpath = https://github.com/SamaraLove/Project-1-Lane-Following/tree/master/test_images
outputpath = https://github.com/SamaraLove/Project-1-Lane-Following/tree/master/test_images_output

#This will get all the files in the folder
testfolder = [ f for f in os.listdir(inputpath) if isfile(join(inputpath,f)) ]
images = np.empty(len(testfolder), dtype=object)
print("There are", len(testfolder), "files in this directory")

#read all files and store them in the array images.
#perform operations to all images in folder

for n in range(0, len(testfolder)):
    images[n] = cv2.imread( join(inputpath,testfolder[n]) )
    print('This image is number:', n, 'in the sequence',)
    plt.imshow(images[n])  #plot original image
    
    #from PipelineFunctions import grayscale
    gray = Functions.grayscale(images[n])
    plt.imshow(gray, cmap='gray')  #grayscale image
    plt.imshow(Functions.gaussian_blur(gray, kernel_size))
   
    edges = Functions.canny(images[n], low_threshold, high_threshold)
    plt.imshow(edges)   #plots binary image 

    initial_img = np.copy(images[n])*0 # creating a blank to draw lines on
    imshape = images.shape
    vertices = np.array([[(140,imshape[0]),(440, 325), (520, 325), (960,imshape[0])]], dtype=np.int32)

    # create a masked edges image
    masked_image = Functions.region_of_interest(initial_img, vertices)
    plt.imshow(masked_image)    #plots binary image with lines within boundary    
    
    #x, y = vertices.T
    #plt.plot(x, y, 'b--', lw=4)
    #lines = cv2.HoughLinesP(masked_image, rho, theta, threshold, np.array([]), min_line_len, max_line_gap)
    #plt.imshow(lines) 

    hough_img = Functions.hough_lines(edges, rho, theta, threshold, min_line_len, max_line_gap)
    #print(hough_img.shape)
    draw_lines = Functions.draw_lines(initial_img, lines, color=[255, 0, 0], thickness=10)
    weighted_img = Functions.weighted_img(images[n], initial_img, α=0.8, β=1., γ=0.)
    #weighted_img = (Functions.weighted_img(images[n], initial_img, α=0.8, β=1., γ=0.))
    
    plt.imshow(hough_img)       #Prints full binary image with red lines only
    plt.imshow(weighted_img)    #Prints original image with lines highlighted red 
    
    #Save images to the test_images_output directory
    # Change the current directory to specified directory  
    os.chdir(outputpath) 
    #filename = 'output' + n +'.jpg'
    filename = 'output' + str(n) +'.jpg'
    
    #cv2.imwrite(filename, gray)     #saving grayscale image
    cv2.imwrite(filename, weighted_img)     #saving grayscale overlay iamge on original

    #if cv2.waitKey(0) & 0xFF == ord('q'):
    #    break
    
    #Break out of the loop    
   # else:
   #     break
    
cv2.destroyAllWindows()

