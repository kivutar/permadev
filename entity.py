import tcod
import ai


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, name, color, ai_text="", blocking=True):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.ai_text = ai_text
        self.t = 0
        self.item_capacity = 0
        self.items = []
        self.location_capacity = 10
        self.locations = []
        self.log = []
        self.max_energy = 3000
        self.energy = 3000
        self.busy = 0
        self.blocking = blocking
        if char == 'G':
            self.item_capacity = 3

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def ai_step(self):
        self.busy -= 1
        if self.ai_text != "" and self.busy <= 0 and self.energy > 0:
            self.busy = 0
            exec(self.ai_text, {
                "simple_sensor": ai.simple_sensor,
                "simple_pick": ai.simple_pick,
                "rand_move": ai.rand_move,
                "self": self,
                })

            # recolor based on battery
            if self.energy <= 0:
                self.color = tcod.grey
            elif self.energy <= 1000:
                self.color = tcod.red
            elif self.energy <= 2000:
                self.color = tcod.yellow
            else:
                self.color = tcod.green
