from __future__ import print_function
from __future__ import division
from imutils import perspective
from imutils import contours
from object_size_to_csv_fun import order_points, squared
import numpy as np
import argparse
import imutils
import cv2
from scipy.spatial import distance as dist
from PIL import Image

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-l", "--length", type=int, required=True,
	help="the length of the tank the subject resides (in mm)")
ap.add_argument("-f", "--filename", type=str, required=True,
	help="the filename of the image and the path")
args = vars(ap.parse_args())

# getting the directory of the image and then the length of the tank as pixels
tank_length_in_pixels = Image.open(args['filename']).size[0]
pixel_to_mm = args["length"] / tank_length_in_pixels
pixel_to_mm_area = squared(pixel_to_mm)

# load our input image, convert it to grayscale, and blur it slightly
image = cv2.imread(args['filename'])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# perform edge detection, then perform a dilation + erosion to
# close gaps between object edges
edged = cv2.Canny(gray, 50, 200)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
print(len(cnts))

# sort the contours from the top-to-bottom and initialize the bounding box
# point colors
if len(cnts) > 1:
	(cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")
colors = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))

# loop over the contours individually
for (i, c) in enumerate(cnts):
	# if the contour is not sufficiently large or too large, ignore it
	if cv2.contourArea(c) < 500:
		continue
	if cv2.contourArea(c) > 2000:
		continue

	area = cv2.contourArea(c) * pixel_to_mm_area
	print(area)
	# compute the rotated bounding box of the contour, then
	# draw the contours
	box = cv2.minAreaRect(c)
	box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
	box = np.array(box, dtype="int")
	cv2.drawContours(image, [box], -1, (0, 255, 255), 2)

	# show the original coordinates
	# print("Object #{}".format(i+1))
	print(box)

	# order the points in the contour such that they appear
	# in top-left, top-right, bottom-right, and bottom-left
	# order, then draw the outline of the rotated bounding
	# box
	if len(box) > 1:
		rect = order_points(box)
	else:
		continue
	(tl, tr, br, bl) = rect
	fish_length_1 = dist.euclidean(tl, tr) * pixel_to_mm
	fish_length_2 = dist.euclidean(tl, bl) * pixel_to_mm
	if fish_length_1 > fish_length_2:
		fish_length	= fish_length_1
	elif fish_length_1 <= fish_length_2:
		fish_length	= fish_length_2

	# show the re-ordered coordinates
	print(rect.astype("int"))
	print("")

	# loop over the original points and draw them
	for ((x,y), color) in zip(rect, colors):
		cv2.circle(edged, (int(x), int(y)), 5, color, -1)

	# draw the object num at the top-left corner
	cv2.putText(edged, 'Length: %.2fmm' % (fish_length),
		(int(rect[0][0] - 15), int(rect[0][1] - 15)),
		cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)


	# show the image
	cv2.imshow("Image", edged)
	cv2.waitKey(0)
