"""
Author: Damien GUEHO
Copyright: Copyright (C) 2023 Damien GUEHO
License: Public Domain
Version: 25
"""

import numpy
import scipy

import time

from systemID.helper.check_argument import *

from systemID.model.model import discrete_ss_model

from systemID.core.algorithms.ricatti_equation import discrete_recursive_ricatti_equation, discrete_algebraic_ricatti_equation


class controller:

    def __init__(self,
                 discrete_ss_model: discrete_ss_model):

        self.model = discrete_ss_model


    def dlqr(self,
             tspan: numpy.ndarray = None,
             S_N: numpy.ndarray = None,
             Q: Callable[[float], numpy.ndarray] = None,
             R: Callable[[float], numpy.ndarray] = None,
             steady_state_gain: bool = False):

        self.tspan = tspan

        # check_arg_is_None_or_system_matrix_dims_01(S_N, self.model.state_dimension, self.model.state_dimension)
        self.S_N = S_N

        # check_arg_is_None_or_system_matrix_dims_01(Q, self.model.state_dimension, self.model.state_dimension)
        self.Q = Q

        # check_arg_is_None_or_system_matrix_dims_01(Q, self.model.input_dimension, self.model.input_dimension)
        self.R = R

        check_arg_is_bool(steady_state_gain)
        self.steady_state_gain = steady_state_gain

        if self.steady_state_gain:
            gains = discrete_algebraic_ricatti_equation(self.model.A(0),
                                                        self.model.B(0),
                                                        self.Q,
                                                        self.R)
            self.G_feedback = gains['G_feedback']
            self.S = gains['S']

        else:
            gains = discrete_recursive_ricatti_equation(self.model.A,
                                                        self.model.B,
                                                        self.tspan,
                                                        self.model.dt,
                                                        self.S_N,
                                                        self.Q,
                                                        self.R)
            self.G_feedback = gains['G_feedback']
            self.S = gains['S']





    # def mpc(self,
    #         ):