import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from TennisAnalysisGeneralInfo import match, player
from util import annotateWE

def calculate_momentum(set_num):
    matchAnnocatedwithWE = annotateWE(match)
    set_data = matchAnnocatedwithWE[matchAnnocatedwithWE.iloc[:,8] + matchAnnocatedwithWE.iloc[:,9] == set_num - 1]
    p1_momentum = []
    p2_momentum = []
    p1_score = 0
    p2_score = 0
    for _, row in set_data.iterrows():
        if row['WE'] == 1:  # Winner
            if row[0] == player[0]["name"]:
                p1_score += 1
            else:
                p2_score += 1
            p1_momentum.append(p1_score)
            p2_momentum.append(p2_score)
        elif row['WE'] == -1:  # Error
            if row[0] == player[0]["name"]:
                p2_score += 1
            else:
                p1_score += 1
            p2_momentum.append(p2_score)
            p1_momentum.append(p1_score)
    return p1_momentum, p2_momentum


# Extract player names
player1 = player[0]["name"]
player2 = player[1]["name"]

# Calculate momentum for each set
set1_p1_momentum, set1_p2_momentum = calculate_momentum( 1)
set2_p1_momentum, set2_p2_momentum = calculate_momentum( 2)

# Create subplots for each set
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Plot momentum for Set 1
ax1.plot([b-a for a, b in zip(set1_p1_momentum, set1_p2_momentum)] ,marker='o', color='blue', label=player1)
# ax1.plot(set1_p2_momentum, marker='o', color='red', label=player2)
ax1.set_xlabel('Points')
ax1.set_ylabel('Momentum')
ax1.set_title('Set 1')
ax1.legend()

# Plot momentum for Set 2
ax2.plot([b-a for a, b in zip(set2_p1_momentum, set2_p2_momentum)],marker='o', color='blue', label=player1)
# ax2.plot(set2_p2_momentum, marker='o', color='red', label=player2)
ax2.set_xlabel('Points')
ax2.set_ylabel('Momentum')
ax2.set_title('Set 2')
ax2.legend()

plt.tight_layout()
plt.show()