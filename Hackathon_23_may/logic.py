import cv2
import numpy as np

def to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def gaussian_blur(img, ksize=5):
    ksize = max(1, ksize)
    if ksize % 2 == 0:  
        ksize += 1
    return cv2.GaussianBlur(img, (ksize, ksize), 0)

def median_blur(img, ksize=5):
    ksize = max(1, ksize)
    if ksize % 2 == 0:
        ksize += 1
    return cv2.medianBlur(img, ksize)

def sobel_edge(img):
    gray = to_grayscale(img)
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    combined = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    return combined

def canny_edge(img, low_threshold=100, high_threshold=200):
    gray = to_grayscale(img)
    edges = cv2.Canny(gray, low_threshold, high_threshold)
    return edges

def threshold_binary(img, thresh=127):
    gray = to_grayscale(img)
    _, binary = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
    return binary

def rotate_image(img, angle=0):
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))
    return rotated

def resize_image(img, scale=1.0):
    if scale <= 0:
        scale = 1.0
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    resized = cv2.resize(img, (width, height))
    return resized

def erosion(img, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    eroded = cv2.erode(img, kernel, iterations=1)
    return eroded

def dilation(img, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilated = cv2.dilate(img, kernel, iterations=1)
    return dilated

def adjust_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    v = np.clip(v, 0, 255)
    final_hsv = cv2.merge((h, s, v))
    img_bright = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img_bright

def adjust_contrast(img, alpha=1.2):
    # alpha: contrast control (1.0-3.0)
    img_contrast = cv2.convertScaleAbs(img, alpha=alpha, beta=0)
    return img_contrast

def flip_image(img, mode='horizontal'):
    if mode == 'horizontal':
        return cv2.flip(img, 1)
    elif mode == 'vertical':
        return cv2.flip(img, 0)
    else:
        return img  
