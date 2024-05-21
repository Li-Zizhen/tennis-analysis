# import pandas as pd
#
# playerIndex = 1
# data = {
#     'Winners': [0]*10,
#     'Errors': [0]*10,
#     '': [''] * 10,
#     'shot Type': ['Forehand', 'Backhand', 'FH Approach', 'BH Approach', 'FH Volley', 'BH Volley', 'Overhead', 'Dropshot', 'Lob', 'Total'],
# }
#
# df = pd.DataFrame(data)
# print(df)


import pandas as pd

# Read the data from the Excel file
df =pd.read_csv('20211121-M-Tour_Finals-F-Daniil_Medvedev-Alexander_Zverev.csv', header = None)

# Function to categorize shots based on the shot code
def categorize_shot(shot_code):
    if shot_code in [1, 3, 5, 7, 9, 11, 13, 15]:
        return 'Forehand'
    elif shot_code in [22, 24, 26, 28, 30, 32, 34, 36]:
        return 'Backhand'
    elif shot_code in [2, 4, 6, 8, 10, 12, 14, 16]:
        return 'FH Approach'
    elif shot_code in [23, 25, 27, 29, 31, 33, 35, 37]:
        return 'BH Approach'
    elif shot_code in [17, 19]:
        return 'FH Volley'
    elif shot_code in [38, 40]:
        return 'BH Volley'
    elif shot_code == 18:
        return 'Overhead'
    elif shot_code == 20:
        return 'Dropshot'
    elif shot_code == 21:
        return 'Lob'
    else:
        return 'Unknown'

# Function to count winners and errors for each player and shot type
def count_stats(player_name):
    player_shots = df.loc[df['Player 1 name'] == player_name, ['Shot', 'Shot outcome']]
    shot_counts = {}
    for shot_type in ['Forehand', 'Backhand', 'FH Approach', 'BH Approach', 'FH Volley', 'BH Volley', 'Overhead', 'Dropshot', 'Lob']:
        shot_counts[shot_type] = {'Winners': 0, 'Errors': 0}

    for _, row in player_shots.iterrows():
        shot_code = row['Shot']
        shot_type = categorize_shot(shot_code)
        outcome = row['Shot outcome']
        if outcome == 5:  # Winner
            shot_counts[shot_type]['Winners'] += 1
        elif outcome in [3, 4]:  # Forced error, Unforced error
            shot_counts[shot_type]['Errors'] += 1

    return shot_counts

# Calculate stats for each player
zverev_stats = count_stats('Alexander Zverev')
medvedev_stats = count_stats('Daniil Medvedev')

# Create a DataFrame from the calculated stats
stats_df = pd.DataFrame({
    'Winner': ['Forehand', 'Backhand', 'FH Approach', 'BH Approach', 'FH Volley', 'BH Volley', 'Overhead', 'Dropshot', 'Lob', 'Total'],
    'Errors': [zverev_stats['Forehand']['Errors'], zverev_stats['Backhand']['Errors'], zverev_stats['FH Approach']['Errors'],
               zverev_stats['BH Approach']['Errors'], zverev_stats['FH Volley']['Errors'], zverev_stats['BH Volley']['Errors'],
               zverev_stats['Overhead']['Errors'], zverev_stats['Dropshot']['Errors'], zverev_stats['Lob']['Errors'], sum(zverev_stats[shot]['Errors'] for shot in zverev_stats)],
    'Winners': [''] + [zverev_stats[shot]['Winners'] for shot in ['Forehand', 'Backhand', 'FH Approach', 'BH Approach', 'FH Volley', 'BH Volley', 'Overhead', 'Dropshot', 'Lob']] + [''],
    '': [''] * 10,
    'Winner': [medvedev_stats['Forehand']['Winners'], medvedev_stats['Backhand']['Winners'], medvedev_stats['FH Approach']['Winners'],
               medvedev_stats['BH Approach']['Winners'], medvedev_stats['FH Volley']['Winners'], medvedev_stats['BH Volley']['Winners'],
               medvedev_stats['Overhead']['Winners'], medvedev_stats['Dropshot']['Winners'], medvedev_stats['Lob']['Winners'], sum(medvedev_stats[shot]['Winners'] for shot in medvedev_stats)],
    'Errors': [medvedev_stats['Forehand']['Errors'], medvedev_stats['Backhand']['Errors'], medvedev_stats['FH Approach']['Errors'],
               medvedev_stats['BH Approach']['Errors'], medvedev_stats['FH Volley']['Errors'], medvedev_stats['BH Volley']['Errors'],
               medvedev_stats['Overhead']['Errors'], medvedev_stats['Dropshot']['Errors'], medvedev_stats['Lob']['Errors'], sum(medvedev_stats[shot]['Errors'] for shot in medvedev_stats)]
})

# Set the index of the DataFrame
stats_df = stats_df.set_index([15, '', 'Forehand', 'Backhand', 'FH Approach', 'BH Approach', 'FH Volley', 'BH Volley', 'Overhead', 'Dropshot', 'Lob', 'Total'])

# Assign player names
stats_df.loc[:9, 'Winners'] = 'Alexander Zverev'
stats_df.loc[:9, 'Errors'] = 'Alexander Zverev'
stats_df.loc[11:, 'Winner'] = 'Daniil Medvedev'
stats_df.loc[11:, 'Errors'] = 'Daniil Medvedev'

print(stats_df)