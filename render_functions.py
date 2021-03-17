import tcod
import glo


def render_all(con, entities, fov_map, fov_recompute, screen_width, screen_height, colors):
    #if fov_recompute:
    for y in range(glo.game_map.height):
        for x in range(glo.game_map.width):
            visible = tcod.map_is_in_fov(fov_map, x, y)
            wall = glo.game_map.tiles[x][y].block_sight

            if visible:
                if wall:
                    tcod.console_put_char_ex(con, x, y, '#', colors.get('light_wall'), colors.get('dark_ground'))
                else:
                    tcod.console_put_char_ex(con, x, y, ' ', colors.get('light_ground'), colors.get('dark_ground_bg'))
                glo.game_map.tiles[x][y].explored = True
            elif glo.game_map.tiles[x][y].explored:
                if wall:
                    tcod.console_put_char_ex(con, x, y, '#', colors.get('dark_wall'), colors.get('dark_ground'))
                else:
                    tcod.console_put_char_ex(con, x, y, ' ', colors.get('dark_ground'), colors.get('dark_ground_bg'))

    for item in glo.items:
        draw_entity(con, item, fov_map)

    for entity in entities:
        draw_entity(con, entity, fov_map)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)
    for item in glo.items:
        clear_entity(con, item)

def draw_entity(con, entity, fov_map):
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y):
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

def clear_entity(con, entity):
    # erase the character that represents this object
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)

