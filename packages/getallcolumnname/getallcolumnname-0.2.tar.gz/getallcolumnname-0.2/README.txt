Name of the package: getallcolumnname
Version:0.2
Description : 
For a give catalog it will fetch the below : 
databases
tables
columns
================

Installation
------------

You can install this package using pip:

```sh
pip install getallcolumnname==0.2

Restart kernel:
From databricks:
==================
dbutils.library.restartPython()

Usage
-----

Here is an example of how to use the functions in this package:

```python
import getallcolumnname

```python

## List of catalogs/hive_metastore from which you want to fetch all columns:
Lets says name of the catalog is : "catalog_test"
LIST_OF_CATALOG = ["catalog_test"]

For hive_metastore :
LIST_OF_CATALOG = ["hive_metastore"]

num_databases, num_tables, column_counts_df, df_all_columns = getallcolumnname.get_catalogs_and_databases(LIST_OF_CATALOG)

Display all the catalogs/hive_metastore provided, its databases, its corresponding tables and its corresponding columns
display(df_all_columns)

END OF README.TXT

