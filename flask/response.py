import cv2,time
from comic_book_reader import findSpeechBubbles
import matplotlib.pyplot as plt
import datetime
import numpy as np
from flask import Flask, request, send_file
import os
from flask_cors import CORS
from PIL import Image
import io
app = Flask(__name__)
cors = CORS(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def panel_extract(image):
	

	timestamp=datetime.datetime.now().strftime("%m_%d_%Y_%H-%M-%S-%f")



	# Load image, grayscale, blur, Otsu's threshold
	
	os.mkdir('output\\{}'.format(timestamp)) 
	original = image.copy()
	path="output\\"+timestamp
	img = image if len(image.shape) == 2 else image[:, :, 0]
	#print(len(img.shape))
	mask = np.zeros(image.shape, dtype=np.uint8)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# cv2.imshow("grayscale",gray)
	# cv2.waitKey()
	cv2.imwrite(path+r"\grayscale.png",gray)




	blur = cv2.GaussianBlur(gray, (5,5), 0)
	thresh = cv2.threshold(blur, 230, 255, cv2.THRESH_BINARY )[1]

	cv2.imwrite(path+r"\thresh.png",thresh)
	# cv2.imshow("thresh",thresh)
	# cv2.waitKey()

	cv2.rectangle(thresh, (0, 0), tuple(img.shape[::-1]), (0, 0, 0), 10)
	num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, 4, cv2.CV_32S)
	ind = np.argsort(stats[:, 4], )[::-1][1]
	panel_block_mask = ((labels == ind) * 255).astype("uint8")
	cv2.rectangle(panel_block_mask, (0, 0), tuple(panel_block_mask.shape[::-1]), (255, 255, 255), 10)
	contours, hierarchy = cv2.findContours(panel_block_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

	cv2.imwrite(path+r"\segment_panels.png",image)

	# cv2.imshow("area",image)
	# cv2.waitKey()

	panels = []


	image_number=0
	response=[]

	for i in range(len(contours)):
		area = cv2.contourArea(contours[i])

		# dimensions
		img_area = image.shape[0] * image.shape[1]


		#print(img_area,"  //  ",0.02*img_area,"  \\  ",0.9*img_area," \\ ",area)
		# if the contour is very small or very big, it's likely wrongly detected
		if area < (0.02 * img_area) or area > (0.9 * img_area):
			continue


		x, y, w, h = cv2.boundingRect(contours[i])
		# create panel mask
		panel_mask = np.ones_like(panel_block_mask, "int32")
		cv2.fillPoly(panel_mask, [contours[i].astype("int32")], color=(0, 0, 0))
		panel_mask = panel_mask[y:y+h, x:x+w].copy()
		# apply panel mask
		panel = original[y:y+h, x:x+w].copy()
		panel[panel_mask == 1] = 255
		panels.append(panel)

		# cv2.imshow("panel",panel)
		# cv2.waitKey()
		os.mkdir(path+r'\panel{}'.format(image_number))
		#cv2.imwrite(path+r'\panel{}'.format(i)+r'\panel{}.png'.format(i),panel)

		cv2.imwrite(path+r'\panel{}'.format(image_number)+r'\panel{}.png'.format(image_number),panel)

		response.append(path+r'\panel{}'.format(image_number)+r'\panel{}.png'.format(image_number))
		image_number+=1





	
	if len(panels)==0:
		print("empty list")
		panels.append(original)


		# cv2.imshow("panel",panels[0])
		# cv2.waitKey()

		cv2.imwrite(path+r'\panel'+r'\panel0.png')
	
#print("\n\nNo of panels ===== ",len(panels),"\n\n")
	print("panels extracted")
	print(response)


		

@app.route("/image_upload", methods=["POST"])
def image_upload():
	print("Hello")
	print(request.files['image'])
	_input = request.files['image']
	npimg = np.fromstring(_input.read(), np.uint8)
	img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
	cv2.imwrite("userInput.png", img)
	panel_extract(img)
	

	return {"message": "Image rcvd image_upload"}



@app.route('/user-sample-images',methods=['POST'])
def user_sample_images():
	
	req=request.get_json(force=True)
	print(req)
	image_filename=req["filename"]
	panel_extract(cv2.imread('sample_images\\panels\\{}'.format(image_filename)))
	return {"message": "Image rcvd user-sample"}





def panel_extractt11():
	for imgs in range(13):

		timestamp=datetime.datetime.now().strftime("%m_%d_%Y_%H-%M-%S-%f")



		# Load image, grayscale, blur, Otsu's threshold
		image = cv2.imread('sample_images\\panels\\{}.jpg'.format(imgs))
		os.mkdir('output\\{}'.format(timestamp)) 
		original = image.copy()
		path="output\\"+timestamp
		img = image if len(image.shape) == 2 else image[:, :, 0]
		#print(len(img.shape))
		mask = np.zeros(image.shape, dtype=np.uint8)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# cv2.imshow("grayscale",gray)
		# cv2.waitKey()
		cv2.imwrite(path+r"\grayscale.png",gray)




		blur = cv2.GaussianBlur(gray, (5,5), 0)
		thresh = cv2.threshold(blur, 230, 255, cv2.THRESH_BINARY )[1]

		cv2.imwrite(path+r"\thresh.png",thresh)
		# cv2.imshow("thresh",thresh)
		# cv2.waitKey()

		cv2.rectangle(thresh, (0, 0), tuple(img.shape[::-1]), (0, 0, 0), 10)
		num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, 4, cv2.CV_32S)
		ind = np.argsort(stats[:, 4], )[::-1][1]
		panel_block_mask = ((labels == ind) * 255).astype("uint8")
		cv2.rectangle(panel_block_mask, (0, 0), tuple(panel_block_mask.shape[::-1]), (255, 255, 255), 10)
		contours, hierarchy = cv2.findContours(panel_block_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

		cv2.imwrite(path+r"\segment_panels.png",image)

		# cv2.imshow("area",image)
		# cv2.waitKey()

		panels = []

		for i in range(len(contours)):
			area = cv2.contourArea(contours[i])

			# dimensions
			img_area = image.shape[0] * image.shape[1]


			#print(img_area,"  //  ",0.02*img_area,"  \\  ",0.9*img_area," \\ ",area)
			# if the contour is very small or very big, it's likely wrongly detected
			if area < (0.02 * img_area) or area > (0.9 * img_area):
				continue
			x, y, w, h = cv2.boundingRect(contours[i])
			# create panel mask
			panel_mask = np.ones_like(panel_block_mask, "int32")
			cv2.fillPoly(panel_mask, [contours[i].astype("int32")], color=(0, 0, 0))
			panel_mask = panel_mask[y:y+h, x:x+w].copy()
			# apply panel mask
			panel = original[y:y+h, x:x+w].copy()
			panel[panel_mask == 1] = 255
			panels.append(panel)

			# cv2.imshow("panel",panel)
			# cv2.waitKey()
			cv2.imwrite(path+r'\panel{}.png'.format(i),panel)

	

		
	if len(panels)==0:
		print("empty list")
		panels.append(original)


		# cv2.imshow("panel",panels[0])
		# cv2.waitKey()

		cv2.imwrite(path+r'\panel1.png')
		
	#print("\n\nNo of panels ===== ",len(panels),"\n\n")

	

@app.route('/segment', methods=['POST'])
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
		npimg = np.fromstring(file.read(), np.uint8)
		img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
		

		contours = findSpeechBubbles(img,timestamp)
		
		print("\n\n\n\n")
		

		return {"message":"20 percent done"}


@app.route("/fetch-sample-images/<filename>")
def fetch_sample_images(filename):
	print(filename)
	return send_file(
		'./sample_images/single/'+filename,
		mimetype='image/jpeg',
		attachment_filename='image.jpg',
		as_attachment=True
	)


@app.route("/sample-images", methods=["GET"])
def sample_images():
	sampleImages = os.listdir("./sample_images/single/")
	response = []
	for image in sampleImages:
		response.append(image)
	
	print(response)

	return {"message": "sample images", "images": response}


# @app.route("/image_upload", methods=["POST"])
# def image_upload():
# 	print("Hello")
# 	print(request.files['image'])
# 	_input = request.files['image']
# 	npimg = np.fromstring(_input.read(), np.uint8)
# 	img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
# 	cv2.imwrite("userInput.png", img)
# 	return {"message": "Image rcvd"}


@app.route("/files/output/directories", methods=["GET"])
def test():
	response = {}
	response['directories'] = []

	for directory in os.listdir("./output"):
		temp = {
			'folderName': directory,
			'files': os.listdir("./output/"+directory),
			'segmentedBubbles': os.listdir("./output/"+directory+"/segmented_bubbles")
		}

		response['directories'].append(temp)

	return {"message": "All directories", "data": response}


if __name__ == "__main__":
	app.run(debug=True)
