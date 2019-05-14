import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from test import *
# import pyautogui
from utility import *
import numpy as np
import tensorflow as tf
from keras.models import *
from keras.layers import *
from keras.layers.advanced_activations import *
from tkinter.filedialog import askopenfilename
# from annotator import *
# from model import * 
from video_crop_and_convert_to_frames import *
from revealfunction import *
import subprocess

COVER_IMAGE_PATH='example_pics/cover_images/'
SECRET_IMAGE_PATH='example_pics/secret_images/'
CONTAINER_IMAGE_PATH='example_pics/container_images/'
COVER_VIDEO_SOURCE='hello.avi'
SECRET_VIDEO_SOURCE='videoplayback.avi'
CONTAINER_VIDEO_SOURCE='videoplayback.avi'
class App():
	
	def __init__(self, window, window_title, video_source = 0):
		# self.model = load_model('whole_model')
		# self.model = define_model()
		# self.model.load_weights('ultra_weights_coco.h5')

		self.window = window
		self.window.window_title = window_title

		self.window.attributes('-fullscreen', True)	
		# self.video_source = video_source
		self.window.configure(background="white")
		# self.frame_count = 0
		
		text = tkinter.Label(self.window, text = 'DEEP VIDEO STEGANOGRAPHY', bg = 'white', font = ('Arial', 36))
		text.place(x = 50, y = 40)
		# self.vid = MyVideoCapture(video_source)
		# self.vid2 = MyVideoCapture('hello1.avi')

		# self.VID_WIDTH = self.vid.width * 1 // 2
		# self.VID_HEIGHT = self.vid.height *1 // 2

		tkinter.Button(self.window,text="HIDE VIDEO", command=self.create_secondwindow,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=250,y=430)
		tkinter.Button(self.window,text="REVEAL VIDEO", command=self.create_thirdwindow,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=550,y=430)
		tkinter.Button(self.window,text="QUIT", command=self.window.destroy,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=1200,y=730)
		self.window.mainloop()

	def create_secondwindow(self):
		root = tkinter.Tk()
		root.attributes('-fullscreen', True)	
		# root.video_source = video_source
		root.configure(background="white")
		root.frame_count = 0
		# tool = LabelTool(root, self.model)
		# root.resizable(width =  True, height = True)
		text = tkinter.Label(root, text = 'HIDE VIDEO', bg = 'white', font = ('Arial', 36))
		text.place(x = 50, y = 40)

		self.vid = MyVideoCapture('hello.avi')
		# self.vid2 = MyVideoCapture(COVER_VIDEO_SOURCE)
		# self.vid3 = MyVideoCapture(CONTAINER_VIDEO_SOURCE)
		
		# self.VID_WIDTH = self.vid.width 
		# self.VID_HEIGHT = self.vid.height 

		self.canvas1 = tkinter.Canvas(root, width = self.vid.width *1//2, height = self.vid.height*1//2)
		self.canvas1.place(x=50,y=200)
		tkinter.Button(root,text="UPLOAD SECRET VIDEO", command=self.browse1,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=80,y=450)
		# print(COVER_VIDEO_SOURCE)

		self.canvas2 = tkinter.Canvas(root, width = self.vid.width*1//2, height = self.vid.height*1//2)
		self.canvas2.place(x=500,y=200)
		tkinter.Button(root,text="UPLOAD COVER VIDEO", command=self.browse2,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=520,y=450)
		# print(SECRET_VIDEO_SOURCE)
		self.canvas3 = tkinter.Canvas(root, width = self.vid.width*1//2, height = self.vid.height*1//2)
		self.canvas3.place(x=950,y=200)
		tkinter.Button(root,text="GET CONTAINER VIDEO", command=lambda : convert_to_frames(SECRET_VIDEO_SOURCE,COVER_VIDEO_SOURCE),bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=920,y=450)
		# play this in container section
		# CONTAINER_VIDEO_PATH=COVER_VIDEO_SOURCE.rstrip('.avi')+'_'+SECRET_VIDEO_SOURCE.rstrip('.avi')+'_container_video.avi'
		tkinter.Button(root,text="Play Videos", command=lambda: self.play_videos(),bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=520,y=550)
		
		text = tkinter.Label(root, text = 'Secret Video', bg = 'white', font = ('Arial', 14))
		text.place(x = 60, y = 150)
		
		text = tkinter.Label(root, text = 'Cover Video', bg = 'white', font = ('Arial', 14))
		text.place(x = 510, y = 150)	

		text = tkinter.Label(root, text = 'Container Video', bg = 'white', font = ('Arial', 14))
		text.place(x = 960, y = 150)
		tkinter.Button(root,text="QUIT", command=root.destroy,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=1200,y=730)
		# self.update()
		root.mainloop()
	
	def browse1(self):
		filename=askopenfilename()
		global SECRET_VIDEO_SOURCE
		SECRET_VIDEO_SOURCE=os.path.basename(filename)
	
	def browse2(self):
		filename=askopenfilename()
		global COVER_VIDEO_SOURCE
		COVER_VIDEO_SOURCE=os.path.basename(filename)

	def browse3(self):
		filename=askopenfilename()
		global CONTAINER_VIDEO_SOURCE
		CONTAINER_VIDEO_SOURCE=os.path.basename(filename)

	def create_thirdwindow(self):
		root = tkinter.Tk()
		root.attributes('-fullscreen', True)	
		# root.video_source = video_source
		root.configure(background="white")
		root.frame_count = 0
		# tool = LabelTool(root, self.model)
		# root.resizable(width =  True, height = True)
		text = tkinter.Label(root, text = 'HIDE VIDEO', bg = 'white', font = ('Arial', 36))
		text.place(x = 50, y = 40)

		self.vid = MyVideoCapture('hello.avi')
		# self.vid2 = MyVideoCapture(COVER_VIDEO_SOURCE)
		# self.vid3 = MyVideoCapture(CONTAINER_VIDEO_SOURCE)
		
		# self.VID_WIDTH = self.vid.width 
		# self.VID_HEIGHT = self.vid.height 

		self.canvas1 = tkinter.Canvas(root, width = self.vid.width*1//2, height = self.vid.height*1//2)
		self.canvas1.place(x=300,y=200)

		self.canvas2 = tkinter.Canvas(root, width = self.vid.width*1//2, height = self.vid.height*1//2)
		self.canvas2.place(x=800,y=200)

		tkinter.Button(root,text="UPLOAD CONTAINER VIDEO", command=self.browse3,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=300,y=450)
		tkinter.Button(root,text="GET SECRET VIDEO", command=lambda : revealvideo(CONTAINER_VIDEO_SOURCE),bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=800,y=450)
		tkinter.Button(root,text="Play Videos", command=lambda: self.play_videos2(),bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=520,y=550)
		# play this in revealed secret section
		# REVEALED_VIDEO_PATH="/Videos/"+COVER_VIDEO_SOURCE.rstrip(".avi")+"_"+SECRET_VIDEO_SOURCE.rstrip(".avi")+"_container_video.avi"
		global REVEALED_VIDEO_PATH
		print(REVEALED_VIDEO_PATH)
		text = tkinter.Label(root, text = 'Container Video', bg = 'white', font = ('Arial', 14))
		text.place(x = 300, y = 150)
		
		text = tkinter.Label(root, text = 'Revealed Secret Video', bg = 'white', font = ('Arial', 14))
		text.place(x = 800, y = 150)	

		# text = tkinter.Label(root, text = 'Container Video', bg = 'white', font = ('Arial', 14))
		# text.place(x = 960, y = 150)

		tkinter.Button(root	,text="QUIT", command=root.destroy,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=1200,y=730)

		root.mainloop()
	
	def play_videos(self):
		self.vid = MyVideoCapture(SECRET_VIDEO_SOURCE)
		self.vid2 = MyVideoCapture(COVER_VIDEO_SOURCE)
		self.vid3 = MyVideoCapture(ret_container_video_path())
		self.update()

	def update(self):
		ret, self.frame = self.vid.get_frame()
		ret2,self.frame2=self.vid2.get_frame()
		ret3,self.frame3=self.vid3.get_frame()
		self.vid4=MyVideoCapture('hello.avi')
		if ret or ret2 or ret3:
			if ret:				
				image = PIL.Image.fromarray(self.frame)
				image= image.resize((int(self.vid4.width//2),int(self.vid4.height//2)),PIL.Image.ANTIALIAS)
				self.photo1 = PIL.ImageTk.PhotoImage(image = image, master=self.canvas1)
				self.photo11=cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				cv2.imwrite(COVER_IMAGE_PATH+'a.jpg',self.photo11)
				self.canvas1.create_image(0, 0, image = self.photo1, anchor=tkinter.NW)
			if ret2:
				image = PIL.Image.fromarray(self.frame2)
				image= image.resize((int(self.vid4.width//2),int(self.vid4.height//2)),PIL.Image.ANTIALIAS)
				self.photo2 = PIL.ImageTk.PhotoImage(image = image, master=self.canvas2)
				self.photo21=cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)
				cv2.imwrite(SECRET_IMAGE_PATH+'b.jpg',self.photo21)
				self.canvas2.create_image(0, 0, image = self.photo2, anchor=tkinter.NW)
			if ret3:
				image = PIL.Image.fromarray(self.frame3)
				image= image.resize((int(self.vid4.width//2),int(self.vid4.height//2)),PIL.Image.ANTIALIAS)
				self.photo3 = PIL.ImageTk.PhotoImage(image = image, master=self.canvas3)
				self.photo31=cv2.cvtColor(self.frame3, cv2.COLOR_BGR2RGB)
				cv2.imwrite(SECRET_IMAGE_PATH+'b.jpg',self.photo31)
				self.canvas3.create_image(0, 0, image = self.photo3, anchor=tkinter.NW)
			
		else:	
			self.vid = MyVideoCapture(SECRET_VIDEO_SOURCE)
			self.vid2 = MyVideoCapture(COVER_VIDEO_SOURCE)
			self.vid3 = MyVideoCapture(ret_container_video_path())	
		self.window.update_idletasks()
		self.window.after_idle(self.update)

	def play_videos2(self):
		self.vid3=MyVideoCapture('hello.avi')
		self.vid = MyVideoCapture(CONTAINER_VIDEO_SOURCE)
		self.vid2 = MyVideoCapture(ret_revealed_video_path())
		self.update2()

	def update2(self):
		ret, self.frame = self.vid.get_frame()
		ret2,self.frame2=self.vid2.get_frame()
		if ret or ret2:
			if ret:				
				image = PIL.Image.fromarray(self.frame)
				# image = image.resize((image.size[0]*1//2, image.size[1]*1//2), PIL.Image.ANTIALIAS)
				image= image.resize((int(self.vid3.width//2),int(self.vid3.height//2)),PIL.Image.ANTIALIAS)
				self.photo1 = PIL.ImageTk.PhotoImage(image = image, master=self.canvas1)
				self.photo11=cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				cv2.imwrite(COVER_IMAGE_PATH+'a.jpg',self.photo11)
				self.canvas1.create_image(0, 0, image = self.photo1, anchor=tkinter.NW)
			if ret2:
				image = PIL.Image.fromarray(self.frame2)
				# image = image.resize((image.size[0]*1//2, image.size[1]*1//2), PIL.Image.ANTIALIAS)
				image= image.resize((int(self.vid3.width//2),int(self.vid3.height//2)),PIL.Image.ANTIALIAS)
				self.photo2 = PIL.ImageTk.PhotoImage(image = image, master=self.canvas2)
				self.photo21=cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)
				cv2.imwrite(SECRET_IMAGE_PATH+'b.jpg',self.photo21)
				self.canvas2.create_image(0, 0, image = self.photo2, anchor=tkinter.NW)
			
		else:	
			self.vid = MyVideoCapture(CONTAINER_VIDEO_SOURCE)
			self.vid2 = MyVideoCapture(ret_revealed_video_path())
		self.window.update_idletasks()
		self.window.after_idle(self.update2)
	
class MyVideoCapture:
	def __init__(self, video_source = 0):
		self.vid = cv2.VideoCapture(video_source)
		if not self.vid.isOpened():
			raise ValueError("Unable to open video source", video_source)

		self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

	def get_frame(self):
		if self.vid.isOpened():
			ret, frame = self.vid.read()
			# frame = frame[::2]
			if ret:
				return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
			else:
				return (ret, None)
		else:
			return (ret, None)

def __del__(self):
	if self.vid.isOpened():
		self.vid.release()
	self.window.mainloop()

# App(tkinter.Tk(), "Spine Endoscopy", '/home/sarthak/Desktop/videos/20190211103137/2018120010/ScopyVideos/1.asf')
App(tkinter.Tk(), "Video Steganography", 'hello.avi')
