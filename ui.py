import tcod

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
			bg = tcod.black
			w = len(item.get("name"))
			if mouse.cy == self.y and mouse.cx >= self.x+x and mouse.cx <= self.x+x+w:
			 	bg = tcod.green
			con.print(self.x+x, self.y, item.get("name"), tcod.white, bg)
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
		con.draw_frame(self.x, self.y, self.width, self.height, "", True, tcod.white, tcod.black)
		for i, item in enumerate(self.items):
			bg = tcod.black
			if mouse.cy == self.y+1+i and mouse.cx >= self.x and mouse.cx <= self.x+self.width:
				bg = tcod.green
			con.print(self.x+1, self.y+1+i, item.get("name"), tcod.white, bg)

class Button:

	def __init__(self, x, y, text, cb):
		self.x = x
		self.y = y
		self.text = text
		self.width = len(self.text)
		self.height = 1
		self.cb = cb

	def update(self, mouse, key):
		if mouse.lbutton_pressed:
			if mouse.cy == self.y and mouse.cx >= self.x and mouse.cx <= self.x+self.width:
				self.cb()

	def draw(self, con, mouse):
		bg = tcod.black
		if mouse.cy == self.y and mouse.cx >= self.x and mouse.cx <= self.x+self.width:
			bg = tcod.green
		con.print(self.x, self.y, self.text, tcod.white, bg)

class Editor:

	def __init__(self, x, y, entity):
		self.x = x
		self.y = y
		self.width = 40
		self.height = 24
		self.entity = entity
		self.text = self.entity.ai_text
		self.cursorPos = len(self.text)
		self.saveBtn = Button(self.x, self.y+self.height-1, "SAVE", lambda: self.saveAndQuit())

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

	def saveAndQuit(self):
		self.entity.ai_text = self.text

	def update(self, mouse, key):
		if key.vk == tcod.KEY_LEFT:
			self.cursorPos -= 1
			self.clamp()
		elif key.vk == tcod.KEY_RIGHT:
			self.cursorPos += 1
			self.clamp()
		elif key.vk == tcod.KEY_DOWN:
			px, py = self.charToPos(self.cursorPos)
			for i in range(self.cursorPos, len(self.text)):
				if self.text[i] == '\n':
					self.cursorPos = i+1+px
					self.clamp()
					break
		elif key.vk == tcod.KEY_UP:
			px, py = self.charToPos(self.cursorPos)
			for i in reversed(range(self.cursorPos)):
				if self.text[i] == '\n':
					self.cursorPos = i-1
					self.clamp()
					break
		elif key.vk == tcod.KEY_BACKSPACE:
			if self.cursorPos > 0:
				self.cursorPos -= 1
				self.clamp()
				self.text = self.text[:self.cursorPos] + self.text[self.cursorPos+1:]
		elif key.vk == tcod.KEY_TEXT:
			self.text = self.text[:self.cursorPos] + key.text + self.text[self.cursorPos:]
			self.cursorPos += 1
			self.clamp()
		elif key.vk == tcod.KEY_ENTER:
			self.text = self.text[:self.cursorPos] + '\n' + self.text[self.cursorPos:]
			self.cursorPos += 1
			self.clamp()

		self.saveBtn.update(mouse, key)

	def draw(self, con, mouse):
		px, py = self.charToPos(self.cursorPos)

		con.draw_frame(self.x, self.y, self.width, self.height, self.entity.name, True, tcod.Color(168,168,168), tcod.Color(0,0,168))
		con.print(self.x+1, self.y+2, self.text, tcod.Color(168,168,168), tcod.Color(0,0,168))
		tcod.console_set_char_background(con, self.x+1+px, self.y+2+py, tcod.Color(0,168,168))

		self.saveBtn.draw(con, mouse)
