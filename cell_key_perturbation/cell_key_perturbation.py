# -*- coding: utf-8 -*-
"""
Created on Wed April 25 15:24:03 2023

This function runs the SDC methods required for frequency tables in IDS - 'cell key perturbation' and a threshold of 10
A frequency table is created from the underlying microdata, cross-tabulating the given variables
Noise is added from the 'ptable' file, and counts<10 are changed to 0 (also done through the ptable)
@author: iain dove
"""

import pandas as pd

def cell_key_perturbation(data,geog,tab_vars,record_key,ptable,ckey_max=256,ptable_max_row=750,ptable_repeated_rows=250):
    
    #create table, counting number of rows with the given geography and variable values:
    #this includes combinations with a count of zero 
    count_df = data.groupby(geog+tab_vars).size().reset_index(name='rs_cv')

    tab = pd.pivot_table(count_df,
                       index=geog+tab_vars,
                       values='rs_cv',                            
                       fill_value = 0,
                       dropna=False,
                       aggfunc=sum).reset_index()
    
    #take the sum of record keys for each combination of variables:
    ckeys_tab = data.groupby(geog+tab_vars).agg(
         ckey = (record_key,'sum'),
         ).reset_index()   
    
    #modulo ckey so range is 0-255 (uniform) by default
    #if using a different range of record keys and cell keys, adjusting the ckey_max parameter will ensure a range of 0-(ckey_max-1)
    ckeys_tab["ckey"]=ckeys_tab["ckey"]%ckey_max

    #join the ckeys onto the 'main' table
    tab = tab.merge(ckeys_tab,how='left',on=geog+tab_vars)
    #after join, missing values appear for ckey where no keys are summed
    tab["ckey"].fillna(0, inplace=True)
    tab["ckey"]=tab["ckey"].astype(int)
    
    #this section ensures that the top rows of the ptable are reused, to save file size 
    #the following uses defaults of cell values up to 750 in the ptable, repeating rows 501-750
    #adjusting the ptable_max_rows and ptable_repeated_rows can change these values. These must match the layout of the ptable provided.
    
    #create pcv - change rows with large counts by -1, modulo 250, +501, for cell values 751-1000, 1001-1250 etc to save ptable file size
    #first create a copy of rs_cv - 'record_swapping cell value'
    tab["pcv"]=tab["rs_cv"]
    #to save conditional statements modify all values first, then reset values<=750
    tab["pcv"] = ((tab["pcv"]-1)%ptable_repeated_rows)+(ptable_max_row-ptable_repeated_rows+1)
    #revert all cells where rs_cv<=750, which use the standard/expected row in the ptable
    tab.loc[ tab["rs_cv"] <=ptable_max_row, "pcv"] = tab["rs_cv"] 

    #merge ptable on by pcv and ckey
    tab = tab.merge(ptable,how='left',on=["pcv","ckey"])
    #after join, missing values for pvalue appear where cells don't get a pvalue
    tab["pvalue"].fillna(0, inplace=True)
    tab["pvalue"]=tab["pvalue"].astype(int)

    #set count=rs_cv+pvalue ie post perturbation, with noise from the ptable
    tab["count"]=tab["rs_cv"]+tab["pvalue"]     
    return tab


"""
#example use below

#read in the census teaching file data for testing the code
#the code expects a pandas dataframe, with one row per statistical unit (person/household/business)
#and one column per variable
micro=pd.read_csv("\\\\Tdata15\SDC_method\Iain\Other\Teaching file\Census 2011 teaching file with rkey.csv")

#reads in a 'ptable' which determines the threshold and perturbation
#Which ptable is used will depend on the SDC required for the data. For testing, a threshold of 10 and rounding to base 5 can be used
ptable_10_5=pd.read_csv("\\\\Tdata15\SDC_method\Census2021\P Table Parameters\ptable_10_5_rule.csv")


#setting inputs: variables, geography, ptable file
record_key="Record_key"
geog=["Region"]
tab_vars=["Age","Health","Occupation"]


#microdata and the ptable need to be read in as dataframes
#using filepaths may be unreliable as it's not known how the data will be stored, formated etc 


#using pre-defined inputs:
perturbed_table= cell_key_perturbation(data=micro,
                                    record_key=record_key,
                                    geog=geog,
                                    tab_vars=tab_vars,
                                    ptable=ptable_10_5)

#result:
perturbed_table

#using direct inputs, and selecting no geography breakdown
perturbed_table= cell_key_perturbation(data=micro,
                                    record_key="Record_key",
                                    geog=[],
                                    tab_vars=["Sex","Industry","Occupation"],
                                    ptable=ptable_10_5)

#result:
perturbed_table
"""

