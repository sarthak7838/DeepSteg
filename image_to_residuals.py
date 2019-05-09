import os
import numpy as np
import cv2
from diffimg import diff
from PIL import Image
from PIL import ImageChops
def to_residuals(folder,test_path):
	ref= os.path.join(folder+'frame001.png')
	refi=Image.open(ref)
	refi.save(test_path+'frame001ref.png')
	for the_file in sorted(os.listdir(folder)):	
		file_path=os.path.join(folder+the_file)
		if(ref==file_path):
			continue
		else : 	 
			res=os.path.join(folder+the_file)
			# print(ref)
			err=diff(ref,res)
			if(err<0.065):
				resi=Image.open(res)
				refi=Image.open(ref)
				arr=np.array(resi)
				arr2=np.array(refi)
				arr3=arr-arr2
				differ=Image.fromarray(arr3)
				differ.save(test_path+the_file.strip('.png')+'res.png')
			else:
				# print("Reference changed\n")
				ref=file_path
				refi=Image.open(ref)
				refi.save(test_path+the_file.strip('.png')+'ref.png')
