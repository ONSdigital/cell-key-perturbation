# Statistical Disclosure Control - Cell key perturbation

The following guidance outlines how to install and apply the Statistical Disclosure Control (SDC) perturbation code in an IDS Notebook from the Statistical Methods Library (SML). SDC is necessary for checking outputs before leaving the IDS, and these methods should be performed before applying for Outputs.  

This guide is for Analytical Users who have outputs from their research space that they want to remove from IDS. 

As well as reading this guide, please ensure that you are familiar with and abide by the IDS Security Operating Procedure (SyOPs) accountabilities and responsibilities. 

You must also read the [Statistical Disclosure Control Guidance for analysts](sdc_guide.md) before requesting any outputs. 

## Introduction

Statistical Disclosure Controls are methods for checking whether data is disclosive or not. Regardless of how research is done, data can be inadvertently disclosive. For example any statistic that references a small number of people (for example, 1 or 2 people from a survey) inherently runs the risk of revealing their identity. The data may not directly identify individuals on its own, but in combination with enough other information it can be possible to indirectly identify people (known as jigsaw identification).  

To prevent this and maintain an ethical statistical platform, all outputs from the IDS must undergo SDC and are then checked before they are allowed to leave the platform. 

# Cell Key Perturbation

One method for SDC is Cell Key Perturbation. Users are encouraged to perform this check on any microdata before requesting its output from the IDS.  

Cell key perturbation adds small amounts of noise to frequency tables. Noise is added to change the counts that appear in the frequency table by small amounts, for example a 14 is changed to a 15. This noise introduces uncertainty in the counts and makes it harder to identify individuals, especially when taking the 'difference' between two similar tables. It protects against the risk of disclosure by differencing since it cannot be determined whether a difference between two similar tables represents a real person, or is caused by the perturbation.

Cell Key Perturbation is consistent and repeatable, so the same cells are always perturbed in the same way.

It is expected that users will tabulate 1 to 4 variables for a particular geography level - for example, tabulate age by sex at local authority level. 

Cell key perturbation is currently available using Python and BigQuery within the IDS. 

### BigQuery

BigQuery version allow users to perform perturbation without reading raw data into local memory. The package would craete the frequency table and run perturbation with a SQL query. Then, it converts the final perturbed table into a pandas dataframe as an output. 

This will allow users to run the method on large datasets without breaking the memory limits. 

### Terminology

- ***Microdata*** - data at the level of individual respondents
- ***Record key*** - A random number assigned to each record 
- ***Cell value*** - The number of records or frequency for a cell
- ***Cell key*** - The sum of record keys for a given cell
- ***pvalue*** - perturbation value. The value of noise added to cells, e.g. +1, -1
- ***pcv*** - perturbation cell value. This is an amended cell value needed to merge on the ptable
- ***ptable*** - perturbation table. The look-up file containing the pvalues, this determines which cells get perturbed and by how much.

## Requirements 

- This method requires microdata and a perturbation table (ptable) file. 
- The microdata and the ptable both need to be supplied as pandas dataframes or BigQuery tables.
- The microdata must include a record key variable for cell key perturbation to be applied.

### Microdata and Record Keys

**Microdata** must be row-level, i.e. one row per statistical unit such as person or household. **Microdata** must contain one column per variable, which are expected to be categorical (they can be numeric but categorical is more suitable for frequency tables). 

**Record keys** should already be attached to the **microdata** as a column of integers in the range 0-255 or 0-4095. The name of the **record key** column could change in different **microdata** tables. For example, **record key** columns in census data tables are named as `resident_record_key`, `household_record_key`, or `family_record_key` depending on the table type.

The range of **record keys** should match the range of **cell keys** in the **ptable**. A warning message will be generated if those ranges do not match.

Cell Key Perturbation is consistent and repeatable, so the same cells are always perturbed in the same way. 

**The **record keys** need to be unchanged, changing the **record keys** would create inconsistent results and provide much less protection. You should use **record keys** attached to your **microdata** if provided instead of creating new ones to obtain consistent perturbation across different runs.**

### Perturbation Table (P-table)

The **perturbation table** contains the parameters which determine which cells are perturbed by how much and which are not (most cells are perturbed by +0). The **ptable** contains each possible combination of **cell key** (`ckey`) and **cell value** (`pcv`), and the **perturbation value** (`pvalue`) for each combination. 

A sample **ptable** that applies the '10-5 rule' is provided with the package and works with **record keys** in the range 0-255. This **ptable** will remove all cells \<10, and round all others to the nearest 5. This provides more protection than necessary but will ensure safe outputs.

Other **ptables** may be available depending on the **microdata** used, for example census 2021 data will require the `ptable_census21` to be used and is based on cell keys in the range 0-255.

**You must use the specific **ptable** provided with the **microdata** you are working with to ensure sufficient and consistent protection, e.g. `ptable_census21` for census 2021.**

# User Instructions

## Installing the SML method

In your IDS workspace, open a new terminal. If you have not already generated an Artifactory identity token and authenticated it with the IDS see the Vertex AI workbench - installing packages guidance for details on how to do this. This will then allow you to install packages.

Once this is done, in the terminal, type the following: 

```python
pip install cell_key_perturbation
```

Press return and wait for this to install `cell_key_perturbation` version 3.0.0. You can close this window when it is finished.  

## Using the SML method

Within your working notebook (Python), you need to import the function: 

```python
# for pandas
from cell_key_perturbation.create_perturbed_table import create_perturbed_table

# for BigQuery
from cell_key_perturbation.bigquery import create_perturbed_table_bigquery
```

You can then call the method using the following parameters:

```python
# for pandas
create_perturbed_table(data, ptable, geog, tab_vars, record_key, threshold)

# for BigQuery
create_perturbed_table_bigquery(client, data, ptable, geog, tab_vars, record_key, threshold)
```

Parameters specific for BigQuery version:
- **`client`** - Google Cloud BigQuery Client object
- **`data`** - (Microdata) - a `string` for the full name of micro-level `data` in BigQuery in "\<PROJECT>.\<DATASET>.\<TABLE>" format.
- **`ptable`** - (Perturbation table) - a `string` for the full name of `ptable` in BigQuery in "\<PROJECT>.\<DATASET>.\<TABLE>" format.

Parameters specific for pandas version:
- **`data`** - (Microdata) - a `pandas.DataFrame` containing the micro-level `data` to be tabulated and perturbed.
- **`ptable`** - (Perturbation table) - a `pandas.DataFrame` containing the `ptable` file which determines when 
perturbation is applied.

Common parameters for both versions:
- **`geog`** - (Geography) - a string vector giving the column name in `data` that contains the desired geography level you wish to tabulate at, e.g. `["Local_Authority", "Ward"]`. This can be the empty vector, `geog=[]`, if no geography level is required.
- **`tab_vars`** - (Variables to tabulate) - a string vector giving the column names in `data` of the variables to be tabulated e.g. `["Age","Health","Occupation"]`. This can also be the empty vector, `tab_vars=[]`. However, at least one of `tab_vars` or `geog` must be populated. if both are left blank an error message will be returned.
- **`record_key`** - a string containing the column name in `data` giving the record keys required for perturbation. 
- **`threshold`** - the value below which a count is suppressed (default 10).

## How to Use the Method in BigQuery

1. Import `create_perturbed_table_bigquery()` function and define the BigQuery client:
```python
from cell_key_perturbation.bigquery import create_perturbed_table_bigquery
from google.cloud import bigquery

client = bigquery.Client()
```

2. Define full names of the microdata and perturbation table in the BigQuery with full location, for example:
```python
microdata = "<PROJECT_ID>.<DATASET_ID>.<microdata>"
ptable = "<PROJECT_ID>.<DATASET_ID>.<ptable>"
```

3. Define variables and parameters, for example:
```python
geog = ["Region"]
tab_vars = ["Age","Health","Occupation"]
record_key = "record_key"
threshold = 10
```

4. Call the function:
```python
perturbed_table = create_perturbed_table_bigquery(client = client,
                                                  data = microdata,
                                                  ptable = ptable,
                                                  geog = geog,
                                                  tab_vars = tab_vars,
                                                  record_key = record_key,
                                                  threshold = 10)
```

5. The returned `perturbed_table` is a `pandas.DataFrame`. You need to drop disclosive columns before exporting the output from the secure data environment. Please refer to the **"Interpreting the Output"** and **"Saving the Output"** sections below for more details.
```python
output_table = perturbed_table.drop(columns = ["pre_sdc_count", "ckey", "pcv", "pvalue"])
```


## Worked Example with Synthetic Data in pandas

This is an example showing how to create a perturbed table from sample data 
generated with provided test data generation functions in this package 
in order to showcase the method.

To generate example microdata and a perturbation table for testing purposes, 
use the following code:

```python
from cell_key_perturbation.utils.generate_test_data import generate_test_data
from cell_key_perturbation.utils.generate_test_ptable import generate_ptable_10_5_rule

microdata = generate_test_data()
ptable_10_5 = generate_ptable_10_5_rule()
```

**NOTE:** Generated test microdata contains record keys. If you are testing perturbation with another microdata, you can generate and attach random record keys in the range 0-255 as following:

```python
from cell_key_perturbation.utils.generate_record_key import generate_random_rkey

microdata = generate_random_rkey(microdata)
```

- **`microdata`**: A sample `pandas.DataFrame` containing randomly generated microdata and record keys.

Example rows of a microdata table are shown below:

 | record_key  | var1  | var5  | var8  | 
 |       :---  | :---- | :---- | :---- | 
 |      84     | 2     | 9     | D     | 
 |     108     | 1     | 9     | C     | 
 |     212     | 1     | 1     | D     | 
 |     212     | 2     | 2     | A     | 
 |      86     | 2     | 4     | A     | 

- **`ptable_10_5`**: A sample perturbation table (`pandas.DataFrame`) that defines the cell key perturbation rules. This specific table applies the ’10 to 5 rule’, which means a suppression threshold of *10* and rounding to the nearest *5*. In other words, this ptable will remove all cells under *10*, and round all others to the nearest *5*.

Example rows of a ptable are shown below:  

 | pcv  | ckey  | pvalue |
 |:---  | :---- | :----  |
 |   1  |    0  |    -1  | 
 |   1  |    1  |    -1  | 
 |   1  |    2  |    -1  | 
 | ...  |  ...  |   ...  |    
 | 750  |  255  |     0  |

To create a perturbed table, first import the main function:

```python
from cell_key_perturbation.create_perturbed_table import create_perturbed_table
```

Then, use the following code to generate the perturbed table using the sample microdata and perturbation table:

```python
perturbed_table = create_perturbed_table(data = microdata,
                                         record_key = "record_key",
                                         geog = ["var1"],
                                         tab_vars = ["var5","var8"],
                                         ptable = ptable_10_5,
                                         threshold=10)
```

## Interpreting the Output

The output from the code is a `pandas.DataFrame` containing a frequency table with 
the counts having been affected by perturbation, as specified in the ptable. 

For most ptables, the most obvious effect will be that all counts less than the threshold will have been removed. Removing counts below a threshold is a condition of exporting data from IDS and many other secure environments.

The table will be in the following format:

  | var1  | var5  | var8  | pre_sdc_count | ckey  | pcv   | pvalue | count  |
  |  :--- | :---- | :---- |       :----   | :---- | :---- | :----  | :----  | 
  |  1    |   1   |   A   |         10    | 173   |  10   |    0   |   10   | 
  |  1    |   1   |   B   |         10    |  88   |  10   |    0   |   10   | 
  |  1    |   1   |   C   |          7    | 180   |   7   |   -7   |  nan   | 
  |  1    |   1   |   D   |         14    |  66   |  14   |    1   |   15   | 
  |  1    |   2   |   A   |         11    | 190   |  11   |   -1   |   10   | 
  | ...   | ...   | ...   |        ...    | ...   | ...   |  ...   |  ...   | 
  

The table contains the variables used as the categories used to summarise the 
data (in this example `var1`, `var5` & `var8`), and five other columns:

- `ckey` is the sum of record keys for each combination of variables.
- `pcv` is the perturbation cell value, the pre-perturbation count modulo 750.
- `pre_sdc_count` is the pre-perturbation count.
- `pvalue` is the perturbation applied to the original count, most commonly 
it will be 0. This is obtained from the ptable using a join on `ckey` and `pcv`.
- `count` is the post-perturbation count, the values to be output. It will be
set to `NaN` if the value is suppressed for being below the threshold.

The columns you are most likely interested in are the variables, which 
are the categories you've summarised by, plus the `count` column.

**WARNING! - The `ckey`, `pcv`, `pre_sdc_count` and `pvalue` columns should be dropped before the 
contingency table is published. Otherwise, the perturbation can be unpicked and the output will be disclosive.**


## Saving the Output

Before the data are ready to be output the disclosive columns must be dropped. These cannot be output as they would allow for the perturbation to be unpicked. This code assumes that you have not changed the default column names; please update it if you have. `drop()` will work on a list of column names in this case, and this code puts it in a new dataframe.

```python
output_table = perturbed_table.drop(columns = ["pre_sdc_count", "ckey", "pcv", "pvalue"])
```

To save this dataframe as a csv use the pandas to_csv method:

```python
output_table.to_csv(“yourfilename.csv”, index = False)
```

Your file name should end “.csv”. If you only specify a file name in the path it will save to your main directory. Setting ‘index’ to ‘False’ here stops it from adding a new ‘index’ column with the row number. Take that part out if you do want an index column.

## Additional Information
The ONS Statistical Methods Library at https://statisticalmethodslibrary.ons.gov.uk/ contains:

* Further information about the methods including a link to the GitHub repository which contains detailed API information as part of the method code.
* Information about other methods available through the library.





