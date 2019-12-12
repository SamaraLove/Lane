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
[image2]: ./examples/grey.jpg "grey"
[image3]: ./examples/blur.jpg "blur"
[image4]: ./examples/canny.jpg "canny"
[image5]: ./examples/dilate.jpg "dilate"
[image6]: ./examples/region.jpg "region"
[image7]: ./examples/mask.jpg "mask"
[image8]: ./examples/houghlines.jpg "houghlines"
[image9]: ./examples/houghdrawlines.jpg "houghdrawlines"

[image10]: ./examples/output_solidWhiteCurve.jpg "output_solidWhiteCurve"
[image11]: ./examples/output_solidWhiteRight.jpg "output_solidWhiteRight"
[image12]: ./examples/output_solidYellowCurve.jpg "output_solidYellowCurve"
[image13]: ./examples/output_solidYellowCurve2.jpg "output_solidYellowCurve2"
[image14]: ./examples/output_solidYellowLeft.jpg "output_solidYellowLeft"
[image15]: ./examples/output_whiteCarLaneSwitch.jpg "whiteCarLaneSwitch"


Original Image:
For this markdown, I will only show the steps with one image, the 'solidwhiteCurve'. The final images for all can be found at the end of this report.
![alt_text][image1]


---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 5 main steps. 

Pior to these I imported the relevant packages and defined the parameters. The pipeline calls in the various functions from 'Helper' which defines the main functions for finding houghlines. 

First, I converted the images to grayscale
![alt text][image2]


Then I applied the guassian blur cv2.GaussianBlur()
![alt text][image3]
Applied the canny function. cv2.Canny() applies Gaussian smoothing, suppresses noise and spurious gradients by averaging. It detects strong edges. 
The pixels between the set limits of low_threshold and high_threshold will be included as long as they are connected to strong edges. 
![alt text][image4]

dilate
![alt text][image5]

Found the region of interest, using a polygon shape. Defined the vertices of a four sided polygon to mask using cv2.fillPoly(). With the origin being in the upper left corner (think of location of a matrix).    
Cropping the image to within the region of interest
![alt text][image6]

mask
![alt text][image7]


cv2.HoughLinesP()
In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...
![alt text][image9]

Iterate over the output "lines" and draw lines on a blank image

Finally, the lines were overlayed on the original image. 
![alt text][image10]

Below is the result of the other 5 images
![alt text][image11]
![alt text][image12]
![alt text][image13]
![alt text][image14]
![alt text][image15]

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
