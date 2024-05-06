import pandas as pd
import numpy as np
import warnings
import pprint
from TennisAnalysisGeneralInfo import getNumberOfAcesAndDoubleFault, getNumberofWinner, getPlayerTotalPointsWon, \
    annotateWinLoseShot, matchLength
from TennisAnalysisGeneralInfo import player1
from TennisAnalysisGeneralInfo import player2
from TennisAnalysisGeneralInfo import match
from TennisAnalysisGeneralInfo import player

warnings.simplefilter(action='ignore', category=FutureWarning)

firstServeSummary = pd.DataFrame(columns=['Info','ADLeft','ADMiddle', 'ADRight', 'DueLeft', 'DueMiddle','DueRight'], index=range(1, 4))
firstServeSummary.loc[1]['Info'] = "Count"
firstServeSummary.loc[2]['Info'] = "Present"
firstServeSummary.loc[3]['Info'] = "Win%"
# As usual the player1 is the player who serve the first, and in the model match it is Daniil
playerIndex = 1
secondServeSummary = firstServeSummary.copy()
def getServeDirectionCount(playerIndex, serveNum):
    def helper(a, b):
        if serveNum == 2:
            return sum((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:, 13] == a) & (
                    match.iloc[:, 15] == b) & (match.iloc[:, 12] == serveNum))
        if serveNum == 1:
            return sum((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:, 13] == a) & (
                    match.iloc[:, 15] == b) & (match.iloc[:, 12] == serveNum) & (match.iloc[:, 21] != 2))

    return [helper(3,4),
            helper(3,5),
            helper(3,6),
            helper(1,6),
            helper(1,5),
            helper(1,4)]
def getServeDirectionPercentage(playerIndex, serveNum):
    adCourt = [x / sum(getServeDirectionCount(playerIndex, serveNum)[0:3]) for x in getServeDirectionCount(playerIndex, serveNum)[0:3]]
    dueCourt = [x / sum(getServeDirectionCount(playerIndex, serveNum)[3:6]) for x in getServeDirectionCount(playerIndex, serveNum)[3:6]]
    return adCourt + dueCourt


def getServeDirectionCountWinChance(playerIndex, serveNum):
    def helper(a, b):
        if serveNum == 2:
            return ((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:, 13] == a) & (
                    match.iloc[:, 15] == b) & (match.iloc[:, 12] == serveNum))
        if serveNum == 1:
            return ((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:, 13] == a) & (
                    match.iloc[:, 15] == b) & (match.iloc[:, 12] == serveNum) & (match.iloc[:, 21] != 2))
    result = []
    for i, j in [[3,4], [3,5],[3,6],[1,6],[1,5],[1,4]]:
        numberOfWin = 0
        successfulFirstServeIndex = helper(i,j)
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
        if (sum(successfulFirstServeIndex) != 0):
            result.append(numberOfWin / sum(successfulFirstServeIndex))
        else:
            result.append(0)
    return result

firstServeSummary.iloc[0][1:7] = getServeDirectionCount(playerIndex, 1)
firstServeSummary.iloc[1][1:7] = getServeDirectionPercentage(playerIndex, 1)
firstServeSummary.iloc[2][1:7] = getServeDirectionCountWinChance(playerIndex, 1)
secondServeSummary.iloc[0][1:7] = getServeDirectionCount(playerIndex, 2)
secondServeSummary.iloc[1][1:7] = getServeDirectionPercentage(playerIndex, 2)
secondServeSummary.iloc[2][1:7] = getServeDirectionCountWinChance(playerIndex, 2)
print(firstServeSummary)
print(secondServeSummary)

