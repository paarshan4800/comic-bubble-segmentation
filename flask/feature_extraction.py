import cv2
from matplotlib import pyplot as plt
from speech_bubble_localization import cropSpeechBubbles,findSpeechBubbles
import os


def segment_panel(var,dir_name):

    #var= filename dir_name=directory name of selected panel
    file = cv2.imread(var)
    var = var.replace("\\", "\\\\")
    dir_name = dir_name.replace("\\", "\\\\")
    
    #finds the position of speech bubbles, returns the plotted outline
    contours, save_location = findSpeechBubbles(file, dir_name)
    
    #crops and return the speech bubbles 
    croppedImageList,extracted_string = cropSpeechBubbles(save_location,file, contours)

    #create white image to show outline of bubble
    white_image = file.copy()
    white_image.fill(255)
    cv2.drawContours(white_image, contours, -1, (0, 255, 0), 3)
    cv2.imwrite(save_location+'Contour_in_white.png', white_image)

    #localized bubbles
    cv2.drawContours(file, contours, -1, (0, 255, 0), 3)
    localized_bubbles = save_location+'localized_bubbles.png'
    cv2.imwrite(localized_bubbles, file)


    os.mkdir(save_location+'segmented_bubbles')

    #print("\n\n\nNUMBER OF SPEECH BUBBLES =====> ",len(croppedImageList),"\n\n")

    #save the obtained cropped speech bubbles
    for img in range(len(croppedImageList)):
        cv2.imwrite(save_location+'segmented_bubbles\\' +
                    'cropped_imgs{}.png'.format(img), croppedImageList[img])

    return localized_bubbles,extracted_string

def extract_path(var):
	var=var[::-1]

	dir_name=""
	flag=False
	_in=0
	for character in var:
		if  not flag:

			if character!='\\':
				continue
			else:
				flag=True
		else:
			dir_name+=character
	dir_name=dir_name[::-1]
	
	var=var[::-1]
	return var,dir_name

