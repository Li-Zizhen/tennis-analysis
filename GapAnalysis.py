import numpy as np

from TennisAnalysisGeneralInfo import match, player, storeToPlayer, player1, player2, getShotTolerance, matchLength, \
    firstServeWinRate, secondServeWinRate
import matplotlib.pyplot as plt
player1["ShotTolerance1-4"] = getShotTolerance(1, 4, 1)
player1["ShotTolerance5-8"] = getShotTolerance(5, 8, 1)
player1["ShotTolerance9-12"] = getShotTolerance(9, 12, 1)
player1["ShotTolerance13+"] = getShotTolerance(13, matchLength, 1)
player1["FirstServeWonRate"] = firstServeWinRate(1)
player2["FirstServeWonRate"] = firstServeWinRate(2)
player1["SecondServeWonRate"] = secondServeWinRate(1)
player2["SecondServeWonRate"] = secondServeWinRate(2)
# Data from the table
categories = ['Pts Won 13+', 'Pts Won 9-12', 'Pts Won 5-8', 'Pts Won 1-4', '2srv Won - All',  '1srv Won - All']
# zverev_data = [player1["ShotTolerance13+"][0],  player1["ShotTolerance9-12"][0],  player1["ShotTolerance5-8"][0],  player1["ShotTolerance1-4"][0], player1["SecondServeWonRate"][0],player1["FirstServeWonRate"]]
# medvedev_data = [player1["ShotTolerance13+"][1],  player1["ShotTolerance9-12"][1],  player1["ShotTolerance5-8"][1],  player1["ShotTolerance1-4"][1], player2["SecondServeWonRate"][0],player2["FirstServeWonRate"]]
#

player1Data = [
    player1["ShotTolerance13+"][0] / (player1["ShotTolerance13+"][0] + player1["ShotTolerance13+"][1]) * 100,
    player1["ShotTolerance9-12"][0] / (player1["ShotTolerance9-12"][0] + player1["ShotTolerance9-12"][1]) * 100,
    player1["ShotTolerance5-8"][0] / (player1["ShotTolerance5-8"][0] + player1["ShotTolerance5-8"][1]) * 100,
    player1["ShotTolerance1-4"][0] / (player1["ShotTolerance1-4"][0] + player1["ShotTolerance1-4"][1]) * 100,
    player1["SecondServeWonRate"][0]*100,
    player1["FirstServeWonRate"]*100
]

player2Data = [
    player1["ShotTolerance13+"][1] / (player1["ShotTolerance13+"][0] + player1["ShotTolerance13+"][1]) * 100,
    player1["ShotTolerance9-12"][1] / (player1["ShotTolerance9-12"][0] + player1["ShotTolerance9-12"][1]) * 100,
    player1["ShotTolerance5-8"][1] / (player1["ShotTolerance5-8"][0] + player1["ShotTolerance5-8"][1]) * 100,
    player1["ShotTolerance1-4"][1] / (player1["ShotTolerance1-4"][0] + player1["ShotTolerance1-4"][1]) * 100,
    player2["SecondServeWonRate"][0]*100,
    player2["FirstServeWonRate"]*100
]
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='polar')

# Set the angles for each category
angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)

# Concatenate the angles to close the polygon
angles = np.concatenate((angles, [angles[0]]))

# Concatenate the data for Zverev and Medvedev to close the polygon
player1Data = player1Data + [player1Data[0]]
player2Data = player2Data + [player2Data[0]]

# Plot the data for Zverev and Medvedev
ax.plot(angles, player1Data, 'o-', linewidth=2,color='red', label=player1["name"])
ax.plot(angles, player2Data, 'o-', linewidth=2,color='green', label=player2["name"])

# Fill the area under the curves
ax.fill(angles, player1Data, alpha=0.25)
ax.fill(angles, player2Data, alpha=0.25)

# Set the category labels
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)

# Rotate the labels to align with the angles
ax.tick_params(axis='x', pad=30)

# Set the radial limits
ax.set_rlim(0, 100)

# Set the radial tick positions and labels
ax.set_rticks([20, 40, 60, 80, 100])
ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'])

# Add gridlines
ax.grid(True)

# Add a title and legend
ax.set_title("Rally Length Analysis", va='bottom')
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

# Display the plot
plt.tight_layout()
plt.show()