import json
import pandas as pd

from pyspark.sql.types import *
from pyspark.sql import SparkSession

def schema_json(df:pd.DataFrame):
    columns_list = []
    for col_name, col_type in df.dtypes.items():
        
        column_dict = {
            "Name": col_name
            ,"Type": str(col_type).replace("datetime64[ns]", "timestamp"
                                 ).replace("object", "string"
                                 ).replace("int64", "bigint"
                                 ).replace("Int64", "bigint"
                                 ).replace("float64", "double"
                                 ).replace("Float64", "double")
            ,"Comment": ""
        }
        columns_list.append(column_dict)

    # Convertir la lista de diccionarios a formato JSON
    schema_json = json.dumps(columns_list, indent=2)

    # Imprimir el JSON generado
    print(schema_json)

    return schema_json

def equivalent_type(f):
    if f == 'datetime64[ns]': return TimestampType()
    elif f == 'int32': return IntegerType()
    elif f == 'Int32': return IntegerType()
    elif f == 'int64': return LongType()
    elif f == 'Int64': return LongType()
    elif f == 'float64': return FloatType()
    elif f == 'Float64': return FloatType()
    else: return StringType()

def define_structure(string, format_type):
    try: typo = equivalent_type(format_type)
    except: typo = StringType()
    return StructField(string, typo)

# Given pandas dataframe, it will return a spark's dataframe.
def pandas_to_spark(spark:SparkSession, pandas_df:pd.DataFrame, manual_types=[]):
    columns = list(pandas_df.columns)
    types = list(pandas_df.dtypes)
    struct_list = []
    for column, typo in zip(columns, types): 
      struct_list.append(define_structure(column, typo))
    p_schema = StructType(struct_list)
    return spark.createDataFrame(pandas_df, p_schema)