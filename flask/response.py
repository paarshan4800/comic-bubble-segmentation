from panel_extracter_final import *
from speech_bubble import *
from extract_bubble import *
from flask import Flask, request, send_file
from flask_cors import CORS
from PIL import Image

app = Flask(__name__)
cors = CORS(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/image_upload", methods=["POST"])
def image_upload():
	_input = request.files['image']
	npimg = np.fromstring(_input.read(), np.uint8)
	img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
	cv2.imwrite("userInput.png", img)
	panel_extract(img)
	
	return {"message": "Image rcvd image_upload"}


@app.route('/user-sample-images',methods=['POST'])
def user_sample_images():
	
	req=request.get_json(force=True)
	image_filename=req["filename"]
	panel_extract(cv2.imread('sample_images\\panels\\{}'.format(image_filename)))
	return {"message": "Image rcvd user-sample"}


@app.route('/segment', methods=['POST'])
def segment():
	#output\\04_08_2021_21-50-23-336467\\panel0\\panel0.png

	var="output\\04_08_2021_21-50-23-336467\\panel0\\panel0.png"
	#var=var.replace("\\panel0.png","")
	var,dir_name=extract_path(var)
	
	
	file=cv2.imread(var)

	contours,save_location = findSpeechBubbles(file,dir_name)
	croppedImageList = cropSpeechBubbles(file, contours)
	
	white_image = file.copy()
	white_image.fill(255)
	cv2.drawContours(white_image, contours, -1, (0, 255, 0), 3)
	cv2.imwrite(save_location+'Contour_in_white.png',white_image)

	cv2.drawContours(file, contours, -1, (0, 255, 0), 3)
	cv2.imwrite(save_location+'localized_bubbles.png',file)
	
	

	os.mkdir(save_location+'segmented_bubbles')

	#print("\n\n\nNUMBER OF SPEECH BUBBLES =====> ",len(croppedImageList),"\n\n")

	for img in range(len(croppedImageList)):
		cv2.imwrite(save_location+'segmented_bubbles\\'+'cropped_imgs{}.png'.format(img),croppedImageList[img])

	
		
	return {"message":"70+ percent done"}


@app.route("/fetch-sample-images/<filename>")
def fetch_sample_images(filename):
	
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
	
	return {"message": "sample images", "images": response}



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
