"""
Author: Damien GUEHO
Copyright: Copyright (C) 2023 Damien GUEHO
License: Public Domain
Version: 25
"""


import numpy
import scipy

from systemID.core.algorithms.time_varying_markov_parameters_from_time_varying_observer_markov_parameters import time_varying_markov_parameters_from_time_varying_observer_markov_parameters
from systemID.core.algorithms.time_varying_observer_gain_markov_parameters_from_time_varying_observer_markov_parameters import time_varying_observer_gain_markov_parameters_from_time_varying_observer_markov_parameters
from systemID.core.algorithms.time_varying_controller_markov_parameters_from_time_varying_observer_markov_parameters import time_varying_controller_markov_parameters_from_time_varying_observer_markov_parameters
from systemID.core.algorithms.time_varying_controller_observer_gain_markov_parameters_from_time_varying_observer_markov_parameters import time_varying_controller_observer_gain_markov_parameters_from_time_varying_observer_markov_parameters


def time_varying_observer_controller_identification_algorithm(input_data: numpy.ndarray,
                                                              feedback_data: numpy.ndarray,
                                                              output_data: numpy.ndarray,
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

    # Dimensions
    (input_dimension, number_steps, number_experiments) = input_data.shape
    output_dimension = output_data.shape[0]


    # Observer order
    observer_order = min(observer_order, number_steps)


    # Time Varying hki_observer1, hki_observer2 and D matrices
    hki_observer11 = numpy.zeros([(number_steps - 1) * output_dimension, observer_order * input_dimension])
    hki_observer12 = numpy.zeros([(number_steps - 1) * output_dimension, observer_order * output_dimension])
    hki_observer21 = numpy.zeros([(number_steps - 1) * input_dimension, observer_order * input_dimension])
    hki_observer22 = numpy.zeros([(number_steps - 1) * input_dimension, observer_order * output_dimension])
    D = numpy.zeros([output_dimension, input_dimension, number_steps])


    # TVOCID
    for k in range(number_steps):

        # Initialize matrices y and V
        if k == 0:
            number_rows_V = input_dimension
        else:
            number_rows_V = input_dimension + min(observer_order, k) * (input_dimension + output_dimension)
        number_columns_V = number_experiments

        V = numpy.zeros([number_rows_V, number_columns_V])
        y = numpy.zeros([output_dimension, number_columns_V])
        uf = numpy.zeros([input_dimension, number_columns_V])

        # Populate matrices y and V
        for j in range(number_columns_V):
            y[:, j] = output_data[:, k, j]
            uf[:, j] = feedback_data[:, k, j]
            V[0:input_dimension, j] = input_data[:, k, j]
            for i in range(min(observer_order, k)):
                V[input_dimension + i * (input_dimension + output_dimension):input_dimension + (i + 1) * (input_dimension + output_dimension), j] = numpy.concatenate((input_data[:, k - i - 1, j], output_data[:, k - i - 1, j]))

        # Least-Squares solution for Observer Markov Parameters
        yt = numpy.concatenate((y, uf), axis=0)
        Mk = numpy.matmul(yt, scipy.linalg.pinv(V))

        # Extract Dk
        D[:, :, k] = Mk[0:output_dimension, 0:input_dimension]

        # Extract Observer Markov Parameters
        for j in range(min(observer_order, k)):
            h_observer = Mk[:, input_dimension + j * (input_dimension + output_dimension):input_dimension + (j + 1) * (input_dimension + output_dimension)]
            h11 = h_observer[0:output_dimension, 0:input_dimension]
            h12 = - h_observer[0:output_dimension, input_dimension:input_dimension + output_dimension]
            h21 = - h_observer[output_dimension:, 0:input_dimension]
            h22 = h_observer[output_dimension:, input_dimension:input_dimension + output_dimension]
            hki_observer11[(k - 1) * output_dimension:k * output_dimension, j * input_dimension:(j + 1) * input_dimension] = h11
            hki_observer12[(k - 1) * output_dimension:k * output_dimension, j * output_dimension:(j + 1) * output_dimension] = h12
            hki_observer21[(k - 1) * input_dimension:k * input_dimension, j * input_dimension:(j + 1) * input_dimension] = h21
            hki_observer22[(k - 1) * input_dimension:k * input_dimension, j * output_dimension:(j + 1) * output_dimension] = h22

    # Get TV Markov Parameters from TV Observer Markov Parameters
    tvmp = time_varying_markov_parameters_from_time_varying_observer_markov_parameters(D, hki_observer11, hki_observer12, observer_order)

    # Get TV Observer Gain Markov Parameters from TV Observer Markov Parameters
    tvogmp = time_varying_observer_gain_markov_parameters_from_time_varying_observer_markov_parameters(hki_observer12, observer_order)

    # Get TV Controller Markov Parameters from TV Observer Markov Parameters
    tvcmp = time_varying_controller_markov_parameters_from_time_varying_observer_markov_parameters(D, tvmp['hki'], hki_observer21, hki_observer22, observer_order)

    # Get TV Controller Oberver Gain Markov Parameters from TV Observer Markov Parameters
    tvcogmp = time_varying_controller_observer_gain_markov_parameters_from_time_varying_observer_markov_parameters(D, tvogmp['hkio'], hki_observer22, observer_order)

    mr = input_dimension + output_dimension
    hki_total = numpy.zeros([mr * (number_steps - 1), mr * (number_steps - 1)])
    for i in range(number_steps - 1):
        for j in range(max(0, i - observer_order + 1), i + 1):
            h1 = numpy.concatenate((tvmp['hki'][i*output_dimension:(i+1)*output_dimension, (j)*input_dimension:(j+1)*input_dimension], tvogmp['hkio'][i*output_dimension:(i+1)*output_dimension, (j)*output_dimension:(j+1)*output_dimension]), axis=1)
            h2 = numpy.concatenate((tvcmp['hki'][i*input_dimension:(i+1)*input_dimension, (j)*input_dimension:(j+1)*input_dimension], tvcogmp['hkio'][i*input_dimension:(i+1)*input_dimension, (j)*output_dimension:(j+1)*output_dimension]), axis=1)
            h = numpy.concatenate((h1, h2), axis=0)
            hki_total[i * mr:(i + 1) * mr, j * mr:(j + 1) * mr] = h


    results['D'] = D
    results['hki'] = tvmp['hki']
    results['hkio'] = tvogmp['hkio']
    results['hkic'] = tvcmp['hki']
    results['hkioc'] = tvcogmp['hkio']
    results['hki_total'] = hki_total
    results['hki_observer11'] = hki_observer11
    results['hki_observer12'] = hki_observer12
    results['hki_observer21'] = hki_observer21
    results['hki_observer22'] = hki_observer22
    # results['Error TVOCID'] = scipy.linalg.norm(yt - numpy.matmul(Mk, V))

    return results
