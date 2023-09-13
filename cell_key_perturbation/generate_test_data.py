# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 11:45:47 2023

Create test data within a secure environment to test the cell key perturbation code
@author: iain dove
"""

import pandas as pd
import numpy as np

np.random.seed(111)

size=1000

record_key_sample = list(np.random.randint(0,256,size))

var1 = list(np.random.choice([1,2,3,4,5], p=[0.25, 0.35, 0.2, 0.1, 0.1], size=(size)))
var2 = list(np.random.choice([1,2], p=[0.5, 0.5], size=(size)))
var3 = list(np.random.choice([1,2,3,4], p=[0.25, 0.35, 0.2, 0.2], size=(size)))
var4 = list(np.random.choice([1,2,3,4], p=[0.25, 0.35, 0.2, 0.2], size=(size)))
var5 = list(np.random.choice([1,2,3,4,5,6,7,8,9,10], p=[0.20, 0.15, 0.08, 0.15, 0.02, 0.025, 0.075, 0.1, 0.1, 0.1], size=(size)))
var6 = list(np.random.choice([1,2,3,4,5], p=[0.25, 0.35, 0.2, 0.1, 0.1], size=(size)))
var7 = list(np.random.choice([1,2,3,4,5], p=[0.25, 0.35, 0.2, 0.1, 0.1], size=(size)))

categories_ABCD = ["A", "B", "C", "D"]
var8 = list(np.random.choice(categories_ABCD,size))

categories_ABCDEFGH = ["A", "B", "C", "D", "E", "F","G","H"]
var9 = list(np.random.choice(categories_ABCDEFGH,size))

var10 = list(np.random.randint(1,50,size))

micro = pd.DataFrame(
    {'record_key' : record_key_sample,
     'var1': var1,
     'var2': var2,
     'var3': var3,
     'var4': var4,
     'var5': var5,
     'var6': var6,
     'var7': var7,
     'var8': var8,
     'var9': var9,
     'var10': var10
    })


"""
#setting inputs: variables, geography, ptable file
record_key="record_key"
geog=["var1"]
tab_vars=["var2","var3"]
#ptable_10_5 = pd.read_csv("\\\\   ptable_location  \ptable_10_5_rule.csv")

#microdata and the ptable need to be read in as dataframes
#using filepaths may be unreliable as it's not known how the data will be stored, formated etc 

#using pre-defined inputs:
perturbed_table= create_perturbed_table(data=micro,
                                    record_key=record_key,
                                    geog=geog,
                                    tab_vars=tab_vars,
                                    ptable=ptable_10_5)
perturbed_table
###############

#setting inputs: variables, geography, ptable file
record_key="record_key"
geog=["var4"]
tab_vars=["var5"]
#ptable_10_5 = pd.read_csv("\\\\   ptable_location  \ptable_10_5_rule.csv")

#microdata and the ptable need to be read in as dataframes
#using filepaths may be unreliable as it's not known how the data will be stored, formated etc 

#using pre-defined inputs:
perturbed_table= create_perturbed_table(data=micro,
                                    record_key=record_key,
                                    geog=geog,
                                    tab_vars=tab_vars,
                                    ptable=ptable_10_5)
perturbed_table
###############

#setting inputs: variables, geography, ptable file
record_key="record_key"
geog=["var1"]
tab_vars=["var5","var8"]
#ptable_10_5 = pd.read_csv("\\\\   ptable_location  \ptable_10_5_rule.csv")

#microdata and the ptable need to be read in as dataframes
#using filepaths may be unreliable as it's not known how the data will be stored, formated etc 


#using pre-defined inputs:
perturbed_table= create_perturbed_table(data=micro,
                                    record_key=record_key,
                                    geog=geog,
                                    tab_vars=tab_vars,
                                    ptable=ptable_10_5)
perturbed_table
###############
"""


"""
Generating 1000 records using seed 111 in numpy, using the ptable_10_5_rule provided for testing, and passing geog=[”var1”] and 
tab_vars=["var2","var3"] (tabulating var1 by var2 by var3) the output should look like this:
  Out[54]: 
    var1  var2  var3  rs_cv  ckey  pcv  pvalue  count
0      1     1     1     25   163   25       0     25
1      1     1     2     51   174   51      -1     50
2      1     1     3     25   149   25       0     25
3      1     1     4     16   104   16      -1     15
4      1     2     1     27   174   27      -2     25
5      1     2     2     35   177   35       0     35
6      1     2     3     23   132   23       2     25
7      1     2     4     24    39   24       1     25
8      2     1     1     36    20   36      -1     35
9      2     1     2     70    41   70       0     70
10     2     1     3     35   253   35       0     35
11     2     1     4     30   245   30       0     30
12     2     2     1     48   155   48       2     50
13     2     2     2     70   246   70       0     70
14     2     2     3     33     9   33       2     35
15     2     2     4     50    92   50       0     50
16     3     1     1     24    88   24       1     25
17     3     1     2     28   109   28       2     30
18     3     1     3     17    27   17      -2     15
19     3     1     4     18    95   18       2     20
20     3     2     1     30   130   30       0     30
21     3     2     2     37    28   37      -2     35
22     3     2     3     23   158   23       2     25
23     3     2     4     13   202   13       2     15
24     4     1     1     17    53   17      -2     15
25     4     1     2     18   181   18       2     20
26     4     1     3     10   215   10       0     10
27     4     1     4     14   195   14       1     15
28     4     2     1     11   128   11      -1     10
29     4     2     2     20   228   20       0     20
30     4     2     3     13   145   13       2     15
31     4     2     4      7   196    7      -7      0
32     5     1     1     12   200   12      -2     10
33     5     1     2     16   124   16      -1     15
34     5     1     3      9   210    9      -9      0
35     5     1     4     11   133   11      -1     10
36     5     2     1     10    69   10       0     10
37     5     2     2     27    34   27      -2     25
38     5     2     3     10    25   10       0     10
39     5     2     4      7    92    7      -7      0
Using ptable_10_5_rule, it should be obvious that counts less than 10 have been removed, and all others have been rounded to the nearest 5    


Generating 1000 records using seed 111 in numpy, using the ptable_10_5_rule provided for testing, and passing geog=["var4"] and 
tab_vars=["var5"] (tabulating var4 by var5) the output should look like this:
Out[56]: 
    var4  var5  rs_cv  ckey  pcv  pvalue  count
0      1     1     40   139   40       0     40
1      1     2     53   204   53       2     55
2      1     3     18    35   18       2     20
3      1     4     45   184   45       0     45
4      1     5      4     7    4      -4      0
5      1     6      3    64    3      -3      0
6      1     7     24   174   24       1     25
7      1     8     30    40   30       0     30
8      1     9     25   252   25       0     25
9      1    10     23   157   23       2     25
10     2     1     64    61   64       1     65
11     2     2     64    78   64       1     65
12     2     3     20   227   20       0     20
13     2     4     39    60   39       1     40
14     2     5      8   240    8      -8      0
15     2     6      7   183    7      -7      0
16     2     7     32    37   32      -2     30
17     2     8     36   216   36      -1     35
18     2     9     39   133   39       1     40
19     2    10     31    64   31      -1     30
20     3     1     30   162   30       0     30
21     3     2     36   200   36      -1     35
22     3     3     18    26   18       2     20
23     3     4     27   189   27      -2     25
24     3     5      3    56    3      -3      0
25     3     6      3    54    3      -3      0
26     3     7     16    45   16      -1     15
27     3     8     23    94   23       2     25
28     3     9     24   147   24       1     25
29     3    10     17    44   17      -2     15
30     4     1     44    69   44       1     45
31     4     2     34   132   34       1     35
32     4     3     19   134   19       1     20
33     4     4     28   167   28       2     30
34     4     5      4   218    4      -4      0
35     4     6      5   145    5      -5      0
36     4     7     17    43   17      -2     15
37     4     8     12   147   12      -2     10
38     4     9     17    48   17      -2     15
39     4    10     18    51   18       2     20

Generating 1000 records using seed 111 in numpy, using the ptable_10_5_rule provided for testing, and passing geog=[”var1”] and 
tab_vars=["var5","var8"] (tabulating var1 by var5 by var8) the output should look like this:
    Out[35]: 
     var1  var5 var8  rs_cv  ckey  pcv  pvalue  count
0       1     1    A     16    63   16      -1     15
1       1     1    B      5   196    5      -5      0
2       1     1    C     10   123   10       0     10
3       1     1    D     10     3   10       0     10
4       1     2    A     12   149   12      -2     10
..    ...   ...  ...    ...   ...  ...     ...    ...
195     5     9    D      0     0    0       0      0
196     5    10    A      2   225    2      -2      0
197     5    10    B      1   230    1      -1      0
198     5    10    C      3    88    3      -3      0
199     5    10    D      0     0    0       0      0

[200 rows x 8 columns] 


"""
