import cv2
import base64
import io
import numpy
import os
from comic_book_reader import  findSpeechBubbles,segmentPage
from flask import Flask, request
import matplotlib.pyplot as plt #modded
import datetime
import pathlib




application = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/segment', methods=['POST'])
def segment():
	# Check if an image was sent with the POST request
	# if 'image' not in request.files or not request.files['image']:
	# 	return 'No file sent', 400

	inputs=request.files.getlist('image0')
	it=0

	for _input in inputs:

		npimg = numpy.fromstring(_input.read(), numpy.uint8)
		img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

		

		
		

		
		timestamp=str(datetime.datetime.now()).replace(' ','_')
		timestamp=timestamp.replace(':','_')
		#print(timestamp)
		

		
		os.mkdir('output\\{}'.format(timestamp)) 

		

		

		
			
		croppedImageList = segmentPage(img,timestamp)

		it+=1
			
			
		
	return {"message":"50 percent done"}


if __name__ == '__main__':

	
	application.run(debug=True)