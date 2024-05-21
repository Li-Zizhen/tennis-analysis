import pandas as pd
import warnings
from TennisAnalysisGeneralInfo import getNumberOfAcesAndDoubleFault, getNumberofWinner, getPlayerTotalPointsWon, \
    annotateWinLoseShot, matchLength
from TennisAnalysisGeneralInfo import match
from TennisAnalysisGeneralInfo import player
from util import annotateBFhands, annotateWE

warnings.simplefilter(action='ignore', category=FutureWarning)

firstReturnSummary = pd.DataFrame(columns=[ 'ad court', 'middle court', 'deuce court', 'Info'], index=range(1, 4))
firstReturnSummary.loc[1]['Info'] = "Count"
firstReturnSummary.loc[2]['Info'] = "Present"
firstReturnSummary.loc[3]['Info'] = "Win%"
secondReturnSummary = firstReturnSummary.copy()

# As usual the player1 is the player who serve the first, and in the model match it is Daniil

def filter(colIndex, targetValue):
    return (match.iloc[:, colIndex] == targetValue)
def getReturnDirectionCount(playerIndex, serveNum):
    def helper(a):
            return sum((match.iloc[:, 0] == player[playerIndex - 1]["name"])
                       & filter(16, a) & filter(12, 3)
                       & filter(23, serveNum))
    return [helper(a) for a in range(3, 0, -1)]
def getReturnDirectionPercentage(playerIndex, serveNum):
    serveDirctionPercentage= [x / sum(getReturnDirectionCount(playerIndex, serveNum))
                              for x in getReturnDirectionCount(playerIndex, serveNum)]
    return serveDirctionPercentage

def getReturnDirectionCountWinChance(playerIndex, serveNum):
    def helper(a):
            return ((match.iloc[:, 0] == player[playerIndex - 1]["name"])
                       & filter(16, a) & filter(12, 3)
                       & filter(23, serveNum))
    result = []
    for j in [3,2,1]:
        numberOfWin = 0
        returnIndex = helper(j)
        annotatedWithWinLose = annotateWinLoseShot()
        for i in range(matchLength):
            if(returnIndex[i] == True):
                j = 0
                while (annotatedWithWinLose.loc[i+j,'Winmark'] == 0):
                    j = j+1
                if ((annotatedWithWinLose.loc[i+j,'Winmark'] == 1) and (playerIndex == 1)):
                    numberOfWin = numberOfWin + 1
                if ((annotatedWithWinLose.loc[i+j,'Winmark'] == -1) and (playerIndex == 2)):
                    numberOfWin = numberOfWin + 1
        if (sum(returnIndex) != 0):
            result.append(numberOfWin / sum(returnIndex))
        else:
            result.append(0)
    return result
def showReturnAnalysis(playerIndex):
    firstReturnSummary.iloc[0][0:3] = getReturnDirectionCount(playerIndex, 1)
    firstReturnSummary.iloc[1][0:3] = getReturnDirectionPercentage(playerIndex, 1)
    firstReturnSummary.iloc[2][0:3] = getReturnDirectionCountWinChance(playerIndex, 1)
    secondReturnSummary.iloc[0][0:3] = getReturnDirectionCount(playerIndex, 2)
    secondReturnSummary.iloc[1][0:3] = getReturnDirectionPercentage(playerIndex, 2)
    secondReturnSummary.iloc[2][0:3] = getReturnDirectionCountWinChance(playerIndex, 2)
    print(player[playerIndex - 1]["name"] + ":")
    print('------------first return analysis')
    print(firstReturnSummary)
    print('------------second return analysis')
    print(secondReturnSummary)

# firstReturnWEHands = pd.DataFrame(columns=['p1 deuce winner', 'p1 deuce error', 'p1 ad winner', 'p1 ad error','Winner&Errors', 'p2 deuce winner', 'p2 deuce error', 'p2 ad winner', 'p2 ad error'], index=range(1, 5))
# firstReturnWEHands.loc[1]['Winner&Errors'] = "1st-Forehand"
# firstReturnWEHands.loc[2]['Winner&Errors'] = "1st-Backhand"
# firstReturnWEHands.loc[3]['Winner&Errors'] = "2nd-Forehand"
# firstReturnWEHands.loc[4]['Winner&Errors'] = "2nd-Backhand"

# court: ad 3, mid 2, deuce 1
# we: winner 1, error -1
# numServe: return first serve 1, re.. 2
# BFhands fh 0, bh, 1
def getWEByHandsAndServeNum(court, we, serveNum, BFhands, playerIndex):
    matchWithHandsAnnotation = annotateBFhands(match)
    matchWithWEAnnotation = annotateWE(match)
    return sum((filter(16, court) & (matchWithWEAnnotation.loc[:, 'WE'] == we)
               & (match.iloc[:, 0] == player[playerIndex - 1]["name"]) & filter(23, serveNum)
               & filter(12, 3) & (matchWithHandsAnnotation.loc[:, 'BFhands'] == BFhands)))
showReturnAnalysis(1)
showReturnAnalysis(2)
# print(getWEByHandsAndServeNum(3, 3,1, 1, 2))
for playerIndex in [1,2]:
    print(player[playerIndex-1]["name"])
    for serveNum in [1,2]:
        print("  serveNum" + str(serveNum))
        for hands in [0,1]:
            hand = "forehand" if hands==0 else "backhand"
            print("    hands: "+ hand)
            for court in [1,2,3]:
                for we in [1, -1]:
                    print("winner " if we == 1 else "Error ", getWEByHandsAndServeNum(court, we, serveNum, hands, playerIndex) ,end = "  ")
            print("")

