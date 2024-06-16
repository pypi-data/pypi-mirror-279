"""
Author: Damien GUEHO
Copyright: Copyright (C) 2023 Damien GUEHO
License: Public Domain
Version: 25
"""


import numpy

def time_varying_markov_parameters(A,
                                   B,
                                   C,
                                   D,
                                   tk,
                                   dt,
                                   number_steps):

    if number_steps <= 0:
        return []
    elif number_steps == 1:
        return [D(tk)]
    else:
        time_varying_markov_parameters = [D(tk)]
        temp = C(tk)
        for i in range(1, number_steps):
            time_varying_markov_parameters.append(temp @ B(tk - i * dt))
            temp = numpy.matmul(temp, A(tk - i * dt))
        return time_varying_markov_parameters
