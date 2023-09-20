# Statistical Method User Notes -- Cell Key Perturbation


### Overview

 | Descriptive      | Details                         |
 |:---              | :----                           |
 | Method name      |Cell key perturbation            | 
 | Method theme     |Statistical disclosure control   |
 | Expert group     |Statistical Disclosure Control   |
 | Languages        |Python                           |
 | Release          |1.0                              |


### User Note Amendments/Change Log

 | Document version  | Description |Author(s)       |     Date        |    Comments      |
 |:---               | :----       |:---            |:---             |:---              |      
 |1.0                |First draft  | Iain Dove      |04/04/23         |First draft       |
 |2.0                |Second draft  | Tara Smith     |31/07/23        |Added step-by-step instructions    |
 |2.1                | Updated    | Sapphira Thorne | 18/09/23        |Tidied up and added relevant GitHub links | 


### Method Specification

[https://github.com/ONSdigital/cell-key-perturbation/blob/main/documentation/Method_Specification_cell_key_perturbation_py.md](https://github.com/ONSdigital/cell-key-perturbation/blob/main/documentation/Method_Specification_cell_key_perturbation_py.md)

### How to run the method (single or multi language)

Please see the following link to the Cell Key Perturbation GitHub
repository:

<https://github.com/ONSdigital/cell-key-perturbation/tree/main>

Python version can be accessed via PyPI using the following code to
import:

```
pip install cell_key_perturbation

from cell_key_perturbation.create_perturbed_table import
create_perturbed_table
```

### Pre-processing and assumptions

The code is intended for use when producing frequency tables based on
microdata (row-level data, one row per statistical unit -- person
household etc.). The microdata will contain one column per variable,
which is expected to be categorical (they can be numeric but categorical
is more suitable for frequency tables). The microdata will also contain
a column for 'record key', which is required to run the method. The
record key will be an integer, randomly uniformly distributed between
0-255.

### Inputs

The 'ptable' file contains the parameters which determine which cells
are perturbed and which are not (most cells are perturbed by +0). The
ptable contains each possible combination of cell key (0-255) and cell
value, and the perturbation a cell with that cell key and cell value
would receive. A user must use the provided ptables to ensure sufficient
protection. By default a ptable that applies the '10-5 rule' will be
provided. This ptable will remove all cells \<10, and round all others
to the nearest 5. This provides more protection than necessary but will
ensure safe outputs. Other ptables may be available depending on the
data used, for example census data will require the ptable_census21 to
be used.

Example rows of a ptable are shown below:

 | Descriptive      | Details           | pvalue      |
 |:---              | :----             | :---        |
 |  1               | 0                 | 0           |
 |  1               | 1                 | 0           |
 |  1               | 2                 | +1           |
 |  1               | 3                 | 0           |
 |  ...             | ...               | ...           |


The microdata and ptable are provided as arguments to the perturbation
function.

The user decides which variables they would like to be tabulated.

Step-by-step instructions:

1.  Install the cell key perturbation package from PyPi, using the
    following line: 'pip install cell_key_perturbation'

2.  Import the pandas package

3.  Run the definition of the 'create_perturbed_table' function

4.  Define the microdata and ptable. These will need to be read in as
    pandas dataframes. Example lines of code are provided within the
    docstrings of the function. The filepaths will need to be edited to
    the location in which your microdata/ptable is saved.

5.  Set the geog and tab_vars. These will both need to be defined as
    vectors. For tab_vars, the variables should be supplied in a vector
    of strings e.g. ```["Age","Health","Occupation"]```. The variables
    can also be left blank, i.e. ```tab_vars=[]```. The geography is also
    supplied as a vector e.g. ```["Region"]```. An example is included in
    the docstrings. We strongly expect users to tabulate at a given
    geography level e.g. Local Authority, Ward. If no geography is
    required, so records from all geographical areas are together, then
    a 'national' geography including all areas could be used,
    alternatively the geography can be left blank with [] (i.e.
    ```geog=[]```). However, at least one of 'tab_vars' or 'geog' must be
    populated - if both are left blank with [] the code will not work.

6.  Define the arguments of the create_perturbed_table function (data,
    record_key, geog, tab_vars and ptable) and run the function to
    create the table. Example code is provided in the docstrings.
    
 | Variable name | Variable Definition |Type of Variable| Format of specific variable (if applicable)| Expected range of the values | Meaning of the values| Expected level of aggregation | Frequency |Comments | 
 |:---       |:---     |:---     |:---   |:--- |:--- |:--- | :--- | :--- |
 | Record key | A random number 'key' which determines which cells receive perturbation |Integer | Numeric/integer | 0-255 | The values do not carry meaning, but they must remain unchanged to provide consistency in the results | It is expected that users will tabulate 1-4 variables for a particular geography level e.g. tabulate age by sex at local authority level |  | | 


### Outputs

The output from the code is a frequency table with the counts having
been affected by perturbation, as specified in the ptable. For most
ptables, the most obvious effect will be that all counts less than 10
will have been reduced to 0 (removed). Counts being below a threshold is
a condition of exporting data from IDS and other secure environments.
The table will be in the following format:

  |Local Authority | Age | Sex | rs_cv | pcv | pvalue | count |
  |:---            |:--- |:--- |:---   |:--- |:---    |:---   | 
  |Fareham         | 0-15 | 1  | 4072  | 572 | 0      | 4072  |
  |Fareham         | 0-15 | 2  | 3985  | 735 | 0      | 3985  |
  |Fareham         | 16-24 | 1  | 2390  | 640 | +1      | 2391  |
  |Fareham         | 16-24 | 2  | 2276  | 526 | 0      | 2276  |
  |...         | ... | ...  | ...  | ... | ...      | ...  |



### Test data / method illustration

The method requires microdata, a ptable file, and the variables to be
tabulated as inputs. The function counts how many rows in the data
contain each combination of categories e.g. how many respondents are of
each age category in each local authority area. The sum of the record
keys for each record in each cell is also calculated. Modulo 256 of the
sum is taken so this 'cell key' is between 0-255. The table now has cell
values and cell keys.

To reduce the size of the ptable, only 750 rows are used, and rows
501-750 are used repeatedly for larger cell values. E.g. instead of
containing 100,001 rows, when the cell value is 100,001 the 501^st^ row
is used. Rows 501-750 will be used for cell values of 501-750, as well
as 751-1000, 1001-1250, 1251-1500 and so on. To achieve this effect an
alternative cell value column is calculated which will be between 0-750.
For cell values 0-750 the pcv will be the same as the cell value. For
cell values above 750, the values are transformed by -1, modulo 250,
+501. This achieves the looping effect so that cell values 751, 1001,
1251 and so on will have a pcv of 501.

After the pcv and cell keys are calculated, the ptable can be merged on,
matching on pcv and 'ckey'. This merge provides a 'pvalue' for each
cell. The post perturbation count ('count' column) is the
pre-perturbation count ('rs_cv'), plus the perturbation value
('pvalue'). After this step, the counts have had the required
perturbation applied. The output is the frequency table with the
post-perturbation 'count' column.

### Supporting Information

The code only requires standard python operations and uses the pandas
package.
