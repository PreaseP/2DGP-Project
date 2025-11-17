from pico2d import *
import game_world
import game_framework

playerLevel = [1, 0] # [level, exp]

playerSkill = {'general' : [0,0,0], 'sword' : [0,0], 'gun' : [0,0]}
# 공격력, 체력, 이동속도 / 검 무기 연성 확률, 검 이동 스킬 / 총 무기 연성 확률, 총 이동 스킬

weaponPercent = [(60, 35, 5), (20, 65, 15), (10, 25, 65)] # 무기 연성 확률 리스트

playerWeapon = {'sword' : [0,0], 'gun' : [0,0]} # [검 등급, 강화 정도] / [총 등급, 강화 정도]

makeCost = 100 # 무기 연성 비용
upgradeCost = [50, 100, 200, 400, 800] # 무기 강화 비용

def make_weapon(weapon_type):
    import random
    global playerWeapon
    rand = random.randint(1, 100)
    percent = playerSkill[weapon_type][0]
    if rand <= weaponPercent[percent][0]:
        grade = 1
    elif rand <= weaponPercent[percent][0] + weaponPercent[percent][1]:
        grade = 2
    else:
        grade = 3

    if playerWeapon[weapon_type][0] <= grade:
        playerWeapon[weapon_type][0] = grade

def upgrade_weapon(weapon_type):
    global playerWeapon
    if playerWeapon[weapon_type][1] < 5:
        playerWeapon[weapon_type][1] += 1

# level up에 필요한 경험치 리스트, 총 25 레벨
expList = (0, 100, 200, 300, 400, 500, 600, 700, 800, 900,
           1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800,
           3000, 3500, 4000, 4500, 5000)

playerType = 'S' # 'S' or 'G'
playerGold = 0
playerSkillPoint = 0

def add_exp(exp):
    global playerLevel, playerSkillPoint
    playerLevel[1] += exp
    while playerLevel[0] < len(expList) - 1 and playerLevel[1] >= expList[playerLevel[0]]:
        playerLevel[1] -= expList[playerLevel[0]]
        playerLevel[0] += 1
        playerSkillPoint += 1

def add_gold(gold):
    global playerGold
    playerGold += gold

def spend_gold(gold):
    global playerGold
    if playerGold >= gold:
        playerGold -= gold
        return True
    else:
        return False

gunAtk = [10, 20, 40, 80]

swordAtk = [10, 20, 40, 80]

def show_status():
    global font
    font = load_font('resources/DungGeunMo.TTF', 20)

    font.draw(10, 700, f"Level: {playerLevel[0]}, EXP: {playerLevel[1]}/{expList[playerLevel[0]]}", (255, 0, 0))
    font.draw(10, 670, f"Account: {playerGold}", (255, 215, 0))

# userdata를 json으로 저장

def save_userdata():
    import json
    data = {
        'playerLevel': playerLevel,
        'playerType': playerType,
        'playerGold': playerGold,
        'playerSkillPoint': playerSkillPoint
    }
    with open('userdata.json', 'w') as f:
        json.dump(data, f)

def load_userdata():
    import json
    global playerLevel, playerType, playerGold, playerSkillPoint
    try:
        with open('userdata.json', 'r') as f:
            data = json.load(f)
            playerLevel = data['playerLevel']
            playerType = data['playerType']
            playerGold = data['playerGold']
            playerSkillPoint = data['playerSkillPoint']
    except FileNotFoundError:
        pass