# Cell Key Perturbation (Python) User Notes

### Finding and Installing the Method

---

This method requires Python 3.7 uses the pandas package.

The Python version of this method can be installed via PyPI and imported using the following code:

```
pip install cell_key_perturbation

from cell_key_perturbation.create_perturbed_table import
create_perturbed_table
```

### Using the Method

---

#### Step-by-Step Instructions

1.  Install the cell key perturbation package from PyPI.

2.  Import the pandas package

3.  Run the import 'create_perturbed_table' function

4.  Define the microdata and ptable. These will need to be read in as pandas dataframes. Example lines of code are provided within the docstrings of the function. The filepaths will need to be edited to the location in which your microdata/ptable is saved.

5.  Set the geog and tab_vars. These will both need to be defined as vectors. For tab_vars, the variables should be supplied in a vector of strings e.g. ```["Age","Health","Occupation"]```. The variables can also be left blank, i.e. ```tab_vars=[]```. The geography is also supplied as a vector e.g. ```["Region"]```. An example is included in the docstrings. We strongly expect users to tabulate at a given geography level e.g. Local Authority, Ward. If no geography is required, so records from all geographical areas are together, then a 'national' geography including all areas could be used, alternatively the geography can be left blank with [] (i.e. ```geog=[]```). However, at least one of 'tab_vars' or 'geog' must be populated - if both are left blank with [] the code will not work.

6.  Define the arguments of the create_perturbed_table function (data, record_key, geog, tab_vars and ptable) and run the function to create the table. Example code is provided in the docstrings.  
    


#### Example Run Through

The microdata and ptable are provided as arguments to the perturbation
function.

Below is a snapshot of an example microdata table and how the input data should look like:

  |Record_key |Region | Age | Sex |
  |:---       |:-----   |:--- |:--- | 
  |84 |Fareham         | 0-15 | 2  |
  |108 |Fareham         | 0-15 | 1  | 
  |212 |Fareham         | 16-24 | 1  | 
  |86 |Fareham         | 16-24 | 2  | 
  |19 |Fareham         | 16-24 | 2  |
  |... |...         | ... | ...  |

The 'ptable' file contains the parameters which determine which cells are perturbed and which are not (most cells are perturbed by +0). The ptable contains each possible combination of cell key (0-255) and cell value, and the perturbation a cell with that cell key and cell value would receive. A user must use the provided ptables to ensure sufficient protection. 


Example rows of a ptable are shown below:

 | pcv      | ckey           | pvalue      |
 |:---              | :----             | :---        |
 |  1               | 0                 | 0           |
 |  1               | 1                 | 0           |
 |  1               | 2                 | +1           |
 |  1               | 3                 | 0           |
 |  ...             | ...               | ...           |


By default a ptable that applies the '10-5 rule' is provided in this package (ptable_10_5). This ptable will remove all cells <10, and round all others to the nearest 5. This provides more protection than necessary but will ensure safe outputs. Other ptables may be available depending on the data used, for example census data will require the ptable_census21 to be used.


To run the method using the example data above you can create a python file in your desired IDE and do the following below:

```
# We can pass our data into the method and save the output to a perturbed table.


# First, specifying key variables
record_key = "Record_key"    
geog = ["Region"]
tab_vars = ["Age","Sex"]


# Calling the perturbation function
perturbed_table = create_perturbed_table(data = micro,
                                        record_key = record_key,
                                        geog = geog,
                                        tab_vars = tab_vars,
                                        ptable = ptable)


# Another example using direct inputs, and selecting no geography breakdown
perturbed_table= create_perturbed_table(data = micro,
                                        record_key = "Record_key",
                                        geog = [],
                                        tab_vars = ["Age", Sex"],
                                        ptable = ptable)


```  
  

#### Example Output

The output from the code is a frequency table with the counts having been affected by perturbation, as specified in the ptable. For most ptables, the most obvious effect will be that all counts less than 10 will have been reduced to 0 (removed). Counts being below a threshold is a condition of exporting data from IDS and other secure environments. The table will be in the following format:

  |Region | Age | Sex | rs_cv | pcv | pvalue | count |
  |:-----           |:--- |:--- |:---   |:--- |:---    |:---   | 
  |Fareham         | 0-15 | 1  | 4072  | 572 | 0      | 4072  |
  |Fareham         | 0-15 | 2  | 3985  | 735 | 0      | 3985  |
  |Fareham         | 16-24 | 1  | 2390  | 640 | +1      | 2391  |
  |Fareham         | 16-24 | 2  | 2276  | 526 | 0      | 2276  |
  |...         | ... | ...  | ...  | ... | ...      | ...  |



### Additional Information

---

The ONS Statistical Methods Library website [methods page](https://statisticalmethodslibrary.ons.gov.uk/methods) contains further information about the methods including a methodological specification, which contains further detail about the mathematical definition of the method algorithm and a link to the github repository which contains detailed API information as part of the method code.

### License

---

Unless stated otherwise, the SML codebase is released under the [MIT License](https://github.com/ONSdigital/sml-python-small/blob/main/LICENSE). This covers both the codebase and any sample code in the documentation.

The documentation is available under the terms of the [Open Government 3.0 license](https://github.com/ONSdigital/sml-supporting-info/blob/main/LICENSE).
