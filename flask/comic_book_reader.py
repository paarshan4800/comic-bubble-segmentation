import cv2
import os
import matplotlib.pyplot as plt 




def get_contour_precedence(contour, cols):
    tolerance_factor = 200
    origin = cv2.boundingRect(contour)
    return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]


def findSpeechBubbles(image):
    
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    
    
    
    #cv2.imwrite('C:/Users/Akash/Desktop/Test_gray.jpg', imageGray)

    plt.imshow(imageGray, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])  
    plt.show()


    
    
    binary = cv2.threshold(imageGray,235,255,cv2.THRESH_BINARY)[1]
    
    contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contourMap = {}
    finalContourList = []

    contourMap = filterContoursBySize(contours)
    

    
    finalContourList = list(contourMap.values())
    finalContourList.sort(key=lambda x:get_contour_precedence(x, binary.shape[1]))

    

    pts_x=[]
    pts_y=[]

    for i in finalContourList:
        
        for j in i:
            
            pts_x.append(j[0][0])
            pts_y.append(-1*j[0][1])
    
    
    plt.scatter(pts_x, pts_y) 
    plt.show() 


    return finalContourList

def filterContoursBySize(contours):
    
    contourMap = {}

    for i in range(len(contours)):
        
        if cv2.contourArea(contours[i]) < 120000 and cv2.contourArea(contours[i]) > 4000:
            
            epsilon = 0.0025*cv2.arcLength(contours[i], True)
            approximatedContour = cv2.approxPolyDP(contours[i], epsilon, True)
            contourMap[i] = approximatedContour

    return contourMap







