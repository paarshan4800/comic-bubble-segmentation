import cv2
import time
import os
import matplotlib.pyplot as plt
import numpy as np
import datetime


def panel_extract(image):

    timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%H-%M-%S-%f")

    # Load image, grayscale, blur, Otsu's threshold

    os.mkdir(r'output\\{}'.format(timestamp))
    original = image.copy()
    path = r'output\\'+timestamp

    # Store original input image with multiple panels
    cv2.imwrite(path+r'\\original_input.png', image)

    img = image if len(image.shape) == 2 else image[:, :, 0]
    # print(len(img.shape))
    mask = np.zeros(image.shape, dtype=np.uint8)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(path+r"\\grayscale.png", gray)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 230, 255, cv2.THRESH_BINARY)[1]

    cv2.imwrite(path+r"\thresh.png", thresh)
    # cv2.imshow("thresh",thresh)
    # cv2.waitKey()

    cv2.rectangle(thresh, (0, 0), tuple(img.shape[::-1]), (0, 0, 0), 10)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        thresh, 4, cv2.CV_32S)
    ind = np.argsort(stats[:, 4], )[::-1][1]
    panel_block_mask = ((labels == ind) * 255).astype("uint8")
    cv2.rectangle(panel_block_mask, (0, 0), tuple(
        panel_block_mask.shape[::-1]), (255, 255, 255), 10)
    contours, hierarchy = cv2.findContours(
        panel_block_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

    cv2.imwrite(path+r"\\segment_panels.png", image)

    panels = []

    image_number = 0
    response = []

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
        cv2.fillPoly(
            panel_mask, [contours[i].astype("int32")], color=(0, 0, 0))
        panel_mask = panel_mask[y:y+h, x:x+w].copy()
        # apply panel mask
        panel = original[y:y+h, x:x+w].copy()
        panel[panel_mask == 1] = 255
        panels.append(panel)

        os.mkdir(path+r'\\panel{}'.format(image_number))

        cv2.imwrite(path+r'\\panel{}'.format(image_number) +
                    r'\\panel{}.png'.format(image_number), panel)

        response.append(path+r'\\panel{}'.format(image_number) +
                        r'\\panel{}.png'.format(image_number))
        image_number += 1

    if len(panels) == 0:
        print("empty list")
        panels.append(original)
        os.mkdir(path+r'\\panel{}'.format(image_number))
        print("created panel")

        # cv2.imshow("panel",panels[0])
        # cv2.waitKey()

        cv2.imwrite(path+r'\\panel0'+r'\\panel0.png',panels[0])
        response.append(path+r'\\panel{}'.format(image_number) +
                        r'\\panel{}.png'.format(image_number))

    inputImage = path+r'\\original_input.png'
    return response, inputImage

#print("\n\nNo of panels ===== ",len(panels),"\n\n")
    # print("panels extracted")
    # print(response)
