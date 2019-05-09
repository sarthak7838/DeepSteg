import cv2 
import os
import copy
import shutil
from image_to_residuals import *
from reconstruct_from_residuals import *
from video_from_frames import *
COVER_IMG_PATH='example_pics/cover_images/'
SECRET_IMG_PATH='example_pics/secret_images_1/'
MAIN_SECRET_IMG_PATH='example_pics/secret_images/'
FINAL_SECRET_IMG_PATH='example_pics/final_secret_images/'
FINAL_CONTAINER_IMG_PATH='example_pics/container_images/'
FINAL_CONTAINER_IMG_PATH2='example_pics/container_images2/'
VIDEO_PATH='Videos/'
# Function to extract frames 
def FrameCapture(path,folder_path): 
      
    for f in os.listdir(folder_path):
        os.remove(f)
        
    # Path to video file 
    vidObj = cv2.VideoCapture(path) 
  
    # Used as counter variable 
    count = 0
  
    # checks whether frames were extracted 
    success = 1
  
    while success: 
  
        # vidObj object calls read 
        # function extract frames 
        success, image = vidObj.read() 
  
        # Saves the frames with frame-count 
        cv2.imwrite(folder_path+"frame%03d.png" % count, image) 
  
        count += 1
    
    return count

def convert_to_frames(secret_path,cover_path):
    # print("Secret Path is"+ secret_path)
    # print("Cover Path is"+ cover_path)
    for the_file in os.listdir(COVER_IMG_PATH):
        os.remove(COVER_IMG_PATH+the_file)
    for the_file in os.listdir(SECRET_IMG_PATH):
        os.remove(SECRET_IMG_PATH+the_file)   
    for the_file in os.listdir(MAIN_SECRET_IMG_PATH):
        os.remove(MAIN_SECRET_IMG_PATH+the_file)  
    for the_file in os.listdir(FINAL_SECRET_IMG_PATH):
        os.remove(FINAL_SECRET_IMG_PATH+the_file) 
    for the_file in os.listdir(FINAL_CONTAINER_IMG_PATH):
        os.remove(FINAL_CONTAINER_IMG_PATH+the_file) 
    cover_count=FrameCapture(cover_path,COVER_IMG_PATH) 
    secret_count=FrameCapture(secret_path,MAIN_SECRET_IMG_PATH)
    os.remove(COVER_IMG_PATH+'frame%03d.png'%(cover_count-1))
    os.remove(MAIN_SECRET_IMG_PATH+'frame%03d.png'%(secret_count-1))
    cover_count=cover_count-1
    secret_count=secret_count-1;
    # print(cover_count)
    # print(secret_count)
    if cover_count>secret_count:
        for i in range(secret_count,cover_count):
            the_file="frame%03d.png" % i
            file_path = os.path.join(COVER_IMG_PATH, the_file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
    elif cover_count<secret_count:
        old_img=COVER_IMG_PATH+"frame%03d.png"%(cover_count-1)
        for i in range(cover_count,secret_count):
            new_img=COVER_IMG_PATH+"frame%03d.png" % i
            shutil.copy(old_img,new_img)
    # to_residuals(SECRET_IMG_PATH,MAIN_SECRET_IMG_PATH)
    # reconstruct(MAIN_SECRET_IMG_PATH,FINAL_SECRET_IMG_PATH)
    os.system("CUDA_VISIBLE_DEVICES=0 python run.py --test=./example_pics --batchSize=1")
    convert_frames_to_video(FINAL_SECRET_IMG_PATH,VIDEO_PATH+cover_path.strip(".mp4")+"_"+secret_path.slice(0,-4)+"_secret_video.mp4")
    convert_frames_to_video(FINAL_CONTAINER_IMG_PATH,VIDEO_PATH+cover_path.slice(".mp4")+"_"+secret_path.slice(0,-4)+"_container_video.mp4")

# Driver Code 
# if __name__ == '__main__':

    # Calling the functiCUDA_VISIBLE_DEVICES=0 python run.py --test=./example_pics --batchSize=1on 
def convert_to_frames2(container_path):
    for the_file in os.listdir(FINAL_CONTAINER_IMG_PATH2):
        os.remove(FINAL_CONTAINER_IMG_PATH2+the_file) 
    container_count=FrameCapture(container_path,FINAL_CONTAINER_IMG_PATH2)
     