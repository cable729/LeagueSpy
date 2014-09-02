import cv2

class Frame:
	
	def __init__(self, file_name):
		self.file_name = file_name
		self.screen_shot = cv2.imread(file_name)

	def get_cs_img(self, player_index):
		'player_index corresponds to 0-4 left side, 5-9 right side'
		'rectangle is 35x30 pixels, located 35 pixels from the center of the screen'
		
		# top of scoreboard + 30 for each position
		top = 930 + 30 * (player_index % 5)
		# width/2 - 35 (champ icon) - 35 (cs text width)
		left = 890 if player_index < 5 else 995

		color_img = self.screen_shot[top:top+30,left:left+35]
		return cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)