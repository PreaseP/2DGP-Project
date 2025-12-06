import random
from pico2d import *

import cockpit_mode
from general_stage import GeneralStage
from players import PlayerS
from playerg import PlayerG
from biri import Biri

import game_framework
import game_world
import userdata

import common

spawn_timer = 0.0

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(cockpit_mode)
        else:
            common.player.handle_event(event)

def init():
    common.map = GeneralStage('stage1')
    game_world.add_object(common.map, 0)

    common.map.right_border = 1
    common.map.left_border = 0

    if userdata.playerType == 'S':
        common.player = PlayerS()
    else:
        common.player = PlayerG()

    common.player.x = get_canvas_width() / 2
    common.player.y = get_canvas_height() / 2

    game_world.add_object(common.player, 1)
    game_world.add_collision_pair('player:monster', common.player, None)

    for _ in range(10):
        biri = Biri()
        game_world.add_object(biri, 1)
        game_world.add_collision_pair('nonBullet:monster', None, biri)
        game_world.add_collision_pair('bullet:monster', None, biri)
        game_world.add_collision_pair('player:monster', None, biri)

def update():

    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    userdata.show_status(common.player.hp)
    update_canvas()

def finish():
    for layer in game_world.world:
        for o in layer:
            # collision_pairs에서 해당 오브젝트 제거
            game_world.remove_collision_object(o)
    game_world.clear()

def pause(): pass
def resume(): pass

