#made by Strauji
import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import threading
import time
name = "Screen recorder" #Change that to your recording name
resolution = pyautogui.size()
codec =cv2.VideoWriter_fourcc(*'XVID')
filename = name+".avi" #XVID is for .avi, there are other codecs documented by the OpenCV
fps = 10.0 
out = cv2.VideoWriter(filename, codec, fps, resolution)
preview_screen_size = (480, 270) 
cv2.namedWindow(name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(name, preview_screen_size[0], preview_screen_size[1])
frames = []
still_recording = False
class video_writer(threading.Thread): #The idea here is simple, we'll create a pool of frames in the main thread, and then write it off to disk here
    def run(self):
        while (len(frames) > 0 or still_recording):
            if(len(frames) >0): #I know it seems redundant, but sometimes, at the very end, the writer will run out of frames before the main thread signals the recording is over, and then will throw an exception
                out.write(frames[0]) #write the first element, a frame, to the disk
                frames.pop(0) #remove the first element that was just recorded
        out.release()#gravation is over, so release the writer
thread = video_writer() 
still_recording = True #Signals the writer that you are still writing frames
thread.start()
while True:
        still_recording = True
        img = ImageGrab.grab(bbox=(0,0,resolution[0],resolution[1]))
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #This will convert the frame from BGR to RGB, it's kinda optional tbh, but i recommend keeping it like that
        frames.append(frame)
        cv2.imshow(name, frame) #This will update the preview screen with the recorded frame
        if cv2.waitKey(1) == ord('q'):
            still_recording = False #Signals to the writer thread that the recording is over
            break
cv2.destroyAllWindows() #Close the preview window
