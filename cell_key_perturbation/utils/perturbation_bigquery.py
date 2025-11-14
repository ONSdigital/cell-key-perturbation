

def build_perturbation_bigquery(data, 
                                ptable, 
                                geog, 
                                tab_vars, 
                                record_key, 
                                threshold=10
                                ):
    """
    Generates a dynamic BigQuery query for cell key perturbation using 
    a microdata table and a perturbation table.

    This function constructs a query that:
    - Computes counts and cell keys for each unique combination of geographic 
    and tabulation variables.
    - Includes zero-count cells by generating the full Cartesian product of 
    variable combinations.
    - Calculates pcv by ensuring the rows of ptable 501-750 are reused for 
    cell values above 750
    - Applies perturbation values from a perturbation table based on cell keys 
    and pseudo cell values (pcv).
    - Suppresses cells below a specified threshold by setting their perturbed 
    count to NULL.
    
    Parameters:
    ----------
    data : str
        Full name and location of the microdata table in the BigQuery database.
    ptable : str
        Full name and location of the ptable in the BigQuery database.
    geog : list of str
        List of geographic variable names to group by (e.g., region, district).
    tab_vars : list of str
        List of tabulation variable names to group by (e.g., age, gender).
    record_key : str
        The name of the column in the microdata table used to compute cell keys 
        (typically a unique identifier).
    threshold : int, optional
        Suppression threshold; cells with perturbed counts below this value 
        will be suppressed (set to NULL).
        Default is 10.

    Returns:
    -------
    str
        A query string that can be executed against a BigQuery database 
        containing the specified microdata and perturbation tables.
    """
    all_vars = geog + tab_vars
    all_vars_str = ", ".join(all_vars)

    dim_ctes = [f"dim_{v} AS (SELECT DISTINCT {v} FROM distinct_vars)" 
                for v in all_vars]
    dim_ctes_str = ",\n\t".join(dim_ctes)

    cross_join = "\n\tCROSS JOIN ".join([f"dim_{v}" for v in all_vars])
    join_conditions = " AND ".join([f"g.{v} = b.{v}" for v in all_vars])
    select_columns = ", ".join([f"g.{v}" for v in all_vars])

    query = f"""
-- Step 1: Create dimension tables
    WITH
        distinct_vars AS (
            SELECT DISTINCT {all_vars_str}
            FROM `{data}`
        ),
        {dim_ctes_str},

-- Step 2: Create full grid of all combinations
    full_grid AS (
        SELECT *
        FROM {cross_join}
    ),

-- Step 3: Aggregate actual counts
    base_counts AS (
        SELECT
            {all_vars_str},
            COUNT(*) AS pre_sdc_count,
            SUM(CAST({record_key} AS INT64)) AS sum_rkey
        FROM `{data}`
        GROUP BY {all_vars_str}
    ),

-- Step 4: Join full grid with actual counts
    full_counts AS (
        SELECT
            {select_columns},
            COALESCE(b.pre_sdc_count, 0) AS pre_sdc_count,
            COALESCE(b.sum_rkey, 0) AS sum_rkey
        FROM full_grid g
        LEFT JOIN base_counts b
            ON {join_conditions}
    ),

-- Step 5: Compute cell key modulo
    ckey_mod AS (
        SELECT *,
            MOD(sum_rkey, (SELECT MAX(ckey) + 1 FROM `{ptable}`)) AS ckey
        FROM full_counts
    ),

-- Step 6: Calculate pcv
    pcv_calc AS (
        SELECT *,
            CASE
                WHEN pre_sdc_count <= 750 THEN pre_sdc_count
                ELSE MOD((pre_sdc_count - 1), 250) + 501
            END AS pcv
        FROM ckey_mod
    ),

-- Step 7: Join with perturbation table
    joined AS (
        SELECT
            {all_vars_str},
            a.pre_sdc_count,
            a.ckey,
            a.pcv,
            COALESCE(b.pvalue, 0) AS pvalue
        FROM pcv_calc a
        LEFT JOIN `{ptable}` b
            ON a.pcv = b.pcv AND a.ckey = b.ckey
    ),

-- Step 8: Apply perturbation and suppression
    final_table AS (
        SELECT *,
            pre_sdc_count + pvalue AS raw_count,
            CASE
                WHEN pre_sdc_count + pvalue < {threshold} THEN NULL
                ELSE pre_sdc_count + pvalue
            END AS count
        FROM joined
    )
    
-- Final output
    SELECT
        {all_vars_str},
        pre_sdc_count,
        ckey,
        pcv,
        pvalue,
        count
    FROM final_table;
    """
    return query
