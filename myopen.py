import argparse
import datetime
import imutils
import time
import cv2
camera = cv2.VideoCapture(0)
min_Area = 60000
firstFrame = None
time.sleep(1)
j = 5
while True:
	grabbed,frame = camera.read()
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (23,23), 0)
	if firstFrame is None:
		firstFrame = gray
		continue
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	(_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	max_Area = 0
	ci = None
	for c in cnts:
		if cv2.contourArea(c) < min_Area:
			continue
		if cv2.contourArea(c) > max_Area:
			max_Area = cv2.contourArea(c)
			ci = c
 		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	if(max_Area>60000 and max_Area<70000):
		if(j<5):
			j +=1
			print j
			continue
		j=0
		print "calling for next song"
	else:
		if(j<5):
			print j
			j +=1
	if(max_Area >= 100000):
		firstFrame = None
		frame = None
		thresh = None
		print "initializing again"
		continue
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
camera.release()
cv2.destroyAllWindows()
