import pickle
import pprint

import pandas as pd
import warnings
from TennisAnalysisGeneralInfo import getNumberOfAcesAndDoubleFault, getNumberofWinner, getPlayerTotalPointsWon

from TennisAnalysisGeneralInfo import match
# from TennisAnalysisGeneralInfo import player

# Below code is use to cache the result from tennis general info
try:
    with open('player_data.pkl', 'rb') as file:
        player1, player2 = pickle.load(file)
except FileNotFoundError:
    from TennisAnalysisGeneralInfo import storeToPlayer
    storeToPlayer()
    with open('player_data.pkl', 'rb') as file:
        player1, player2 = pickle.load(file)
player = [player1, player2]
pprint.pprint(player1)
pprint.pprint(player2)
warnings.simplefilter(action='ignore', category=FutureWarning)

summary = pd.DataFrame(columns=['Player1Winner','Player1Error', 'Info', 'Player2Winner', 'Player2Errors'], index=range(1, 7))
summary.loc[1]['Info'] = "Serve"
summary.loc[2]['Info'] = "Return"
summary.loc[3]['Info'] = "Serve+1"
summary.loc[4]['Info'] = "Return+1"
summary.loc[5]['Info'] = "Last Shot(5+)"
summary.loc[6]['Info'] = "Total"

def getNumOfWinnerErrorInReturn(playerIndex):
    return (sum((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:,21] == 5) & (match.iloc[:,12] == 3)),
            sum((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & match.iloc[:, 21].isin([3, 4]) & (match.iloc[:,12] == 3)))

def getNumOfWinnerErrorInServePlusOne(playerIndex):
    return (sum((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:, 21] == 5) & (match.iloc[:,23] == 3) & (match.iloc[:,12] == 4)),
            sum((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & match.iloc[:, 21].isin([3, 4]) & (match.iloc[:,23] == 3) & (match.iloc[:,12] == 4)))

def getNumOfWinnerErrorInReturnPlusOne(playerIndex):
    return (sum((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & (match.iloc[:, 21] == 5) & (match.iloc[:,34] == 3) & (match.iloc[:,23] == 4) & (match.iloc[:,12] == 4)),
            sum((match.iloc[:, 0] == player[playerIndex - 1]["name"]) & match.iloc[:, 21].isin([3, 4]) & (match.iloc[:,34] == 3) & (match.iloc[:,23] == 4) & (match.iloc[:,12] == 4)))

summary.iloc[0][0:2] = getNumberOfAcesAndDoubleFault(1)
summary.iloc[0][3:5] = getNumberOfAcesAndDoubleFault(2)
summary.iloc[1][0:2] = getNumOfWinnerErrorInReturn(1)
summary.iloc[1][3:5] = getNumOfWinnerErrorInReturn(2)
summary.iloc[2][0:2] = getNumOfWinnerErrorInServePlusOne(1)
summary.iloc[2][3:5] = getNumOfWinnerErrorInServePlusOne(2)
summary.iloc[3][0:2] = getNumOfWinnerErrorInReturnPlusOne(1)
summary.iloc[3][3:5] = getNumOfWinnerErrorInReturnPlusOne(2)

summary.iloc[5][0:2] = (getNumberofWinner(1), getPlayerTotalPointsWon(2)-getNumberofWinner(2))
summary.iloc[5][3:5] = (getNumberofWinner(2), getPlayerTotalPointsWon(1)-getNumberofWinner(1))

# Because the 5+ is gotten from total sub others, it is dependent.
summary.iloc[4][0:2] = summary.iloc[5][0:2] - summary.iloc[3][0:2] - summary.iloc[2][0:2] - summary.iloc[1][0:2] -  summary.iloc[0][0:2]
summary.iloc[4][3:5] = summary.iloc[5][3:5] - summary.iloc[3][3:5] - summary.iloc[2][3:5] - summary.iloc[1][3:5] -  summary.iloc[0][3:5]

print(summary)

