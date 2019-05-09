import os
import os
import numpy as np
import cv2
from diffimg import diff
from PIL import Image
from PIL import ImageChops

def reconstruct(folder,folder2):
	ref=os.path.join(folder+'frame001ref.png')
	for the_file in sorted(os.listdir(folder)):
		if('res' in the_file):
			resi=Image.open(folder+the_file)
			refi=Image.open(ref)
			arr=np.array(resi)
			arr2=np.array(refi)
			arr3=arr2+arr
			adder=Image.fromarray(arr3)
			adder.save(folder2+the_file)
		else:
			refi=Image.open(folder+the_file)
			refi.save(folder2+the_file)
			ref=os.path.join(folder+the_file)