import cv2
import base64
import io
import numpy
import os
from comic_book_reader import  findSpeechBubbles
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
	if 'image' not in request.files or not request.files['image']:
		return 'No file sent', 400

	#print()
	timestamp=str(datetime.datetime.now()).replace(' ','_')
	timestamp=timestamp.replace(':','_')
	print(timestamp)
	

	# set path here
	os.mkdir('C:\\Users\\Akash\\Desktop\\ops\\{}'.format(timestamp)) 



	file = request.files['image']

	if file and allowed_file(file.filename):
		npimg = numpy.fromstring(file.read(), numpy.uint8)
		img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
		

		contours = findSpeechBubbles(img,timestamp)

		

		
		print("\n\n\n\n")
		

		return {"message":"20 percent done"}


if __name__ == '__main__':
	application.run(debug=True)