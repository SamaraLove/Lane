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

My pipeline consisted of 6 main steps. 

Pior to these I imported the relevant packages and defined the parameters. The pipeline calls in the various functions from 'Helper' which defines the main functions for finding houghlines. 

First, I converted the images to grayscale
![alt text][image2]

Then I applied the guassian blur cv2.GaussianBlur()to smooth the image and avoid noise.
![alt text][image3]

Applied the canny function. cv2.Canny()which applies Gaussian smoothing, suppresses noise and spurious gradients by averaging. It detects strong edges. The pixels between the set limits of low_threshold and high_threshold will be included as long as they are connected to strong edges. 
![alt text][image4]

The dilate()function was added as it dilates the edge image. This makes the lines thicker which improves the houghlines fit.
![alt text][image5]

The region of interest was found using a polygon shape. The vertices of a four sided polygon was defined to mask using cv2.fillPoly(). With the origin being in the upper left corner (think of location of a matrix). This reduces the space that we will focus on for the next transforms.
![alt text][image6]

The masked image was cropped to within the region of interest
![alt text][image7]

The houghlines detect the shape edges in the cropped image data. The cv2.HoughLinesP() transform was used which generates many points.
![alt text][image8]

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by using a linear model y=mx+c to iterate over the output "lines". I needed to either average the lines if there are many dashes detected for the lane or extrapolate them if there are some partially detected lines. 
The linear model enables us to use the gradient to find whether the lines belong to the left or right lanes based on their positive or negative gradient respectively. 
A global left and right lanes were created from the average of the multiple pixels/points on either line. The end points were required to extrapolate the lines from the horizon to the y intercept. The y intercepts were calculated using the linear model. Lastly, using the cv2.line() function, the left and right lines were drawn using the end points and the global lines. 
![alt text][image9]

Finally, the lines were overlayed on the original image using the cv2.addWeighted() function
![alt text][image10]

Below is the result of the other 5 images saved in the output directory.
![alt text][image11]
![alt text][image12]
![alt text][image13]
![alt text][image14]
![alt text][image15]

### 2. Identify potential shortcomings with your current pipeline

This project was not tested on images/ videos of different sizes – the vertices are static and not actively changing per image/video requirements which could lead to issues when cars drive in tight turns or up/down hills. Similarly, the parameters for the canny/hough transforms etc. are all fixed, so if the camera angle/position changes this would cause errors.

The video detection is jittery, and doesn't always produce a constant line feed.

### 3. Suggest possible improvements to your pipeline

A possible improvement would be to filter out small segments of the lines (length < 40 pixels) as they could be noise.

Another potential improvement could be to ignore lines with certain gradients (i.e. 0 is ignored). I could also ignore lines with gradients that differ from the expected average of slope, >0.5?). Although a linear model may not be the best fit, other solutions such as a quadratic equation fit could be explored. 

To counteract the jitter, the line detection could happen more actively. One aspect could be to train the dataset so that we can use machine learning to detect the lines within the masked area. There could also be two cameras which detect the lane lines and the images have to be compared and merged to avoid any potential view blocking issues. 

