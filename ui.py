import tcod as libtcod

class MenuBar:

	def __init__(self, x, y, items):
		self.x = x
		self.y = y
		self.width = 0
		self.height = 1
		self.items = items

	def update(self, mouse, key):
		if mouse.lbutton_pressed:
			x = 0
			for item in self.items:
				w = len(item.get("name"))
				if mouse.cy == self.y and mouse.cx >= self.x+x and mouse.cx <= self.x+x+w:
					item.get("cb")()

	def draw(self, con, mouse):
		x = 0
		for item in self.items:
			bg = libtcod.black
			w = len(item.get("name"))
			if mouse.cy == self.y and mouse.cx >= self.x+x and mouse.cx <= self.x+x+w:
			 	bg = libtcod.green
			con.print(self.x+x, self.y, item.get("name"), libtcod.white, bg)
			x += w + 1

class Dropdown:

	def __init__(self, x, y, items):
		self.x = x
		self.y = y
		self.width = 12
		self.height = len(items)+2
		self.items = items

	def update(self, mouse, key):
		if mouse.lbutton_pressed:
			for i, item in enumerate(self.items):
				if mouse.cy == self.y+1+i and mouse.cx >= self.x and mouse.cx <= self.x+self.width:
					item.get("cb")()

	def draw(self, con, mouse):
		con.draw_frame(self.x, self.y, self.width, self.height, "", True, libtcod.white, libtcod.black)
		for i, item in enumerate(self.items):
			bg = libtcod.black
			if mouse.cy == self.y+1+i and mouse.cx >= self.x and mouse.cx <= self.x+self.width:
				bg = libtcod.green
			con.print(self.x+1, self.y+1+i, item.get("name"), libtcod.white, bg)

class Editor:

	def __init__(self, x, y, entity):
		self.x = x
		self.y = y
		self.width = 40
		self.height = 24
		self.entity = entity
		self.text = self.entity.ai_text
		self.cursorPos = len(self.text)

	def charToPos(self, c):
		x = 0
		y = 0
		for i in range(c):
			x += 1
			if self.text[i] == '\n':
				y += 1
				x = 0
		return (x, y)

	def lines(self):
		lines = 0
		for i in range(len(self.text)):
			if self.text[i] == '\n':
				lines += 1
		return lines

	def clamp(self):
		self.cursorPos = max(0, self.cursorPos)
		self.cursorPos = min(len(self.text), self.cursorPos)

	def update(self, mouse, key):
		if key.vk == libtcod.KEY_LEFT:
			self.cursorPos -= 1
			self.clamp()
		elif key.vk == libtcod.KEY_RIGHT:
			self.cursorPos += 1
			self.clamp()
		elif key.vk == libtcod.KEY_DOWN:
			(px, py) = self.charToPos(self.cursorPos)
			for i in range(self.cursorPos, len(self.text)):
				if self.text[i] == '\n':
					self.cursorPos = i+1+px
					self.clamp()
					break
		elif key.vk == libtcod.KEY_UP:
			(px, py) = self.charToPos(self.cursorPos)
			for i in reversed(range(self.cursorPos)):
				if self.text[i] == '\n':
					self.cursorPos = i-1
					self.clamp()
					break
		elif key.vk == libtcod.KEY_BACKSPACE:
			if self.cursorPos > 0:
				self.cursorPos -= 1
				self.clamp()
				self.text = self.text[:self.cursorPos] + self.text[self.cursorPos+1:]
		elif key.vk == libtcod.KEY_TEXT:
			self.text = self.text[:self.cursorPos] + key.text + self.text[self.cursorPos:]
			self.cursorPos += 1
			self.clamp()
		elif key.vk == libtcod.KEY_ENTER:
			self.text = self.text[:self.cursorPos] + '\n' + self.text[self.cursorPos:]
			self.cursorPos += 1
			self.clamp()

	def draw(self, con, mouse):
		(px, py) = self.charToPos(self.cursorPos)

		con.draw_frame(self.x, self.y, self.width, self.height, self.entity.name, True, libtcod.white, libtcod.black)
		con.print(self.x+1, self.y+2, self.text, libtcod.white, libtcod.black)
		libtcod.console_set_char_background(con, self.x+1+px, self.y+2+py, libtcod.green)
