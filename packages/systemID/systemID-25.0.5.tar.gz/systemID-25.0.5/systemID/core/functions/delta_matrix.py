"""
Author: Damien GUEHO
Copyright: Copyright (C) 2023 Damien GUEHO
License: Public Domain
Version: 25
"""


import numpy
from systemID.core.functions.markov_parameters import time_varying_markov_parameters

def delta_matrix(A,
                 B,
                 C,
                 D,
                 tk,
                 dt,
                 number_steps):

    # Get dimensions
    output_dimension, input_dimension=D(tk).shape

    # Get Delta Matrix
    Delta = numpy.zeros([number_steps * output_dimension, number_steps * input_dimension])


    for i in range(number_steps):
        tvmp = time_varying_markov_parameters(A, B, C, D, i * dt + tk, dt, i + 1)
        Delta[i * output_dimension:(i + 1) * output_dimension, 0:(i + 1) * input_dimension] = numpy.concatenate(tvmp[::-1], axis=1)

    return Delta
