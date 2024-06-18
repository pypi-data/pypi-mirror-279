from datetime import datetime

def create(name, extension:str = "csv"):
    current_date = datetime.now().strftime("%Y_%M_%dT%H_%m_%S")
    return f"{name}_{current_date}.{extension}"