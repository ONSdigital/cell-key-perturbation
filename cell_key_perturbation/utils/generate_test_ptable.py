# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 11:44:42 2025

@author: aydina
"""

import pandas as pd
import itertools

def generate_ptable_10_5_rule(max_pcv = 750, key_range = 255):
    """
    Function to generate a sample p-table based on 10-5 rule
    
    Parameters:
    -----------
    max_pcv : integer
        Max value for pcv. Default is 750.
    key_range : integer
        Range for the cell key. Default is 255.
        
    Returns:
        - (pd.DataFrame): Perturbation table with columns 'pcv','ckey','pvalue'
    """
    # Generate all combinations of pcv (1 to 750) and ckey (0 to 255)
    pcv_range = range(1, max_pcv + 1)
    ckey_range = range(0, key_range + 1)
    combinations = list(itertools.product(pcv_range, ckey_range))
    
    # Create the ptable
    ptable = pd.DataFrame(combinations, columns=['pcv', 'ckey'])
    ptable['pvalue'] = ptable['pcv'].apply(_calculate_pvalue)
    
    return ptable



def _calculate_pvalue(pcv):
    """
    Function to calculate pvalue for each pcv based on 10-5 rule
    
    Parameters:
        - pcv (int): Perturbation cell value
        
    Returns:
        - (int): Perturbation value, i.e. noise added to cells
    """
    if pcv < 10:
        return -pcv
    else:
        mod = pcv % 5
        if mod == 0:
            return 0
        elif mod == 1:
            return -1
        elif mod == 2:
            return -2
        elif mod == 3:
            return 2
        elif mod == 4:
            return 1