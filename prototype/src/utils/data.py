import typing
import pandas as pd

QSIM_CSV_HEADER: str = "id,x,y\n"
def open_csv(name: str) -> typing.IO:
    f = open(name, "w")
    f.write(QSIM_CSV_HEADER)
    return f


def csv_to_dataframe(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename)
