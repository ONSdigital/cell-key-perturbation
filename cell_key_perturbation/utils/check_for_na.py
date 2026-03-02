# -*- coding: utf-8 -*-


import pandas as pd

def check_for_na(df, cols):
    """
    Check DataFrame for missingness in specified tabulation variables.

    Parameters
    ----------
    df : pandas.DataFrame
        Perturbed frequency table.
    cols : list of str
        Tabulation variables to check.

    Returns
    -------
    None
        Emits a warning if any column contains missing values.
    """

    # Identify columns with at least one missing value
    na_cols = [col for col in cols if df[col].isna().any()]

    # Issue a warning if any NA columns were found
    if na_cols:
        print("Warning: "
            "Missing values detected in the following variable(s): {}\n"
            "Consider removing frequencies for missing values "
            "from the output table."
            .format(", ".join(na_cols))
        )
