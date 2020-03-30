import cv2
import numpy as np
from pygame import mixer

#INITIALIZATION
mixer.init()

#Played or Not
snareBool = 0
kickBool  = 0
hihatBool = 0

#Color of stick (HSV)
color1 = [17, 15, 100]
color2 = [80, 76, 220]

#Position of drum-kit
        #Bass drum
Kup, Kdown, Kright, Kleft = 280, 380, 540, 640
        #Hi-Hat
Hup, Hdown, Hright, Hleft = 140, 240, 300, 400
        #Snare Drum
Sup, Sdown, Sright, Sleft = 140, 240, 750, 850

#display drumkit
def ShowImage():
        img = cv2.imread('bass.jfif')
        img_height, img_width = 100, 100
        dsize=(100,100)
        resize=cv2.resize(img, dsize, interpolation=cv2.INTER_AREA)
            # add image to frame
        clone[ Kup:Kup+img_height , Kright:Kright+img_width ] = resize
        img = cv2.imread('hiHat.jfif')
        resize=cv2.resize(img, dsize, interpolation=cv2.INTER_AREA)
        clone[ Hup:Hup+img_height , Hright:Hright+img_width ] = resize
        img = cv2.imread('snare.jpg')
        resize=cv2.resize(img, dsize, interpolation=cv2.INTER_AREA)
        clone[ Sup:Sup+img_height , Sright:Sright+img_width ] = resize

        
def Contours(image):
	img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresholded = cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)[1]
	cnts = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
	return len(cnts)

#Play Drum-kit    
def playKick():
	mixer.music.load('kick.mp3')
	mixer.music.play()

def playHihat():
	mixer.music.load('hihat.mp3')
	mixer.music.play()

def playSnare():
	mixer.music.load('snare.mp3')
	mixer.music.play()

#Main Funtion	
if __name__ == "__main__":
        #input
        #Camera initialization
	cam = cv2.VideoCapture(0)
	cam.set(3, 1280)
	cam.set(4, 720)
	cam.set(cv2.CAP_PROP_FPS, 60)
	while True:
		status, frame = cam.read()

		# take a clone 
		clone = frame.copy()
		clone = cv2.flip(clone, 1)
		clone = cv2.resize(clone, (1280,720))

		# drum regions
		reg_kick  = clone[Kup:Kdown, Kright:Kleft]
		reg_hihat = clone[Hup:Hdown, Hright:Hleft]
		reg_snare = clone[Sup:Sdown, Sright:Sleft]

		# blur the regions
		reg_kick  = cv2.GaussianBlur(reg_kick,  (7, 7), 0)
		reg_hihat = cv2.GaussianBlur(reg_hihat, (7, 7), 0)
		reg_snare = cv2.GaussianBlur(reg_snare, (7, 7), 0)
                
		c1 = np.array(color1, dtype="uint8")
		c2 = np.array(color2, dtype="uint8")

		mask_kick  = cv2.inRange(reg_kick,  c1, c2)
		mask_hihat = cv2.inRange(reg_hihat, c1, c2)
		mask_snare = cv2.inRange(reg_snare, c1, c2)
		
		out_kick   = cv2.bitwise_and(reg_kick,  reg_kick,  mask=mask_kick)
		out_hihat  = cv2.bitwise_and(reg_hihat, reg_hihat, mask=mask_hihat)
		out_snare  = cv2.bitwise_and(reg_snare, reg_snare, mask=mask_snare)

		cnts_kick  = Contours(out_kick)
		cnts_hihat = Contours(out_hihat)
		cnts_snare = Contours(out_snare)

		if (cnts_kick > 0) and (kickBool == 0):
			playKick()
			kickBool = 1
		elif (cnts_kick == 0):
			kickBool = 0

		if (cnts_hihat > 0) and (hihatBool == 0):
			playHihat()
			hihatBool = 1
		elif (cnts_hihat == 0):
			hihatBool = 0	

		if (cnts_snare > 0) and (snareBool == 0):
			playSnare()
			snareBool = 1
		elif (cnts_snare == 0):
			snareBool = 0
		ShowImage()
		cv2.imshow("AIR DRUM", clone)

		#press '*' to close the program
		if cv2.waitKey(1) & 0XFF == ord('*'):
			break
	cam.release()
	cv2.destroyAllWindows()
