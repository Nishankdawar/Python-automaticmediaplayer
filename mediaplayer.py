import os,time
import pygame
import imutils
import cv2,numpy
from pydub import AudioSegment

camera = cv2.VideoCapture(0)
min_Area = 60000
firstFrame = None
j = 5
pygame.mixer.init()

def get_filepaths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths 
def play_song(directory):
	pygame.mixer.music.load(directory)
	pygame.mixer.music.play()
# def play(i,n):
# 	if(i==n):
# 		i=0
# 	play_song(files_to_play[i])
# 	while pygame.mixer.music.get_busy() == True:
# 		ret,img = cap.read()
# 		cv2.imshow('',img)
# 		k = cv2.waitKey(10)
# 		if(k == 83):
# 			i += 1
# 			if(i==n):
# 				i = 0
# 			play(i,n)
# 		if(k == 81):
# 			i -= 1
# 			if(i<0):
# 				i = n-1
# 			play(i,n)
# 		continue
# 	play(i+1,n)
full_file_paths = get_filepaths("/home/kidminks/myfun/music")
n = 1
f = []
files_to_change = []
for f in full_file_paths:
  if f.endswith(".mp3"):
    files_to_change.append(f)
    print f
for f in full_file_paths:
	if f.endswith(".wav"):
		n += 1
		print f
for f in files_to_change:
	song = AudioSegment.from_mp3(f)
	song.export("/home/kidminks/myfun/music/wav/{}.wav".format(n), format="wav")
	os.remove(f)
	n += 1

full_file_paths = get_filepaths("/home/kidminks/myfun/music/wav")
files_to_play = []
for f in full_file_paths:
	if f.endswith(".wav"):
		files_to_play.append(f)
		print f
n = len(files_to_play)
i = 0
# play(i,n)
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
 	# 	(x, y, w, h) = cv2.boundingRect(c)
		# cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	if(max_Area >= 100000):
		firstFrame = None
		frame = None
		thresh = None
		print "initializing again"
		continue
	if(max_Area>60000 and max_Area<70000):
		if(j<5):
			j +=1
			print j
			continue
		j=0
		print "calling for next song"
		if(i==n):
			i=0
		play_song(files_to_play[i])
		i += 1
	else:
		if(j<5):
			print j
			j +=1
	if pygame.mixer.music.get_busy() == False:
		if(i==n):
			i=0
		play_song(files_to_play[i])
		i +=1
		continue
	# cv2.imshow("Real", frame)
	# cv2.imshow("Thresh", thresh)
	# cv2.imshow("Difference", frameDelta)
	# key = cv2.waitKey(1) & 0xFF
	# if key == ord("q"):
	# 	break
camera.release()
cv2.destroyAllWindows()