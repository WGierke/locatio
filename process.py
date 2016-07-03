import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def read_data(file_name):
    """Read DataFrame"""
    file_path_full = os.getcwd() + '/data/' + file_name

    if os.path.isfile(file_path_full):
        return pd.DataFrame.from_csv(file_path_full, sep=';')

def replace_nan_with_empty(df):
    for col in df.columns.values:
        df[col] = df[col].apply(lambda x: str(x).replace(str(x), '') if isinstance(x, float) and math.isnan(x) else x) 
    return df

def clean_data(df):
    print("Data Cleaning")
    print("Removing NaN columns")
    # Drop NaN columns
    for col in df.columns.values:
        row_count = len(df[col])
        nan_count = df[col].isnull().sum()
        if row_count == nan_count:
            print(col + " only contains NaNs")
            df = df.drop(col, 1)
    return df

def get_processed_data(file_name):
    df = read_data(file_name)
    df = clean_data(df)
    return df

def visualize_unknown_data(df):
    known = []
    unknown = []

    for col in df.columns.values:
        unknown_count = df[col].isnull().sum()
        unknown.append(unknown_count)
        known_count = len(df[col]) - df[col].isnull().sum()
        known.append(known_count)

    N = len(df.columns)
    ind = np.arange(N)
    width = 0.5

    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 18
    plt.rcParams["figure.figsize"] = fig_size
    plt.style.use('seaborn-dark-palette')

    p1 = plt.bar(ind, known, width, color='r')
    p2 = plt.bar(ind, unknown, width, color='b', bottom=known)

    plt.ylabel('Entries')
    plt.title('Unknown and Known Entries')
    plt.xticks(ind + width/2., df.columns.values)
    plt.legend((p1[0], p2[0]), ('Known', 'Unknown'))
    plt.show()