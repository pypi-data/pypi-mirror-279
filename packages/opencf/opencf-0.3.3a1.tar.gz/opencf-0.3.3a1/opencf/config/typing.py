import typing as _typing

import numpy as np

if _typing.TYPE_CHECKING:
    NumPyArrayNumeric = np.ndarray[
        _typing.Any, np.dtype[np.integer[_typing.Any] | np.floating[_typing.Any]]
    ]
else:
    NumPyArrayNumeric = np.ndarray

MatLike = NumPyArrayNumeric
