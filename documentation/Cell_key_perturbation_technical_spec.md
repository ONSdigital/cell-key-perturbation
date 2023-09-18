# Cell key Perturbation Technical specification (python cell-key-perturbation)

### 1.0 Meta

Support area -- Methodology -- Statistical Disclosure Control

Support contact <sdc.queries@ons.gov.uk>

Method theme -- disclosure control

(Method classification -- post-tabular disclosure control)

Status -- In use (census 2021)

### 2.0 Description

Cell key perturbation adds noise ('perturbation') to cell counts in
frequency tables. This noise introduces uncertainty in individual
values, and thereby introduces uncertainty to potential disclosures. The
method is specifically designed to protect against disclosure by
differencing.

### 3.0 Terminology

Record key -- A random number between 0-255 assigned to each record
(person, household or other statistical unit). These keys do not change.
(A range of 0-255 is used for census 2021, an alternative implementation
may use a different range like 0-4095 or decimals between 0 and 1)

Cell key -- The sum of record keys for a given cell. Modulo 256 is taken
so the cell keys remain in the range 0-255.

Cell value -- The number of records in cell, ie the number of people
with given characteristics

pvalue -- perturbation value. The value of noise added to cells, e.g.
+1, -1

pcv -- perturbation cell value. This is an amended cell value needed to
merge on the ptable

ptable -- perturbation table. The lookup file containing the pvalues,
this determines which cell get perturbed.

### 4.0 Method input and output

Arguments: (data, record_key, tab_vars, geog, ptable)

Data -- the data to be analysed. Input data must be one row per record
(person, household, business, or other statistical unit) and one column
per variable (geography, age, sex etc).

Record key - Data must contain a column for record keys, which are
numeric (integers) over a fixed range. The record keys must be
approximately uniformly distributed. Census record keys are in the range
0-255.

tab_vars - The variables to be tabulated are supplied, not including
geography. No variables can be used by entering tab_vars as a blank
vector ```( tab_vars = \[ \] )```.

geog -- the geographic level for the data to be tabulated by. No
geography can be used by entering geog as a blank vector ```( geog = \[ \])```. If no geography and no tab_vars are entered the code will fail (no
variables to tabulate).

ptable - A parameter file, known as the 'ptable' also needs to be
supplied. The ptable contains one row for each combination of cell value
and cell key, and the corresponding pvalue to apply to that cell. The
ptable needs three columns: pcv -- the cell value before the
perturbation, ckey -- the sum of record keys for that cell, and pvalue
-- the value that cell is set to be perturbed by.

The output is a frequency table, with counts of records for each
combination of the supplied variables, which have been altered by the
addition of the noise.

### 5.0 Algorithm

The user supplies the data to be analysed, variables to be tabulated
including geography, and the ptable.

A standard frequency table is produced containing combinations of the
provided variables and the number of records with those characteristics.

A similar table is produced on the same variables taking the sum of the
record keys for each cell (row) of the frequency table. These tables are
merged so the table now contains both the number of records in a cell
and the sum of the record keys of those records.

Modulo 256 is taken of the sum of record keys to produce 'cell keys'
which are uniform distributed in the range 0-255.

A 'pcv' is created: Where the cell value \<= 750, pcv = cell value\
where cell value \>750, pcv = modulo((cell value -1), 250), +501.

The ptable, containing pvalues, is merged onto the frequency table
matching on pcv and cell key.

The post perturbation value = cell value + pvalue. This post-SDC value
is used in outputs.

### 6.0 Error handling

Input data will need to be checked for errors, and that data contains
record keys in the appropriate format.

Any planned data editing should also be performed before the
perturbation. The method will assume the data is correct and produce
outputs accordingly.

Where data contain missing values, the method will by default carry out
perturbation and produce results for missing categories. If categories
are to be combined or values imputed to replace missing data, this
should be done before the perturbation.
