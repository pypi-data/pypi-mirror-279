# from data_extractor.from_logging import log_function_usage
def extract_distinct(cusor_obj,column_name,table_name):
    # log_function_usage('extract_distinct-database-general_functionality.py')
    return cusor_obj.execute(f"SELECT COUNT(DISTINCT {column_name}) AS unique_count FROM {table_name};")

def count_number_for_each_distinct(cusor_obj,column_name,table_name):
    # log_function_usage('count_number_for_each_distinct-database-general_functionality.py')
    cusor_obj.execute(f"SELECT {column_name}, COUNT(*) AS count_per_value FROM {table_name} GROUP BY {column_name} ORDER BY count_per_value DESC;")
    rows = cusor_obj.fetchall()
    final = {}
    if rows:
        for row in rows:
            final[row[0]] = row[1]
        return final 
    else:
        return None
    
def count_number_for_each_distinct_limited_by_scope(cusor_obj, column_count,scope_column, scope_value,table_name,):
    cusor_obj.execute(f"SELECT {column_count}, COUNT(*) AS occurrence_count FROM {table_name} WHERE {scope_column} = '{scope_value}' GROUP BY {column_count}")
    rows = cusor_obj.fetchall()
    # How do I want to return the value?
    final = {}
    if rows:
        for row in rows:
            final[row[0]] = row[1]
        return final 
    else:
        return None





