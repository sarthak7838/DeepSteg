import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from test import *
import pyautogui
from utils import *
import numpy as np
import tensorflow as tf
from keras.models import *
from keras.layers import *
from keras.layers.advanced_activations import *
from annotator import *

"""Constants"""
LABELS = ['0.0', '1.0', '2.0', '5.0', '7.0', '9.0', '10.0']

IMAGE_H, IMAGE_W = 416, 416
GRID_H,  GRID_W  = 13 , 13
BOX              = 5
CLASS            = len(LABELS)
OBJ_THRESHOLD    = 0.3#0.5
NMS_THRESHOLD    = 0.3#0.45
ANCHORS          = [1.77,3.13, 2.53,4.71, 3.52,5.27, 5.95,7.03, 7.34,2.31]

NO_OBJECT_SCALE  = 1.0
OBJECT_SCALE     = 5.0
COORD_SCALE      = 1.0
CLASS_SCALE      = 1.0

BATCH_SIZE       = 16
WARM_UP_BATCHES  = 0
TRUE_BOX_BUFFER  = 50

def space_to_depth_x2(x):
	return tf.space_to_depth(x, block_size = 2)

"""Model"""
def define_model():
	input_image = Input(shape=(IMAGE_H, IMAGE_W, 3))
	true_boxes  = Input(shape=(1, 1, 1, TRUE_BOX_BUFFER , 4))

	# Layer 1
	x = Conv2D(32, (3,3), strides=(1,1), padding='same', name='conv_1', use_bias=False)(input_image)
	x = BatchNormalization(name='norm_1')(x)
	x = LeakyReLU(alpha=0.1)(x)
	x = MaxPooling2D(pool_size=(2, 2))(x)

	# Layer 2
	x = Conv2D(64, (3,3), strides=(1,1), padding='same', name='conv_2', use_bias=False)(x)
	x = BatchNormalization(name='norm_2')(x)
	x = LeakyReLU(alpha=0.1)(x)
	x = MaxPooling2D(pool_size=(2, 2))(x)

	# Layer 3
	x = Conv2D(128, (3,3), strides=(1,1), padding='same', name='conv_3', use_bias=False)(x)
	x = BatchNormalization(name='norm_3')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 4
	x = Conv2D(64, (1,1), strides=(1,1), padding='same', name='conv_4', use_bias=False)(x)
	x = BatchNormalization(name='norm_4')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 5
	x = Conv2D(128, (3,3), strides=(1,1), padding='same', name='conv_5', use_bias=False)(x)
	x = BatchNormalization(name='norm_5')(x)
	x = LeakyReLU(alpha=0.1)(x)
	x = MaxPooling2D(pool_size=(2, 2))(x)

	# Layer 6
	x = Conv2D(256, (3,3), strides=(1,1), padding='same', name='conv_6', use_bias=False)(x)
	x = BatchNormalization(name='norm_6')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 7
	x = Conv2D(128, (1,1), strides=(1,1), padding='same', name='conv_7', use_bias=False)(x)
	x = BatchNormalization(name='norm_7')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 8
	x = Conv2D(256, (3,3), strides=(1,1), padding='same', name='conv_8', use_bias=False)(x)
	x = BatchNormalization(name='norm_8')(x)
	x = LeakyReLU(alpha=0.1)(x)
	x = MaxPooling2D(pool_size=(2, 2))(x)

	# Layer 9
	x = Conv2D(512, (3,3), strides=(1,1), padding='same', name='conv_9', use_bias=False)(x)
	x = BatchNormalization(name='norm_9')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 10
	x = Conv2D(256, (1,1), strides=(1,1), padding='same', name='conv_10', use_bias=False)(x)
	x = BatchNormalization(name='norm_10')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 11
	x = Conv2D(512, (3,3), strides=(1,1), padding='same', name='conv_11', use_bias=False)(x)
	x = BatchNormalization(name='norm_11')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 12
	x = Conv2D(256, (1,1), strides=(1,1), padding='same', name='conv_12', use_bias=False)(x)
	x = BatchNormalization(name='norm_12')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 13
	x = Conv2D(512, (3,3), strides=(1,1), padding='same', name='conv_13', use_bias=False)(x)
	x = BatchNormalization(name='norm_13')(x)
	x = LeakyReLU(alpha=0.1)(x)

	skip_connection = x

	x = MaxPooling2D(pool_size=(2, 2))(x)

	# Layer 14
	x = Conv2D(1024, (3,3), strides=(1,1), padding='same', name='conv_14', use_bias=False)(x)
	x = BatchNormalization(name='norm_14')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 15
	x = Conv2D(512, (1,1), strides=(1,1), padding='same', name='conv_15', use_bias=False)(x)
	x = BatchNormalization(name='norm_15')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 16
	x = Conv2D(1024, (3,3), strides=(1,1), padding='same', name='conv_16', use_bias=False)(x)
	x = BatchNormalization(name='norm_16')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 17
	x = Conv2D(512, (1,1), strides=(1,1), padding='same', name='conv_17', use_bias=False)(x)
	x = BatchNormalization(name='norm_17')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 18
	x = Conv2D(1024, (3,3), strides=(1,1), padding='same', name='conv_18', use_bias=False)(x)
	x = BatchNormalization(name='norm_18')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 19
	x = Conv2D(1024, (3,3), strides=(1,1), padding='same', name='conv_19', use_bias=False)(x)
	x = BatchNormalization(name='norm_19')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 20
	x = Conv2D(1024, (3,3), strides=(1,1), padding='same', name='conv_20', use_bias=False)(x)
	x = BatchNormalization(name='norm_20')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 21
	skip_connection = Conv2D(64, (1,1), strides=(1,1), padding='same', name='conv_21', use_bias=False)(skip_connection)
	skip_connection = BatchNormalization(name='norm_21')(skip_connection)
	skip_connection = LeakyReLU(alpha=0.1)(skip_connection)
	skip_connection = Lambda(space_to_depth_x2)(skip_connection)

	x = concatenate([skip_connection, x])

	# Layer 22
	x = Conv2D(1024, (3,3), strides=(1,1), padding='same', name='conv_22', use_bias=False)(x)
	x = BatchNormalization(name='norm_22')(x)
	x = LeakyReLU(alpha=0.1)(x)

	# Layer 23
	x = Conv2D(BOX * (4 + 1 + CLASS), (1,1), strides=(1,1), padding='same', name='conv_23')(x)
	output = Reshape((GRID_H, GRID_W, BOX, 4 + 1 + CLASS))(x)

	# small hack to allow true_boxes to be registered when Keras build the model 
	# for more information: https://github.com/fchollet/keras/issues/2790
	output = Lambda(lambda args: args[0])([output, true_boxes])

	model = Model([input_image, true_boxes], output)
	model.compile(loss='categorical_crossentropy', optimizer='adam')
	return model

def annotated(model,frame,vid_width,vid_height):
		# ret, frame = self.vid2.get_frame()
		
		input_img = cv2.resize(frame, (416, 416)) / 255.
		input_img = input_img[:,:,::-1]
		input_img = np.expand_dims(input_img, 0)

		dummy_array = np.zeros((1,1,1,1,TRUE_BOX_BUFFER, 4))

		netout = model.predict([input_img, dummy_array])
		boxes = decode_netout(netout[0],
								obj_threshold = 0.4,
								nms_threshold = 0.4,
								anchors = ANCHORS,
								nb_class = CLASS)
		coord = {}
		maxscore = {}
		for box in boxes:
			xmin, xmax, ymin, ymax, label, score = box.xmin, box.xmax, box.ymin, box.ymax, box.get_label(), box.get_score()
			labelx = int(float(LABELS[label]))

			if labelx not in coord or score > maxscore[labelx]:
				coord[labelx] = [(int(xmin * vid_width), int(ymin * vid_height)), (int(xmax * vid_width), int(ymax * vid_height))]
				maxscore[labelx] = score

		# print(len(coord))
		# coordinate_list={ 0:[(0,0),(50,50)], 1:[(50,50),(100,100)], 2:[(100,100),(150,150)], 5:[(200,200),(250,250)], 6:[(250,250),(300,300)], 7:[(300,300),(350,350)], 9:[(350,350),(400,400)], 10:[(400,400),(450,450)]}
		# return frame, coordinate_list
		return frame, coord, maxscore