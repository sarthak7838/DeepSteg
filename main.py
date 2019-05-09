import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from test import *
import pyautogui
from utility import *
import numpy as np
import tensorflow as tf
from keras.models import *
from keras.layers import *
from keras.layers.advanced_activations import *
from tkinter.filedialog import askopenfilename
from annotator import *
# from model import * 
from video_crop_and_convert_to_frames import *
import subprocess

COVER_IMAGE_PATH='example_pics/cover_images/'
SECRET_IMAGE_PATH='example_pics/secret_images/'
CONTAINER_IMAGE_PATH='example_pics/container_images/'
COVER_VIDEO_SOURCE='videoplayback.mp4'
SECRET_VIDEO_SOURCE='hello.mp4'
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
		# self.vid2 = MyVideoCapture('hello1.mp4')

		# self.VID_WIDTH = self.vid.width * 1 // 2
		# self.VID_HEIGHT = self.vid.height *1 // 2

		# self.canvas1 = tkinter.Canvas(window, width = self.vid.width *1//2, height = self.vid.height*1//2)
		# self.canvas1.place(x=50,y=150)

		# self.canvas2 = tkinter.Canvas(window, width = self.vid.width*1//2, height = self.vid.height*1//2)
		# self.canvas2.place(x=500,y=150)

		# self.canvas3 = tkinter.Canvas(window, width = self.vid.width*1//2, height = self.vid.height*1//2)
		# self.canvas3.place(x=950,y=150)

		# text = tkinter.Label(self.window, text = 'Secret Video', bg = 'white', font = ('Arial', 14))
		# text.place(x = 60, y = 150)
		
		# text = tkinter.Label(self.window, text = 'Cover Video', bg = 'white', font = ('Arial', 14))
		# text.place(x = 510, y = 150)	

		# text = tkinter.Label(self.window, text = 'Container Video', bg = 'white', font = ('Arial', 14))
		# text.place(x = 960, y = 150)
		
		# color_list = {0:(255,0,0),1:(0,255,0),2:(0,0,255),3:(255,255,0),4:(255,0,127),5:(160,160,160),6:(0,0,0),7:(255,255,255),8:(51,0,0)}

		# text = tkinter.Label(self.window, text = 'F - Fat epidural', bg = 'white', fg='red', font = ('Arial', 14))
		# text.place(x = 80, y = 640)		
		# text = tkinter.Label(self.window, text = 'A - Annulus', bg = 'white',fg='green', font = ('Arial', 14))
		# text.place(x = 80, y = 670)		
		# text = tkinter.Label(self.window, text = 'E - Endplate', bg = 'white',fg='blue', font = ('Arial', 14))
		# text.place(x = 80, y = 700)		

				
		# text = tkinter.Label(self.window, text = 'O - Opening in the Disc', fg='#FF007F',bg = 'white', font = ('Arial', 14))
		# text.place(x = 480, y = 640)		
		# text = tkinter.Label(self.window, text = 'N - Nerve after cutting annulus', fg='#A0A0A0',bg = 'white', font = ('Arial', 14))
		# text.place(x = 480, y = 670)		

		# text = tkinter.Label(self.window, text = 'B - Bone of Facet', bg = 'white', fg='black', font = ('Arial', 14))
		# text.place(x = 480, y = 700)		
		# text = tkinter.Label(self.window, text = 'D - Disc material to be removed ', fg='#00FFFF',bg = 'white', font = ('Arial', 14))
		# text.place(x =880, y = 640)		
		# text = tkinter.Label(self.window, text = 'I - Instrument', bg = 'white', fg='brown', font = ('Arial', 14))
		# text.place(x = 880, y = 670)

		# self.warning = tkinter.Label(self.window, text = 'Caution : Near nerve', fg = 'red', bg = 'white', font = ('Arial', 36))

		# self.update()

		# self.btn_snapshot = tkinter.Button(self.window, text='Take Snapshot', command = self.snapshot, bg='black', fg='white', font=('Arial',14), highlightcolor='grey', width = 30)
		# self.btn_snapshot.place(x=50, y = 730)


		# self.btn_snapshot2 = tkinter.Button(self.window, text='Add to Training Data', command = self.snapshot2, bg='black', fg='white', font=('Arial',14), highlightcolor='grey', width = 30)
		# self.btn_snapshot2.place(x=450, y = 730)
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
		self.vid = MyVideoCapture('hello.mp4')
		self.vid2 = MyVideoCapture('hello.mp4')

		self.VID_WIDTH = self.vid.width 
		self.VID_HEIGHT = self.vid.height 

		self.canvas1 = tkinter.Canvas(root, width = self.vid.width *1//2, height = self.vid.height*1//2)
		self.canvas1.place(x=50,y=150)
		tkinter.Button(root,text="UPLOAD SECRET VIDEO", command=self.browse1,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=80,y=450)
		print(COVER_VIDEO_SOURCE)

		self.canvas2 = tkinter.Canvas(root, width = self.vid.width*1//2, height = self.vid.height*1//2)
		self.canvas2.place(x=500,y=150)
		tkinter.Button(root,text="UPLOAD COVER VIDEO", command=self.browse2,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=520,y=450)
		# print(SECRET_VIDEO_SOURCE)
		self.canvas3 = tkinter.Canvas(root, width = self.vid.width*1//2, height = self.vid.height*1//2)
		self.canvas3.place(x=950,y=150)
		tkinter.Button(root,text="GET CONTAINER VIDEO", command=lambda : convert_to_frames(SECRET_VIDEO_SOURCE,COVER_VIDEO_SOURCE),bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=920,y=450)
		text = tkinter.Label(root, text = 'Secret Video', bg = 'white', font = ('Arial', 14))
		text.place(x = 60, y = 150)
		
		text = tkinter.Label(root, text = 'Cover Video', bg = 'white', font = ('Arial', 14))
		text.place(x = 510, y = 150)	

		text = tkinter.Label(root, text = 'Container Video', bg = 'white', font = ('Arial', 14))
		text.place(x = 960, y = 150)
		tkinter.Button(root,text="QUIT", command=root.destroy,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=1200,y=730)

		root.mainloop()
	
	def browse1(self):
		filename=askopenfilename()
		SECRET_VIDEO_SOURCE=filename
	
	def browse2(self):
		filename=askopenfilename()
		COVER_VIDEO_SOURCE=filename

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
		self.vid = MyVideoCapture('hello.mp4')
		self.vid2 = MyVideoCapture('hello.mp4')

		self.VID_WIDTH = self.vid.width 
		self.VID_HEIGHT = self.vid.height 

		self.canvas1 = tkinter.Canvas(root, width = self.vid.width *1//2, height = self.vid.height*1//2)
		self.canvas1.place(x=50,y=150)

		self.canvas2 = tkinter.Canvas(root, width = self.vid.width*1//2, height = self.vid.height*1//2)
		self.canvas2.place(x=500,y=150)

		self.canvas3 = tkinter.Canvas(root, width = self.vid.width*1//2, height = self.vid.height*1//2)
		self.canvas3.place(x=950,y=150)

		text = tkinter.Label(root, text = 'Secret Video', bg = 'white', font = ('Arial', 14))
		text.place(x = 60, y = 150)
		
		text = tkinter.Label(root, text = 'Cover Video', bg = 'white', font = ('Arial', 14))
		text.place(x = 510, y = 150)	

		text = tkinter.Label(root, text = 'Container Video', bg = 'white', font = ('Arial', 14))
		text.place(x = 960, y = 150)
		tkinter.Button(root	,text="QUIT", command=root.destroy,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=1200,y=730)

		root.mainloop()
	
	def update(self):
		ret, self.frame = self.vid.get_frame()
		ret2,self.frame2=self.vid2.get_frame()
		if ret:
			image = PIL.Image.fromarray(self.frame)
			image = image.resize((image.size[0]*1//2, image.size[1]*1//2), PIL.Image.ANTIALIAS)
			self.photo1 = PIL.ImageTk.PhotoImage(image = image)
			
			image = PIL.Image.fromarray(self.frame2)
			image = image.resize((image.size[0]*1//2, image.size[1]*1//2), PIL.Image.ANTIALIAS)
			self.photo2 = PIL.ImageTk.PhotoImage(image = image)
			for f in os.listdir(COVER_IMAGE_PATH):
				# os.remove(f)
				print(f)
			for f in os.listdir(SECRET_IMAGE_PATH):
				# os.remove(f)
				print(f)
			for f in os.listdir(CONTAINER_IMAGE_PATH):
				# os.remove(f)
				print(f)
			self.photo11=cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
			self.photo21=cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)
			cv2.imwrite(COVER_IMAGE_PATH+'a.jpg',self.photo11)
			cv2.imwrite(SECRET_IMAGE_PATH+'b.jpg',self.photo21)
			os.system("CUDA_VISIBLE_DEVICES=0 python run.py --test=./example_pics --batchSize=1")
			# annotated_frame, coord_list = self.annotated(self.frame);
			# annotated_frame = draw_bounding_box(annotated_frame, coord_list)
			# annotated_image = PIL.Image.fromarray(annotated_frame)
			# annotated_image = annotated_image.resize((annotated_image.size[0]*5//6, annotated_image.size[1]*5//6), PIL.Image.ANTIALIAS)
			# self.photo2 = PIL.ImageTk.PhotoImage(image = annotated_image)			
			if self.frame_count == 0:
				# annotated_frame, coord_list, score = annotated(self.model,self.frame,self.VID_WIDTH,self.VID_HEIGHT)
				# self.warning.place(x = 900, y = 40)
				# if 6 not in coord_list:
				# 	self.warning.place_forget()
	
				# annotated_frame = draw_bounding_box(annotated_frame, coord_list,self.VID_WIDTH*2//1)
				self.annotated_frame1=cv2.imread(CONTAINER_IMAGE_PATH+"c.jpg")
				annotated_frame=self.annotated_frame1
				self.frame3=annotated_frame
				annotated_image = PIL.Image.fromarray(annotated_frame)
				annotated_image = annotated_image.resize((annotated_image.size[0], annotated_image.size[1]), PIL.Image.ANTIALIAS)
				self.photo3 = PIL.ImageTk.PhotoImage(image = annotated_image)			
			self.frame_count = (self.frame_count + 1)%2

			self.canvas1.create_image(0, 0, image = self.photo1, anchor=tkinter.NW)
			self.canvas2.create_image(0, 0, image = self.photo2, anchor=tkinter.NW)
			self.canvas3.create_image(0, 0, image = self.photo3, anchor=tkinter.NW)

		self.window.update_idletasks()
		self.window.after_idle(self.update)


	def snapshot(self):
		# Get a frame from the video source
		pyautogui.screenshot("screenshots/frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg")

	def snapshot2(self):
		self.frame2=cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)
		cv2.imwrite("training_data/frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg",self.frame2)

	# def annotated(self, frame):
	# 	# ret, frame = self.vid2.get_frame()
		
	# 	input_img = cv2.resize(frame, (416, 416)) / 255.
	# 	input_img = input_img[:,:,::-1]
	# 	input_img = np.expand_dims(input_img, 0)

	# 	dummy_array = np.zeros((1,1,1,1,TRUE_BOX_BUFFER, 4))

	# 	netout = self.model.predict([input_img, dummy_array])
	# 	boxes = decode_netout(netout[0],
	# 							obj_threshold = 0.3,
	# 							nms_threshold = 0.3,
	# 							anchors = ANCHORS,
	# 							nb_class = CLASS)
	# 	coord = {}
	# 	maxscore = {}
	# 	for box in boxes:
	# 		xmin, xmax, ymin, ymax, label, score = box.xmin, box.xmax, box.ymin, box.ymax, box.get_label(), box.get_score()
	# 		labelx = int(float(LABELS[label]))

	# 		if labelx not in coord or score > maxscore[labelx]:
	# 			coord[labelx] = [(int(xmin * self.VID_WIDTH), int(ymin * self.VID_HEIGHT)), (int(xmax * self.VID_WIDTH), int(ymax * self.VID_HEIGHT))]
	# 			maxscore[labelx] = score

	# 	# print(len(coord))
	# 	# coordinate_list={ 0:[(0,0),(50,50)], 1:[(50,50),(100,100)], 2:[(100,100),(150,150)], 5:[(200,200),(250,250)], 6:[(250,250),(300,300)], 7:[(300,300),(350,350)], 9:[(350,350),(400,400)], 10:[(400,400),(450,450)]}
	# 	# return frame, coordinate_list
	# 	return frame, coord, maxscore

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
App(tkinter.Tk(), "Video Steganography", 'hello.mp4')
