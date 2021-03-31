import cv2
import numpy as np

# Load image, grayscale, blur, Otsu's threshold
image = cv2.imread(r'C:\Users\HOME\Desktop\New folder\comic-book-reader\INputs\shehulk.jpg')
original = image.copy()
img = image if len(image.shape) == 2 else image[:, :, 0]
print(len(img.shape))
mask = np.zeros(image.shape, dtype=np.uint8)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blur, 230, 255, cv2.THRESH_BINARY )[1]

# cv2.imwrite("output\\thresh.png",thresh)
cv2.imshow("thresh",thresh)
cv2.waitKey()

cv2.rectangle(thresh, (0, 0), tuple(img.shape[::-1]), (0, 0, 0), 10)
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, 4, cv2.CV_32S)
ind = np.argsort(stats[:, 4], )[::-1][1]
panel_block_mask = ((labels == ind) * 255).astype("uint8")
cv2.rectangle(panel_block_mask, (0, 0), tuple(panel_block_mask.shape[::-1]), (255, 255, 255), 10)
contours, hierarchy = cv2.findContours(panel_block_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
panels = []

for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    img_area = img.shape[0] * img.shape[1]
    # if the contour is very small or very big, it's likely wrongly detected
    if area < (0.02 * img_area) or area > (0.9 * img_area):
        continue
    x, y, w, h = cv2.boundingRect(contours[i])
    # create panel mask
    panel_mask = np.ones_like(panel_block_mask, "int32")
    cv2.fillPoly(panel_mask, [contours[i].astype("int32")], color=(0, 0, 0))
    panel_mask = panel_mask[y:y+h, x:x+w].copy()
    # apply panel mask
    panel = img[y:y+h, x:x+w].copy()
    panel[panel_mask == 1] = 255
    panels.append(panel)

    cv2.imshow("panel",panel)
    cv2.waitKey()
    cv2.imwrite(r'Panels\panel{}.jpg'.format(i),panel)
print(panels)

