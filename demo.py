import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from test import *
from utility import *
import numpy as np
import tensorflow as tf
from keras.models import *
from keras.layers import *
from keras.layers.advanced_activations import *
from tkinter.filedialog import askopenfilename
from video_crop_and_convert_to_frames import *
from revealfunction import *
import subprocess

LARGE_FONT= ("Verdana", 12)

COVER_IMAGE_PATH='example_pics/cover_images/'
SECRET_IMAGE_PATH='example_pics/secret_images/'
CONTAINER_IMAGE_PATH='example_pics/container_images/'
COVER_VIDEO_SOURCE='hello.avi'
SECRET_VIDEO_SOURCE='videoplayback.avi'
CONTAINER_VIDEO_SOURCE='videoplayback.avi'

class App(tkinter.Tk):

    def __init__(self, *args, **kwargs):
        
        tkinter.Tk.__init__(self, *args, **kwargs)
        container = tkinter.Frame(self)
        self.attributes('-fullscreen', True)
        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        button3=tkinter.Button(self,text="QUIT", command=self.destroy,bg="white",highlightcolor="grey",bd=3,font=('Arial',14))
        button3.place(x=1200,y=680)

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self,parent)
        
        text = tkinter.Label(self, text = 'DEEP VIDEO STEGANOGRAPHY', bg = 'white', font = ('Arial', 36))
        text.place(x = 50, y = 40)
        
        tkinter.Button(self,text="HIDE VIDEO", command=lambda: controller.show_frame(PageOne),bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=250,y=430)
        tkinter.Button(self,text="REVEAL VIDEO", command=lambda: controller.show_frame(PageTwo),bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=550,y=430)

class PageOne(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        text = tkinter.Label(self, text = 'HIDE VIDEO', bg = 'white', font = ('Arial', 36))
        text.place(x = 50, y = 40)

        self.vid = MyVideoCapture('hello.avi')

        self.canvas1 = tkinter.Canvas(self, width = self.vid.width *1//2, height = self.vid.height*1//2)
        self.canvas1.place(x=50,y=200)
        tkinter.Button(self,text="UPLOAD SECRET VIDEO", command=self.browse1,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=80,y=450)

        self.canvas2 = tkinter.Canvas(self, width = self.vid.width*1//2, height = self.vid.height*1//2)
        self.canvas2.place(x=500,y=200)
        tkinter.Button(self,text="UPLOAD COVER VIDEO", command=self.browse2,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=520,y=450)
        self.canvas3 = tkinter.Canvas(self, width = self.vid.width*1//2, height = self.vid.height*1//2)
        self.canvas3.place(x=950,y=200)
        tkinter.Button(self,text="GET CONTAINER VIDEO", command=lambda : convert_to_frames(SECRET_VIDEO_SOURCE,COVER_VIDEO_SOURCE),bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=920,y=450)
        text = tkinter.Label(self, text = 'Secret Video', bg = 'white', font = ('Arial', 14))
        text.place(x = 60, y = 150)
        tkinter.Button(self,text="Play Videos", command=lambda: self.play_videos(),bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=520,y=550)
        text = tkinter.Label(self, text = 'Cover Video', bg = 'white', font = ('Arial', 14))
        text.place(x = 510, y = 150)    

        text = tkinter.Label(self, text = 'Container Video', bg = 'white', font = ('Arial', 14))
        text.place(x = 960, y = 150)

        tkinter.Button(self,text="BACK", command=lambda: controller.show_frame(StartPage),bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=1000,y=680)

        
    def browse1(self):
        filename=askopenfilename()
        global SECRET_VIDEO_SOURCE
        SECRET_VIDEO_SOURCE=os.path.basename(filename)
    
    def browse2(self):
        filename=askopenfilename()
        global COVER_VIDEO_SOURCE
        COVER_VIDEO_SOURCE=os.path.basename(filename)

    
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
        if ret:
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
        self.update_idletasks()
        self.after(30,self.update)
        # self.window.after(15, self.update)



class PageTwo(tkinter.Frame):

    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        text = tkinter.Label(self, text = 'REVEAL VIDEO', bg = 'white', font = ('Arial', 36))
        text.place(x = 50, y = 40)

        self.vid = MyVideoCapture('hello.avi')

        self.canvas1 = tkinter.Canvas(self, width = self.vid.width*1//2, height = self.vid.height*1//2)
        self.canvas1.place(x=300,y=200)

        self.canvas2 = tkinter.Canvas(self, width = self.vid.width*1//2, height = self.vid.height*1//2)
        self.canvas2.place(x=800,y=200)

        tkinter.Button(self,text="UPLOAD CONTAINER VIDEO", command=self.browse3,bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=300,y=450)
        tkinter.Button(self,text="GET SECRET VIDEO", command=lambda : revealvideo(CONTAINER_VIDEO_SOURCE),bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=800,y=450)
        tkinter.Button(self,text="Play Videos", command=lambda: self.play_videos2(),bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=520,y=550)
        
        global REVEALED_VIDEO_PATH
        print(REVEALED_VIDEO_PATH)
        text = tkinter.Label(self, text = 'Container Video', bg = 'white', font = ('Arial', 14))
        text.place(x = 300, y = 150)
        
        text = tkinter.Label(self, text = 'Revealed Secret Video', bg = 'white', font = ('Arial', 14))
        text.place(x = 800, y = 150)   

        tkinter.Button(self,text="BACK", command=lambda: controller.show_frame(StartPage),bg="white",highlightcolor="grey",bd=3,font=('Arial',14)).place(x=1000,y=680)


    def play_videos2(self):
        self.vid3=MyVideoCapture('hello.avi')
        self.vid = MyVideoCapture(CONTAINER_VIDEO_SOURCE)
        self.vid2 = MyVideoCapture(ret_revealed_video_path())
        self.update2()

    def browse3(self):
        filename=askopenfilename()
        global CONTAINER_VIDEO_SOURCE
        CONTAINER_VIDEO_SOURCE=os.path.basename(filename)


    def update2(self):
        ret, self.frame = self.vid.get_frame()
        ret2,self.frame2=self.vid2.get_frame()
        if ret or ret2:
            if ret:             
                image = PIL.Image.fromarray(self.frame)
                image= image.resize((int(self.vid3.width//2),int(self.vid3.height//2)),PIL.Image.ANTIALIAS)
                self.photo1 = PIL.ImageTk.PhotoImage(image = image, master=self.canvas1)
                self.photo11=cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                cv2.imwrite(COVER_IMAGE_PATH+'a.jpg',self.photo11)
                self.canvas1.create_image(0, 0, image = self.photo1, anchor=tkinter.NW)
            if ret2:
                image = PIL.Image.fromarray(self.frame2)
                image= image.resize((int(self.vid3.width//2),int(self.vid3.height//2)),PIL.Image.ANTIALIAS)
                self.photo2 = PIL.ImageTk.PhotoImage(image = image, master=self.canvas2)
                self.photo21=cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)
                cv2.imwrite(SECRET_IMAGE_PATH+'b.jpg',self.photo21)
                self.canvas2.create_image(0, 0, image = self.photo2, anchor=tkinter.NW)
            
        else:   
            self.vid = MyVideoCapture(CONTAINER_VIDEO_SOURCE)
            self.vid2 = MyVideoCapture(ret_revealed_video_path())
        self.update_idletasks()
        self.after(30,self.update2)
        # self.window.after(15, self.update2)
     

      
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


app = App()
app.mainloop()
