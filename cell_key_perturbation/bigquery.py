
import pandas as pd

from cell_key_perturbation.utils.perturbation_bigquery import build_perturbation_bigquery
from cell_key_perturbation.utils.validate_inputs_before_perturbation import validate_inputs_bigquery

def create_perturbed_table_bigquery(client,
                                    data,
                                    ptable,
                                    geog,
                                    tab_vars,
                                    record_key,
                                    use_existing_ons_id = True,
                                    threshold = 10
                                    ):
    """
    Function creates a frequency table which has has a cell key perturbation 
    technique applied with help from a p-table. 
    This function runs the method in BigQuery with SQL before reading the 
    microdata and ptable into the memory. Therefore, it's able to handle 
    large datasets faster and without memory issues.
    
    This function applies the following steps:
        1) Validate inputs
        2) Build the frequency table from micro data
        3) Merge the frequency table with perturbation table
        4) Apply perturbation and suppression
    
    Parameters:
    ----------
    client : google.cloud.bigquery.client
        Google Cloud BigQuery Client object
    data : str
        Full name and location of the microdata table in the BigQuery database,
        in a full BigQuery table format: <PROJECT>.<DATASET>.<TABLE>
        The data should contain one row per statistical unit (person, 
        household, business or other) and one column per variable (e.g. age,
        sex, health status)
    ptable : str
        Full name and location of the ptable in the BigQuery database,
        in a full BigQuery table format: <PROJECT>.<DATASET>.<TABLE>
    geog : list of str
        A vector with one entry, the column name in 'data' that contains the 
        desired geography level for the frequency table. 
        The column name should be held in a string. For example ["Region"], 
        ["Local Authority"]. If no geography breakdown is 
        needed, this should be an empty vector: []
    tab_vars : list of str
        A vector containing the column names in 'data' of the variables to be 
        tabulated. For example ["Age","Health","Occupation"]
    record_key : str
        The column name in 'data' that contains the record keys required for 
        perturbation. For example: "Record_Key"
    use_existing_ons_id : Boolean
        Whether to create record keys from ons_id, if ons_id exists in data.
        It will be irrelevant if microdata does not contain ons_id.
        Default is True.
    threshold : integer
        Suppression threshold; cells with perturbed counts below this value
        will be suppressed (set to NULL).
        Default is 10.
        
    Returns:
    -------
    perturbed_table : pandas.DataFrame
        A frequency table which has had cell key perturbation and a suppression
        threshold applied.
    """
    
    query = build_perturbation_bigquery(data = data,
                                        ptable = ptable,
                                        geog = geog,
                                        tab_vars = tab_vars,
                                        record_key = record_key,
                                        threshold = threshold
                                        )
    
    # Update query to generate record keys from "ons_id" if exists
    columns = [field.name for field in client.get_table(data).schema]
    
    if use_existing_ons_id & ("ons_id" in columns):
        print('NOTE: "ons_id" column is available in data!',
              'Updating query to generate record keys from "ons_id"!')
    
        query = query.replace(
            f"CAST({record_key} AS INT64)",
            "MOD(SAFE_CAST(ons_id AS INT64), 4096)"
            )
    
    validate_inputs_bigquery(client = client,
                             data = data,
                             ptable = ptable,
                             geog = geog,
                             tab_vars = tab_vars,
                             record_key = record_key,
                             use_existing_ons_id = use_existing_ons_id,
                             threshold = threshold
                             )
    
    perturbed_table = client.query(query).to_dataframe()
    
    perturbed_table = (
        perturbed_table.sort_values(geog + tab_vars)
                       .reset_index(drop=True)
    )
    
    return perturbed_table