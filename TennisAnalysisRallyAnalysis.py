import pandas as pd
import warnings
from TennisAnalysisGeneralInfo import getNumberOfAcesAndDoubleFault, getNumberofWinner, getPlayerTotalPointsWon, \
    annotateWinLoseShot, matchLength
from TennisAnalysisGeneralInfo import match
from TennisAnalysisGeneralInfo import player
from util import annotateBFhands, annotateWE

warnings.simplefilter(action='ignore', category=FutureWarning)

vallySummary = pd.DataFrame(columns=['ad court', 'middle court', 'deuce court', 'Info'], index=range(1, 7))
vallySummary.loc[1]['Info'] = "shortCount"
vallySummary.loc[2]['Info'] = "shortPresent"
vallySummary.loc[3]['Info'] = "deepCount"
vallySummary.loc[4]['Info'] = "deepPresent"
vallySummary.loc[5]['Info'] = "veryDeepCount"
vallySummary.loc[6]['Info'] = "veryDeepPresent"

# As usual the player1 is the player who serve the first, and in the model match it is Daniil

def filter(colIndex, targetValue):
    return (match.iloc[:, colIndex] == targetValue)

def getRallyDirectionDepthCount(playerIndex, depth):
    def helper(direction, depth):
            return sum((match.iloc[:, 0] == player[playerIndex - 1]["name"])
                       & filter(16, direction) & filter(12, 4)
                       & filter(17, depth))
    return [helper(direction, depth) for direction in range(3, 0, -1) ]
def getRallyDirectionPercentage(playerIndex, depth):
    totalNumberOfVally= sum([sum(getRallyDirectionDepthCount(playerIndex, dep)) for dep in range(1, 4)])

    serveDirctionPercentage = [x / totalNumberOfVally if totalNumberOfVally!=0 else 0 for x in getRallyDirectionDepthCount(playerIndex, depth)]

    return serveDirctionPercentage

def showReturnAnalysis(playerIndex):
    for i in [0, 2, 4]:
        vallySummary.iloc[i][0:3] = getRallyDirectionDepthCount(playerIndex, (i/2)+1)
    for i in [1, 3, 5]:
        vallySummary.iloc[i][0:3] = getRallyDirectionPercentage(playerIndex, (i//2)+1)
    print(player[playerIndex - 1]["name"] + ":")
    print('------------Vally analysis')
    print(vallySummary)

showReturnAnalysis(1)
showReturnAnalysis(2)

# we: winner 1, error -1
# BFhands fh 0, bh, 1

def getWEByHandsandApproach(BFhands, playerIndex):
    matchWithHandsAnnotation = annotateBFhands(match)
    matchWithWEAnnotation = annotateWE(match)
    return sum((matchWithWEAnnotation.loc[:, 'WE'] == 1)
               & (match.iloc[:, 0] == player[playerIndex - 1]["name"])
               & (filter(12, 4))
               & (matchWithHandsAnnotation.loc[:, 'BFhands'] == BFhands)
               & (filter(20, 1))) , sum((matchWithWEAnnotation.loc[:, 'WE'] == -1)
               & (match.iloc[:, 0] == player[playerIndex - 1]["name"])
               & (filter(12, 4))
               & (matchWithHandsAnnotation.loc[:, 'BFhands'] == BFhands)
               & (filter(20, 1)))


# after watching the raw data, I found the winner only exist 1 for alex. tennis abstract or analytics may be wrong.
def getWEByHands(BFhands, playerIndex):
    matchWithHandsAnnotation = annotateBFhands(match)
    matchWithWEAnnotation = annotateWE(match)
    def helper(we):
        return sum((matchWithWEAnnotation.loc[:, 'WE'] == we)
               & (match.iloc[:, 0] == player[playerIndex - 1]["name"])
               & (filter(12, 4))
               & (matchWithHandsAnnotation.loc[:, 'BFhands'] == BFhands)
               )
    return helper(1), helper(-1)

def getWEByHandsandVolley(BFhands, playerIndex):
    matchWithWEAnnotation = annotateWE(match)
    def helper(we):
        bfhand = 26 if BFhands == 0 else 5
        return sum((matchWithWEAnnotation.loc[:, 'WE'] == we)
               & (match.iloc[:, 0] == player[playerIndex - 1]["name"])
               & (filter(12, 4))
                & (filter(14, bfhand))
               )
    return helper(1), helper(-1)
def getWEByHandsandType(shotType1, shotType2, playerIndex):
    matchWithWEAnnotation = annotateWE(match)
    def helper(we):
        return sum((matchWithWEAnnotation.loc[:, 'WE'] == we)
               & (match.iloc[:, 0] == player[playerIndex - 1]["name"])
               & (filter(12, 4))
                & (filter(14, shotType1) | filter(14, shotType2))
               )
    return helper(1), helper(-1)
data = {
    'Player1Winners': [0]*10,
    'Player1Errors': [0]*10,
    '': ['Forehand', 'Backhand', 'FH Approach', 'BH Approach', 'FH Volley', 'BH Volley', 'Overhead', 'Dropshot', 'Lob', 'Total'],
    'Player2Winners': [0] * 10,
    'Player2Errors': [0] * 10,
}
vallyShotTypeAna = pd.DataFrame(data)
for i, (hand, playerNum) in enumerate([(0, 1), (0, 2), (1, 1), (1, 2)]):
    vallyShotTypeAna.loc[vallyShotTypeAna.index[2 + i // 2], [f'Player{playerNum}Winners', f'Player{playerNum}Errors']] = getWEByHandsandApproach(hand, playerNum)
    # print(getWEByHandsandApproach(hand, playerNum))

for i, (hand, playerNum) in enumerate([(0, 1), (0, 2), (1, 1), (1, 2)]):
    vallyShotTypeAna.loc[vallyShotTypeAna.index[i // 2], [f'Player{playerNum}Winners', f'Player{playerNum}Errors']] = getWEByHands(hand, playerNum)
    # print(getWEByHands(hand, playerNum))
for i, (hand, playerNum) in enumerate([(0, 1), (0, 2), (1, 1), (1, 2)]):
    vallyShotTypeAna.loc[vallyShotTypeAna.index[4+ i // 2], [f'Player{playerNum}Winners', f'Player{playerNum}Errors']] = getWEByHandsandVolley(hand, playerNum)
    # print(getWEByHands(hand, playerNum))
for i, (shotType1,shotType2, playerNum) in enumerate([(7,28, 1), (7, 28, 2), (9, 30, 1), (9, 30, 2)]):
    vallyShotTypeAna.loc[vallyShotTypeAna.index[6+ i // 2], [f'Player{playerNum}Winners', f'Player{playerNum}Errors']] = getWEByHandsandType(shotType1,shotType2, playerNum)
    # print(getWEByHands(hand, playerNum))

vallyShotTypeAna.loc[vallyShotTypeAna.index[8], [f'Player1Winners',
                                                          f'Player1Errors']] = getWEByHandsandType(11, 32,
                                                                                                             1)
vallyShotTypeAna.loc[vallyShotTypeAna.index[8], [f'Player2Winners',
                                                 f'Player2Errors']] = getWEByHandsandType(11, 32,
                                                                                                    2)
# vallyShotTypeAna = vallyShotTypeAna.astype(int)
vallyShotTypeAna.iloc[9, 0:2] = vallyShotTypeAna.iloc[:-1, 0:2].sum()
vallyShotTypeAna.iloc[9, 3:5] = (vallyShotTypeAna.iloc[:-1, 3:5].sum())
integer_columns = ['Player1Winners', 'Player1Errors', 'Player2Winners','Player2Errors']
vallyShotTypeAna[integer_columns] = vallyShotTypeAna[integer_columns].astype(int)

print(vallyShotTypeAna)

