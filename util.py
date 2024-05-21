import pandas as pd

def shiftColumnByIndex(df, column_index, n):
    """
    Shifts a column in the DataFrame down by n positions based on column index and creates a new column to indicate the shifted column.

    Args:
        df (pd.DataFrame): The DataFrame to be modified.
        column_index (int): The index of the column to shift.
        n (int): The number of positions to shift the column down.

    Returns:
        pd.DataFrame: The DataFrame with the shifted column.
    """
    # Validate column index
    if column_index < 0 or column_index >= len(df.columns):
        raise IndexError(f"Column index {column_index} is out of bounds.")

    # Create an empty Series to maintain shape
    fill = pd.Series([None] * n)

    # Shift the specified column
    df['shifted'] = pd.concat([fill, df.iloc[:, column_index][:-n]], ignore_index=True)

    return df

# 0 is forehand, 1 is backhand
def annotateBFhands(df):
    matchWithAnnotation = df.assign(BFhands=0)
    condition1 = (df.iloc[:, 14] >= 0) & (df.iloc[:, 14] < 20)
    matchWithAnnotation.loc[condition1, 'BFhands'] = 0
    condition2 = (df.iloc[:, 14] >= 21) & (df.iloc[:, 14] <= 40)
    matchWithAnnotation.loc[condition2, 'BFhands'] = 1
    return matchWithAnnotation

# Winner 1, error -1
def annotateWE(df): # annoate winner or forced/unforced error
    matchWithAnnotation = df.assign(WE=0)
    condition1 = (df.iloc[:, 21] == 5)
    matchWithAnnotation.loc[condition1, 'WE'] = 1
    condition2 = (df.iloc[:, 21] == 3) | (df.iloc[:, 21] == 4)
    matchWithAnnotation.loc[condition2, 'WE'] = -1
    return matchWithAnnotation

# need annoate with col: first return, second return, vally length,