from datetime import datetime
import pandas as pd

def add_patition_dates(df:pd.DataFrame, current_date:datetime) -> pd.DataFrame:
    df['year'] = current_date.year
    df['month'] = current_date.month
    df['day'] = current_date.day
    return df

# Definir la función para convertir a datetime y quitar la zona horaria
def convert_to_datetime_without_timezone(dt_str):
    return pd.to_datetime(dt_str, format="ISO8601").dt.strftime("%Y-%m-%d %H:%M:%S")