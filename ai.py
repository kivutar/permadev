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

def rand_move(self):
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

def memorize_location(self, x, y):
	self.locations.append((x, y))

wanderer_text = """rand_move(self)
"""

gatherer_text = """item = simple_sensor(self)
if item:
  simple_pick(self, item)
rand_move(self)
"""
