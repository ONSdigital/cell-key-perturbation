# Statistical Disclosure Control - Cell key perturbation

The following guidance outlines how to install and apply the Statistical Disclosure Control (SDC) perturbation code in an IDS Notebook from the Statistical Methods Library (SML). SDC is necessary for checking outputs before leaving the IDS, and these methods should be performed before applying for Outputs.  

This guide is for Analytical Users who have outputs from their research space that they want to remove from IDS. 

As well as reading this guide, please ensure that you are familiar with and abide by the IDS Security Operating Procedure (SyOPs) accountabilities and responsibilities. 

You must also read the [Statistical Disclosure Control Guidance for analysts](sdc_guide.md) before requesting any outputs. 

## Introduction

Statistical Disclosure Controls are methods for checking whether data is disclosive or not. Regardless of how research is done, data can be inadvertently disclosive. For example any statistic that references a small number of people (for example, 1 or 2 people from a survey) inherently runs the risk of revealing their identity. The data may not directly identify individuals on its own, but in combination with enough other information it can be possible to indirectly identify people (known as jigsaw identification).  

To prevent this and maintain an ethical statistical platform, all outputs from the IDS must undergo SDC and are then checked before they are allowed to leave the platform. 

## Terminology
Microdata - data at the level of individual respondents

Record key - A random number assigned to each record

Cell value - The number of records or frequency for a cell

Cell key - The sum of record keys for a given cell

pvalue - perturbation value. The value of noise added to cells, e.g. +1, -1

pcv - perturbation cell value. This is an amended cell value needed to merge on the ptable

ptable - perturbation table. The look-up file containing the pvalues, this determines which cells get perturbed and by how much.

## Cell key perturbation

One method for SDC is Cell Key Perturbation. Users are encouraged to perform this check on any microdata before requesting its output from the IDS.  Cell key perturbation adds small amounts of noise to frequency tables. Noise is added to change the counts that appear in the frequency table by small amounts, for example a 14 is changed to a 15. This noise introduces uncertainty in the counts and makes it harder to identify individuals, especially when taking the 'difference' between two similar tables. It protects against the risk of disclosure by differencing since it cannot be determined whether a difference between two similar tables represents a real person, or is caused by the perturbation.

Cell Key Perturbation is consistent and repeatable, so the same cells are always perturbed in the same way.

It is expected that users will tabulate 1 to 4 variables for a particular geography level - for example, tabulate age by sex at local authority level. 

Cell key perturbation is currently only available using Python within the IDS. 

### Installing the SML method

In your IDS workspace, open a new terminal. If you have not already generated an Artifactory identity token and authenticated it with the IDS see the Vertex AI workbench - installing packages guidance for details on how to do this. This will then allow you to install packages.

Once this is done, in the terminal, type the following: 

```python
pip install cell_key_perturbation
```

Press return and wait for this to install cell_key_perturbation 2.0.0. You can close this window when it is finished.  

### Using the SML method

Within your working notebook (Python), you need to import the function using 

```python
from cell_key_perturbation.create_perturbed_table import create_perturbed_table
```

You can then call the method using the following parameters:

```python
perturbed_table = create_perturbed_table(data = micro, 

record_key = record_key, 

geog = geog, 

tab_vars = tab_vars, 

ptable = ptable,

threshold = threshold
) 
```

### Functioning parameters
* Data (‘`micro`’) – a pandas dataframe containing the micro-level data to be tabulated and perturbed
* Geography (‘`geog`’) – a string vector giving the column name in 'data' that contains the desired geography level you wish to tabulate at, e.g. ["Local_Authority", "Ward"]. This can be the empty vector, geog=[], if no geography level is required.
* Variables to tabulate (‘`tab_vars`’) - a string vector giving the column names in 'data' of the variables to be tabulated e.g. ["Age","Health","Occupation"]. This can also be the empty vector, tab_vars=[]. However, at least one of 'tab_vars' or 'geog' must be populated. if both are left blank an error message will be returned.
* Record keys (‘`record_key`’) – a string containing the column name in 'data' giving the record keys required for perturbation.
* Perturbation data file (‘ptable’). This should contain a dataframe with the perturbation details supplied by ONS. This needs to be read in to a dataframe. It combines with the tabulated data to determine which values need to be perturbed (rounded).
* threshold - the value below which a count is suppressed (default 10).


The ‘ptable’ file contains the parameters which determine which cells are perturbed and which are not (most cells are perturbed by +0). The ptable contains each possible combination of cell key (0 to 255) and cell value, and the perturbation a cell with that cell key and cell value would receive. You must use the provided ptables to ensure sufficient protection. 

By default, a ptable, 10_5 ptable, that applies the ’10 to 5 rule’ will be provided. This ptable will remove all cells under 10, and round all others to the nearest 5. This ensures safe outputs. 

Other ptables may be available depending on the data used, for example census data will require the ptable_census21 to be used. 

### Steps

1. Import the data you want to produce crosstabs for, into a pandas dataframe. This may be from a file, or from BigQuery, or whatever data source you have access to. The data must be: 

<ol type="a">
  <li>Microdata (row-level data, one row per statistical unit – person, household, etcetera.)</li>
  <li>Contain one column per variable, which will be categorical.</li>
</ol>

2. Set the data up with a column for ‘record key’. The record key must be an integer, randomly uniformly distributed between 0-255. This is required to run the method. You should only use this method when using the 10_5 ptable for perturbation. See sample code below to generate and add a record key column to a dataframe.

You can use the generate_test_data function to produce a dataframe with record keys. 
```python
from cell_key_perturbation.generate_test_data import generate_test_data

testTable = generate_test_data()
```

Alternatively, if you have real data to perturb, use:


```python
import pandas as pd
import numpy as np

# Produce a pseudo-random number generator.
# This means the results are random but can be recreated by using the same "seed" value. 
seed = 2025                                 
rng = np.random.default_rng(seed)

dataFileName = "Test_dataframe.csv"    #put in a dataframe to test.
testTable =pd.read_csv(dataFileName)   #If you already have a pandas dataframe you want to perturb use this as testTable instead.
size = len(testTable.index)

#Generate a list of numbers between 0 and 255
record_key_sample = list(rng.integers(low = 0, high = 256, size = size))

# add the record key column to dataframe
testTable["record_key"] = record_key_sample
testTable
```

|  | var1 | var2 | var3 | var4 | var5 | record_key |
|--|------|------|------|------|------|----------------|
| 0 | 2 | 2 | 4 | B | E | 128 |
| 1 | 2 | 2 | 4 | B | A | 57 |
| 2 | 5 | 2 | 9 | D | A | 178 |
| 3 | 2 | 1 | 4 | A | E | 213 |
| 4 | 3 | 2 | 1 | C | G | 64 |
| ... | ... | ... | ... | ... | ... | ... |
| 99995 | 1 | 1 | 7 | A | E | 13 |
| 99996 | 3 | 2 | 1 | A | D | 90 |
| 99997 | 4 | 1 | 1 | D | A | 92 |
| 99998 | 2 | 2 | 1 | D | C | 31 |
| 99999 | 2 | 1 | 1 | D | D | 24 |

100000 rows x 6 columns



3. Set the parameters as seen in the code below, described in the next step.

```python

from cell_key_perturbation.create_perturbed_table import create_perturbed_table 

# set parameters
micro = testTable              # uses testTable dataframe from the above cell
record_key = "record_key"   
geog = ["var1"]                 
tab_vars = ["var3", "var4"]
ptable = pd.read_csv("/opt/conda/ptable_10_5_rule.csv")   # If you are using a different ptable, put the path to this instead

perturbed_table = create_perturbed_table(
      data = micro,
      record_key = record_key,
      geog = geog,
      tab_vars = tab_vars,
      ptable = ptable
      )
      
perturbed_table
```

|  | var1 | var2 | var4 | pre_sdc_count | ckey | pcv | pvalue | count |
|--|------|------|------|-------|------|-----|--------|-------|
| 0 | 1 | 1 | A | 1287 | 59 | 537 | \-2 | 1285 |
| 1 | 1 | 1 | B | 1226 | 132 | 726 | \-1 | 1225 |
| 2 | 1 | 1 | C | 1 | 140 | 743 | 2 | 1245 |
| 3 | 1 | 1 | D | 1246 | 154 | 746 | \-1 | 1245 |
| 4 | 1 | 2 | A | 929 | 217 | 679 | 1 | 930 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 195 | 5 | 9 | D | 224 | 68 | 224 | 1 | 225 |
| 196 | 5 | 10 | A | 239 | 97 | 239 | 1 | 240 |
| 197 | 5 | 10 | B | 279 | 213 | 279 | 1 | 280 |
| 198 | 5 | 10 | C | 260 | 223 | 260 | 0 | 260 |
| 199 | 5 | 10 | D | 244 | 227 | 244 | 1 | 245 |

200 rows x 8 columns

4.    In this example, each parameter is set to a variable for clarity. The parameters are as described above

 a.    ‘`micro`’ should be set to the dataframe.

 b.    ‘`record_key`’ is the name of the column that contains the record keys.

 c.    ‘`geog`’ should contain the name of the region you wish to tabulate by.

 d.    ‘`tab_vars`’ should contain the name or names of the variables you wish to group by

 e.    ‘`ptable`’ should contain a dataframe with the perturbation details supplied by ONS.

5. You can view it as a dataframe, and save it as a file if required by using the procedure below.

## Interpreting the output

“The output from the code is a frequency table with the counts having been affected by perturbation, as specified in the ptable. For most ptables, the most obvious effect will be that all counts less than 10 will have been reduced to 0 (removed). Counts being below a threshold is a condition of exporting data from IDS and many other secure environments.”

The table contains the factors from the processed data as columns, plus five generated columns:

'ckey' is the sum of record keys for each combination of variables

'pcv' is the perturbation cell value, the pre-perturbation count modulo 750

'pre_sdc_count' is the pre-perturbation count

'pvalue' is the perturbation applied to the original count, most commonly it will be 0. This is obtained from the ptable using a join on ckey and pcv.

'count' is the post-perturbation count, the values to be output

The columns you are most likely interested in are the variables, which are the categories you’ve summarised by, plus the ‘count’ column which is the values per category.

## Saving the output

Before the data are ready to be output the disclosive columns must be dropped. These cannot be output as they would allow for the perturbation to be unpicked. This code assumes that you have not changed the default column names; please update it if you have. `drop()` will work on a list of column names in this case, and this code puts it in a new dataframe.

```plaintext
output_table = perturbed_table.drop(columns = ["pre_sdc_count", "ckey", "pcv", "pvalue"])
```

To save this dataframe as a csv use the pandas to_csv method:

```plaintext
output_table.to_csv(“yourfilename.csv”, index = False)
```

Your file name should end “.csv”. If you only specify a file name in the path it will save to your main directory. Setting ‘index’ to ‘False’ here stops it from adding a new ‘index’ column with the row number. Take that part out if you do want an index column.

## Additional Information
The ONS Statistical Methods Library at https://statisticalmethodslibrary.ons.gov.uk/ contains:

* Further information about the methods including a link to the GitHub repository which contains detailed API information as part of the method code.
* Information about other methods available through the library.
