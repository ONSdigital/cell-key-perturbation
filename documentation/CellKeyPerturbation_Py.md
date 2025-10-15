# Cell Key Perturbation in Python 
# SML User Guide

## Overview

 | Descriptive      | Details                                             |
 |:---              | :----                                               |
 | Support Area     | Statistical Disclosure Control                      | 
 | Method Theme     | Statistical Disclosure Control                      |
 | Status           | Ready to Use                                        |
 | Inputs           | data, record_key, geog, tab_vars, ptable, threshold |
 | Outputs          | frequency table with cell key perturbation applied  |
 | Method Version   | 2.0.0                                               |
 | Code Repository  | [https://github.com/ONSdigital/cell-key-perturbation](https://github.com/ONSdigital/cell-key-perturbation) |
 
## Summary

This method creates a frequency table which has had cell key perturbation 
applied to the counts to protect against disclosure. 

Cell key perturbation adds small amounts of noise to frequency tables. 
Noise is added to change the counts that appear 
in the frequency table by small amounts, for example a 14 is changed to a 15. 
This noise introduces uncertainty in the counts and makes it harder to identify
individuals, especially when taking the 'difference' between two similar
tables. It protects against the risk of disclosure by differencing since it 
cannot be determined whether a difference between two similar tables represents 
a real person, or is caused by the perturbation.

Cell Key Perturbation is consistent and repeatable, so the same cells are 
always perturbed in the same way.

# User Notes

## Finding and Installing the method

This method requires Python 3.7 or above and uses the pandas package.

><sub>To prevent downgrading software on your system, we recommend creating a virtual environment to install and run SML methods. This will enable you to install the method with the required version of Python, etc, without disrupting the newer versions you may be running on your system. </sub>


The method package can be installed from PyPI/Artifactory using the following 
code in the terminal or command prompt:

```py
pip install cell_key_perturbation
```

In your code you can import the cell key perturbation package using:

```py
from cell_key_perturbation.create_perturbed_table import create_perturbed_table
```

## Requirements and Dependencies 

- This method requires microdata and a perturbation table (ptable) file. 
- The microdata and the ptable each need to be supplied as a pandas dataframe.
- The microdata must include a record key variable for cell key perturbation 
to be applied.
- There must be a sufficient number of records with record keys. If less than 
50% of records have a record key, perturbation cannot be applied.
- There are no methods dependent on cell key perturbation.


## Assumptions and Validity 

The microdata must contain one column per variable, which are expected to be 
categorical (they can be numeric but categorical is more suitable for 
frequency tables). 

Record keys should already be attached to the data. The 'record key' column 
in the microdata will be an interger, randomly 
uniformly distributed either in the range 0-255 or 0-4095. 

A ptable file needs to be supplied which determines which cells are perturbed 
and by how much (most cells are perturbed by +0). 

The ptable used and the record keys attached to the microdata should ideally use  
the same record key range, 0-255 or 0-4095. A warning message will be generated 
if the record key ranges do not match.

By default a ptable that applies the '10-5 rule' is provided with the method 
package and works with record keys in the range 0-255. This ptable will 
remove all cells \<10, and round all others to the nearest 5. This provides 
more protection than necessary but will ensure safe outputs. If this ptable 
is used with admin data, meaning the record key ranges do not match, it 
is acceptable to disregard the warning in this circumstance.

Other ptables may be available depending on the data used, for example 
census 2021 data will require the ptable_census21 to be used and is based 
on cell keys in the range 0-255.

Cell Key Perturbation is consistent and repeatable, so the same cells are 
always perturbed in the same way provided the record keys are not changed.


## How to Use the Method

### Method Input

The 'create_perturbed_table()' function which creates the frequency table with 
cell key perturbation applied has the following arguments:

create_perturbed_table(data, geog, tab_vars, record_key, ptable, threshold)

- data - a pandas dataframe containing the data to be tabulated and perturbed.
- geog - a string vector giving the column name in 'data' that contains the 
desired geography level you wish to tabulate at, e.g. ["Local_Authority", 
"Ward"]. This can be the empty vector, geog=[], if no geography level is 
required.
- tab_vars - a string vector giving the column names in 'data' of the variables 
to be tabulated e.g. ["Age","Health","Occupation"]. This can also be the empty 
vector, tab_vars=[]. However, at least one of 'tab_vars' or 'geog' must be 
populated. if both are left blank an error message will be returned.
- record_key - a string containing the column name in 'data' giving the 
record keys required for perturbation. 
- ptable - a pandas dataframe containing the 'ptable' file which determines when 
perturbation is applied.
- threshold - the value below which a count is suppressed (default 10).

Example rows of a microdata table are shown below:

 | record_key  | var1  | var5  | var8  | 
 |       :---  | :---- | :---- | :---- | 
 |      84     | 2     | 9     | D     | 
 |     108     | 1     | 9     | C     | 
 |     212     | 1     | 1     | D     | 
 |     212     | 2     | 2     | A     | 
 |      86     | 2     | 4     | A     | 
   
Example rows of a ptable are shown below:  

 | pcv  | ckey  | pvalue |
 |:---  | :---- | :----  |
 |   1  |    0  |    -1  | 
 |   1  |    1  |    -1  | 
 |   1  |    2  |    -1  | 
 |   1  |    3  |    -1  | 
 |   1  |    4  |    -1  |  
 | ...  |  ...  |   ...  |    
 | 750  |  251  |     0  |
 | 750  |  252  |     0  | 
 | 750  |  253  |     0  | 
 | 750  |  254  |     0  |  
 | 750  |  255  |     0  |


### Method Output 

The output from the code is a pandas dataframe containing a frequency table with 
the counts having been affected by perturbation, as specified in the ptable. 

The table will be in the following format:


  | var1  | var5  | var8  | pre_sdc_count | ckey  | pcv   | pvalue | count  |
  |  :--- | :---- | :---- |       :----   | :---- | :---- | :----  | :----  | 
  |  1    |   1   |   A   |         16    |  64   |  16   |   -1   |   15   | 
  |  1    |   1   |   B   |          5    | 196   |   5   |   -5   |    0   | 
  |  1    |   1   |   C   |         10    | 123   |  10   |    0   |   10   | 
  |  1    |   1   |   D   |         10    |   3   |  10   |    0   |   10   | 
  |  1    |   2   |   A   |         12    | 149   |  12   |   -2   |   10   | 
  | ...   | ...   | ...   |        ...    | ...   | ...   |  ...   |  ...   | 
  

The table contains the variables used as the categories used to summarise the 
data (in this example var1, var5 & var8), and five other columns:

- 'ckey' is the sum of record keys for each combination of variables
- 'pcv' is the perturbation cell value, the pre-perturbation count modulo 750
- 'pre_sdc_count' is the pre-perturbation count 
- 'pvalue' is the perturbation applied to the original count, most commonly 
it will be 0. This is obtained from the ptable using a join on ckey and pcv.
- 'count' is the post-perturbation count, the values to be output

The columns you are most likely interested in are the variables, which 
are the categories you've summarised by, plus the 'count' column.

The ckey, pcv, pre_sdc_count and pvalue columns should be dropped before the 
contingency table is published.


## Example (Synthetic) Data

The following are included in the method package: 

- **generate_test_data** : function to create an example data set, a randomly generated data set with record keys in the range 0-255.

```py
from cell_key_perturbation.generate_test_data import generate_test_data
micro = generate_test_data()
```

- **ptable_10_5_rule.csv** : file containing example ptable, ptable_10_5, which applies the 10_5 rule and has record keys in the range 0-255.
  
This will be located in your installation directory and can be also found in the [example_data](https://github.com/ONSdigital/sml-public/tree/main/example_data/CellKeyPerturbation) folder of this repository. It should be read in as a pandas dataframe specifying the filepath:
  
```py
#import pandas as pd
ptable_10_5 = pd.read_csv("ptable_10_5_rule.csv")
```

## Worked Example

1.  Install the cell key perturbation package.
```py
pip install cell_key_perturbation
```

2.  Import the package.
```py
from cell_key_perturbation.create_perturbed_table import create_perturbed_table
```

3. You can test calling the method using the example data (micro) and 
ptable (ptable_10_5), specifying the record_key, geog and tab_vars as
columns in micro. For example:

```py
perturbed_table = create_perturbed_table(data = micro,
                                         record_key = "record_key",
                                         geog = ["var1"],
                                         tab_vars = ["var5","var8"],
                                         ptable = ptable_10_5,
                                         threshold=10)
```

4.  To use the method with your own microdata and ptable, ensure that these are 
each ready to pass to the method in the form of a pandas dataframe and that your 
dataset includes a column for record key. 

5.  Define the arguments of the create_perturbed_table function (data, 
record_key, geog, tab_vars and ptable) and run the function to create the 
table. 
- The geog parameter should be supplied as a vector e.g. ```["Region"]```. 
We strongly expect users to tabulate at a given geography level e.g. Local 
Authority, Ward. If no geography is required, so records from all geographical 
areas are together, then a 'national' geography including all areas could be 
used, alternatively the geography can be left blank 
(i.e.```geog=[]```). 
- The tab_vars parameter should be supplied as a vector of strings 
e.g. ```["Age","Health","Occupation"]``` but can also be left blank, 
(i.e. ```tab_vars=[]```). 
- At least one of 'tab_vars' or 'geog' must be populated - if both are left 
blank an error message will be returned and the method will not work.

6. Drop the additional columns used for processing before publishing the data. 
The resulting frequency table and counts can be saved to a csv file. 
For example:

```py
output_table = perturbed_table.drop(columns = [‘pre_sdc_count’, ‘ckey’, ‘pcv’, ‘pvalue’])
output_table.to_csv(“yourfilename.csv”, index = False)
```

## Other Outputs and Metadata

In addition to the category variables and the post-perturbation count, the 
output data set contains 5 additional columns which were used for processing. 
The ckey, pcv, pre_sdc_count and pvalue columns should be dropped before the 
contingency table is published.


# Methodology

## Terminology

- Microdata - data at the level of individual respondents
- Record key - A random number assigned to each record 
- Cell value - The number of records or frequency for a cell
- Cell key - The sum of record keys for a given cell
- pvalue - perturbation value. The value of noise added to cells, e.g. +1, -1
- pcv - perturbation cell value. This is an amended cell value needed to merge on the ptable
- ptable - perturbation table. The look-up file containing the pvalues, this determines which cells get perturbed and by how much.


## Statistical Process Flow / Formal Definition

The user is required to supply microdata and to specify which columns in the
data they want to tabulate by. They must also supply a ptable which will 
determine which cells get perturbed and by how much.

The microdata needs to contain a column for 'record key'. Record keys are 
random, uniformly distributed integers within the chosen range. Previously, 
record keys between 0-255 have been used (as for census-2021). The method has 
been extended to also handle record keys in the range 0-4096 for the purpose of 
processing administrative data. 

It is expected that users will tabulate 1-4 variables for a particular geography 
level e.g. tabulate age by sex at local authority level. 

The create_perturbed_table function counts how many rows in the data
contain each combination of categories e.g. how many respondents are of
each age category in each local authority area. The sum of the record
keys for each record in each cell is also calculated. Modulo 256 or 4096
of the sum is taken so this 'cell key' is within range. The table now has 
perturbation cell values (pcv) and cell keys (ckey).

The ptable is merged with the data, matching on 'pcv' and 'ckey'. The merge 
provides a 'pvalue' for each cell. The post perturbation count ('count' column) 
is the pre-perturbation count ('rs_cv'), plus the perturbation value
('pvalue'). After this step, the counts have had the required perturbation 
applied. The output is the frequency table with the post-perturbation 'count' 
column. The result is that counts have been deliberately changed based on the 
ptable, for the purpose of disclosure protection.

To limit the size of the ptable, only 750 rows are used, and rows
501-750 are used repeatedly for larger cell values. E.g. instead of
containing 100,001 rows, when the cell value is 100,001 the 501st row
is used. Rows 501-750 will be used for cell values of 501-750, as well
as 751-1000, 1001-1250, 1251-1500 and so on. To achieve this effect an
alternative cell value column (pcv) is calculated which will be between 0-750.
For cell values 0-750 the pcv will be the same as the cell value. For
cell values above 750, the values are transformed by -1, modulo 250,
+501. This achieves the looping effect so that cell values 751, 1001,
1251 and so on will have a pcv of 501.

After cell key perturbation is applied, a threshold is applied so that any 
counts below the threshold will be suppressed (set to missing). The user can 
specify the value for the threshold, but if they do not, the default value of 
10 will be applied. Setting the threshold to zero would mean no suppression is 
applied.

As well as specifying the level of perturbation, the ptable can also be used 
to apply rounding, and a threshold for small counts. The example ptable 
supplied with this method, ptable_10_5, applies the 10_5 rule (supressing 
values less than 10 and rounding others to the nearest 5) for record keys 
in the range 0-255.

## Assumptions & Vailidity

The microdata must contain one column per variable, which are expected to be 
categorical (they can be numeric but categorical is more suitable for 
frequency tables). 

Record keys should already be attached to the data, and the range of record 
keys in the ptable should match that in the data, 0-255 or 0-4095.

Cell Key Perturbation is consistent and repeatable, so the same cells are 
always perturbed in the same way. The record keys need to be unchanged, 
changing the record keys would create inconsistent results and provide 
much less protection. 

# Additional Information

The ONS Statistical Methods Library at https://statisticalmethodslibrary.ons.gov.uk/ contains:
-	Further information about the methods including a link to the GitHub 
repository which contains detailed API information as part of the method code.
-	Information about other methods available through the library.


## License

Unless stated otherwise, the SML codebase is released under the MIT License. 
This covers both the codebase and any sample code in the documentation.
The documentation is available under the terms of the Open Government 3.0 
license.