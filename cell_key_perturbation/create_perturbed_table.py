# -*- coding: utf-8 -*-
"""
Created on Wed April 25 15:24:03 2023

This function runs the SDC methods required for frequency tables in IDS - 'cell key perturbation' and a threshold of 10
A frequency table is created from the underlying microdata, cross-tabulating the given variables
Noise is added from the 'ptable' file, and counts<10 are changed to 0 (also done through the ptable)
@author: iain dove
"""

import pandas as pd

def create_perturbed_table(data, geog, tab_vars, record_key, ptable):
    """
    Function creates a frequency table which has has a cell key perturbation technique applied with help from a p-table. 
    
    Cell Key Perturbation adds a small amount of noise to some cells in a table, meaning that users cannot be sure
    whether differences between tables represent a real person, or are caused by the perturbation. 
    Cell Key Perturbation is consistent and repeatable, so the same cells are always perturbed in the same way.

    Parameters
    ----------
    data : Pandas data frame
    A pandas data frame containing the data to be tabulated and perturbed. The data should contain one row per statistical 
    unit (person, household, business or other) and one column per variable (age, sex, health status)
        
    geog : Vector
    A vector with one entry, the column name in 'data' that contains the desired geography level for the frequency table. 
    The column name should be held in a string. For example ["Region"], ["Local Authority"]. If no geography breakdown is 
    needed, this should be an empty vector: []

    tab_vars: Vector
    A vector containing the column names in 'data' of the variables to be tabulated. For example ["Age","Health","Occupation"]

    record_key: String
    The column name in 'data' that contains the record keys required for perturbation. For example: "Record_Key"

    ptable: Pandas data frame
    A pandas data frame containing the 'ptable' file. The ptable file determines when perturbation is applied. 
    'ptable_10_5_rule.csv' is supplied with this package, which applies a threshold of 10, and rounding to base 5.
    
    Returns
    -------
    aggregated_table: Pandas data frame
    A frequency table which has had cell key perturbation applied. The application of perturbation will depend on the ptable supplied.
    'ptable_10_5_rule.csv' applies a threshold of 10, and rounding to base 5.

    Examples
    --------
    >>> micro = pd.read_csv("\\\\Tdata15\SDC_method\Iain\Other\Teaching file\Census 2011 teaching file with rkey.csv")
    >>> ptable_10_5 = pd.read_csv("\\\\Tdata15\SDC_method\Census2021\P Table Parameters\ptable_10_5_rule.csv")

    >>> record_key = "Record_key"
    >>> geog = ["Region"]
    >>> tab_vars = ["Age","Health","Occupation"]

    >>> perturbed_table = create_perturbed_table(data = micro,
                                        record_key = record_key,
                                        geog = geog,
                                        tab_vars = tab_vars,
                                        ptable = ptable_10_5)

    >>> perturbed_table

    #using direct inputs, and selecting no geography breakdown
    >>> perturbed_table= create_perturbed_table(data = micro,
                                        record_key = "Record_key",
                                        geog = [],
                                        tab_vars = ["Sex","Industry","Occupation"],
                                        ptable = ptable_10_5)

    """
    # Input checks ============================================================
    # 1. Type validation on input data & ptable
    # 2. Check that at least one variable specified for geog or tab_vars
    # 3. Check variable is specified for record_key
    # 4. Check geog, tab_vars & record_key specified are columns in data
    # 5. Check ptable contains required columns
    # ------------------------------------------------------------------------
    if not (isinstance(data, pd.DataFrame)):
        raise TypeError("Specified value for data must be a Pandas Dataframe.")
    if not (isinstance(ptable, pd.DataFrame)):
        raise TypeError("Specified value for ptable must be a Pandas Dataframe.")
    if ((len(geog)==0) & (len(tab_vars)==0)):
        raise Exception("No variables for tabulation. Please specify value for geog or tab_vars.")
    if (len(record_key)==0):
        raise Exception("Please specify a value for record_key.")
    if (len(geog)>0):
        if not(all([item in data.columns for item in geog])):
            raise Exception("Specified value(s) for geog must be column(s) in data.")
    if (len(tab_vars)>0):
        if not(all([item in data.columns for item in tab_vars])):
            raise Exception("Specified value(s) for tab_vars must be column(s) in data.")
    if (len(record_key)>0):
        if (not (record_key in data.columns)):
            raise Exception("Specified value for record_key must be a column in data.")
    if not(all([item in ptable.columns for item in ["pcv","ckey","pvalue"]])):
        raise Exception("Supplied ptable must contain columns named 'pcv','ckey' and 'pvalue'.")
    # =========================================================================
    
    count_df = data.groupby(geog+tab_vars).size().reset_index(name='rs_cv')

    aggregated_table = pd.pivot_table(count_df,
                       index = geog + tab_vars,
                       values='rs_cv',                            
                       fill_value = 0,
                       dropna=False,
                       aggfunc = sum).reset_index()
    
    max_ckey = ptable["ckey"].max()
    max_rkey = data[record_key].max()
    
    if max_ckey!=max_rkey:
        print("The ranges of record keys and cell keys appear to be different. The maximum record key is ",max_rkey,", whereas the maximum cell key is ",max_ckey,". Please check you are using the appropriate ptable for this data")
    
    ckeys_table = data.groupby(geog+tab_vars).agg(
         ckey = (record_key,'sum'),
         ).reset_index()   
    
    ckeys_table["ckey"] = ckeys_table["ckey"]%(max_ckey+1)

    aggregated_table = aggregated_table.merge(ckeys_table,how ='left',on = geog + tab_vars)

    aggregated_table["ckey"].fillna(0, inplace = True)
    aggregated_table["ckey"] = aggregated_table["ckey"].astype(int)
    
    #create pcv - change rows with large counts by -1, modulo 250, +501
    #this section ensures that rows of the ptable 501-750 are reused 
    #for cell values 751-1000, 1001-1250 etc to save ptable file size
    #first create a copy of rs_cv - 'record_swapping cell value'
    aggregated_table["pcv"] = aggregated_table["rs_cv"]
    #to save conditional statements modify all values first, then reset values<=750
    aggregated_table["pcv"] = ((aggregated_table["pcv"]-1)%250)+501
    #revert all cells where rs_cv<=750, which use the standard/expected row in the ptable
    aggregated_table.loc[ aggregated_table["rs_cv"] <=750, "pcv"] = aggregated_table["rs_cv"] 


    aggregated_table = aggregated_table.merge(ptable, how ='left', on = ["pcv","ckey"])

    aggregated_table["pvalue"].fillna(0, inplace = True)
    aggregated_table["pvalue"] = aggregated_table["pvalue"].astype(int)

    aggregated_table["count"] = aggregated_table["rs_cv"] + aggregated_table["pvalue"]     

    return aggregated_table



if __name__ == "__main__":
    import doctest
    doctest.testmod()
