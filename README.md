# cell_key_perturbation

<!-- badges: start -->
<!-- badges: end -->

This is the python package which runs the SDC methods required for 
frequency tables in IDS.
It enables the user to create a frequency table which has cell key
perturbation applied to the counts, meaning that users cannot be sure
whether differences between tables represent a real person, or are
caused by the perturbation.

Cell Key Perturbation is consistent and repeatable, so the same cells
are always perturbed in the same way.


## Installation

The method package can be installed from PyPI using :

```
pip install cell_key_perturbation
```

## Example

This is an example showing how to create a perturbed table from sample data 
generated with provided test data generation functions in this package 
in order to showcase the method.

To generate example microdata and a perturbation table for testing purposes, 
use the following code:

```
from cell_key_perturbation.utils.generate_test_data import generate_test_data
from cell_key_perturbation.utils.generate_test_ptable import generate_ptable_10_5_rule

micro = generate_test_data()
ptable_10_5 = generate_ptable_10_5_rule()
```

- **`micro`**: A sample `pandas.DataFrame` containing randomly generated microdata. 

- **`ptable_10_5`**: A sample perturbation table (`pandas.DataFrame`) that 
defines the cell key perturbation rules. It uses a threshold of **10** and 
applies rounding to the nearest **5**.


To create a perturbed table, first import the main function:

```
from cell_key_perturbation.create_perturbed_table import create_perturbed_table
```

Then, use the following code to generate the perturbed table using the sample microdata and perturbation table:

```
perturbed_table = create_perturbed_table(data = micro,
                                         record_key = "record_key",
                                         geog = ["var1"],
                                         tab_vars = ["var5","var8"],
                                         ptable = ptable_10_5,
                                         threshold=10)
```
