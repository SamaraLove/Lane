# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 11:29:11 2019

@author: LOVESA
"""
# Do all the relevant imports
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2 

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


### Read in the file and convert to grayscale   ###
#Create videocapture object and read the input video file
video = cv2.VideoCapture('solidWhiteRight.mp4',0)

#Error checking
#Check if the camera opened successfully 
if(video.isOpened()==False):
    print("Error opening the video stream file")

# Obtaining the default resolutions of the frame - system dependent.
# Convert the resolutions from float to integer.
frame_width = int(video.get(3))
frame_height = int(video.get(4))
fps = (video.get(cv2.CAP_PROP_FPS))

### Write to the video file ###
# Define the codec and create VideoWriter object.
# Define the fps, in this case equal to 10. frame size is also another parameter.
#The output is stored in 'outpy.avi' file.
#MJPG is chosen as the FourCC
 
#VideoWriter(const String &filename, int fourcc, double fps, Size frameSize, bool isColor=true)

outputVideo = cv2.VideoWriter('outputVideoSL.avi',cv2.VideoWriter_fourcc('M','J','P','G'), fps, (frame_width,frame_height),isColor=False)


#Read until the video is completed
while(video.isOpened()):
    #Capture frame by frame
    ret, frame = video.read()
    
    if ret == True:
        # Operations on the frame, conversion to grey scale
         
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        #Display the resulting frame
        #cv2.imshow('Gray_video_frame', gray)
        #cv2.imshow('vid OG', frame)
        #Display orginal video for comparison 
         
        gaussian_blur = Functions.gaussian_blur(gray, kernel_size)
        cv2.imshow('gaussian_blur_video_frame', gaussian_blur)
       
        edges = Functions.canny(gray, low_threshold, high_threshold)
        cv2.imshow('Canny_video_frame',edges)   #plots binary image 
    
        #initial_img = np.copy(images[n])*0 # creating a blank to draw lines on
        #imshape = video.shape
        vertices = np.array([[(140,0),(440, 325), (520, 325), (920,0)]], dtype=np.int32)

        # create a masked edges image
        #masked_image = Functions.region_of_interest(video, vertices)
        #plt.imshow(masked_image)    #plots binary image with lines within boundary 
        
        
        
        # Write the frame into the file 'outputVideoSL.avi'
        #outputVideo.write(gray)
        #outputVideo.write(gaussian_blur)

        #Exit if Q is pressed
        #wait time in milliseconds each frame is displayed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    #Break out of the loop    
    else:
        break

#Release the video capture and video write objects
video.release()     
outputVideo.release()
 #Close all frames
cv2.destroyAllWindows()    