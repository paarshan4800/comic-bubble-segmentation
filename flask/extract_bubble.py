import cv2,time
import os
import matplotlib.pyplot as plt 
import numpy as np
import datetime

def cropSpeechBubbles(image, contours, padding = 0):
	croppedImageList = []
	for contour in contours:
		rect = cv2.boundingRect(contour)
		[x, y, w, h] = rect
		croppedImage = image[y-padding:y+h+padding, x-padding:x+w+padding]
		croppedImageList.append(croppedImage)

    
	return croppedImageList