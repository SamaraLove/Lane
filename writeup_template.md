# **Finding Lane Lines on the Road** 

## Writeup Template
### Project 1. "Becoming a Self-Driving Car Engineer" Nanodegree (Udacity)


---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)
[image1]: ./examples/solidWhiteCurve.jpg "solidWhiteCurve"
[image2]: ./examples/solidWhiteRight.jpg "solidWhiteRight"
[image3]: ./examples/solidYellowCurve.jpg "solidYellowCurve"
[image4]: ./examples/solidWhiteRight.jpg "solidWhiteRight"
[image5]: ./examples/solidYellowCurve2.jpg "solidYellowCurve2"
[image6]: ./examples/whiteCarLaneSwitch.jpg "whiteCarLaneSwitch"

Original Images:
![]<img src="solidWhiteCurve" width="200">
![alt_text][image2]{:height="36px" width="36px"}.
![alt_text][image3]
![alt text][image4][image5][image6]
---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 5 main steps. 

Pior to these I imported the relevant packages and defined the parameters. The pipeline calls in the various functions from 'Helper' which defines the main functions for finding houghlines. 

First, I converted the images to grayscale
![alt text][image1]


Then I applied the guassian blur cv2.GaussianBlur()

Applied the canny function. cv2.Canny() applies Gaussian smoothing, suppresses noise and spurious gradients by averaging. It detects strong edges. 
The pixels between the set limits of low_threshold and high_threshold will be included as long as they are connected to strong edges. 


Found the region of interest, using a polygon shape. Defined the vertices of a four sided polygon to mask using cv2.fillPoly(). With the origin being in the upper left corner (think of location of a matrix).    
Cropping the image to within the region of interest


cv2.HoughLinesP()

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

Iterate over the output "lines" and draw lines on a blank image

Finally, the lines were overlayed on the original image. 


If you'd like to include images to show how the pipeline works, here is how to include an image: 

![alt text][image1]


### 2. Identify potential shortcomings with your current pipeline

The project was fun to work on, it was a jump from the classroom material and the project instructions were somewhat vauge. 

This project was not tested on images/ videos of different sizes – the vertices are static and not actively changing per image/video requirements
Ignore lines with certain gradients (i.e. 0 is ignored, could also ignore lines with gradients that differ from the expected average of slope, >0.5?)


Video is a bit jittery, could

One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to filter out small segments of the lines (length < 40 pixels) as they could be noise

Another potential improvement could be to ...
