# Extracted Code

```python
attribute_value = None
    for column in attribute_value_query_result:
    attribute_value = column.column_name
    return attribute_value
    attribute_date_query = f"
    tests
    get_table_data.py
    Educkdb.db
    get_fact_table
    attribute_date_query_job = CLIENT.query(attribute_date_query)
    generate_schema_yml.py
    attribute_value_query_job = CLIENT.query(attribute_value_query)
    attribute_value_query
    dbt_project
    get_fact_tables
    Imp Code
from google.cloud import bigquery
alltable_function_generator.py
generate_test_model_files.py
generate_dbt_model_files.py
AND (LOWER (column_name) LIKE '%value%');
WHERE table_name = '{curr_table_name}'
all_columns.append(column.column_name)
return closest_date_col
from google.cloud.bigquery.table import RowIterator
CLIENT = bigquery.Client (project=PROJECT_ID)
PROJECT_ID = "ai-cwow-store-dev-b082"

def get_attribute_value(curr_table_name:str) -> str:
get_attribute_value
FROM `{PROJECT_ID}.cwow_store . INFORMATION_SCHEMA. COLUMNS
attribute_date_query_result = attribute_date_query_job.result()
dbt_project.yml
closest_date_col = get_closest_column (all_columns , curr_table_name)
table_data
attribute_value_query_result = attribute_value_query_job.result()
AND (LOWER(column_name) LIKE '%date%');
.gitignore

def get_closest_column (all_cols : str, curr_table_name: str) -> str:
update_metadata_csv.py
all_columns = []
_test_model_files.py
_function_generator.py
metadata_csv.py
schema.py
_drop_functions.py
FROM `{PROJECTID }.cwow_store . INFORMATION_SCHEMA. COLUMNS
_dbt_model_files.py
attribute_value_query = f".
= None
drop_functions.py

def get_attribute_date(curr_table_name: str) -> str:
SELECT column_name
    for column in attribute_date_query_result:
    csvs_output.py
    dbt_model_files.py
    curr_words = curr_table_name. lower().split("_")
    for col in all_cols:
    for word in curr_col_words:
    attribute_date_query_job.result()
    attribute_date_query_result =
    float("-inf")
    max_same_words
    curr_table_name.lowe r().split ("_")
    curr_words =
    col. lower().split ("_")
    WHERE table_name
    (curr_table_name
    test_model_files.py
    FROM {PROJECT_ID} .cwow store.INFORMATION_SCHEMA.COLUMNS
    schema_yml.py
    closest_col = None
    curr_col_words = col. lower().split("_")
    max_same_words = float("-inf")
    Ccubiect areal fact
    FROM `{PROJECT_ID}.cwow_store. INFORMATION_SCHEMA. TABLES
    closest_col = col
    model_files.py
    _generator.py
    _functions.py
    if word in curr_words:
    return closest_col
    WHERE table_name LIKE 'repo {subject_area}% fact'

def get_fact_tables_and_attributes (subject_area: str):
return table_name_query_result
Get all the fact tables, and there associated attirbute values, date, table_name, and feature name
_schema_yml.py
    if subject_area == "orders":
    else:
    -_Gen
    WHERE table_name LIKE 'repo_{subject_area}_fact'
    curr total
    = CLIENT.query(table_query)
    closest_col
    functions.py

def get_table_names (subject_area:str)
FROM {PROJECT_ID} .cwow store. INFORMATION SCHEMA. TABLES
table_query =
SELECT table_name
vitals' we are retreiving the table info for
subject_area (str): The subject_area name
table_name_query_job
table_name_query_result
== "orders":
les.py
__csv.py
2_generator.py
table_name_query_job.result()
det get table_names (subject_area:str) -> RowIterator:
table_query = fm
table_name_query_result = table_name query_job.result()
AND table_name NOT LIKE 'repo_orders_hd%';"
csv.py
get_attribute_date(curr_table_name=cu rr_table_name)
(list) : A list a of all the fact tables and there attirbute values, date, table_name, and feature name
continue
return tables
curr_table_name == "repo_orders_hd_nocturnal_flag_fact"
tables =
"repo_patient transplant fact"
"repo_patient amputation_fact"
attribute_date
_yml.py
== "score":
or curr_table_name == "repo_patient amputation_fact"
feature_name = feature_name.replace("score_", "kdqol score_")
get table_names (subject_area=subject_area)
== "repo_dialysis_servicefact"
tables.append((attrbute_value, attribute_date, curr_table_name, feature_name))
ml.py
attrbute_value = get_attribute_value(curr_table_name=curr_table_name)
curr_table_name. replace("repo_", "").replace(" fact", "")
or curr_table_name
generator.py
ctions.py
"repo_patient amputation fact"
feature_name.replace("score_", "kdqol score_")
111111
sv.py
iles.py
feature_name =
UTF-8
nerator.py
feature_name = feature_name. replace("score_", "kdqol_score_")
st_model_files.py
adata_csv.py
svs output.py
data.py
ot_model_files.py
nction_generator.py
table_names =
attrbute_value
    if subject_a rea
    attribute_date = get_attribute_date(curr_table_name=curr_table_name)
    if subject_area == "score":
    "repo_orders_hd_nocturnal_flag_fact"
    "repo_patient_transplant fact"
    odel_files.py
    (method) def append(
    Append object to the end of the list.
    feature
    object: Any,
    ta.py
    "repo_patient_transplant_fact"
    e("score_", "kdqol_score_")
    tion_generator.py
    or curr_table_name == "repo_dialysis_service_fact"
    generate_csvs_output.py
    # get the curr_table_name
    packages.yml
    update_schema.py
    README.md
    duckdb.db
    or curr_table_name ** "repo dialysis service fact"
    pom.xml
    attribute_date = get_attribute_date(curr_table_name=curr_tabl
    generi
    curr_table_name = table_name.table_name
    helger.py
    le.replace("score_", "kdqol_scor
    "repo_patient_amputation_fact"
    "repo_dialysis_service_fact"
    operations.py
    get_attribute_value(cu rr_table_name=cu rr_tab
    or curr_table_name == "repo_patient_amputation_fact"
    table_name.table_name
    testing/src/feature_store_sql/generate_table_functions/generators/utils/helper.py
    gener feature-
    get_table_names (subject_area=subject_area)
    je.replace("score_", "kdqol_score_")
    te_drop_functions.py
    TIMELINE
    utils
    subject_area (str): The subject_area name -- 'vitals' we are retreiving the table info for
    for table_name in table_names :
    or curr_table_name == "repo_patient_transplant_fact"
    get_attribute_value(cu rr_table_name=cu rr_table_name)
    operations
    helper.py
    feature_name = curr_table_name, replace(" repo_", "").replace ("_fact", "")
    model files.py
    ackages.yml
    Args:
    date_metadata_csv.py
    table_names = get_table_names (subject_area=subject_area)
    table_data.py
    ations.py
    data
    table_query = fum
    er.py
    max_same_words = curr_total
    ators
    table_name_query_job = CLIENT.query(table_query)
    table_name_query_result = table_name_query_job.result()
    Returns:
    files.py
    _schema.py
    _metadata_csv.py
    ions.py
    curr_total += 1
    table_query = f"
    tions.py
    Func_Gen
    generate_drop_functions.py

def get_table_names(subject_area:str) -> RowIterator:
generators
all_table_function_generator.py
curr_total = 0
Launchpad
BQ_SQL_Func_Gen
DELL
OUTLINE
attribute_value_que ry_job
attribute_value_query_result
attribute_value_query_job.result()
clocest col - None
```