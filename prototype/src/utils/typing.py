from typing import Annotated, Literal
import numpy as np
import numpy.typing as npt

scalar = np.float64
vector = Annotated[npt.NDArray[scalar], Literal[2]]
matrix = Annotated[npt.NDArray[scalar], Literal['N', 'N']]

