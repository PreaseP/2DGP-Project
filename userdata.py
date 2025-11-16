playerLevel = [1, 0] # [level, exp]

expList = [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500] # level up에 필요한 경험치 리스트

def add_exp(exp):
    global playerLevel
    playerLevel[1] += exp
    while playerLevel[0] < len(expList) - 1 and playerLevel[1] >= expList[playerLevel[0]]:
        playerLevel[1] -= expList[playerLevel[0]]
        playerLevel[0] += 1

playerType = 'G' # 'S' or 'G'

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