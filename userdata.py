from pico2d import *
import game_world
import game_framework

playerLevel = [1, 0] # [level, exp]

# level up에 필요한 경험치 리스트, 총 35 레벨
expList = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900,
           1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800,
           3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500,
           8000, 8500, 9000, 9500, 10000, 11000, 12000]

def add_exp(exp):
    global playerLevel
    playerLevel[1] += exp
    while playerLevel[0] < len(expList) - 1 and playerLevel[1] >= expList[playerLevel[0]]:
        playerLevel[1] -= expList[playerLevel[0]]
        playerLevel[0] += 1

playerType = 'S' # 'S' or 'G'

playerGold = 0

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
        'playerGold': playerGold
    }
    with open('userdata.json', 'w') as f:
        json.dump(data, f)

def load_userdata():
    import json
    global playerLevel, playerType, playerGold
    try:
        with open('userdata.json', 'r') as f:
            data = json.load(f)
            playerLevel = data['playerLevel']
            playerType = data['playerType']
            playerGold = data['playerGold']
    except FileNotFoundError:
        pass