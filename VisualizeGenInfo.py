import pickle
import pprint

import matplotlib.pyplot as plt
# from TennisAnalysisGeneralInfo import storeToPlayer, player1, player2


# Call the function to generate the analysis data
# storeToPlayer()

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
# Function to visualize the tennis analysis
def visualize_tennis_analysis():
    fig, axs = plt.subplots(2, 4, figsize=(16, 10))
    fig.subplots_adjust(hspace=0.2, wspace=0.2)

    # Total Points Won
    total_points = player1["totalPointsWon"] + player2["totalPointsWon"]
    axs[0, 0].pie([player1["totalPointsWon"] / total_points * 100, player2["totalPointsWon"] / total_points * 100],
                  labels=[f"{player1['name']} ({player1['totalPointsWon']})", f"{player2['name']} ({player2['totalPointsWon']})"], autopct='%1.0f%%')
    axs[0, 0].set_title("Total Points Won")
    # Shot Tolerance
    shot_tolerance_labels = ["1-4", "5-8", "9-12", "13+"]
    player1_shot_tolerance = [player1["ShotTolerance1-4"][0], player1["ShotTolerance5-8"][0],
                              player1["ShotTolerance9-12"][0], player1["ShotTolerance13+"][0]]
    player2_shot_tolerance = [player1["ShotTolerance1-4"][1], player1["ShotTolerance5-8"][1],
                              player1["ShotTolerance9-12"][1], player1["ShotTolerance13+"][1]]

    axs[0, 1].bar(shot_tolerance_labels, player1_shot_tolerance, label=player1["name"])
    axs[0, 1].bar(shot_tolerance_labels, player2_shot_tolerance, bottom=player1_shot_tolerance, label=player2["name"])

    # Add numbers on top of each column
    for i, v in enumerate(player2_shot_tolerance):
        axs[0, 1].text(i, v + player2_shot_tolerance[i], str(v), ha='center', va='bottom')

    for i, v in enumerate(player1_shot_tolerance):
        axs[0, 1].text(i, v, str(v), ha='center', va='top')

    axs[0, 1].set_title("Shot Tolerance")
    axs[0, 1].legend()

    # Winners & Errors
    total_winners_errors = player1["NumberOfWinner"] + player2["NumberOfWinner"] + player1["OpponentsError"] + player2[
        "OpponentsError"]
    axs[0, 2].pie(
        [player1["NumberOfWinner"], player2["NumberOfWinner"], player1["OpponentsError"], player2["OpponentsError"]],
        labels=[f"{player1['name']} Winners",
                f"{player2['name']} Winners",
                f"{player1['name']} Opp Errors",
                f"{player2['name']} Opp Errors"],
        autopct=lambda pct: f"{pct:.0f}%\n({int(round(pct / 100. * total_winners_errors))})")
    axs[0, 2].set_title("Winners & Errors")

    # 1st Serve %
    axs[1, 0].bar(player1["name"], player1["FirstServePercentage"] * 100, color='#1F77B4')
    axs[1, 0].bar(player2["name"], player2["FirstServePercentage"] * 100, color='#FF7F0E')
    axs[1, 0].text(0, player1["FirstServePercentage"] * 100, f"{player1['FirstServePercentage']:.0%}", ha='center',
                   va='bottom')
    axs[1, 0].text(1, player2["FirstServePercentage"] * 100, f"{player2['FirstServePercentage']:.0%}", ha='center',
                   va='bottom')
    axs[1, 0].set_title("1st Serve %")
    axs[1, 0].set_ylim(0, 100)
    axs[1, 0].legend()

    # 1st Serves Won
    axs[1, 1].bar(player1["name"], player1["FirstServeWonRate"] * 100, color='#1F77B4')
    axs[1, 1].bar(player2["name"], player2["FirstServeWonRate"] * 100, color='#FF7F0E')
    axs[1, 1].text(0, player1["FirstServeWonRate"] * 100, f"{player1['FirstServeWonRate']:.0%}", ha='center',
                   va='bottom')
    axs[1, 1].text(1, player2["FirstServeWonRate"] * 100, f"{player2['FirstServeWonRate']:.0%}", ha='center',
                   va='bottom')
    axs[1, 1].set_title("1st Serves Won")
    axs[1, 1].set_ylim(0, 100)
    # axs[1, 1].legend()

    # 2nd Serves Won
    axs[1, 2].bar(player1["name"], player1["SecondServeWonRate"][0] * 100, color='#1F77B4')
    axs[1, 2].bar(player2["name"], player2["SecondServeWonRate"][0] * 100, color='#FF7F0E')
    axs[1, 2].text(0, player1["SecondServeWonRate"][0] * 100, f"{player1['SecondServeWonRate'][0]:.0%}", ha='center',
                   va='bottom')
    axs[1, 2].text(1, player2["SecondServeWonRate"][0] * 100, f"{player2['SecondServeWonRate'][0]:.0%}", ha='center',
                   va='bottom')
    axs[1, 2].set_title("2nd Serves Won")
    axs[1, 2].set_ylim(0, 100)
    # axs[1, 2].legend()

    # Break Points Saved
    # axs[1, 3].bar(["Player 1", "Player 2"], [player1["NumberOfBreakPointSaved,Faced"][0] / player1["NumberOfBreakPointSaved,Faced"][1] * 100 if player1["NumberOfBreakPointSaved,Faced"][1] > 0 else 0,
    #                                            player2["NumberOfBreakPointSaved,Faced"][0] / player2["NumberOfBreakPointSaved,Faced"][1] * 100 if player2["NumberOfBreakPointSaved,Faced"][1] > 0 else 0])
    # axs[1, 3].set_title("Break Points Saved")
    # axs[1, 3].set_ylim(0, 100)

    # Aces & Double Faults
    axs[0, 3].bar(["Aces", "DF"], [player1["AcesDoubleFault"][0], player1["AcesDoubleFault"][1]], label=player1["name"])
    axs[0, 3].bar(["Aces", "DF"], [player2["AcesDoubleFault"][0], player2["AcesDoubleFault"][1]], label=player2["name"])
    axs[0, 3].set_title("Aces & Double Faults")
    # axs[0, 3].legend()

    # # 1st Return Won
    # axs[2, 1].pie([26, 100 - 26], labels=["Won", "Lost"], autopct='%1.0f%%')
    # axs[2, 1].set_title("1st Return Won")
    #
    # # 2nd Return Won
    # axs[2, 2].pie([48, 100 - 48], labels=["Won", "Lost"], autopct='%1.0f%%')
    # axs[2, 2].set_title("2nd Return Won")
    # Break Points Converted
    if player1["NumberOfBreakPointSaved,Faced"][1] > 0:
        player1_break_points_converted = player1["NumberOfBreakPointSaved,Faced"][0] / \
                                         player1["NumberOfBreakPointSaved,Faced"][1] * 100
        axs[1, 3].bar(player1["name"], player1_break_points_converted, color='#0070C0', label=player1["name"])
        axs[1, 3].text(0, player1_break_points_converted,
                       f"{player1['NumberOfBreakPointSaved,Faced'][0]}/{player1['NumberOfBreakPointSaved,Faced'][1]}\n({player1_break_points_converted:.0f}%)",
                       ha='center', va='bottom')
    else:
        axs[1, 3].bar(player1["name"], 0, color='#0070C0', label=player1["name"])
        axs[1, 3].text(0, 0, "N/A", ha='center', va='bottom')

    if player2["NumberOfBreakPointSaved,Faced"][1] > 0:
        player2_break_points_converted = player2["NumberOfBreakPointSaved,Faced"][0] / \
                                         player2["NumberOfBreakPointSaved,Faced"][1] * 100
        axs[1, 3].bar(player2["name"], player2_break_points_converted, color='#FF9900', label=player2["name"])
        axs[1, 3].text(1, player2_break_points_converted,
                       f"{player2['NumberOfBreakPointSaved,Faced'][0]}/{player2['NumberOfBreakPointSaved,Faced'][1]}\n({player2_break_points_converted:.0f}%)",
                       ha='center', va='bottom')
    else:
        axs[1, 3].bar(player2["name"], 0, color='#FF9900', label=player2["name"])
        axs[1, 3].text(1, 0, "N/A", ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

# Call the function to visualize the tennis analysis
visualize_tennis_analysis()