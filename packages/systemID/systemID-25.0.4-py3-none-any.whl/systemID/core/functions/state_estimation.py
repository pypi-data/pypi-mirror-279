"""
Author: Damien GUEHO
Copyright: Copyright (C) 2023 Damien GUEHO
License: Public Domain
Version: 25
"""


import numpy
import scipy

from systemID.core.functions.observability_matrix import observability_matrix
from systemID.core.functions.delta_matrix import delta_matrix

def state_estimation(input_data: numpy.ndarray,
                     output_data: numpy.ndarray,
                     A,
                     B,
                     C,
                     D,
                     number_steps: int,
                     dt: float,
                     tk: float = 0):

    output_dimension, input_dimension = D(tk).shape

    time_step = int(round(tk / dt))

    u = input_data[:, time_step:time_step+number_steps]
    y = output_data[:, time_step:time_step+number_steps]

    U = u.T.reshape(1, number_steps * input_dimension).reshape(number_steps * input_dimension, 1)
    Y = y.T.reshape(1, number_steps * output_dimension).reshape(number_steps * output_dimension, 1)

    O = observability_matrix(A, C, number_steps, tk=tk, dt=dt)

    Delta = delta_matrix(A, B, C, D, tk, dt, number_steps)

    x = scipy.linalg.pinv(O) @ (Y - Delta @ U)

    return x