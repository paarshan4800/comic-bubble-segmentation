import cv2
import base64
import io
import numpy
import os
from comic_book_reader import  findSpeechBubbles
from flask import Flask, request

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

    file = request.files['image']

    if file and allowed_file(file.filename):
        npimg = numpy.fromstring(file.read(), numpy.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        
        contours = findSpeechBubbles(img)
        print("\n\n\n\n")
        cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
        #cv2.imwrite('C:/Users/Akash/Desktop/Contours.jpg', img)

        _, buffer = cv2.imencode('.jpg', img)

        return {"message":"20 percent done"}


if __name__ == '__main__':
    application.run(debug=True)