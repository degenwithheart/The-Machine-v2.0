"""Image processing and utility functions"""
import cv2
import numpy as np
from PIL import Image

def resize_image(img, max_width=800):
    """Resize image maintaining aspect ratio"""
    h, w = img.shape[:2]
    if w > max_width:
        ratio = max_width / w
        img = cv2.resize(img, (max_width, int(h * ratio)))
    return img

def enhance_image(img):
    """Apply basic image enhancement"""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    enhanced = cv2.merge([l,a,b])
    return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
