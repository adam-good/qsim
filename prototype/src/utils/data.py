import typing
import numpy as np
import pandas as pd
import quantum.qubit as q

QSIM_CSV_HEADER: str = "id,x,y\n"
def open_csv(name: str) -> typing.IO:
    f = open(name, "w")
    f.write(QSIM_CSV_HEADER)
    return f


def csv_to_dataframe(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename)

def csv_to_list(filename: str) -> dict[str, list[q.QuantumState]]:
    df = pd.read_csv(filename) # TODO: don't use pandas
    data: dict[str, list[q.QuantumState]] = {label:[] for label in df['id']}
    tuples = zip(df['id'], df['x'], df['y'])
    for (label, x, y) in tuples:
        vec = np.array([x,y])
        data[label].append(q.QuantumState(vec))

    return data   
