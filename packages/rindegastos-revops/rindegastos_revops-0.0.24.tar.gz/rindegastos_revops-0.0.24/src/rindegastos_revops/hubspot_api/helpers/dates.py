from datetime import datetime
import pandas as pd

def str_isoformat(date:datetime) -> str:
    return  f"{date.isoformat(timespec='milliseconds')}Z"

def convert_to_datetime_without_timezone(dt_str):
    return pd.to_datetime(dt_str, format="ISO8601").dt.strftime("%Y-%m-%d %H:%M:%S")