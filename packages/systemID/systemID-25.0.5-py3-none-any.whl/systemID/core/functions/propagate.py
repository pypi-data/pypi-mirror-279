"""
Author: Damien GUEHO
Copyright: Copyright (C) 2023 Damien GUEHO
License: Public Domain
Version: 25
"""


import numpy
import scipy

from systemID.core.functions.runge_kutta_45 import runge_kutta_45

def propagate_discrete_ss_model(model,
                                number_steps: int,
                                x0: numpy.ndarray = None,
                                input_data: numpy.ndarray = None,
                                observer_data: numpy.ndarray = None,
                                process_noise_data: numpy.ndarray = None,
                                measurement_noise_data: numpy.ndarray = None):
    """
        Purpose:
            Propagate an initial condition and/or input data through a discrete-time state-space model. Model
            can be linear, bilinear or nonlinear.

        Parameters:
            - **model** (``systemID.discrete_ss_model``): the discrete-time state-space model.
            - **number_steps** (``int``): the number of steps.
            - **x0** (``numpy.ndarray``, optional): a numpy.ndarray of size (state_dimension, number_experiments)
             of initial conditions.
            - **input_data** (``numpy.ndarray``, optional): a numpy.ndarray of size
            (input_dimension, number_steps, number_experiments) of (time-varying) input data.

        Returns:
            - **y** (``numpy.ndarray``): a numpy.ndarray of size (output_dimension, number_steps, number_experiments)
             of output data.
            - **x** (``numpy.ndarray``): a numpy.ndarray of size (state_dimension, number_steps, number_experiments)
             of state data.

        Imports:
            - ``import numpy``

        Description:
            This program ...

        See Also:
            - :py:mod:`~systemID.core.functions.propagate_continuous_ss_model`
    """

    # Get model type and dimensions
    model_type = model.model_type
    state_dimension = model.state_dimension
    output_dimension = model.output_dimension
    input_dimension = model.input_dimension

    # Get time parameters
    dt = model.dt

    # Get model functions
    (A, N, B, C, D, F, H, G_observer, G_feedback) = model.A, model.N, model.B, model.C, model.D, model.F, model.H, model.G_observer, model.G_feedback


    if x0 is None and input_data is None:
        raise ValueError("x0 and input_data cannot both be None")

    if x0 is None:
        if len(input_data.shape) < 3:
            number_experiments = 1
        else:
            number_experiments = input_data.shape[2]
    else:
        if len(x0.shape) < 2:
            number_experiments = 1
        else:
            number_experiments = x0.shape[1]

    ux = numpy.zeros([state_dimension, number_steps, number_experiments])
    uy = numpy.zeros([output_dimension, number_steps, number_experiments])

    if input_data is not None and B is not None:
        if len(input_data.shape) == 1:
            input_data = numpy.expand_dims(input_data, axis=(0, 2))
        if len(input_data.shape) == 2:
            input_data = numpy.expand_dims(input_data, axis=2)
        for i in range(number_steps):
            ux[:, i, :] += numpy.matmul(B(i * dt), input_data[:, i, :])
            uy[:, i, :] += numpy.matmul(D(i * dt), input_data[:, i, :])

    if G_feedback is not None:
        feedback = True
        u_feedback = numpy.zeros([input_dimension, number_steps, number_experiments])
    else:
        feedback = False
        u_feedback = None

    if observer_data is not None and G_observer is not None:
        observer = True
        if len(observer_data.shape) == 1:
            observer_data = numpy.expand_dims(observer_data, axis=(0, 2))
        if len(observer_data.shape) == 2:
            observer_data = numpy.expand_dims(observer_data, axis=2)
        x_observer = numpy.zeros([state_dimension, number_steps, number_experiments])
    else:
        observer = False
        x_observer = None

    if process_noise_data is not None:
        if len(process_noise_data.shape) == 1:
            process_noise_data = numpy.expand_dims(process_noise_data, axis=(0, 2))
        if len(process_noise_data.shape) == 2:
            process_noise_data = numpy.expand_dims(process_noise_data, axis=2)
        for i in range(number_steps):
            ux[:, i, :] += process_noise_data[:, i, :]

    if measurement_noise_data is not None:
        if len(measurement_noise_data.shape) == 1:
            measurement_noise_data = numpy.expand_dims(measurement_noise_data, axis=(0, 2))
        if len(measurement_noise_data.shape) == 2:
            measurement_noise_data = numpy.expand_dims(measurement_noise_data, axis=2)
        for i in range(number_steps):
            uy[:, i, :] += measurement_noise_data[:, i, :]


    if len(x0.shape) == 1:
        x0 = numpy.expand_dims(x0, axis=1)


    # Initialize vectors
    x = numpy.zeros([state_dimension, number_steps + 1, number_experiments])
    if x0 is not None:
        x[:, 0, :] = x0
    y = numpy.zeros([output_dimension, number_steps, number_experiments])

    if model.model_type == 'linear':
        for i in range(number_steps):
            if feedback:
                u_feedback[:, i, :] = - numpy.matmul(G_feedback(i * dt), x[:, i, :])
                y[:, i, :] = numpy.matmul(C(i * dt), x[:, i, :]) + uy[:, i, :] + numpy.matmul(D(i * dt), u_feedback[:, i, :])
                if observer:
                    x_observer[:, i, :] = numpy.matmul(G_observer(i * dt), (observer_data[:, i, :] - y[:, i, :]))
                    x[:, i + 1, :] = numpy.matmul(A(i * dt), x[:, i, :]) + ux[:, i, :] + x_observer[:, i, :] + numpy.matmul(B(i * dt), u_feedback[:, i, :])
                else:
                    x[:, i + 1, :] = numpy.matmul(A(i * dt), x[:, i, :]) + ux[:, i, :] + numpy.matmul(B(i * dt), u_feedback[:, i, :])
            else:
                y[:, i, :] = numpy.matmul(C(i * dt), x[:, i, :]) + uy[:, i, :]
                if observer:
                    x_observer[:, i, :] = numpy.matmul(G_observer(i * dt), (observer_data[:, i, :] - y[:, i, :]))
                    x[:, i + 1, :] = numpy.matmul(A(i * dt), x[:, i, :]) + ux[:, i, :] + x_observer[:, i, :]
                else:
                    x[:, i + 1, :] = numpy.matmul(A(i * dt), x[:, i, :]) + ux[:, i, :]

        return y, x, x_observer, u_feedback


    if model_type == 'bilinear':

        for i in range(number_steps):
            if initial_condition_response:
                y[:, i] = numpy.matmul(C(i * dt), x[:, i])
                x[:, i + 1] = numpy.matmul(A(i * dt), x[:, i])

            else:
                y[:, i] = numpy.matmul(C(i * dt), x[:, i]) + numpy.matmul(D(i * dt), u[:, i])
                x[:, i + 1] = numpy.matmul(A(i * dt), x[:, i]) + numpy.matmul(N(i * dt), numpy.kron(u[:, i], x[:, i])) + numpy.matmul(B(i * dt), u[:, i])

        return y, x


    if model_type == 'nonlinear':

        for i in range(number_steps):
                y[:, i] = G(x[:, i], i * dt, u[:, i])
                x[:, i + 1] = F(x[:, i], i * dt, u[:, i])

        return y, x



def propagate_continuous_ss_model(model,
                                  tspan: numpy.ndarray,
                                  x0: numpy.ndarray = None,
                                  input_signal = None,
                                  fixed_step_size: bool = False,
                                  integration_step: float = None,
                                  rtol: float = 1e-12,
                                  atol: float = 1e-12):
    """
        Purpose:
            Propagate an initial condition and/or input data through a continuous-time state-space model. Model
            can be linear, bilinear or nonlinear.

    Parameters:
        - **model** (``systemID.continuous_ss_model``): the continuous-time state-space model.
        - **tspan** (``numpy.ndarray``): a numpy.ndarray that represents the time span.
        - **x0** (``numpy.ndarray``, optional): a numpy.ndarray of size (state_dimension, number_experiments)
         of initial conditions.
        - **input_data** (``func``, optional): a function that represents the input data.

    Returns:
        - **y** (``numpy.ndarray``): a numpy.ndarray of size (output_dimension, number_steps, number_experiments)
         of output data.
        - **x** (``numpy.ndarray``): a numpy.ndarray of size (state_dimension, number_steps, number_experiments)
         of state data.

    Imports:
        - ``import numpy``

    Description:
        This program ...

    See Also:
        - :py:mod:`~systemID.core.functions.propagate_discrete_ss_model`
    """

    output_dimension = model.output_dimension

    (f, h, g_feedback, g_observer) = model.f, model.h, model.g_feedback, model.g_observer

    if fixed_step_size:
        sol = runge_kutta_45(f, x0, tspan, integration_step, args=(input_signal,))
    else:
        sol = scipy.integrate.odeint(f, x0, tspan, args=(input_signal,), rtol=rtol, atol=atol)

    x = sol.T
    y = numpy.zeros([output_dimension, tspan.shape[0]])
    i = 0
    for t in tspan:
        y[:, i] = h(x[:, i], t, input_signal(t))
        i += 1

    return y, x
