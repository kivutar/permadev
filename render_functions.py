import tcod
import glo


def render_all(con, entities, screen_width, screen_height, colors):
    for y in range(glo.game_map.height):
        for x in range(glo.game_map.width):
            wall = glo.game_map.tiles[x][y].block_sight
            explored = glo.game_map.tiles[x][y].explored

            if explored:
                if wall:
                    tcod.console_put_char_ex(con, x, y, '#', colors.get('light_wall'), colors.get('dark_ground'))
                else:
                    tcod.console_put_char_ex(con, x, y, ' ', colors.get('light_ground'), colors.get('dark_ground_bg'))

    for item in glo.items:
        draw_entity(con, item)

    for entity in entities:
        draw_entity(con, entity)

def draw_entity(con, entity):
    tcod.console_set_default_foreground(con, entity.color)
    tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)
