# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 11:45:47 2023

Create test data within a secure environment to test the cell key perturbation code
@author: iain dove
"""

import pandas as pd
import numpy as np

def generate_test_data(size = 1000, key_range = 256):
    """
    Function to generate a sample microdata for testing purposes
    
    Parameters:
    -----------
    size : integer
        Number of rows in test data. Default is 1000.
    key_range : integer
        Range for the record key. Default is 256.
        
    Returns:
        - (pd.DataFrame): Sample microdata with record_key
    """

    np.random.seed(111)
    
    record_key_sample = list(np.random.randint(0, key_range, size))
    
    var1 = list(np.random.choice([1,2,3,4,5], p=[0.25, 0.35, 0.2, 0.1, 0.1], size=(size)))
    var2 = list(np.random.choice([1,2], p=[0.5, 0.5], size=(size)))
    var3 = list(np.random.choice([1,2,3,4], p=[0.25, 0.35, 0.2, 0.2], size=(size)))
    var4 = list(np.random.choice([1,2,3,4], p=[0.25, 0.35, 0.2, 0.2], size=(size)))
    var5 = list(np.random.choice([1,2,3,4,5,6,7,8,9,10], p=[0.20, 0.15, 0.08, 0.15, 0.02, 0.025, 0.075, 0.1, 0.1, 0.1], size=(size)))
    var6 = list(np.random.choice([1,2,3,4,5], p=[0.25, 0.35, 0.2, 0.1, 0.1], size=(size)))
    var7 = list(np.random.choice([1,2,3,4,5], p=[0.25, 0.35, 0.2, 0.1, 0.1], size=(size)))
    
    categories_ABCD = ["A", "B", "C", "D"]
    var8 = list(np.random.choice(categories_ABCD,size))
    
    categories_ABCDEFGH = ["A", "B", "C", "D", "E", "F","G","H"]
    var9 = list(np.random.choice(categories_ABCDEFGH,size))
    
    var10 = list(np.random.randint(1,50,size))
    
    micro = pd.DataFrame(
        {'record_key' : record_key_sample,
         'var1': var1,
         'var2': var2,
         'var3': var3,
         'var4': var4,
         'var5': var5,
         'var6': var6,
         'var7': var7,
         'var8': var8,
         'var9': var9,
         'var10': var10
        })

    return micro

