import tcod as libtcod
import ai

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, name, color, ai=None, ai_text=""):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.ai = ai
        self.ai_text = ai_text
        self.period = 25
        self.t = 0
        self.item_capacity = 0
        self.items = []
        self.location_capacity = 10
        self.locations = []
        self.log = []
        self.max_energy = 3000
        self.energy = 3000
        if char == 'G':
            self.item_capacity = 3

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def ai_step(self, game_map, items):
        self.t += 1
        if self.ai != None and self.ai_text != "" and self.period == self.t and self.energy > 0:
            self.t = 0
            exec(self.ai_text, {
                "simple_sensor": ai.simple_sensor,
                "simple_pick": ai.simple_pick,
                "simple_move": ai.simple_move,
                "self": self,
                "items": items,
                "game_map": game_map,
                })

            # recolor based on battery
            if self.energy <= 0:
                self.color = libtcod.grey
            elif self.energy <= 1000:
                self.color = libtcod.red
            elif self.energy <= 2000:
                self.color = libtcod.yellow
            else:
                self.color = libtcod.green
