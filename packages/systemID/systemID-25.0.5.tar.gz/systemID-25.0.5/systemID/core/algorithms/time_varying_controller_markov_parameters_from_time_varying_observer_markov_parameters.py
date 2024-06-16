"""
Author: Damien GUEHO
Copyright: Copyright (C) 2023 Damien GUEHO
License: Public Domain
Version: 25
"""


import numpy


def time_varying_controller_markov_parameters_from_time_varying_observer_markov_parameters(D: numpy.ndarray,
                                                                                           hki11: numpy.ndarray,
                                                                                           hki_observer21: numpy.ndarray,
                                                                                           hki_observer22: numpy.ndarray,
                                                                                           observer_order: int):
    """
    Purpose:


    Parameters:
        -

    Returns:
        -

    Imports:
        -

    Description:


    See Also:
        -
    """

    # Results
    results = {}

    # Dimensions and number of steps
    output_dimension, input_dimension, number_steps = D.shape

    # Build matrix
    r = numpy.zeros([(number_steps - 1) * input_dimension, (number_steps - 1) * input_dimension])
    for i in range(number_steps - 1):
        for j in range(max(0, i - observer_order + 1), i + 1):
            r[i * input_dimension:(i + 1) * input_dimension, j * input_dimension:(j + 1) * input_dimension] = hki_observer21[i * input_dimension:(i + 1) * input_dimension, (i - j) * input_dimension:(i - j + 1) * input_dimension] \
                                                                                                                - numpy.matmul(hki_observer22[i * input_dimension:(i + 1) * input_dimension, (i - j) * output_dimension:(i - j + 1) * output_dimension], D[:, :, j])
    # Build matrix h22
    h22 = numpy.zeros([(number_steps - 1) * input_dimension, (number_steps - 1) * output_dimension])
    for i in range(1, number_steps - 1):
        for j in range(max(0, i - observer_order), i):
            h22[i * input_dimension:(i+1) * input_dimension, j * output_dimension:(j+1) * output_dimension] = hki_observer22[i * input_dimension:(i+1) * input_dimension, (i-j-1) * output_dimension:(i-j) * output_dimension]

    # Calculate Markov parameters
    hki = r - numpy.matmul(h22, hki11)

    results['hki'] = hki
    results['h22'] = h22
    results['r'] = r

    return results
