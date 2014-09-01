import cv2

class Frame:
	
	def __init__(self, file_name):
		self.file_name = file_name
		self.screen_shot = cv2.imread(file_name)

	def _get_cs_img(self, player_index):
		'player_index is 0-4 left side, 5-9 right side'
		'rectangle is 35x30 pixels, located 35 pixels from the center of the screen and 3'
		
		# top of scoreboard + 30 for each position
		top = 930 + 30 * (player_index % 5)
		# width/2 - 35 (champ icon) - 35 (cs text width)
		left = 890 if player_index < 5 else 995

		color_img = self.screen_shot[top:top+30,left:left+35]
		return cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

	def _thresh_img(self, img, num):
		# ret, thresh = cv2.adaptiveThreshold(img, 127, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, num)
		ret,thresh4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)
		return thresh