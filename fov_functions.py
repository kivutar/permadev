import tcod
import glo

def initialize_fov():
    fov_map = tcod.map_new(glo.game_map.width, glo.game_map.height)

    for y in range(glo.game_map.height):
        for x in range(glo.game_map.width):
            tcod.map_set_properties(fov_map, x, y, not glo.game_map.tiles[x][y].block_sight,
                                       not glo.game_map.tiles[x][y].blocked)

    return fov_map

def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    tcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)
