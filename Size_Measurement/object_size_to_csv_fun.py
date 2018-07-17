from __future__ import print_function
from __future__ import division
from imutils import perspective
from imutils import contours
import imutils
import numpy as np
import cv2
from scipy.spatial import distance as dist
from PIL import Image
import glob


def order_points(pts):
	# sort the points based on their x-coordinates
	xSorted = pts[np.argsort(pts[:, 0]), :] # 0 indicates sorting based on x-coordinate

	# grab the left-most and right-most points from the sorted
	# x--coordinate points
	leftMost = xSorted[:2, :]
	rightMost = xSorted[2:, :]

	# now, sort the left-most coordinates according to their
	# y-coordinates so we can grab the top-left and bottom-left
	# points, respectively
	leftMost = leftMost[np.argsort(leftMost[:, 1]), :] # 1 indicates sorting based on y-coordinate
	(tl, bl) = leftMost

	# now that we have the top-left coordiante, use it as an
	# anchor to calculate the Euclidian distance between the
	# top-left and right-most points; by the Pythagorean
	# theorem, the point with the largest distance will be
	# our bottom-right point
	# np.newaxis increases the dimension of an existing array by one more dimension
	D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0] 
	(br, tr) = rightMost[np.argsort(D)[::-1], :]

	# return the coordinates in the top-left, top-right,
	# bottom-right, and bottom-left order
	return np.array([tl, tr, br, bl], dtype = "float32")

def squared(x):
	return x*x

def measure_object_size(path):
	# get the reference point of the image
	tank_length_in_pixels = Image.open(path).size[0]
	pixel_to_mm = args["length"] / tank_length_in_pixels
	pixel_to_mm_area = squared(pixel_to_mm)

	# load our input image, convert it to grayscale, and blur it slightly
	image = cv2.imread(path)
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

	# sort the contours from the top-to-bottom and initialize the bounding box
	# point colors
	(cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")
	colors = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))

	# loop over the contours individually
	lst = []
	area = []
	for (i, c) in enumerate(cnts):
		# if the contour is not sufficiently large or too large, ignore it
		if cv2.contourArea(c) < 500:
			continue
		elif cv2.contourArea(c) > 2000:
			continue

		# store the area
		area.append(cv2.contourArea(c) * pixel_to_mm_area)
		# compute the rotated bounding box of the contour, then
		# draw the contours
		box = cv2.minAreaRect(c)
		box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
		box = np.array(box, dtype="int")
		cv2.drawContours(image, [box], -1, (0, 255, 255), 2)

		# order the points in the contour such that they appear
		# in top-left, top-right, bottom-right, and bottom-left
		# order, then draw the outline of the rotated bounding box
		rect = order_points(box)
		(tl, tr, br, bl) = rect
		fish_length_1 = dist.euclidean(tl, tr) * pixel_to_mm
		fish_length_2 = dist.euclidean(tl, bl) * pixel_to_mm
		if fish_length_1 > fish_length_2:
			fish_length	= fish_length_1
		elif fish_length_1 <= fish_length_2:
			fish_length	= fish_length_2
		lst.append(fish_length)
		if fish_length > 30:
			del lst[-1]
		if fish_length < 10:
			del lst[-1]
		
	return lst, area
