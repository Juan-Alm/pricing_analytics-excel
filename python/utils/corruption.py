# Composable functions to apply selectively per column

import random
import numpy as np
import pandas as pd

from .helpers import sample_indices




# Data type corruption


def numeric_to_string(series: pd.Series, fraction: float):
    """Convert numeric values to strings."""

    series = series.astype(object)  # <-- force object type

    idx = sample_indices(len(series), fraction)

    for i in idx:
        if pd.notna(series.iloc[i]):
            series.iloc[i] = str(series.iloc[i])

    return series


def inject_text_in_numeric(series: pd.Series, fraction: float):
    """Inject text values into numeric columns."""

    series = series.astype(object)  # <-- cast to object to allow strings

    noise = ["N/A", "unknown", "--", "error"]
    idx = sample_indices(len(series), fraction)

    for i in idx:
        series.iloc[i] = random.choice(noise)

    return series


def mixed_numeric_formats(series: pd.Series, fraction: float):
    """Mix numeric representations (int, string, words)."""

    series = series.astype(object)

    word_map = {
        100: "one hundred",
        50: "fifty",
        10: "ten"
    }

    idx = sample_indices(len(series), fraction)

    for i in idx:
        val = series.iloc[i]

        if isinstance(val, (int, float)):
            choice = random.choice(["str", "word", "normal"])

            if choice == "str":
                series.iloc[i] = str(val)
            elif choice == "word" and int(val) in word_map:
                series.iloc[i] = word_map[int(val)]

    return series



# Date corruption


def corrupt_dates(series: pd.Series, fraction: float):
    """Inject invalid or mixed date formats."""
    idx = sample_indices(len(series), fraction)

    series = series.astype(object)

    for i in idx:
        choice = random.choice(["invalid", "format"])

        if choice == "invalid":
            series.iloc[i] = "2024/99/99"
        else:
            series.iloc[i] = pd.Timestamp(series.iloc[i]).strftime(
                random.choice(["%d/%m/%Y", "%m-%d-%Y", "%Y/%m/%d"])
            )

    return series



# Outliers


def inject_outliers(series: pd.Series, fraction: float, multiplier=10):
    """Inject extreme high values."""
    idx = sample_indices(len(series), fraction)

    for i in idx:
        if pd.notna(series.iloc[i]) and isinstance(series.iloc[i], (int, float)):
            series.iloc[i] = series.iloc[i] * multiplier * random.randint(10, 100)

    return series


def inject_negative_values(series: pd.Series, fraction: float):
    """Flip some values to negative."""
    idx = sample_indices(len(series), fraction)

    for i in idx:
        if isinstance(series.iloc[i], (int, float)):
            series.iloc[i] = -abs(series.iloc[i])

    return series


def inject_percentage_errors(series: pd.Series, fraction: float):
    """Create invalid percentage values (e.g. >100%)."""
    idx = sample_indices(len(series), fraction)

    for i in idx:
        series.iloc[i] = random.uniform(1.5, 5.0)  # 150%–500%

    return series



# Key integrity


def break_foreign_keys(series: pd.Series, fraction: float, invalid_pool=None):
    """Inject invalid foreign keys."""

    series = series.astype(object)
    
    idx = sample_indices(len(series), fraction)

    for i in idx:
        if invalid_pool:
            series.iloc[i] = random.choice(invalid_pool)
        else:
            series.iloc[i] = f"INVALID_{random.randint(1000,9999)}"

    return series



# Business logic issues


def inconsistent_prices(df: pd.DataFrame, id_col: str, price_col: str, fraction: float):
    """
    Same ID with different prices.
    """
    idx = sample_indices(len(df), fraction)

    for i in idx:
        df.loc[i, price_col] = df.loc[i, price_col] * random.uniform(0.5, 1.5)

    return df



# Duplication


def duplicate_transactions(df: pd.DataFrame, fraction: float):
    """Duplicate rows to simulate ingestion duplication issues."""
    n = int(len(df) * fraction)
    dup = df.sample(n=n, replace=True)
    return pd.concat([df, dup], ignore_index=True)



# GENERAL PIPELINE


def apply_corruption_pipeline(df: pd.DataFrame, config: dict):
    """
    Apply a configurable corruption pipeline.
    
    config example:
    {
        "numeric_to_string": {"columns": ["units_sold"], "rate": 0.05},
        "inject_text": {"columns": ["price"], "rate": 0.03}
    }
    """

    for rule, params in config.items():
        cols = params.get("columns", [])
        rate = params.get("rate", 0.01)

        for col in cols:
            if col not in df.columns:
                continue

            if rule == "numeric_to_string":
                df[col] = numeric_to_string(df[col], rate)

            elif rule == "inject_text":
                df[col] = inject_text_in_numeric(df[col], rate)

            elif rule == "outliers":
                df[col] = inject_outliers(df[col], rate)

            elif rule == "negative":
                df[col] = inject_negative_values(df[col], rate)

            elif rule == "percentage":
                df[col] = inject_percentage_errors(df[col], rate)

            elif rule == "dates":
                df[col] = corrupt_dates(df[col], rate)

            elif rule == "fk":
                df[col] = break_foreign_keys(df[col], rate)

    return df