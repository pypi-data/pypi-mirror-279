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


# class statistical_uq:
#
#     def __init__(self,
#                  discrete_ss_model: discrete_ss_model):
#
#         self.model = discrete_ss_model
#
#
#     def dlqr(self,




