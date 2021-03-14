import tcod as libtcod

class Dropdown:

	def __init__(self, x, y, items):
		self.x = x
		self.y = y
		self.width = 10
		self.height = len(items)+2
		self.items = items

	def update(self, mouse):
		if mouse.lbutton:
			for i, item in enumerate(self.items):
				if mouse.cy == self.y+1+i:
					item.get("cb")()

	def draw(self, con, mouse):
		con.draw_frame(self.x, self.y, self.width, self.height, "", True, libtcod.white, libtcod.black)
		for i, item in enumerate(self.items):
			bg = libtcod.black
			if mouse.cy == self.y+1+i:
				bg = libtcod.green
			con.print(self.x+1, self.y+1+i, item.get("name"), libtcod.white, bg)

class Editor:

	def __init__(self, x, y, entity):
		self.x = x
		self.y = y
		self.width = 40
		self.height = 24
		self.entity = entity

	def update(self, mouse):
		pass

	def draw(self, con, mouse):
		con.draw_frame(self.x, self.y, self.width, self.height, self.entity.name, True, libtcod.white, libtcod.black)
		con.print(self.x+1, self.y+2, self.entity.ai_text, libtcod.white, libtcod.black)
