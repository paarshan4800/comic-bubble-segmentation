import enchant
from autocorrect import Speller
import cv2
import numpy as np
import re
import pytesseract

d = enchant.Dict("en_US")
spell = Speller(lang='en')


def shrinkByPixels(im, pixels):
	h = im.shape[0]
	w = im.shape[1] 
	return im[pixels:h-pixels, pixels:w-pixels]

# Adjust the gamma in an image by some factor
def adjust_gamma(image, gamma=1.0):
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
	return cv2.LUT(image, table)




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