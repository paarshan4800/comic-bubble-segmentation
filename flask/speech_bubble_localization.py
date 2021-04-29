import cv2,time,io
import os
import matplotlib.pyplot as plt 
import numpy as np
import datetime
from speech_bubble_extraction import cropSpeechBubbles



def get_contour_precedence(contour, cols):
	tolerance_factor = 200
	origin = cv2.boundingRect(contour)
	return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]


def findSpeechBubbles(image,path):

	save_location=path+"\\\\"
	
	printlist=[] 

	cv2.imwrite(save_location+'input_img.png',image)

	#convert image to grayscale
	imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cv2.imwrite(save_location+'gray_img.png',imageGray)
  
	#threshold image
	binary = cv2.threshold(imageGray,235,255,cv2.THRESH_BINARY)[1]
	cv2.imwrite(save_location+'binary_thresh.png',binary)
	
	#binary threshold image 
	binary_inv= cv2.threshold(imageGray,235,255,cv2.THRESH_BINARY_INV)[1]
	cv2.imwrite(save_location+'binary_inv.png',binary_inv)
	
	#obtain contours and heirarchy
	contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	#initialize contourmap and finalContourList
	contourMap = {}
	finalContourList = []
	contourMap = filterContoursBySize(contours)
	contourMap=filterContainingContours(contourMap, hierarchy)


	#convert finalContourList into list
	finalContourList = list(contourMap.values())

	#sort the contour list based on condition
	finalContourList.sort(key=lambda x:get_contour_precedence(x, binary.shape[1]))

	#save x and y co-ordinates 
	pts_x=[]
	pts_y=[]
	
   
	for i in finalContourList:
		for j in i:
			
			printlist.append('('+str(j[0][0])+','+str(j[0][1])+')')
			pts_x.append(j[0][0])
			pts_y.append(-1*j[0][1])
			
				
	
	plt.scatter(pts_x,pts_y)
	plt.savefig(save_location+'contour.png')
	plt.clf()
	
	

	it=0
	f= open(save_location+'contour_list_coords.txt',"w+")
	str_to_write=''
	for r in printlist:
		it+=1
		str_to_write+=r
		if it%10==0:
			f.write(str_to_write+'\n')
			str_to_write=''
	
	f.write(str_to_write+'\n')
			
	return finalContourList,save_location




def filterContoursBySize(contours):
	contourMap = {}
	for i in range(len(contours)):
		# Filter out speech bubble candidates with unreasonable size
		if cv2.contourArea(contours[i]) < 120000 and cv2.contourArea(contours[i]) > 4000:
			# Smooth out contours that were found
			epsilon = 0.0025*cv2.arcLength(contours[i], True)
			approximatedContour = cv2.approxPolyDP(contours[i], epsilon, True)
			contourMap[i] = approximatedContour
	return contourMap

def filterContainingContours(contourMap, hierarchy):
	
	for i in list(contourMap.keys()):
		currentIndex = i
		while hierarchy[0][currentIndex][3] > 0:
			if hierarchy[0][currentIndex][3] in contourMap.keys():
				contourMap.pop(hierarchy[0][currentIndex][3])
			currentIndex = hierarchy[0][currentIndex][3]

	
	return contourMap