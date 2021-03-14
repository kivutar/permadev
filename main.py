#!/usr/bin/env python3
import tcod as libtcod
from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all
from colors import colors
from pprint import pprint

def main():
    paused = True
    mode = "map"
    editentity = None

    screen_width = 60
    screen_height = 40
    map_width = 60
    map_height = 40

    room_max_size = 10
    room_min_size = 6
    max_rooms = 20

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', "DEV", libtcod.white, None, "")
    entities = [player]
    items = []

    libtcod.console_set_custom_font('my20x20.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'PERMADEV', False)
    libtcod.sys_set_fps(30)

    con = libtcod.console.Console(screen_width, screen_height)

    game_map = GameMap(map_width, map_height, entities, items)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.console_clear(con)

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if not paused:
            for entity in entities:
                entity.ai_step(game_map, items)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(con, entities, items, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        fov_recompute = False

        if paused:
            con.print(0, 0, "PAUSED", libtcod.red, libtcod.yellow)
        else:
            con.print(0, 0, "RUNNING")

        if paused:
            for entity in entities:
                if entity.x == mouse.cx and entity.y == mouse.cy:
                    libtcod.console_set_char_background(con, mouse.cx, mouse.cy, libtcod.grey)
                    #con.draw_frame(mouse.cx, mouse.cy, 20, 3, entity.name, True, libtcod.white, libtcod.black)
                    con.print(mouse.cx+1, mouse.cy, entity.name, libtcod.black, libtcod.green)

        if paused and mouse.lbutton:
            for entity in entities:
                if entity.x == mouse.cx and entity.y == mouse.cy:
                    mode = "dev"
                    editentity = entity

        if paused and mode == "dev":
            con.draw_frame(2, 2, 40, 24, editentity.name, True, libtcod.white, libtcod.black)
            # y = 0
            # for l in editentity.log:
            #     y += 1
            #     con.print(3, 3+y, l, libtcod.white, libtcod.black)
            con.print(3, 4, editentity.ai_text, libtcod.white, libtcod.black)

        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

        libtcod.console_flush()

        clear_all(con, entities, items)

        action = handle_keys(key)
        # handle_mouse(mouse)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        toggle = action.get('toggle')

        if toggle:
            paused = not paused
            mode = "map"

        if not paused:
            if move:
                dx, dy = move
                if not game_map.is_blocked(player.x + dx, player.y + dy):
                    player.move(dx, dy)
                    fov_recompute = True
                # for entity in entities:
                #     if entity.x == player.x and entity.y == player.y and entity != player:
                #         pprint(vars(entity))

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
     main()
