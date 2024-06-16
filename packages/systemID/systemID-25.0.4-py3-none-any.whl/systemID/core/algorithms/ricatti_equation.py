"""
Author: Damien GUEHO
Copyright: Copyright (C) 2023 Damien GUEHO
License: Public Domain
Version: 25
"""

import numpy
import scipy

from typing import Callable

def discrete_recursive_ricatti_equation(A: Callable[[float], numpy.ndarray],
                                        B: Callable[[float], numpy.ndarray],
                                        tspan: numpy.ndarray,
                                        dt: float,
                                        S_N: numpy.ndarray = None,
                                        Q: Callable[[float], numpy.ndarray] = None,
                                        R: Callable[[float], numpy.ndarray] = None):

    results = {}

    number_steps = len(tspan)
    state_dimension, input_dimension = B(0).shape

    S_m = numpy.zeros([state_dimension, state_dimension, number_steps])
    G_feedback_m = numpy.zeros([input_dimension, state_dimension, number_steps])

    S_m[:, :, -1] = S_N

    # Solve the DRE recursively backwards
    k = 0
    for tk in reversed(tspan[:-1]):
        A_k = A(tk)
        B_k = B(tk)
        Q_k = Q(tk)
        R_k = R(tk)

        # Compute the control gain F_feedback at time step tk
        F = scipy.linalg.inv(R_k + B_k.T.dot(S_m[:, :, -1-k]).dot(B_k)).dot(B_k.T).dot(S_m[:, :, -1-k]).dot(A_k)
        G_feedback_m[:, :, -2-k] = F

        # Compute the Riccati matrix Sk at time step tk
        Sk = Q_k + A_k.T.dot(S_m[:, :, -1-k]).dot(A_k) - A_k.T.dot(S_m[:, :, -1-k]).dot(B_k).dot(numpy.linalg.inv(R_k + B_k.T.dot(S_m[:, :, -1-k]).dot(B_k))).dot(B_k.T).dot(S_m[:, :, -1-k]).dot(A_k)

        k += 1

        S_m[:, :, -1-k] = Sk

    def S(tk):
        return S_m[:, :, int(round(tk / dt))]

    def G_feedback(tk):
        return G_feedback_m[:, :, int(round(tk / dt))]

    results['S'] = S
    results['G_feedback'] = G_feedback

    return results



def discrete_algebraic_ricatti_equation(A: numpy.ndarray,
                                        B: numpy.ndarray,
                                        Q: numpy.ndarray = None,
                                        R: numpy.ndarray = None):

    results = {}

    S_m = scipy.linalg.solve_discrete_are(A,
                                          B,
                                          Q,
                                          R,
                                          e=None,
                                          s=None,
                                          balanced=True)

    G_feedback_m = scipy.linalg.inv(R + B.T.dot(S_m).dot(B)).dot(B.T).dot(S_m).dot(A)

    def S(tk):
        return S_m

    def G_feedback(tk):
        return G_feedback_m

    results['S'] = S
    results['G_feedback'] = G_feedback

    return results
