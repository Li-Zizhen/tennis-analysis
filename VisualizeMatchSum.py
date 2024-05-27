import pickle

import pandas as pd
import numpy as np
import warnings
import pprint
from TennisAnalysisGeneralInfo import getNumberOfAcesAndDoubleFault, getNumberofWinner, getPlayerTotalPointsWon

try:
    with open('player_data.pkl', 'rb') as file:
        player1, player2 = pickle.load(file)
except FileNotFoundError:
    from TennisAnalysisGeneralInfo import storeToPlayer
    storeToPlayer()
    with open('player_data.pkl', 'rb') as file:
        player1, player2 = pickle.load(file)
pprint.pprint(player1)
pprint.pprint(player2)
from TennisAnalysisMatchSummary import summary

from TennisAnalysisGeneralInfo import match
from TennisAnalysisGeneralInfo import player
import matplotlib.pyplot as plt

warnings.simplefilter(action='ignore', category=FutureWarning)

# ... (rest of your code remains the same)

# Create a stacked bar chart
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(summary))
width = 0.35

p1 = ax.bar(x - width/2, summary['Player1Winner'], width, label=player1['name'] + ' Winners')
p2 = ax.bar(x - width/2, summary['Player1Error'], width, bottom=summary['Player1Winner'], label=player1['name'] + ' Errors')
p3 = ax.bar(x + width/2, summary['Player2Winner'], width, label=player2['name'] + ' Winners')
p4 = ax.bar(x + width/2, summary['Player2Errors'], width, bottom=summary['Player2Winner'], label=player2['name'] + ' Errors')

ax.set_ylabel('Count')
ax.set_title('Tennis Match Analysis')
ax.set_xticks(x)
ax.set_xticklabels(summary['Info'])
ax.legend()

plt.tight_layout()
plt.show()