# -*- coding: utf-8 -*-
"""
Created on Wed April 25 15:24:03 2023

This function runs the SDC methods required for frequency tables in IDS - 
'cell key perturbation'. A frequency table is created from the underlying 
microdata, cross-tabulating the given variables.
Noise is added from the 'ptable' file, and counts below threshold 
(default=10) are changed to nan. 
@author: iain dove
"""

import pandas as pd
import numpy as np

from cell_key_perturbation.utils.validate_inputs_before_perturbation import validate_inputs

def create_perturbed_table(data,
                           ptable,
                           geog,
                           tab_vars,
                           record_key,
                           threshold = 10
                           ):
    """
    Function creates a frequency table which has has a cell key perturbation 
    technique applied with help from a p-table. 
    
    Cell Key Perturbation adds a small amount of noise to some cells in a 
    table, meaning that users cannot be sure
    whether differences between tables represent a real person, or are caused 
    by the perturbation. 
    Cell Key Perturbation is consistent and repeatable, so the same cells are 
    always perturbed in the same way.

    Parameters
    ----------
    data : Pandas data frame
    A pandas data frame containing the data to be tabulated and perturbed. 
    The data should contain one row per statistical 
    unit (person, household, business or other) and one column per variable 
    (age, sex, health status)
    
    ptable: Pandas data frame
    A pandas data frame containing the 'ptable' file. The ptable file 
    determines when perturbation is applied. 
    'ptable_10_5_rule.csv' is supplied with this package, which applies a 
    threshold of 10, and rounding to base 5.
        
    geog : Vector
    A vector with one entry, the column name in 'data' that contains the 
    desired geography level for the frequency table. 
    The column name should be held in a string. For example ["Region"], 
    ["Local Authority"]. If no geography breakdown is 
    needed, this should be an empty vector: []

    tab_vars: Vector
    A vector containing the column names in 'data' of the variables to be 
    tabulated. For example ["Age","Health","Occupation"]

    record_key: String
    The column name in 'data' that contains the record keys required for 
    perturbation. For example: "Record_Key"
    
    threshold: Integer
    Threshold below which cell counts are supressed. Counts below this value 
    will be returned as nan. 
    The default threshold is 10. Setting threshold=0 would mean no counts are 
    supressed.
    
    Returns
    -------
    aggregated_table: Pandas data frame
    A frequency table which has had cell key perturbation and a threshold 
    applied. The threshold is specified using the threshold parameter which has 
    a defualt of 10. 
    The application of perturbation will depend on the ptable supplied.
    'ptable_10_5_rule.csv' applies a threshold of 10, and rounding to base 5.

    Examples
    --------
    >>> from utils.generate_test_data import generate_test_data
    >>> from utils.generate_test_ptable import generate_ptable_10_5_rule
    
    >>> micro = generate_test_data()
    >>> ptable_10_5 = generate_ptable_10_5_rule()
    
    # or
    >>> ptable_10_5 = pd.read_csv("../data_files/ptable_10_5_rule.csv")

    >>> record_key = "record_key"
    >>> geog = ["var1"]
    >>> tab_vars = ["var5","var8"]

    >>> perturbed_table = create_perturbed_table(data = micro,
    ...                                          record_key = record_key,
    ...                                          geog = geog,
    ...                                          tab_vars = tab_vars,
    ...                                          ptable = ptable_10_5)

    >>> perturbed_table

    #using direct inputs, and selecting no geography breakdown
    >>> perturbed_table = create_perturbed_table(data = micro,
    ...                                          record_key = "record_key",
    ...                                          geog = [],
    ...                                          tab_vars = ["var1","var5","var8"],
    ...                                          ptable = ptable_10_5)

    >>> perturbed_table

    """
    #%%# Step 0: Validate Inputs
    validate_inputs(data, ptable, geog, tab_vars, record_key, threshold)
    
    #%%# Step 1: Create frequency table
    count_df = (
        data.groupby(geog + tab_vars)
            .size()
            .reset_index(name='pre_sdc_count')
    )

    aggregated_table = pd.pivot_table(count_df,
                                      index = geog + tab_vars,
                                      values='pre_sdc_count',                            
                                      fill_value = 0,
                                      dropna=False,
                                      aggfunc = "sum").reset_index()
    
    #%%# Step 2: Calculate sum of the record keys and apply modulo to obtain cell keys
    ckeys_table = (
        data.groupby(geog + tab_vars)
            .agg(ckey = (record_key, 'sum'))
            .reset_index()
    )
    
    ckeys_table["ckey"] = ckeys_table["ckey"] % (ptable["ckey"].max() + 1)

    aggregated_table = aggregated_table.merge(ckeys_table,
                                              how ='left',
                                              on = geog + tab_vars)

    aggregated_table["ckey"] = aggregated_table["ckey"].fillna(0)
    aggregated_table["ckey"] = aggregated_table["ckey"].astype(int)
    
    #%%# Step 3: Create pcv by ensuring the rows of ptable 501-750 are reused for cell values above 750
    aggregated_table["pcv"] = aggregated_table["pre_sdc_count"]
    aggregated_table["pcv"] = ((aggregated_table["pcv"] -1) % 250) + 501
    aggregated_table.loc[
        aggregated_table["pre_sdc_count"] <= 750, 
        "pcv"
    ] = aggregated_table["pre_sdc_count"] 

    #%%# Step 4: Merge aggregated table and ptable (left join) to get perturbation value for each cell
    aggregated_table = aggregated_table.merge(ptable, 
                                              how ='left', 
                                              on = ["pcv","ckey"])
    aggregated_table["pvalue"] = aggregated_table["pvalue"].fillna(0)
    aggregated_table["pvalue"] = aggregated_table["pvalue"].astype(int)

    #%%# Step 5: Apply the perturbation and suppress counts less than the threshold
    aggregated_table["count"] = (aggregated_table["pre_sdc_count"] 
                                 + aggregated_table["pvalue"])
    aggregated_table.loc[
        aggregated_table["count"] < threshold, 
        "count"
    ] = np.nan

    return aggregated_table

if __name__ == "__main__":
    import doctest
    doctest.testmod()
