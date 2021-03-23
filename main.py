#!/usr/bin/env python3
import tcod
from entity import Entity
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import render_all
from colors import colors
from pprint import pprint
import ui
import glo

def main():
    paused = True

    screen_width = 60
    screen_height = 40
    map_width = 60
    map_height = 40

    room_max_size = 10
    room_min_size = 6
    max_rooms = 20

    entities = []

    tcod.console_set_custom_font('my16x16.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(screen_width, screen_height, 'PERMADEV', False)
    tcod.sys_set_fps(30)

    con = tcod.console.Console(screen_width, screen_height)

    glo.game_map = GameMap(map_width, map_height, entities, glo.items)
    glo.game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height)

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        con.clear()

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        if not paused:
            for entity in entities:
                entity.ai_step()

        render_all(con, entities, screen_width, screen_height, colors)

        if paused:
            con.print(0, 0, "PAUSED", tcod.red, tcod.yellow)
            glo.uis.append(ui.MenuBar(7, 0, [
                    {
                        "name": "Action",
                        "cb": lambda: glo.uis.append(ui.Dropdown(7, 1, [
                            {
                                "name": "Mark zone",
                                "cb": lambda: glo.uis.append(ui.Dropdown(19, 1, [
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
                                "cb": lambda: glo.uis.append(ui.Dropdown(19, 2, [
                                    {
                                        "name": "Wall",
                                        "cb": lambda: print("foo")
                                    },
                                    {
                                        "name": "Door",
                                        "cb": lambda: print("foo")
                                    },
                                    {
                                        "name": "Wire",
                                        "cb": lambda: print("foo")
                                    },
                                    {
                                        "name": "Panel",
                                        "cb": lambda: print("foo")
                                    },
                                ]))
                            },
                            {
                                "name": "Dig",
                                "cb": lambda: print("foo")
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
                    {
                        "name": "Zones",
                        "cb": lambda: print("foo")
                    },
                ]))
        else:
            con.print(0, 0, "RUNNING")

        if paused:
            for entity in entities:
                if entity.x == mouse.cx and entity.y == mouse.cy:
                    tcod.console_set_char_background(con, mouse.cx, mouse.cy, tcod.grey)
                    con.print(mouse.cx+1, mouse.cy, entity.name, tcod.black, tcod.green)

        if paused and mouse.lbutton:
            for entity in entities:
                if entity.x == mouse.cx and entity.y == mouse.cy:
                    glo.uis.append(ui.Editor(3, 4, entity))

        for u in glo.uis:
            u.update(mouse, key)

        for u in glo.uis:
            u.draw(con, mouse)

        tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

        tcod.console_flush()

        action = handle_keys(key)

        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        toggle = action.get('toggle')

        if toggle:
            paused = not paused
            glo.uis = []

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


if __name__ == '__main__':
     main()
