import ai

# equipment can unlock the use of a few functions
func_for_eq = {
    "Legs": [ai.move],                # for moving and climbing
    "Wheels": [ai.move],              # for moving fast on flat ground
    "Sonar": [ai.sonar],              # middle distance wall sensor
    "Sensor": [ai.simple_sensor, ai.wall_sensor], # check for nearby items and walls
    "IR Sensor": [],                  # middle distance enemy detection based on heat
    "Arms": [ai.simple_pick, ai.dig], # used to pick item on the floor and can mine a bit
    "Li-ION Battery": [],             # to store energy
    "Item Storage": [],               # to transport heavy items
    "ML Kit": [],                     # get bonus when repeating a task
    "Driller": [ai.dig],              # to dig / mine
    "Bomb": [],                       # to destroy walls, of self destroy
    "Hacking Kit": [],                # to invite neutral / aggro bots to the team
}

class Equipment:
    def __init__(self, name):
        self.name = name
        self.char = name[0]
        self.funcs = func_for_eq.get(name)
        self.durability = 100
