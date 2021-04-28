import cv2,time
import os
import matplotlib.pyplot as plt 
import numpy as np
import datetime
import pytesseract
import enchant
from speech_bubble import *
import re
from autocorrect import Speller


d = enchant.Dict("en_US")
spell = Speller(lang='en')


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

	
	
	
	return croppedImageList,extracted_string


def shrinkByPixels(im, pixels):
	h = im.shape[0]
	w = im.shape[1] 
	return im[pixels:h-pixels, pixels:w-pixels]

# Adjust the gamma in an image by some factor
def adjust_gamma(image, gamma=1.0):
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
	return cv2.LUT(image, table)



#uncomment the next block for 100 percent

def processScript(script):
	

	# Tesseract sometimes picks up 'I' chars as '|'
	script = script.replace('|','I')
	# We want new lines to be spaces so we can treat each speech bubble as one line of text
	script = script.replace('\n',' ')
	# Remove multiple spaces from our string
	words = script.split()
	script = ' '.join(words)

	for char in script:
		# Comic books tend to be written in upper case, so we remove anything other than upper case chars
		if char not in ' -QWERTYUIOPASDFGHJKLZXCVBNM,.?!""\'’1234567890':
			script = script.replace(char,'')

	# This line removes "- " and concatenates words split on two lines
	
	script = re.sub(r"(?<!-)- ", "", script)
	words = script.split()
	for i in range(0, len(words)):
		# Spellcheck all words
		if not d.check(words[i]):
			alphaWord = ''.join([j for j in words[i] if j.isalpha()])
			if alphaWord and not d.check(alphaWord):
				words[i]=spell(words[i].lower()).upper()
		# Remove single chars other than 'I' and 'A'
		if len(words[i]) == 1:
			if (words[i] != 'I' and words[i] != 'A'):
				words[i] = ''

	# Remove any duplicated spaces
	script = ' '.join(words)
	words = script.split()
	final = ' '.join(words)

	# Remove all two char lines other than 'NO' and 'OK'
	if len(final) == 2 and script != "NO" and script != "OK":
		return ''

	return final

# Apply the ocr engine to the given image and return the recognized script where illegitimate characters are filtered out
def tesseract(image):
	
	script = pytesseract.image_to_string(image, lang = 'eng')
	junk=script
			
	corrected_text= processScript(script)
	junklist=""
	hash_map={}
	for i in corrected_text:
		if i not in hash_map.keys():
			hash_map[i]=1
		else:
			hash_map[i]+=1
	for i in junk:
		if i not in hash_map.keys():
			junklist+=i

	return junklist,corrected_text+"\n"




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
		#  This occasionally helps tesseract recognize single word lines, but increases processing time.
		count = 0
		while (script == '' and count < 3):
			count+=1
			croppedImage = shrinkByPixels(croppedImage, 5)
			#cv2.imwrite("denoise/croppedImageSHRUNK{}_{}.png".format(it,count),croppedImage)
			junk,script = tesseract(croppedImage)

		if script != '' and script not in scriptList:
			scriptList.append(script)

	return junk,scriptList

