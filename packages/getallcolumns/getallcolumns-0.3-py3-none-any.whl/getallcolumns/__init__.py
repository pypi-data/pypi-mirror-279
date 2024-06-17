

# COMMAND ----------

#with try catch
#working version
def get_hello():
    result = "True"
    print("New package")
    return result

def get_catalogs_and_databases(LIST_OF_CATALOG):
    # Initialize Spark Session
    #spark = SparkSession.builder.appName("GetCatalogsAndDatabases").getOrCreate()
    
    # Initialize variables
    df_catalogs_and_databases = None
    df_tables = None
    df_all_columns = None
    column_counts = []
    df_catalogs_and_databases_and_tables = None  # Initialize here
    
    try:
        for catalog in LIST_OF_CATALOG:
            print(f"Fetching databases in catalog: {catalog}")
            _df = spark.sql(f'SHOW DATABASES IN {catalog}')\
                .select(
                    lit(catalog).alias('catalog'),
                    col('databaseName').alias('database')
                )
            
            # Union the DataFrame to collect all databases across catalogs
            if df_catalogs_and_databases is None:
                df_catalogs_and_databases = _df
            else:
                df_catalogs_and_databases = df_catalogs_and_databases.union(_df)

        # Collect all databases and count the number of databases
        list_catalogs_and_databases = [
            {
                'catalog': row[0], 
                'database': row[1]
            } 
            for row in df_catalogs_and_databases.collect()
        ]
        
        print("List of databases found:")
        for db in list_catalogs_and_databases:
            print(f"Catalog: {db['catalog']}, Database: {db['database']}")
        
        num_databases = len(list_catalogs_and_databases)

        # Loop through databases and tables to collect all tables and count them
        for current_item in list_catalogs_and_databases:
            try:
                print(f"Fetching tables in catalog: {current_item['catalog']}, database: {current_item['database']}")
                df_tables = spark.sql(f"SHOW TABLES IN {current_item['catalog']}.{current_item['database']}")\
                    .select(
                        lit(current_item['catalog']).alias('catalog'),
                        lit(current_item['database']).alias('database'),
                        col('tableName').alias('table')
                    )

                if df_catalogs_and_databases_and_tables is None:
                    df_catalogs_and_databases_and_tables = df_tables
                else:
                    df_catalogs_and_databases_and_tables = df_catalogs_and_databases_and_tables.union(df_tables)
            
            except Exception as e:
                print(f"Error fetching tables in catalog {current_item['catalog']} and database {current_item['database']}: {str(e)}")
                continue

        list_catalogs_and_databases_and_tables = [
            {
                'catalog': row[0],
                'database': row[1],
                'table': row[2]
            }
            for row in df_catalogs_and_databases_and_tables.collect()
        ]

        print("List of tables found:")
        for table in list_catalogs_and_databases_and_tables:
            print(f"Catalog: {table['catalog']}, Database: {table['database']}, Table: {table['table']}")
        
        num_tables = len(list_catalogs_and_databases_and_tables)

        # Loop through tables to collect all columns and count them
        for current_item in list_catalogs_and_databases_and_tables:
            try:
                table_full_name = f"{current_item['catalog']}.{current_item['database']}.{current_item['table']}"
                print(f"Fetching columns for table: {table_full_name}")
                df_columns = spark.sql(f"DESCRIBE TABLE {table_full_name}")\
                    .select(
                        lit(current_item['catalog']).alias('catalog'),
                        lit(current_item['database']).alias('database'),
                        lit(current_item['table']).alias('table'),
                        col('col_name').alias('column')
                    ).filter(col('column') != '')
                
                column_count = df_columns.count()
                column_counts.append((current_item['catalog'], current_item['database'], current_item['table'], column_count))

                if df_all_columns is None:
                    df_all_columns = df_columns
                else:
                    df_all_columns = df_all_columns.union(df_columns)
            
            except Exception as e:
                print(f"Error fetching columns for table {table_full_name}: {str(e)}")
                continue

        # Create DataFrame for column counts
        column_counts_df = spark.createDataFrame(column_counts, ["catalog", "database", "table", "column_count"])

        return num_databases, num_tables, column_counts_df, df_all_columns
    
    except Exception as e:
        print(f"Error occurred in the main function: {str(e)}")
        raise

if __name__ == "__main__":
    # Initialize Spark Session inside the main block
    #spark = SparkSession.builder.appName("GetCatalogsAndDatabases").getOrCreate()
    
    try:
        # Call the function with the list of catalogs
        num_databases, num_tables, column_counts_df, df_all_columns = get_catalogs_and_databases(LIST_OF_CATALOG)
        
        # Print counts
        print(f"Number of databases: {num_databases}")
        print(f"Number of tables: {num_tables}")
        
        # Show the DataFrame with column counts for each table
        #column_counts_df.show(truncate=False)
        display(column_counts_df)
        #df_all_columns.show(truncate=False)
        display(df_all_columns)
    
    except Exception as e:
        print(f"Error occurred in the main block: {str(e)}")

