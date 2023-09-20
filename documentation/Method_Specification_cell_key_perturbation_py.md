---
output:
  html_document: default
  pdf_document: default
---
# Statistical Method Specification - Cell key perturbation

## Overview

 | Descriptive      | Details                                             |
 |:---              | :----                                               |
 | Support Area     | Statistical Disclosure Control                      |
 | Version          | 1.1                                                 |
 | Description      | Cell-key perturbation adds small amounts of noise to frequency tables, to protect against disclosure| 
 |  Method theme    |  Statistical Disclosure Control                     |
 |  Method Classification         |  Statistical Disclosure Control       |
 |  Status          |  Code Complete with documentation                   |
 |  Inputs          |  data, record_key, tab_vars, geog, ptable (see working example).      |
 |  Outputs         |  Frequency table with cell key perturbation applied |


## Method Specification

### Method Specification Amendments/Change Log

 | Document version  | Description |Author(s)       |     Date        |    Comments      |
 |:---               | :----       |:---            |:---             |:---              |      
 |1.0                |First draft  | Iain Dove      |02/05/23         |First draft       |
 |1.1               |Update       | Sapphira Thorne |14/09/23        |Tidied up specification to remove template notes and added in pandas as a dependency. |

### Summary

Cell-key perturbation adds small amounts of noise to frequency tables,
to protect against disclosure.

Noise is added to change the counts that appear in the frequency table
by small amounts, for example a 14 is changed to a 15. This noise
introduces uncertainty in the counts and makes it harder to identify
individuals, especially when taking the 'difference' between two similar
tables.

An input file called a 'ptable' is needed which specifies the level of
perturbation. These can also be used to apply rounding, and a threshold
for small counts.*

***Technical terms specific to this method that are used in the
specification***

-   Frequency table - sometimes known as contingency table, a list of
    characteristics/categories in the data and a count of how many
    records match those characteristics.

-   Perturbation - adding noise to frequency tables to change the
    counts

-   Record key (rkey) - a random number between 0-255. There is one
    record key for each record. The record keys should be attached to
    the dataset before perturbation can be applied. The record keys are
    used to decide which perturbation gets applied to which cells/counts
    in the frequency table. The record keys need to stay the same in the
    data so that the perturbation applied is consistent.

-   Cell key - the sum of record keys of all records which appear in a
    cell. Modulo 256 is taken so the range of cell keys is 0-255. The
    cell keys use record keys to determine when to apply perturbation.

-   Ptable - a parameter file which controls when perturbation is
    applied. The ptable contains a list of every combination of cell
    value (1-750) and cell key (0-255) and decides what noise is added
    based on this combination.

The method produces a frequency table based on a set of variables. It
adds record keys together to make a cell key for each count in the
table. It merges on the ptable which decides when perturbation is
applied. Noise from the ptable is added to the counts. The result is
that counts have been deliberately changed based on the ptable, for the
purpose of disclosure protection.

### Requirements and Dependencies

The data will need a record key variable for cell key perturbation to be
applied (see method input).

The method requires pandas to be installed. There are no methods
dependent on cell key perturbation.

### Assumptions and Validity

Cell-Key Perturbation works based on the following assumptions:

-   The analyst is producing a frequency table that requires cell key
    perturbation protection.

-   The analyst has a ptable available to them, relevant to their
    dataset, supplied by the SDC team or data owners.

-   The data used contains one row per record (person, household,
    business, or other individual) and one column for each
    variable/characteristic.

The method is only suitable for producing frequency tables, and cannot
be applied without a ptable file. It may or may not be possible to apply
the method to data that does not contain one row per record and one
column per variable. Contact the disclosure control expert group to
discuss your requirements.



### Method Input

 | Variable Definition |Type of Variable| Format of specific variable (if applicable)| Expected range of the values | Meaning of the values| Expected level of aggregation | Comments | 
 |:---       |:---     |:---     |:---   |:--- |:--- |:--- |
 | Record key| Integer | Integer | 0-255 |The numbers are random and have no meaning. The 'keys' are used as inputs in perturbation to apply consistency| One per statistical unit (person, household, business) |  The name of the record key column is supplied to the function. Record key variables may be named as record_key, record_key_person etc |
 
-   The microdata used is expected to contain one row per record
    (person, household, business, or other individual) and one column
    for each variable/characteristic.

-   The microdata needs a column containing record key, random numbers
    between 0-255.

-   The method needs a ptable file, containing the perturbation/noise to
    be added.

-   The function call requires a list of variables to be tabulated

-   The record key needs to be numeric (integer) so it can be used in
    calculations (modulo sum). The other variables are expected to be
    categorical (they can be numeric but categorical is more suitable
    for frequency tables).



### Method Output

 |Variable definition| Type of variable| Format of specific variable (if applicable)| Expected range of the values| Meaning of the values | Expected level of aggregation | Comments |
 |:---       |:---     |:---     |:---   |:--- |:--- |:--- |
 |ckey       | integer || 0-255   | No intrinsic meaning. This value determines the perturbation to be added and ensures consistency | One value per cell in a frequency table | | |
 |pcv        | integer || 0-750 | No intrinsic meaning. This value is an edited version of the count designed to reduce the necessary size of the ptable file. For cell values 0-750, pcv is the same as cell value | One value per cell in a frequency table | | |     
 |count     | integer  || >=0  | The cell value after perturbation. The 'count' of how many records contain a combination of characteristics, plus the noise added by perturbation. E.g. there could be 4 Jewish males in an area. Noise of +1 is applied to the cell so the post perturbation 'count' is 5. | One value per cell in a frequency table | | | 
 
-   The count table will be in 'long' format sometimes known as tidy
    format, with one row per combination of characteristics. One column
    is included for each variable tabulated, e.g.: Local Authority, Age,
    Sex, count, pcv, pvalue, count; Bristol, 16-24, 1, 503, 503, +2,
    505.

### Statistical Process Flow/Formal Definition

The code produces a frequency table, counting how many records contain
combinations of each of the supplied variables. In the same step, it
takes the sum of the record keys of those records and takes modulo 256.
The modulo is used so that cell keys are uniform in the range is 0-255,
which allows the method to specify and control the perturbation rate.

To prevent the need for a very large ptable file, the rows 501-750 are
also used for higher cell counts. Row 501 is used for cell counts 501,
751, 1001, 1251\... Row 502 is used for cell counts 502, 752, 1002. To
achieve this effect, a column named \'pcv\' (perturbation cell value) is
created and cell counts above 750 are transformed by subtracting 1,
taking modulo 250 (to get the range 0-249) then adding 501 (to get the
range 501-750).

The ptable file is merged on using a left join, so every cell in the
table is covered, matching on values of cell-key and pcv. The
post-perturbation count is created by adding the pre-perturbation count
and the designated noise from the ptable, the 'pvalue' column
(perturbation value).

The end result is a table of combinations of variables, provided by the
user, and the 'count' column has had the required noise from the
ptable applied.

### Worked Example

```
micro = pd.read_csv("\\location\teaching file with rkey.csv")

ptable_10_5 = pd.read_csv("\\location\P Table Parameters\ptable_10_5_rule.csv")

record_key = "Record_key"    

geog = ["Region"]

tab_vars = ["Age","Health","Occupation"]

perturbed_table = create_perturbed_table(data = micro,
                                        record_key = record_key,
                                        geog = geog,
                                        tab_vars = tab_vars,
                                        ptable = ptable_10_5)

>>> perturbed_table

#using direct inputs, and selecting no geography breakdown

perturbed_table= create_perturbed_table(data = micro,
                                        record_key = "Record_key",
                                        geog = [],
                                        tab_vars = ["Sex","Industry","Occupation"],
                                        ptable = ptable_10_5)


```

### Treatment of Special Cases

By default the code will include all categories observed in the data.
Users may choose to remove or include null/missing values in their
outputs.

Frequency tables are more suitable for categorical data. Numeric data
can be passed through the perturbation although the counts are more
likely to be small and be suppressed by the threshold of 10 (counts less
than 10 are changed to appear as 0). Users may wish to band numeric data
into categories for tabulation.

### Metadata Requirements

The method does not provide any metadata. An analyst should note which
input microdata was used and which ptable file was used.

### Example (Synthetic) Data 

A working example is included in the 'generate test data' python script.

### Code

Python code can be found in GitHub: [ons-sml/cell-key-perturbation:
SML integration of ONSdigital/cell-key-perturbation
(github.com)](https://github.com/ons-sml/cell-key-perturbation)

Python version can be accessed via PyPI using the following code to
import:

```
pip install cell_key_perturbation

from cell_key_perturbation.create_perturbed_table import
create_perturbed_table
```


### Issues for Consideration

-   The expected errors are inputs being provided in alternative
    formats.

-   Variables to be tabulated should be provided as a vector of strings
    e.g. ```["Industry","Occupation","Religion"]```
    
-   The microdata and ptable are to be provided as pandas dataframes.
    (This is instead of providing the function with filepath locations,
    to allow for storage of the files in different formats and reading
    the files in by different means.)
