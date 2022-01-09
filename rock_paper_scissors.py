# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
#关进问题应该还是在于转移矩阵如何建立
#可能是关注的太少，只关注最后两个，可能还不太科学，需要进一步改进。

import random

#定义赢输平次数？
winEas,loseEas,tieEas = 0.0,0.0,0.0

#定义字典，不知何用？看上去像最后两次出拳，赢输平
buildTMatrix = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}
buildTMatrixL = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}
buildTMatrixT = {'rr': 1, 'rp': 1, 'rs': 1, 'pr': 1, 'pp': 1, 'ps': 1, 'sr': 1, 'sp': 1, 'ss': 1}

#定义t矩阵形状，3行3列，初始值为零，赢输平
n = 3
m = 3
tMatrix = [[0] * m for i in range(n)]
tMatrixL = [[0] * m for i in range(n)]
tMatrixT = [[0] * m for i in range(n)]

#石头剪刀布的初始概率都是1/3
probabilitiesRPS = [1/3,1/3,1/3]

machineChoice = 0

def player(prev_play, opponent_history=[]):
    #采用全局概率
    global probabilitiesRPS
    global machineChoice
    
    opponent_history.append(prev_play)
    
    
    if len(opponent_history)>2:
        #为什么要用两种出拳表达？
        choices = ["Rock","Paper","Scissors"]
        choi = ['r','p','s']

        coresp_dict={"R":0,"P":1,"S":2}

        if (opponent_history[-1]!='') & (opponent_history[-2]!=''):
          prevChoice = coresp_dict[opponent_history[-2]]
          choice = coresp_dict[opponent_history[-1]]

          #输入0代表石头，1代表布，2代表剪刀

          #判断上次输赢
          result = checkWin(choice,machineChoice,1)
              #根据本次出拳，上次出拳，以及上次结果，建立转移概率
          transMatrix = buildTransitionProbabilities(prevChoice,choice,result)
          #U机器出拳定义为1-100之间整数？
          machineChoice = random.randint(1, 100)
          #更新出拳概率
          probabilitiesRPS[0] = transMatrix[prevChoice][0]
          probabilitiesRPS[1] = transMatrix[prevChoice][1]
          probabilitiesRPS[2] = transMatrix[prevChoice][2]
          #不明白为何这么算
          rangeR = probabilitiesRPS[0] * 100
          rangeP = probabilitiesRPS[1] * 100 + rangeR
          #给出了出拳规则,把120转换为RPS
          if (machineChoice <= rangeR):
              machineChoice = 1
              return "P"
          elif (machineChoice <= rangeP):
              machineChoice = 2
              return "S"
          else:
              machineChoice = 0
              return "R"
        else:
          return "S" #一共8个，起不了决定性作用
    else:
        return "R" #一共2个，起不了决定性作用

#建立转移矩阵，得先知道输赢，那就应该是上次输赢
def buildTransitionProbabilities(pC,c,winloss):
    #这是全局参数
    global buildTMatrix
    global buildTMatrixL
    global buildTMatrixT
    #又定义了一遍
    choi = ['r','p','s']
    #更新最初定义的字典
    if winloss == "Win!":
        for i, x in buildTMatrix.items():
            #具体赋值过程还看不太懂，pC什么意思？
            if ('%s%s' % (choi[pC],choi[c]) == i):
                buildTMatrix['%s%s' % (choi[pC], choi[c])] += 1
    elif winloss == "Tied!":
        for i, x in buildTMatrixT.items():
            if ('%s%s' % (choi[pC],choi[c]) == i):
                buildTMatrixT['%s%s' % (choi[pC], choi[c])] += 1
    else:
        for i, x in buildTMatrixL.items():
            if ('%s%s' % (choi[pC],choi[c]) == i):
                buildTMatrixL['%s%s' % (choi[pC], choi[c])] += 1
    return buildTransitionMatrix(winloss)

#建立转移矩阵
def buildTransitionMatrix(winlosstwo):
    #采用全局变量
    global tMatrix
    global tMatrixL
    global tMatrixT
    
    #如果赢了，如何建立矩阵
    if winlosstwo == "Win!":
        rock = buildTMatrix['rr'] + buildTMatrix['rs'] +buildTMatrix['rp']
        paper = buildTMatrix['pr'] + buildTMatrix['ps'] +buildTMatrix['pp']
        scissors = buildTMatrix['sr'] + buildTMatrix['ss'] +buildTMatrix['sp']
        choi = ['r','p','s']
        #看不懂这个循环是如何更新矩阵的
        for row_index, row in enumerate(tMatrix):
            for col_index, item in enumerate(row):
                a = int(buildTMatrix['%s%s' % (choi[row_index],choi[col_index])])
                if (row_index == 0):
                    c = a/rock
                elif (row_index == 1):
                    c = a/paper
                else:
                    c = a/scissors
                row[col_index] = float(c)
        return (tMatrix)
    
    elif winlosstwo == "Tied!":
        rock = buildTMatrixT['rr'] + buildTMatrixT['rs'] +buildTMatrixT['rp']
        paper = buildTMatrixT['pr'] + buildTMatrixT['ps'] +buildTMatrixT['pp']
        scissors = buildTMatrixT['sr'] + buildTMatrixT['ss'] +buildTMatrixT['sp']
        choi = ['r','p','s']
        for row_index, row in enumerate(tMatrixT):
            for col_index, item in enumerate(row):
                a = int(buildTMatrixT['%s%s' % (choi[row_index],choi[col_index])])
                if (row_index == 0):
                    c = a/rock
                elif (row_index == 1):
                    c = a/paper
                else:
                    c = a/scissors
                row[col_index] = float(c)
        return (tMatrixT)

    else:
        rock = buildTMatrixL['rr'] + buildTMatrixL['rs'] +buildTMatrixL['rp']
        paper = buildTMatrixL['pr'] + buildTMatrixL['ps'] +buildTMatrixL['pp']
        scissors = buildTMatrixL['sr'] + buildTMatrixL['ss'] +buildTMatrixL['sp']
        choi = ['r','p','s']
        for row_index, row in enumerate(tMatrixL):
            for col_index, item in enumerate(row):
                a = int(buildTMatrixL['%s%s' % (choi[row_index],choi[col_index])])
                if (row_index == 0):
                    c = a/rock
                elif (row_index == 1):
                    c = a/paper
                else:
                    c = a/scissors
                row[col_index] = float(c)
        return (tMatrixL)

#检查输赢，根据对方出拳，机器出拳，模式检查输赢
def checkWin(user, machine, mode):
    win = False
    tie = False
    if (user == 0):
        if (machine == 2):
            win = True
            tie = False
        elif (machine == 1):
            win = False
            tie = False
        elif (user == 0):
            tie = True
        else:
            print ("Something wierd happened and machine was: %s" % machine)
    elif (user == 1):
        if (machine == 0):
            win = True
            tie = False
        elif (machine == 2):
            win = False
            tie = False
        elif (machine == 1):
            tie = True
        else:
            print ("Something wierd happened and machine was: %s" % machine)
    else:
        if (machine == 1):
            win = True
            tie = False
        elif (machine == 0):
            win = False
            tie = False
        elif (machine == 2):
            tie = True
        else:
            print ("Something wierd happened and machine was: %s" % machine)

    if (tie == True):
        checkStats(2, mode)
        return "Tied!"
    elif (win):
        checkStats(0, mode)
        return "Win!"
    else:
        checkStats(1, mode)
        return "Lose!"

#检查状态，就是输赢次数
def checkStats(wlt,modeChosen):
    global winEas
    global loseEas
    global tieEas

    if (modeChosen == 1):
        if (wlt == 0):
            winEas += 1
        elif (wlt == 1):
            loseEas += 1
        else:
            tieEas += 1
