import pandas as pd
from django.conf import settings

def read_files(file, index_col=None):
    table = pd.read_csv(f"{settings.BASE_DIR}/data/{file}.csv", index_col=index_col)
    return table

def get_Ke(d, value):
    for k, v in d.items():
        if v == value:
            return k
        elif k == value:
            return v