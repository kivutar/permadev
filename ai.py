from random import randint


# picks a random direction around the entity
def random_dir():
	dirs = [
		(-1,-1),
		(-1, 0),
		(-1, 1),
		( 0,-1),
		( 0, 0),
		( 0, 1),
		( 1,-1),
		( 1, 0),
		( 1, 1),
	]
	i = randint(0, 8)
	return dirs[i]

# check if an item is on the same tile as the entity
def simple_sensor(self, items):
	self.energy -= 1
	if self.energy <= 0:
		self.log.append("SENSOR FAILED: OUT OF ENERGY")
		return None

	for item in items:
		if item.x == self.x and item.y == self.y:
			return item
	return None

def simple_move(self, game_map):
	self.energy -= 2
	if self.energy <= 0:
		self.log.append("MOVE FAILED: OUT OF ENERGY")
		return None

	d = random_dir()
	if not game_map.is_blocked(self.x + d[0], self.y + d[1]):
		self.move(d[0], d[1])
		self.log.append("SIMPLE MOVE TO %s %s" % d)
	else:
		self.log.append("FAILED MOVE TO %s %s" % d)

def simple_pick(self, items, item):
	self.energy -= 4
	if self.energy <= 0:
		self.log.append("PICK FAILED: OUT OF ENERGY")
		return None

	if item.x == self.x and item.y == self.y:
		if len(self.items) < self.item_capacity:
			items.remove(item)
			self.items.append(item)
			self.log.append("SIMPLE PICK")
			return True
		else:
			self.log.append("FAILED PICK: CAPACITY REACHED")
	else:
		self.log.append("FAILED PICK: OBJECT NOT FOUND")
	return False

def memorize_location(self, x, y):
	self.locations.append((x, y))

wanderer_text = """simple_move(self, game_map)
"""

def wanderer(self, game_map, items):
	simple_move(self, game_map)

gatherer_text = """item = simple_sensor(self, items)
if item != None:
  res = simple_pick(self, items, item)
  if res == False:
    simple_move(self, game_map)
else:
  simple_move(self, game_map)
"""

def gatherer(self, game_map, items):
	item = simple_sensor(self, items)
	if item != None:
		res = simple_pick(self, items, item)
		if res == False:
			simple_move(self, game_map)
	else:
		simple_move(self, game_map)
