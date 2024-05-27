import pandas as pd
import numpy as np
import warnings
import pprint
import pickle

from util import annotateWE

warnings.simplefilter(action='ignore', category=FutureWarning)
match = pd.read_csv('20211121-M-Tour_Finals-F-Daniil_Medvedev-Alexander_Zverev.csv', header = None)

num_columns = len(match.columns)
default_columns = [f'Column{i+1}' for i in range(num_columns)]
match.columns = default_columns

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
    # player1Based = swtichToPlayer1BasedTable()
    # counter = 0
    # for i in range(1,matchLength):
    #     if (player1Based.iloc[i, 3+playerIndex] == (player1Based.iloc[i-1,3+playerIndex]+1)):
    #         counter = counter + 1
    #     if (player1Based.iloc[i, 3+playerIndex] <= (player1Based.iloc[i-1,3+playerIndex]-3)):
    #         counter = counter + 1
    #     if (playerIndex == 1):
    #         if (player1Based.iloc[i, 3+playerIndex] >= player1Based.iloc[i, 4+playerIndex] and (i == matchLength - 1)):
    #             counter = counter + 1
    #     if (playerIndex == 2):
    #         if (player1Based.iloc[i, 3 + playerIndex] >= player1Based.iloc[i, 2 + playerIndex] and (i == matchLength - 1)):
    #             counter = counter + 1
    # return counter
    if (playerIndex == 1):
        return sum(annotateWinLoseShot()['Winmark'] == 1)


    if (playerIndex == 2):
        return sum(annotateWinLoseShot()['Winmark'] == -1)


# The annotation is at the shot that results in winning the point
def annotateWinLoseShot():
    player1Based = swtichToPlayer1BasedTable()
    matchWithAnnotation = match.assign(Winmark=0)

    for i in range(1, matchLength):
        if (player1Based.iloc[i, 4] == (player1Based.iloc[i-1,4]+1)):
            matchWithAnnotation.loc[i-1, 'Winmark'] = 1
        elif ((player1Based.iloc[i, 4] <= (player1Based.iloc[i-1,4]-3)) and (player1Based.iloc[i-1, 4] >  player1Based.iloc[i-1, 5])):
            matchWithAnnotation.loc[i - 1, 'Winmark'] = 1
        elif (player1Based.iloc[i, 4] >=  player1Based.iloc[i, 5]  and (i == (matchLength - 1))):
            matchWithAnnotation.loc[i , 'Winmark'] = 1
        elif (player1Based.iloc[i, 5] == (player1Based.iloc[i-1,5]+1)):
            matchWithAnnotation.loc[i-1, 'Winmark'] = -1
        elif ((player1Based.iloc[i, 5] <= (player1Based.iloc[i-1,5]-3)) and (player1Based.iloc[i-1, 4] <  player1Based.iloc[i-1, 5])):
            matchWithAnnotation.loc[i - 1, 'Winmark'] = -1
        elif (player1Based.iloc[i, 5] >= player1Based.iloc[i, 4] and (i == (matchLength - 1))):
            matchWithAnnotation.loc[i , 'Winmark'] = -1

    return matchWithAnnotation
def annotateWinLoseSet():
    player1Based = swtichToPlayer1BasedTable()
    matchWithAnnotation = match.assign(SetWinmark=0)

    for i in range(1, matchLength):
        if (player1Based.iloc[i, 6] == (player1Based.iloc[i-1,6]+1)):
            matchWithAnnotation.loc[i-1, 'SetWinmark'] = 1
        if (player1Based.iloc[i, 6] <= (player1Based.iloc[i-1,6]-5)):
            matchWithAnnotation.loc[i - 1, 'SetWinmark'] = 1
        if (player1Based.iloc[i, 6] >=player1Based.iloc[i, 7] and (i == matchLength - 1)):
            matchWithAnnotation.loc[i , 'SetWinmark'] = 1
        if (player1Based.iloc[i, 7] == (player1Based.iloc[i-1,7]+1)):
            matchWithAnnotation.loc[i-1, 'SetWinmark'] = -1
        if (player1Based.iloc[i, 7] <= (player1Based.iloc[i-1,7]-5)):
            matchWithAnnotation.loc[i - 1, 'SetWinmark'] = -1
        if (player1Based.iloc[i, 7] >= player1Based.iloc[i, 6] and (i == matchLength - 1)):
            matchWithAnnotation.loc[i , 'SetWinmark'] = -1

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
# However, if the game continued and become 4:3 this will also be marked.(little bug)
def annotateBreakPoints():
    matchWithAnnotation = match.assign(BreakPoint=0)
    for i in range(1, matchLength):
        if ((match.iloc[i, 5] >= 3) and (match.iloc[i,5]-match.iloc[i,4]>=1) and (match.iloc[i, 12] == 1)):
            if ((match.iloc[i, 0] == player2['name'])):
                matchWithAnnotation.loc[i-1, 'BreakPoint'] = 1
            elif ((match.iloc[i, 0] == player1['name'])):
                matchWithAnnotation.loc[i-1, 'BreakPoint'] = -1
    return matchWithAnnotation

# return (number of saved bp, total number of bp faced)
def numberOfBreakPointsSaved(playerIndex):
    annotatedMatchWithBP = annotateBreakPoints()
    annotatedSetWithWinLose = annotateWinLoseSet()
    if (playerIndex == 1):
        numberOfSave = 0
        for i in range(matchLength):
            if (annotatedMatchWithBP.loc[i, 'BreakPoint'] == -1):
                j = 0
                while (annotatedSetWithWinLose.loc[i + j, 'SetWinmark'] == 0):
                    j = j + 1
                if ((annotatedSetWithWinLose.loc[i + j, 'SetWinmark'] == 1) ):
                    numberOfSave = numberOfSave + 1
        return numberOfSave, sum(annotatedMatchWithBP['BreakPoint']==-1)

    if (playerIndex == 2):
        numberOfSave = 0
        for i in range(matchLength):
            if (annotatedMatchWithBP.loc[i, 'BreakPoint']  == 1):
                j = 0
                while (annotatedSetWithWinLose.loc[i + j, 'SetWinmark'] == 0):
                    j = j + 1
                if ((annotatedSetWithWinLose.loc[i + j, 'SetWinmark'] == -1)):
                    numberOfSave = numberOfSave + 1
        return numberOfSave, sum(annotatedMatchWithBP['BreakPoint']==1)


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

# the opponent below is from player1's perspective.
def getShotToleranceBreakDown(start, end):
    matchWithLength = annotateLength()
    annotatedMatch = annotateWE(matchWithLength)
    opponentNumberOfWinByWinner = sum((-end <= annotatedMatch['GameLength']) & (annotatedMatch['GameLength'] <= -start) & (annotatedMatch['WE'] == 1) )
    opponentNumberOfWinByOppError = sum((-end <= annotatedMatch['GameLength']) & (annotatedMatch['GameLength'] <= -start) & (annotatedMatch['WE'] == -1) )

    playerNumberOfWinByWinner = sum((annotatedMatch['GameLength'] <= end) & (start <= annotatedMatch['GameLength'])  & (annotatedMatch['WE'] == 1))
    playerNumberOfWinByOppError= sum((annotatedMatch['GameLength'] <= end) & (start <= annotatedMatch['GameLength'])  & (annotatedMatch['WE'] == -1))
    return playerNumberOfWinByWinner, playerNumberOfWinByOppError, opponentNumberOfWinByWinner, opponentNumberOfWinByOppError


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

    # player2["ShotTolerance1-4"] = getShotTolerance(1,4,2)

    # player2["ShotTolerance5-8"] = getShotTolerance(5,8,2)
    # player2["ShotTolerance9-12"] = getShotTolerance(9,12,2)
    # player2["ShotTolerance13+"] = getShotTolerance(13,matchLength,2)

    player1["NumberOfBreakPointSaved,Faced"] = numberOfBreakPointsSaved(1)
    player2["NumberOfBreakPointSaved,Faced"] = numberOfBreakPointsSaved(2)
    with open('player_data.pkl', 'wb') as file:
        pickle.dump((player1, player2), file)


# storeToPlayer()
# with open('player_data.pkl', 'rb') as file:
#     player1, player2 = pickle.load(file)
# pprint.pprint(player1)
# pprint.pprint(player2)
# print(getShotToleranceBreakDown(1, 4))
# print(getShotToleranceBreakDown(5, 8))
# print(getShotToleranceBreakDown(9, 12))
# print(getShotToleranceBreakDown(13, matchLength))
