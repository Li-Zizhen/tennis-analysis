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

def annotateWinLoseShot():
    player1Based = swtichToPlayer1BasedTable()
    matchWithAnnotation = match.assign(Winmark=0)

    for i in range(1, matchLength):
        if (player1Based.iloc[i, 4] == (player1Based.iloc[i-1,4]+1)):
            matchWithAnnotation.loc[i-1, 'Winmark'] = 1
        if (player1Based.iloc[i, 4] == (player1Based.iloc[i-1,4]-3)):
            matchWithAnnotation.loc[i - 1, 'Winmark'] = 1
        if (player1Based.iloc[i, 4] == 3 and (i == matchLength - 1)):
            matchWithAnnotation.loc[i - 1, 'Winmark'] = 1
    for i in range(1, matchLength):
        if (player1Based.iloc[i, 5] == (player1Based.iloc[i-1,5]+1)):
            matchWithAnnotation.loc[i-1, 'Winmark'] = -1
        if (player1Based.iloc[i, 5] == (player1Based.iloc[i-1,5]-3)):
            matchWithAnnotation.loc[i - 1, 'Winmark'] = -1
        if (player1Based.iloc[i, 5] == 3 and (i == matchLength - 1)):
            matchWithAnnotation.loc[i - 1, 'Winmark'] = -1

    return matchWithAnnotation
def getSuccessfulFirstServeIndex(playerIndex):
    return (match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:,12] == 1) & (match.iloc[:,21] != 2)

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



#playerIndex = 1: first player, =2 second player
# first player is who serves first serves in entire game
def getNumberofWinner(playerIndex):
    return sum(((match.iloc[:,21] == 1)|(match.iloc[:,21] == 5)|(match.iloc[:,21] == 6)) & (match.iloc[:,0] == player[playerIndex-1]["name"]))

def getNumberOfServe(playerIndex):
    return sum((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:,12] == 1))
def getNumberOfSecondServe(playerIndex):
    return sum((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:,12] == 2))
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


storeToPlayer()
a = annotateWinLoseShot()
b = getSuccessfulFirstServeIndex(1)
c = firstServeWinRate(2)
print(c)
print(player1, player2)