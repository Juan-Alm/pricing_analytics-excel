# Small reusable functions

import random
import numpy as np
import pandas as pd

def set_seed(seed: int):
    """set seed for reproducibility across RNG in the project.
    It takes a single integer that represent the seed value.
    calls the seeding methods from python's and Numpy's "random" module,
    passing the same seed to both"""
    random.seed(seed)
    np.random.seed(seed)

def random_choice_with_none(options, p_none = 0.1):
    """Return a random element from a provided sequence or None.
    It takes the sequence of options and a probability.
    first generates a random float between 0 and 1, if the value is less than the probability, return None.
    Otherwise, select a random element"""
    if random.random() < p_none:
        return None
    return random.choice(options)

def random_string_noise(value, p_noise = 0.2):
    """Introduce small text noise (case changes and typos).
    Takes a value (intended to be a string) and a probability.
    fisrt check if the input is string, if not, return it unchanged.
    Then generate a random number between 0 and 1, if this number exceeds the probability, return the string unchanged.
    Otherwise, selects and returns a random transformation to the string"""
    if not isinstance(value, str):
        return value
    
    if random.random() > p_noise:
        return value
    
    transformations = [
        lambda x: x.upper(),
        lambda x: x.lower(),
        lambda x: x.capitalize(),
        lambda x: x + " ",
        lambda x: x.replace("a", "@"),
        lambda x: x.replace("e", "3")
    ]

    func = random.choice(transformations)
    return func(value)

def sample_indices(n, fraction):
    """return a selected subset of indices based on a specified fraction of the total.
    Takes an integer (n) representing the total number of items, and a fraction.
    First computes the number of indices to select (k), 
    and then use Numpy's random.choice to sample "k" unique integers (0 to n-1)."""
    k = int(n * fraction)
    return np.random.choice(n, k, replace = False)

def introduce_missing(series: pd.Series, fraction: float):
    """injects missing values into a pandas Series (a column) at random positions.
    Takes a Series and a fraction indicating the proportion of values to replace with NaN.
    First obtain random positional indices, then use .iloc to assign np.nan, finally returns the modified Series"""
    idx = sample_indices(len(series), fraction)
    series.iloc[idx] = np.nan
    return series


def introduce_null_like(series: pd.Series, fraction: float):
    """Replace values with common null-like placeholders.
    Compute how many elements to modify by using the length of the Series and the fraction.
    Fist obtain the indeces and then iterate over them assigning a placeholder.
    Return the modified Series"""
    placeholders = ["N/A", "NULL", "unknown", "--", ""]
    idx = sample_indices(len(series), fraction)

    for i in idx:
        series.iloc[i] = random.choice(placeholders)

    return series


def duplicate_rows(df: pd.DataFrame, fraction: float):
    """increases the size of a DataFrame by duplicating a fraction of its rows.
    First calculate the number of rows to duplicate.
    Then uses .sample() to randomly select rows with replacement.
    This sample is stored as a df and then is concatenated with the original df"""
    n = int(len(df) * fraction)
    dup_rows = df.sample(n=n, replace=True)
    return pd.concat([df, dup_rows], ignore_index=True)


def shuffle_series(series: pd.Series):
    """randomly reorders the values of a pandas Series.
    Uses frac=1 to permute all rows and then reset the index."""
    return series.sample(frac=1).reset_index(drop=True)