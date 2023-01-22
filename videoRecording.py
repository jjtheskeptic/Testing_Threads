#How to record video: https://www.etutorialspoint.com/index.php/320-how-to-capture-a-video-in-python-opencv-and-save
# import the necessary packages
#current execute command: python3 /home/pi/Documents/Python/GitHub/VideoSample2/pi_surveillance.py


import imutils 
from imutils.video import VideoStream # must install: https://pypi.org/project/imutils/
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2
import os




# filter warnings, load the configuration
warnings.filterwarnings("ignore")
dir_path=os.path.dirname(os.path.realpath(__file__))
conf_path=os.path.join(dir_path,'conf.json')
conf=json.load(open(conf_path))  #conf = json.load(open(args["conf"]))
client = None



videoDeviceNumber=conf["videoDeviceNumber"]
filenameDateFormatString="%Y_%m_%d_%H_%M_%S"

vs=VideoStream(src=videoDeviceNumber).start()   # this works for external USB camera on new laptop: 0:internal; 2:external USB
#on the pi, deviceNumber0 works for the external USB camera
# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print("[INFO] warming up...")
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0
# capture frames from the camera
while True: #for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

#### BEGIN my comment block
	# grab the raw NumPy array representing the image and initialize
	# the timestamp and occupied/unoccupied text
	#frame_raw=vs.read() #frame = f.array
	#frame=frame_raw
	# timestamp = datetime.datetime.now()
	# text = "Unoccupied"
		

	# # resize the frame, convert it to grayscale, and blur it
	# frame = imutils.resize(frame, width=500)

	
	# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
	# # if the average frame is None, initialize it
	# if avg is None:
	# 	print("[INFO] starting background model...")
	# 	avg = gray.copy().astype("float")
	# 	#rawCapture.truncate(0)
	# 	continue
	# #qprint("[INFO] waiting for scene changes...")
	# # accumulate the weighted average between the current frame and
	# # previous frames, then compute the difference between the current
	# # frame and running average
	# cv2.accumulateWeighted(gray, avg, 0.5)
	# frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    # 	# threshold the delta image, dilate the thresholded image to fill
	# # in holes, then find contours on thresholded image
	# thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
	# 	cv2.THRESH_BINARY)[1]
	# thresh = cv2.dilate(thresh, None, iterations=2)
	# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	# 	cv2.CHAIN_APPROX_SIMPLE)
	# cnts = imutils.grab_contours(cnts)

	# # loop over the contours
	# for c in cnts:
	# 	# if the contour is too small, ignore it
	# 	if cv2.contourArea(c) < conf["min_area"]:
	# 		continue

	# 	# compute the bounding box for the contour, draw it on the frame,
	# 	# and update the text
	# 	(x, y, w, h) = cv2.boundingRect(c)
	# 	cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	# 	text = "Motion Detected"

	# # draw the text and timestamp on the frame
	# ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	# cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
	# 	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	# cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
	# 	0.35, (0, 0, 255), 1)
    #     # check to see if the room is occupied
##### END my comment block	
##### recording

	print("[INFO] - recording-"+datetime.datetime.now().strftime("%A %d %B %Y %I_%M_%S%p")) 
	# write the image to temporary file
	#t = TempImage()
	#cv2.imwrite(t.path, frame)
	try:
		captureStartTime = datetime.datetime.now()		
		startTimeString = captureStartTime.strftime("%A %d %B %Y %I_%M_%S%p")	
		
		videoFileName="/ImageFiles/"+datetime.datetime.now().strftime(filenameDateFormatString)+".avi"	
		videoFilePath="{0}{1}".format(dir_path,videoFileName)		
		# #try this: https://www.etutorialspoint.com/index.php/320-how-to-capture-a-video-in-python-opencv-and-save
		#The codec's seem to be here - not sure if needed or not: https://github.com/cisco/openh264/releases
		
		video_output=cv2.VideoWriter(videoFilePath,cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'),60, tuple(conf["resolution"]))
		servoTriggered=False
		while  ((datetime.datetime.now()-captureStartTime).seconds < conf["video_recording_seconds"]) :
			textOutputPixelY=10
			frame_raw=vs.read()
			for aCounter in range(8):	#print the objects detected to the frame											
				detectionText="aCounter:{0}".format(aCounter)
				cv2.putText(frame_raw, "{}".format(detectionText), (10,textOutputPixelY),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
				textOutputPixelY+=15
			video_output.write(frame_raw)
			
		print("[INFO] Video capture stopped: ",datetime.datetime.now().strftime("%A %d %B %Y %I_%M_%S%p"))				
	except Exception as e:
		print("[ErrNo {0}] {1}".format("error", e))


####################################################################
	# check to see if the frames should be displayed to screen
	if conf["show_video"]:
		# display the security feed
		cv2.imshow("Cat-Cam", frame_raw)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key is pressed, break from the loop
		if key == ord("q"):
			break
