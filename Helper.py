import math
import cv2
import numpy as np

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[0, 0, 255], thickness=5):
    """
    Original provided code:    
    This function draws `lines` with `color` and `thickness`.  
    This function draws `lines` with `color` and `thickness`.    
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)
    """
    """
    Edited code below
    HoughLinesP output is line segments, where all you have is two points on the line

    Need to either average the lines if there are many dashes detected for the lane
    Or extrapolate them if there are some partially detected lines
    Can ignore the vertical line (denominator in slope 0)
    using a linear model (y=mx+c), use the direction of slope to determine which side the line is from
    Left Lane: Potitive gradient  - As the values of column co-ordinate increases, the values of rows co-ordinate decreases. 
    Right Lane: Negative gradient - As the values of column co-ordinate increases, the values of rows co-ordinate increases. 
    Technically they should give roughly the same gradient, with one being negative (for straight lines, not corners)
        
    Have detected two left lanes and two right lanes (either side of the lane)
    Will construct a global left and right lane
    Use use the y intercept to extrapolate the line to the edge pixel

     """

    imshape = img.shape
    
    #Global variables y-axis coordinates -- for extrapolating
    #shape attribute for numpy arrays returns the dimensions of the array. 
    #So .shape[0] is n rows, first dimension of your array.
    global_ymin = img.shape[0]
    global_ymax = img.shape[0]

    # right lane line variables
    #Creating empty lists
    global_right_grad = []
    global_right_y = []
    global_right_x = []
    
    # left lane line variables
    #Creating empty lists
    global_left_grad = []
    global_left_y = []
    global_left_x = []
    
    #HoughLinesP output gives two points on the line
    #So coordinates we have are x1,y1 and x2, y2
    for line in lines:
        for x1,y1,x2,y2 in line:
            gradient, intercept = np.polyfit((x1,x2), (y1,y2), 1)
            global_ymin = min(min(y1, y2), global_ymin)
            
            #Separating the coordinates to their left and right lanes
            #Left Lane: Potitive gradient
            if (gradient > 0):
                global_left_grad += [gradient]
                global_left_y += [y1, y2]
                global_left_x += [x1, x2]
            #Right Lane: Negative gradient
            else:
                global_right_grad += [gradient]
                global_right_y += [y1, y2]
                global_right_x += [x1, x2]
    
    # if no valid line exists,return without further operations
    if len(global_left_grad) == 0 or len(global_right_grad) == 0:
        print("No valid lines are detected")
        return
    
    #Creating the global left lane with the average of the points
    left_mean_grad = np.mean(global_left_grad)
    left_y_mean = np.mean(global_left_y)
    left_x_mean = np.mean(global_left_x)
    
    #Calculating the yintercepts
    #Using the linear model y = mx+c 
    left_intercept = left_y_mean - (left_mean_grad * left_x_mean)
    
    #Creating the global right lane with the average of the points
    right_mean_grad = np.mean(global_right_grad)
    right_y_mean = np.mean(global_right_y)
    right_x_mean = np.mean(global_right_x)
    
    #Calculating the yintercepts
    right_intercept = right_y_mean - (right_mean_grad * right_x_mean)
    
    #Checking if there are points in each variable 
    #Finding the top and bottom points
    if ((len(global_left_grad) > 0) and (len(global_right_grad) > 0)):
        upper_left_x = int((global_ymin - left_intercept) / left_mean_grad)
        lower_left_x = int((global_ymax - left_intercept) / left_mean_grad)
        upper_right_x = int((global_ymin - right_intercept) / right_mean_grad)
        lower_right_x = int((global_ymax - right_intercept) / right_mean_grad)
        
        #Drawing the left and right lines using top and bottom points
        cv2.line(img, (upper_left_x, global_ymin), (lower_left_x, global_ymax), color, thickness)
        cv2.line(img, (upper_right_x, global_ymin), (lower_right_x, global_ymax), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)