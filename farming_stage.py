import random
from pico2d import *

import cockpit_mode
import death_mode
import pause_menu
from farming_map import FarmingMap
from players import PlayerS
from playerg import PlayerG
from slime import Slime
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
            game_framework.push_mode(pause_menu)
        else:
            common.player.handle_event(event)

def init():
    global small_font, bgm
    common.map = FarmingMap()
    game_world.add_object(common.map, 0)

    small_font = load_font('resources/DungGeunMo.TTF', 20)

    global spawn_timer
    spawn_timer = 5.0

    if userdata.playerType == 'S':
        common.player = PlayerS()
    else:
        common.player = PlayerG()
    game_world.add_object(common.player, 1)
    game_world.add_collision_pair('player:monster', common.player, None)

    slimes = [Slime(random.choice([random.randint(40, 400), random.randint(800, 1240)]), random.choice([random.randint(20, 200), random.randint(500, 700)]))
                     for _ in range (10)]
    for slime in slimes:
        game_world.add_collision_pair('nonBullet:monster', None, slime)
        game_world.add_collision_pair('bullet:monster', None, slime)
        game_world.add_collision_pair('player:monster', None, slime)
    game_world.add_objects(slimes, 1)

    bgm = load_music('resources/sound/farming.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()

    common.playing = False

def update():
    global spawn_timer

    spawn_timer += game_framework.frame_time

    if spawn_timer >= 10.0:
        new_slime = [Slime(random.choice([random.randint(-300, -150), random.randint(1280 + 150, 1280 + 300)]), random.choice([random.randint(-240, -120), random.randint(720 + 120, 720 + 240)]))
                     for _ in range (5)]
        game_world.add_objects(new_slime, 1)
        for slime in new_slime:
            game_world.add_collision_pair('nonBullet:monster', None, slime)
            game_world.add_collision_pair('bullet:monster', None, slime)
            game_world.add_collision_pair('player:monster', None, slime)
        spawn_timer = 0.0

    if common.player.hp == 0:
        game_framework.push_mode(death_mode)
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    userdata.show_status(common.player.hp, common.player.max_hp)

    if userdata.playerType == 'S':
        if common.player.dash_time > 0.0:
            small_font.draw(480, 80, f'이동 스킬 재사용 대기시간 : {common.player.dash_time:.1f}초', (0, 255, 0))
    else:
        if common.player.slide_time > 0.0:
            small_font.draw(480, 80, f'이동 스킬 재사용 대기시간 : {common.player.slide_time:.1f}초', (0, 255, 0))

    if common.player.weapon_time > 0.0:
        small_font.draw(480, 100, f'무기 스킬 대기시간 : {common.player.weapon_time:.1f}초', (255, 0, 0))

    update_canvas()


def finish():
    for layer in game_world.world:
        for o in layer:
            # collision_pairs에서 해당 오브젝트 제거
            game_world.remove_collision_object(o)
    game_world.clear()

def pause(): pass
def resume(): pass

