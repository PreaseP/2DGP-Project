import random
from pico2d import *

import cockpit_mode
import death_mode
import pause_menu
from general_stage import GeneralStage
from keese import Keese as monster2
from players import PlayerS
from playerg import PlayerG
from biri import Biri as monster1
from relic import Relic
from wraith import Wraith as monster3

import game_framework
import game_world
import userdata

import common

phaseClear = False
font = None

def spawn_monster(num):
    if num == 0:
        for _ in range(5):
            mob = monster1()
            game_world.add_object(mob, 1)
            game_world.add_collision_pair('nonBullet:monster', None, mob)
            game_world.add_collision_pair('bullet:monster', None, mob)
            game_world.add_collision_pair('player:monster', None, mob)
        for _ in range(2):
            mob = monster2()
            game_world.add_object(mob, 1)
            game_world.add_collision_pair('nonBullet:monster', None, mob)
            game_world.add_collision_pair('bullet:monster', None, mob)
            game_world.add_collision_pair('player:monster', None, mob)
        common.monsterCount = 7
    elif num == 1:
        for _ in range(2):
            mob = monster1()
            game_world.add_object(mob, 1)
            game_world.add_collision_pair('nonBullet:monster', None, mob)
            game_world.add_collision_pair('bullet:monster', None, mob)
            game_world.add_collision_pair('player:monster', None, mob)
        for _ in range(5):
            mob = monster2()
            game_world.add_object(mob, 1)
            game_world.add_collision_pair('nonBullet:monster', None, mob)
            game_world.add_collision_pair('bullet:monster', None, mob)
            game_world.add_collision_pair('player:monster', None, mob)
        for _ in range(1):
            mob = monster3()
            game_world.add_object(mob, 1)
            game_world.add_collision_pair('nonBullet:monster', None, mob)
            game_world.add_collision_pair('bullet:monster', None, mob)
            game_world.add_collision_pair('player:monster', None, mob)
        common.monsterCount = 8
    elif num == 2:
        for _ in range(4):
            mob = monster2()
            game_world.add_object(mob, 1)
            game_world.add_collision_pair('nonBullet:monster', None, mob)
            game_world.add_collision_pair('bullet:monster', None, mob)
            game_world.add_collision_pair('player:monster', None, mob)
        for _ in range(6):
            mob = monster3()
            game_world.add_object(mob, 1)
            game_world.add_collision_pair('nonBullet:monster', None, mob)
            game_world.add_collision_pair('bullet:monster', None, mob)
            game_world.add_collision_pair('player:monster', None, mob)
        common.monsterCount = 10
    elif num == 3:
        common.monsterCount = -1  # 마지막 스테이지, 몬스터 없음

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
    global font, small_font, bgm
    font = load_font('resources/DungGeunMo.TTF', 50)
    small_font = load_font('resources/DungGeunMo.TTF', 20)
    bgm = load_music('resources/sound/stage1.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()

    common.playing = False

    common.map = GeneralStage('stage1')
    game_world.add_object(common.map, 0)

    common.map.left_border = 0
    common.map.right_border = 1

    if userdata.playerType == 'S':
        common.player = PlayerS()
    else:
        common.player = PlayerG()

    common.player.x = get_canvas_width() / 2
    common.player.y = get_canvas_height() / 2

    game_world.add_object(common.player, 1)
    game_world.add_collision_pair('player:monster', common.player, None)
    game_world.add_collision_pair('player:relic', common.player, None)

    relic = Relic(type=1)
    game_world.add_object(relic, 1)
    game_world.add_collision_pair('player:relic', None, relic)

    spawn_monster(common.map.left_border)

def update():
    global phaseClear

    if common.monsterCount == 0 and phaseClear == False:
        phaseClear = True
        common.map.right_border += 1

    if phaseClear == True and common.player.x >= common.borders[common.map.right_border] - 640:
        phaseClear = False
        common.map.left_border += 1
        spawn_monster(common.map.left_border)

    if common.player.hp == 0:
        game_framework.push_mode(death_mode)

    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    userdata.show_status(common.player.hp)

    if phaseClear:
        # 우측 상단에 'GO!' 표시
        font.draw(1100, 650, 'GO!', (255, 0, 0))

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

