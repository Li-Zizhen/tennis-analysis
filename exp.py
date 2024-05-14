import pandas as pd

# Read the CSV file
data = pd.read_csv("20211121-M-Tour_Finals-F-Daniil_Medvedev-Alexander_Zverev.csv", header=None)

# Calculate return statistics
return_stats = data[data[12] == 3].groupby([1, 15]).size().reset_index(name="Count")
return_stats = return_stats.pivot_table(index=1, columns=15, values="Count", fill_value=0)
return_stats.index.name = None
return_stats.columns.name = "RETURN"
return_stats = return_stats.reindex(columns=[1, 2, 99], fill_value=0)
return_stats.columns = ["1st Return Won", "2nd Return Won", "Break Points Converted"]
return_stats.insert(0, "", ["Alexander Zverev", "Danil Medvedev"])
return_stats.iloc[0, 0] = "%"
return_stats.iloc[1, 0] = "#"

# Calculate winners and errors
winners_errors = data.groupby([1, 14, 21]).size().reset_index(name="Count")
winners_errors = winners_errors[(winners_errors[14] <= 20) & (winners_errors[21].isin([3, 4, 5]))]
winners_errors = winners_errors.pivot_table(index=[1, 21], columns=14, values="Count", fill_value=0)
winners_errors.columns = ["1st-Forehand", "1st-Backhand", "2nd-Forehand", "2nd-Backhand"]
winners_errors = winners_errors.unstack(level=1)
winners_errors.columns = winners_errors.columns.swaplevel(0, 1)
winners_errors.sort_index(axis=1, level=0, inplace=True)
winners_errors.columns = ["Deuce Winner", "Deuce Error", "Ad Winner", "Ad Error"]
winners_errors.index.name = None
winners_errors.insert(0, "Winners & Errors", ["1st-Forehand", "1st-Backhand", "2nd-Forehand", "Total"])

# Print the analysis
print("Return Statistics:")
print(return_stats)
print("\nWinners & Errors:")
print(winners_errors)