import cv2
from text_extraction import shrinkByPixels, tesseract


def cropSpeechBubbles(save_location,image, contours, padding = 0):
	
	croppedImageList = []
	for contour in contours:
		rect = cv2.boundingRect(contour)
		[x, y, w, h] = rect
		croppedImage = image[y-padding:y+h+padding, x-padding:x+w+padding]
		croppedImageList.append(croppedImage)

	# TESSERACT OCR MODULE#
	junk,extracted_text=parseComicSpeechBubbles(croppedImageList)

	#text file that stores extracted text
	f= open(save_location+'extracted_text.txt',"w+")
	extracted_string="".join(extracted_text)
	f.write(extracted_string+'\n')
	f.close()

	#writing junk values
	junkfile= open(save_location+'junk_detected.txt',"w+")
	junk_string="".join(junk)
	junkfile.write(junk+'\n')
	junkfile.close()

	
	
	#return the cropped image and extracted text
	return croppedImageList,extracted_string

def parseComicSpeechBubbles(croppedImageList, shouldShowImage = True):
	scriptList = []

	for it,croppedImage in enumerate(croppedImageList):
		
		# Enlarge cropped image
		croppedImage = cv2.resize(croppedImage, (0,0), fx = 2, fy = 2)
		# # Denoise
		croppedImage = cv2.fastNlMeansDenoisingColored(croppedImage, None, 10, 10, 7, 15)

		if shouldShowImage:
			pass
			#cv2.imwrite("denoise/croppedImage{}.png".format(it),croppedImage)

		# Pass cropped image to the ocr engine
		junk,script = tesseract(croppedImage)

		
		
		# If we don't find any characters, try shrinking the cropped area. 
		#This occasionally helps tesseract recognize single word lines, but increases processing time. 
		# We omly shrink once and try to detect new text
		count = 0
		while (script == '' and count < 1):
			count+=1
			croppedImage = shrinkByPixels(croppedImage, 5)
			#cv2.imwrite("denoise/croppedImageSHRUNK{}_{}.png".format(it,count),croppedImage)
			junk,script = tesseract(croppedImage)

		if script != '' and script not in scriptList:
			scriptList.append(script)

	return junk,scriptList

