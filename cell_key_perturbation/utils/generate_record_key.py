
import numpy as np
import pandas as pd


def generate_record_key_from_ons_id(data, record_key_col):
    """
    Function to generate record key from ons_id by taking modulo 4096.

    - Converts 'ons_id' to numeric by allowing null values.
    - Uses pandas nullable integer dtype ('Int64') to keep missing values.
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Microdata with ons_id to calculate record keys

    Returns
    -------
    df: pd.DataFrame
        DataFrame with 'ons_record_key' added
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError("data must be a pandas DataFrame")
    
    df = data.copy()
    ons_id_numeric = pd.to_numeric(df["ons_id"], errors="coerce")
    df[record_key_col] = (ons_id_numeric % 4096).astype("Int64")

    return df


def generate_random_rkey(data):
    """
    Function to create and attach random record keys to microdata
    
    Parameters:
    -----------
    data : pandas.DataFrame
        Microdata to add random record keys
        
    Returns:
    --------
    df : pandas.DataFrame
        Microdata with record_keys column added
    """
    seed = 2025                                 
    rng = np.random.default_rng(seed)
    
    df = data.copy()
    size = len(df.index)
    
    record_key_sample = list(rng.integers(low = 0, high = 256, size = size))
    
    df["record_key"] = record_key_sample
    
    return df

