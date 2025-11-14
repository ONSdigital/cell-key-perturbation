
import numpy as np


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

