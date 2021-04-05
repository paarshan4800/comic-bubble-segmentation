import cv2
import datetime
import os
import numpy as np

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
        
    print("\n\nNo of panels :===== ",len(panels),"\n\n")
