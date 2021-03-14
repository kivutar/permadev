#!/usr/bin/env python3
import tcod as libtcod
from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all
from colors import colors
from pprint import pprint
import ui

def main():
    paused = True

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

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', "DEV", libtcod.white, "")
    entities = [player]
    items = []
    uis = []

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
            uis.append(ui.MenuBar(7, 0, [
                    {
                        "name": "Action",
                        "cb": lambda: uis.append(ui.Dropdown(7, 1, [
                            {
                                "name": "Plan",
                                "cb": lambda: uis.append(ui.Dropdown(15, 2, [
                                    {
                                        "name": "Storage",
                                        "cb": lambda: print("foo")
                                    },
                                    {
                                        "name": "Living",
                                        "cb": lambda: print("foo")
                                    },
                                    {
                                        "name": "Danger",
                                        "cb": lambda: print("foo")
                                    },
                                ]))
                            },
                            {
                                "name": "Build",
                                "cb": lambda: uis.append(ui.Dropdown(15, 2, [
                                    {
                                        "name": "Wall",
                                        "cb": lambda: print("foo")
                                    },
                                    {
                                        "name": "Door",
                                        "cb": lambda: print("foo")
                                    },
                                ]))
                            },
                        ]))
                    },
                    {
                        "name": "Units",
                        "cb": lambda: print("foo")
                    },
                    {
                        "name": "Stats",
                        "cb": lambda: print("foo")
                    },
                ]))
        else:
            con.print(0, 0, "RUNNING")

        if paused:
            for entity in entities:
                if entity.x == mouse.cx and entity.y == mouse.cy:
                    libtcod.console_set_char_background(con, mouse.cx, mouse.cy, libtcod.grey)
                    con.print(mouse.cx+1, mouse.cy, entity.name, libtcod.black, libtcod.green)

        if paused and mouse.lbutton:
            for entity in entities:
                if entity.x == mouse.cx and entity.y == mouse.cy:
                    uis.append(ui.Editor(3, 4, entity))

        for u in uis:
            u.update(mouse)

        for u in uis:
            u.draw(con, mouse)

        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

        libtcod.console_flush()

        clear_all(con, entities, items)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        toggle = action.get('toggle')

        if toggle:
            paused = not paused
            uis = []

        if not paused:
            if move:
                dx, dy = move
                if not game_map.is_blocked(player.x + dx, player.y + dy):
                    player.move(dx, dy)
                    fov_recompute = True

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
     main()
