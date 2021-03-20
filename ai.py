from random import randint
import glo


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
def simple_sensor(self):
	self.busy += 5
	self.energy -= 1
	if self.energy <= 0:
		self.log.append("SENSOR FAILED: OUT OF ENERGY")
		return None

	for item in glo.items:
		if item.x == self.x and item.y == self.y:
			return item
	return None

def wall_sensor(self):
	self.busy += 5
	self.energy -= 1
	if self.energy <= 0:
		self.log.append("SENSOR FAILED: OUT OF ENERGY")
		return None

	if self.x == 1 or self.y == 1 or self.x == glo.game_map.width-1 or self.y == glo.game_map.height-1:
		self.log.append("SENSOR FAILED: OUT OF MAP")
		return None

	if glo.game_map.tiles[self.x][self.y-1].blocked:
		return (self.x, self.y-1)
	if glo.game_map.tiles[self.x][self.y+1].blocked:
		return (self.x, self.y+1)
	if glo.game_map.tiles[self.x-1][self.y].blocked:
		return (self.x-1, self.y)
	if glo.game_map.tiles[self.x+1][self.y].blocked:
		return (self.x+1, self.y)

	return None

def rand_move(self):
	if self.char == 'W':
		self.busy += 5
	else:
		self.busy += 15
	self.energy -= 2
	if self.energy <= 0:
		self.log.append("MOVE FAILED: OUT OF ENERGY")
		return None

	d = random_dir()
	if not glo.game_map.is_blocked(self.x + d[0], self.y + d[1]):
		self.move(d[0], d[1])
		self.log.append("SIMPLE MOVE TO %s %s" % d)
	else:
		self.log.append("FAILED MOVE TO %s %s" % d)

def simple_pick(self, item):
	self.busy += 10
	self.energy -= 4
	if self.energy <= 0:
		self.log.append("PICK FAILED: OUT OF ENERGY")
		return None

	if item.x == self.x and item.y == self.y:
		if len(self.items) < self.item_capacity:
			glo.items.remove(item)
			self.items.append(item)
			self.log.append("SIMPLE PICK")
			return True
		else:
			self.log.append("FAILED PICK: CAPACITY REACHED")
	else:
		self.log.append("FAILED PICK: OBJECT NOT FOUND")
	return False

def dig(self, x, y):
	self.busy += 20
	self.energy -= 50
	if self.energy <= 0:
		self.log.append("DIG FAILED: OUT OF ENERGY")
		return None

	if glo.game_map.tiles[x][y].blocked:
		glo.game_map.tiles[x][y].blocked = False
		glo.game_map.tiles[x][y].block_sight = False
		glo.game_map.tiles[x][y].explored = True
		self.log.append("SIMPLE DIG")
		return True
	else:
		self.log.append("FAILED DIG: WALL NOT FOUND")
	return False

def memorize_location(self, x, y):
	self.locations.append((x, y))

wanderer_text = """rand_move(self)
"""

gatherer_text = """item = simple_sensor(self)
if item:
  simple_pick(self, item)
rand_move(self)
"""

miner_text = """wall = wall_sensor(self)
if wall !=  None:
  dig(self, wall[0], wall[1])
rand_move(self)
"""
