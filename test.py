import cv2

color_list = {0:(255,0,0),1:(0,255,0),2:(0,0,255),5:(255,0,127),6:(160,160,160),7:(0,0,0),9:(0,255,255),10:(51,0,0)}
label_list = {0:'F',1:'A',2:'E',5:'O',6:'N',7:'B',9:'D',10:'I'}
def draw_bounding_box(image, coordinate_list,width):
	# image=cv2.imread("abc.jpeg")
	for text, item in coordinate_list.items():
		x=item[1][0]
		y=item[1][1]
		cv2.rectangle(image,item[0],item[1],color_list[text],2)
		cv2.putText(image, label_list[text], (x+5,y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color_list[text], 2, cv2.LINE_AA)
		# if(text==2):
		# 	cv2.rectangle(image,((int)(width)-item[1][0],item[0][1]),((int)(width)-item[0][0],item[1][1]),color_list[text],2)
		# 	cv2.putText(image, label_list[text], (x+5,y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color_list[text], 2, cv2.LINE_AA)
	# image=cv2.imread("abc.jpeg")
	# cv2.imwrite('image.jpeg', image)
	return image
