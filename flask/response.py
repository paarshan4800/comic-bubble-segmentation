#MODULES IMPORTED
import pytesseract
import os
import numpy as np
import cv2

#import functions
from panel_extraction import panel_extract
from feature_extraction import segment_panel,extract_path

#FLASK MODULES
from flask import Flask, request, send_file
from flask_cors import CORS

#Image processing
from PIL import Image





app = Flask(__name__)
cors = CORS(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


#----------------IMPORTANT CHANGE----------------
pytesseract.pytesseract.tesseract_cmd =  'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' 

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/fetch-images")
def fetch_images():
    filepath = request.args.get('filepath')
    print(filepath)
    return send_file(
        filepath,
        mimetype='image/jpeg',
        attachment_filename='image.jpg',
        as_attachment=True
    )

# Returns sample input images filepaths


@app.route("/sample-images", methods=["GET"])
def sample_images():
    sampleImages = os.listdir("./sample_images/panels/")
    response = []
    for image in sampleImages:
        response.append("sample_images/panels/" + image)

    return {"message": "sample images", "images": response}


# User uploading own image
@app.route("/image_upload", methods=["POST"])
def image_upload():
    _input = request.files['image']
    npimg = np.fromstring(_input.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    cv2.imwrite("userInput.png", img)
    panels, inputImage = panel_extract(img)

    return {"message": "Image rcvd image_upload", "inputImage": inputImage, "panels": panels}


# User selecting images from given samples
@app.route('/user-sample-images', methods=['POST'])
def user_sample_images():

    req = request.get_json(force=True)
    image_filename = req["filename"]
    print(image_filename)
    panels, inputImage = panel_extract(cv2.imread(image_filename))
    return {"message": "Image rcvd user-sample", "inputImage": inputImage, "panels": panels}


# Start segmentation process provided filepath like output\04_09_2021_14-11-47-950603\panel0\panel0.png
@app.route('/segment', methods=['POST'])
def segment():

    req = request.get_json(force=True)
    var = req["filename"]
    print(var)

    var, dir_name = extract_path(var)
    localized_bubbles,extracted_string=segment_panel(var,dir_name)

    

    return {"message": "100 percent done", "chosenPanel": var, "localized_bubbles": localized_bubbles,"extracted_string":extracted_string}


@app.route("/files/output/directories", methods=["GET"])
def test():
    response = {}
    response['directories'] = []

    # directory -> timestamp
    for directory in os.listdir("./output"):
        temp = {
            'folderName': directory,
            'files': [],
            'folders': []
        }

        # inside timestamp folder
        for item in os.listdir("./output/"+directory):
            # If file
            if "." in item:
                temp['files'].append(item)
            # If folder
            else:
                temp['folders'].append(item)

        subfolder = []

        # Inside each panel folder
        for folder in temp['folders']:
            temp_panel = {}
            temp_panel['folderName'] = folder
            temp_panel['files'] = os.listdir("./output/"+directory+"/"+folder)

            # Checking whether segmented bubbles folder has been created or not
            # It will be created if the panel has been sent to /segment
            # Otherwise it wont be created
            if "segmented_bubbles" in os.listdir("./output/"+directory+"/"+folder):
                temp_panel['segmentedBubbles'] = os.listdir(
                    "./output/"+directory+"/"+folder+"/segmented_bubbles")

            subfolder.append(temp_panel)

        temp['folders'] = subfolder

        response['directories'].append(temp)

    return {"message": "All directories", "data": response}


@app.route("/folders", methods=["POST"])
def folders():
    data = request.get_json(force=True)
    allContent = os.listdir(data["path"])

    files = []
    folders = []
    for content in allContent:
        if "." in content:
            files.append(content)
        else:
            folders.append(content)

    return {"currentDirectoryPath":data["path"],"files": files, "folders": folders}


if __name__ == "__main__":
    app.run(debug=True)
