import os 
from PIL import Image
from PIL.ExifTags import TAGS
import glob

def check_directory():
	directory = r'.\images'
	data_path = os.path.join(directory, '*jpg')
	files = glob.glob(data_path)

	for image in files:
		with Image.open(image) as f:
			info = f._getexif()
		if info == None:
			os.remove(image)
			print('Deleted '+ image)
