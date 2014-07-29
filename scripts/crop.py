from PIL import Image, ImageFilter
import glob, os, PIL.ImageOps

def getCroppedScores(image):
	im = Image.open(image)

	# red side
	for i in range(0, 5):
		yield PIL.ImageOps.invert(im.crop((795, 930 + 30*i, 880, 960 + 30*i)))
	# blue side
	for i in range(0, 5):
		yield PIL.ImageOps.invert(im.crop((1045, 930 + 30*i, 1130, 960 + 30*i)))
	return

files = glob.glob("..\screens\screen*.png")
i = 0
for file in files:
	for im in getCroppedScores(file):
		newim = im.resize((380, 120))
		newim = newim.filter(ImageFilter.SHARPEN)
		newim = newim.filter(ImageFilter.DETAIL)
		# newim = newim.filter(ImageFilter.MaxFilter(3))
		newim = newim.resize((85, 30))
		newim.save("..\screens\scores\score{0}.png".format(i))
		i = i + 1