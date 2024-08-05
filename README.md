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

This is an example showing how to create a perturbed table from data
which has been included in this package in order to showcase the method.

micro - example dataset (pandas dataframe) containing randomly generated
data.

ptable_10_5 - example ptable (pandas dataframe) containing the rules to
apply cell key perturbation with a threshold of 10 and rounding to base
5.

```
from cell_key_perturbation.create_perturbed_table import create_perturbed_table

perturbed_table = create_perturbed_table(data = micro,
                                         record_key = "record_key",
                                         geog = ["var1"],
                                         tab_vars = ["var5","var8"],
                                         ptable = ptable_10_5,
                                         threshold=10)
```


