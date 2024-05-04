import pandas as pd
import numpy as np

match = pd.read_csv('20211121-M-Tour_Finals-F-Daniil_Medvedev-Alexander_Zverev.csv')
player1 = {"name":match.iloc[0,0]}
player2 = {"name":match.iloc[0,1]}
player = [player1, player2]
matchLength = match.shape[0]
matchWidth = match.shape[1]

def swtichToPlayer1BasedTable():

    player1pgsdata = pd.DataFrame(np.empty((matchLength,matchWidth)))

    for i in range(matchLength):
        if(match.iloc[i,0] ==  player1["name"]):
            player1pgsdata.iloc[i, :] = match.iloc[i, :]
        elif(match.iloc[i,0] == player2["name"]):
            for j in range(10):
                if(j%2 == 0):
                    player1pgsdata.iloc[i,j] = match.iloc[i, j+1]
                else:
                    player1pgsdata.iloc[i,j] = match.iloc[i, j-1]
            player1pgsdata.iloc[i,10:] = match.iloc[i, 10:]
    return player1pgsdata

# playerIndex = 1 -> player1, index=2->player2
def getPlayerTotalPointsWon(playerIndex):
    player1Based = swtichToPlayer1BasedTable()
    counter = 0
    for i in range(1,matchLength):
        if (player1Based.iloc[i, 3+playerIndex] == (player1Based.iloc[i-1,3+playerIndex]+1)):
            counter = counter + 1
        if (player1Based.iloc[i, 3+playerIndex] == (player1Based.iloc[i-1,3+playerIndex]-3)):
            counter = counter + 1
        if (player1Based.iloc[i, 3+playerIndex] == 3 and (i == matchLength - 1)):
            counter = counter + 1
    return counter

# The annotation is at the shot that results in winning the point
def annotateWinLoseShot():
    player1Based = swtichToPlayer1BasedTable()
    matchWithAnnotation = match.assign(Winmark=0)

    for i in range(1, matchLength):
        if (player1Based.iloc[i, 4] == (player1Based.iloc[i-1,4]+1)):
            matchWithAnnotation.loc[i-1, 'Winmark'] = 1
        if (player1Based.iloc[i, 4] == (player1Based.iloc[i-1,4]-3)):
            matchWithAnnotation.loc[i - 1, 'Winmark'] = 1
        if (player1Based.iloc[i, 4] == 3 and (i == matchLength - 1)):
            matchWithAnnotation.loc[i , 'Winmark'] = 1
        if (player1Based.iloc[i, 5] == (player1Based.iloc[i-1,5]+1)):
            matchWithAnnotation.loc[i-1, 'Winmark'] = -1
        if (player1Based.iloc[i, 5] == (player1Based.iloc[i-1,5]-3)):
            matchWithAnnotation.loc[i - 1, 'Winmark'] = -1
        if (player1Based.iloc[i, 5] == 3 and (i == matchLength - 1)):
            matchWithAnnotation.loc[i , 'Winmark'] = -1

    return matchWithAnnotation

# annotate length of points in player1's view, positive for player1 and negative for player2
# The annotation is at the shot that results in winning the point
def annotateLength():
    player1Based = swtichToPlayer1BasedTable()
    matchWithAnnotation = match.assign(GameLength=0)
    counter = 0

    for i in range(1, matchLength):
        if  (player1Based.iloc[i, 4] == (player1Based.iloc[i-1,4]+1)):
            matchWithAnnotation.loc[i-1, 'GameLength'] = counter
        elif  (player1Based.iloc[i, 4] == (player1Based.iloc[i-1,4]-3)):
            matchWithAnnotation.loc[i-1, 'GameLength'] = counter
        elif  (player1Based.iloc[i, 4] == 3 and (i == matchLength - 1)):
            matchWithAnnotation.loc[i , 'GameLength'] = counter
        elif  (player1Based.iloc[i, 5] == (player1Based.iloc[i-1,5]+1)):
            matchWithAnnotation.loc[i-1, 'GameLength'] = -counter
        elif  (player1Based.iloc[i, 5] == (player1Based.iloc[i-1,5]-3)):
            matchWithAnnotation.loc[i-1, 'GameLength'] = -counter
        elif  (player1Based.iloc[i, 5] == 3 and (i == matchLength - 1)):
            matchWithAnnotation.loc[i , 'GameLength'] = -counter
        else:
            counter = counter + 1

        if (player1Based.iloc[i, 12] == 1 or player1Based.iloc[i, 12] == 2):
            counter = 1

    return matchWithAnnotation
# Break points here are points that one points from winning the game while opponent is serving
# The annotation is at shot that leads to breakserve opportunities
# If player1 gets the break points opportunity, that shot will be marked as 1
# If p..2 gets oppo, that shot .. -1
def annotateBreakPoints():
    matchWithAnnotation = match.assign(BreakPoint=0)
    for i in range(1, matchLength):
        if ((match.iloc[i, 0] == player2['name']) and (match.iloc[i, 4] >= 3) and (match.iloc[i,4]-match.iloc[i,5]>=1) and (match.iloc[i, 12] == 1)):
            matchWithAnnotation.loc[i-1, 'BreakPoint'] = 1
        elif ((match.iloc[i, 0] == player1['name']) and (match.iloc[i, 5] >= 3) and (match.iloc[i,5]-match.iloc[i,4]>=1) and (match.iloc[i, 12] == 1)):
            matchWithAnnotation.loc[i-1, 'BreakPoint'] = -1
    return matchWithAnnotation



# para: [start, end] player's winning chance if the length of point is between this range.
# return: (winning chance, player's number of wins, opponent's number of wins)
def getShotTolerance(start, end, playerIndex):
    matchWithLength = annotateLength()
    if (playerIndex == 1):
        opponentNumberOfWin = sum((-end <= matchWithLength['GameLength']) & (matchWithLength['GameLength'] <= -start))
        playerNumberOfWin = sum((matchWithLength['GameLength'] <= end) & (start <= matchWithLength['GameLength']))
        return playerNumberOfWin, opponentNumberOfWin
    if (playerIndex == 2):
        playerNumberOfWin = sum((-end <= matchWithLength['GameLength']) & (matchWithLength['GameLength'] <= -start))
        opponentNumberOfWin = sum((matchWithLength['GameLength'] <= end) & (start <= matchWithLength['GameLength']))
        return playerNumberOfWin, opponentNumberOfWin


# The index of successful first serve.
def getSuccessfulFirstServeIndex(playerIndex):
    return (match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:,12] == 1) & (match.iloc[:,21] != 2)

# The index of second serve
def getSecondServeIndex(playerIndex):
    return (match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:,12] == 2)

# Represents what is the winning chance if the first serve is successful.
def firstServeWinRate(playerIndex):
    numberOfWin = 0
    successfulFirstServeIndex = getSuccessfulFirstServeIndex(playerIndex)
    annotatedWithWinLose = annotateWinLoseShot()
    for i in range(matchLength):
        if(successfulFirstServeIndex[i] == True):
            j = 0
            while (annotatedWithWinLose.loc[i+j,'Winmark'] == 0):
                j = j+1
            if ((annotatedWithWinLose.loc[i+j,'Winmark'] == 1) and (playerIndex == 1)):
                numberOfWin = numberOfWin + 1
            if ((annotatedWithWinLose.loc[i+j,'Winmark'] == -1) and (playerIndex == 2)):
                numberOfWin = numberOfWin + 1
    return numberOfWin / sum(successfulFirstServeIndex)

# Represents what is the winning chance if has second serve (no mater second serve is fault or not)
def secondServeWinRate(playerIndex):
    numberOfWin = 0
    secondServeIndex = getSecondServeIndex(playerIndex)
    annotatedWithWinLose = annotateWinLoseShot()
    for i in range(matchLength):
        if(secondServeIndex[i] == True):
            j = 0
            while (annotatedWithWinLose.loc[i+j,'Winmark'] == 0):
                j = j+1
            if ((annotatedWithWinLose.loc[i+j,'Winmark'] == 1) and (playerIndex == 1)):
                numberOfWin = numberOfWin + 1
            if ((annotatedWithWinLose.loc[i+j,'Winmark'] == -1) and (playerIndex == 2)):
                numberOfWin = numberOfWin + 1
    return numberOfWin / sum(secondServeIndex),numberOfWin,  sum(secondServeIndex)


#playerIndex = 1: first player, =2 second player
# first player is who serves first serves in entire game
def getNumberofWinner(playerIndex):
    return sum(((match.iloc[:,21] == 1)|(match.iloc[:,21] == 5)|(match.iloc[:,21] == 6)) & (match.iloc[:,0] == player[playerIndex-1]["name"]))

def getNumberOfServe(playerIndex):
    return sum((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:,12] == 1))
def getNumberOfSecondServe(playerIndex):
    return sum((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:,12] == 2))

# Get number of aces and double faults of a player, return (aces, double fault)
def getNumberOfAcesAndDoubleFault(playerIndex):
    return (sum((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:,21] == 1)),
            sum((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:,21] == 2) & (match.iloc[:,12] == 2)))

def storeToPlayer():
    player1["totalPointsWon"] = getPlayerTotalPointsWon(1)
    player2["totalPointsWon"] = getPlayerTotalPointsWon(2)
    player1["NumberOfWinner"] = getNumberofWinner(1)
    player2["NumberOfWinner"] = getNumberofWinner(2)
    player1["OpponentsError"] = player1["totalPointsWon"] - getNumberofWinner(1)
    player2["OpponentsError"] = player2["totalPointsWon"] - getNumberofWinner(2)
    player1["NumberOfServe"] = getNumberOfServe(1)
    player2["NumberOfServe"] = getNumberOfServe(2)
    player1["NumberOfSecondServe"] = getNumberOfSecondServe(1)
    player2["NumberOfSecondServe"] = getNumberOfSecondServe(2)
    player1["FirstServePercentage"] = 1 - player1["NumberOfSecondServe"]/player1["NumberOfServe"]
    player2["FirstServePercentage"] = 1 - player2["NumberOfSecondServe"]/player2["NumberOfServe"]
    player1["FirstServeWonRate"] = firstServeWinRate(1)
    player2["FirstServeWonRate"] = firstServeWinRate(2)
    player1["SecondServeWonRate"] = secondServeWinRate(1)
    player2["SecondServeWonRate"] = secondServeWinRate(2)
    player1["AcesDoubleFault"] = getNumberOfAcesAndDoubleFault(1)
    player2["AcesDoubleFault"] = getNumberOfAcesAndDoubleFault(2)
    player1["ShotTolerance1-4"] = getShotTolerance(1,4,1)
    player1["ShotTolerance5-8"] = getShotTolerance(5,8,1)
    player1["ShotTolerance9-12"] = getShotTolerance(9,12,1)
    player1["ShotTolerance13+"] = getShotTolerance(13,matchLength,1)

# a = annotateLength()
# print(a)
# print(sum((a['GameLength']<5) & (a['GameLength']>0)))
# print(sum((-5<a['GameLength']) & (a['GameLength']<0)))
a = annotateBreakPoints()
print(a)
print(sum(a['BreakPoint']))
storeToPlayer()
print(player1, player2)