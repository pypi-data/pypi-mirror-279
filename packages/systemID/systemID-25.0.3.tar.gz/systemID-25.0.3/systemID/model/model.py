"""
Author: Damien GUEHO
Copyright: Copyright (C) 2023 Damien GUEHO
License: Public Domain
Version: 25
"""


import numpy
import time

from systemID.helper.check_argument import *

from systemID.core.algorithms.eigensystem_realization_algorithm import eigensystem_realization_algorithm
from systemID.core.algorithms.eigensystem_realization_algorithm_with_data_correlation import eigensystem_realization_algorithm_with_data_correlation
from systemID.core.algorithms.eigensystem_realization_algorithm_from_initial_condition_response import eigensystem_realization_algorithm_from_initial_condition_response
from systemID.core.algorithms.eigensystem_realization_algorithm_with_data_correlation_from_initial_condition_response import eigensystem_realization_algorithm_with_data_correlation_from_initial_condition_response
from systemID.core.algorithms.observer_controller_eigensystem_realization_algorithm import observer_controller_eigensystem_realization_algorithm
from systemID.core.algorithms.controller_eigensystem_realization_algorithm import controller_eigensystem_realization_algorithm

from systemID.core.algorithms.time_varying_eigensystem_realization_algorithm_from_initial_condition_response import time_varying_eigensystem_realization_algorithm_from_initial_condition_response
from systemID.core.algorithms.time_varying_eigensystem_realization_algorithm import time_varying_eigensystem_realization_algorithm
from systemID.core.algorithms.time_varying_observer_controller_eigensystem_realization_algorithm import time_varying_observer_controller_eigensystem_realization_algorithm

from systemID.core.algorithms.observer_kalman_identification_algorithm import observer_kalman_identification_algorithm
from systemID.core.algorithms.observer_kalman_identification_algorithm_with_observer import observer_kalman_identification_algorithm_with_observer
from systemID.core.algorithms.markov_parameters_from_observer_markov_parameters import markov_parameters_from_observer_markov_parameters
from systemID.core.algorithms.observer_controller_identification_algorithm import observer_controller_identification_algorithm
from systemID.core.algorithms.markov_controller_parameters_from_observer_controller_markov_parameters import markov_controller_parameters_from_observer_controller_markov_parameters

from systemID.core.algorithms.time_varying_observer_kalman_identification_algorithm_with_observer import time_varying_observer_kalman_identification_algorithm_with_observer
from systemID.core.algorithms.time_varying_observer_controller_identification_algorithm import time_varying_observer_controller_identification_algorithm

from systemID.core.functions.propagate import propagate_discrete_ss_model, propagate_continuous_ss_model
from systemID.core.functions.augment_data import augment_data_with_polynomial_basis_functions, augment_data_with_given_functions



class model:

    def __init__(self,
                 model_type: str,
                 output_dimension: int = None,
                 input_dimension: int = None,
                 parameter_dimension: int = None):

        check_arg_is_one_of(model_type, ['linear', 'bilinear', 'nonlinear'])
        self.model_type = model_type

        check_arg_is_None_or_positive_integer(output_dimension)
        self.output_dimension = output_dimension

        check_arg_is_None_or_positive_integer(input_dimension)
        self.input_dimension = input_dimension

        check_arg_is_None_or_positive_integer(parameter_dimension)
        self.parameter_dimension = parameter_dimension


class discrete_ss_model(model):

    def __init__(self,
                 model_type: str,
                 dt: float,
                 state_dimension: int,
                 input_dimension: int = None,
                 output_dimension: int = None,
                 parameter_dimension: int = None,
                 A: Callable[[float], numpy.ndarray] = None,
                 N: Callable[[float], numpy.ndarray] = None,
                 B: Callable[[float], numpy.ndarray] = None,
                 C: Callable[[float], numpy.ndarray] = None,
                 D: Callable[[float], numpy.ndarray] = None,
                 F: Callable[[numpy.ndarray, float, numpy.ndarray], numpy.ndarray] = None,
                 H: Callable[[numpy.ndarray, float, numpy.ndarray], numpy.ndarray] = None,
                 G_feedback: Callable[[numpy.ndarray, float, numpy.ndarray], numpy.ndarray] = None,
                 G_observer: Callable[[numpy.ndarray, float, numpy.ndarray], numpy.ndarray] = None):

        super().__init__(model_type, output_dimension, input_dimension, parameter_dimension)

        check_arg_is_positive_float(dt)
        self.dt = dt

        check_arg_is_positive_integer(state_dimension)
        self.state_dimension = state_dimension

        check_arg_is_None_or_system_matrix_dims_01(A, self.state_dimension, self.state_dimension)
        self.A = A

        check_arg_is_None_or_system_matrix_dims_0(N, self.state_dimension)
        self.N = N
        if N is not None:
            self.input_dimension = int(N(0).shape[1] / self.state_dimension)

        check_arg_is_None_or_system_matrix_dims_0(B, self.state_dimension)
        self.B = B
        if B is not None:
            self.input_dimension = B(0).shape[1]

        check_arg_is_None_or_system_matrix_dims_1(C, self.state_dimension)
        self.C = C
        if C is not None:
            self.output_dimension = C(0).shape[0]

        check_arg_is_None_or_system_matrix(D)
        self.D = D
        if D is not None:
            self.output_dimension, self.input_dimension = D(0).shape

        check_arg_is_None_or_Callable(F)
        self.F = F

        check_arg_is_None_or_Callable(H)
        self.H = H

        self.G_feedback = G_feedback
        self.G_observer = G_observer


    # Funcion for LTI fit
    def lti_fit(self,
                output_data: numpy.ndarray,
                input_data: numpy.ndarray = None,
                feedback_data: numpy.ndarray = None,
                parameter_data: numpy.ndarray = None,
                number_markov_parameters: int = None,
                observer_order: int = None,
                stable_order: int = None,
                p: int = None,
                q: int = None,
                xi: int = None,
                zeta: int = None,
                tau: int = None,
                lifting_order: int = 1,
                lifting_functions: list = None,
                update_state_dimension: bool = True,
                data_correlations: bool = False):

        # Start timer
        t = time.time()

        # Create fit_config dictionary
        self.fit_config = {}

        # Check output_data
        check_arg_is_3Ddata_with_optional_dim0(output_data, self.output_dimension)
        self.fit_config['output_data'] = output_data
        self.output_dimension = output_data.shape[0]
        self.fit_config['number_steps'] = output_data.shape[1]
        self.fit_config['number_experiments'] = output_data.shape[2]

        # Check input_data
        check_arg_is_None_or_3Ddata_with_optional_dim0_and_dim12(input_data, self.input_dimension, self.fit_config['number_steps'], self.fit_config['number_experiments'])
        self.fit_config['input_data'] = input_data
        if input_data is not None:
            self.input_dimension = input_data.shape[0]

        # Check feedback data
        check_arg_is_None_or_3Ddata_with_optional_dim0_and_dim12(feedback_data, self.input_dimension, self.fit_config['number_steps'], self.fit_config['number_experiments'])
        self.fit_config['feedback_data'] = feedback_data
        if feedback_data is not None:
            self.input_dimension = feedback_data.shape[0]

        # Check parameter_data
        check_arg_is_None_or_3Ddata_with_dim1(parameter_data, self.fit_config['number_experiments'])
        self.fit_config['parameter_data'] = parameter_data
        if self.fit_config['parameter_data'] is not None:
            self.parameter_dimension = parameter_data.shape[0]

        # Hyperparameters for OKID/TVOKID
        self.fit_config['number_markov_parameters'] = number_markov_parameters
        self.fit_config['observer_order'] = observer_order
        if stable_order is None:
            self.fit_config['stable_order'] = 0
        else:
            self.fit_config['stable_order'] = stable_order

        # Hyperparameters for Hankel matrices
        check_arg_is_None_or_positive_integer(p)
        self.fit_config['p'] = p
        check_arg_is_None_or_positive_integer(q)
        self.fit_config['q'] = q
        check_arg_is_None_or_positive_integer(xi)
        self.fit_config['xi'] = xi
        check_arg_is_None_or_positive_integer(zeta)
        self.fit_config['zeta'] = zeta
        check_arg_is_None_or_positive_integer(tau)
        self.fit_config['tau'] = tau
        check_arg_is_bool(data_correlations)
        self.fit_config['data_correlations'] = data_correlations

        # Lifting order for polynomial Koopman embedding
        check_arg_is_None_or_positive_integer(lifting_order)
        self.fit_config['lifting_order'] = lifting_order
        check_arg_is_None_or_list(lifting_functions)
        self.fit_config['lifting_functions'] = lifting_functions
        check_arg_is_bool(update_state_dimension)
        self.fit_config['update_state_dimension'] = update_state_dimension
        if self.fit_config['lifting_order'] > 1:
            self.fit_config['output_data'] = augment_data_with_polynomial_basis_functions(data=self.fit_config['output_data'],
                                                                                          order=self.fit_config['lifting_order'],
                                                                                          max_order=self.fit_config['lifting_order'])
            if self.fit_config['update_state_dimension']:
                self.state_dimension = self.fit_config['output_data'].shape[0]
            self.output_dimension = self.fit_config['output_data'].shape[0]
        elif self.fit_config['lifting_functions'] is not None and len(self.fit_config['lifting_functions']) > 0:
            self.fit_config['output_data'] = augment_data_with_given_functions(data=self.fit_config['output_data'],
                                                                               given_functions=self.fit_config['lifting_functions'])
            if update_state_dimension:
                self.state_dimension = self.fit_config['output_data'].shape[0]
            self.output_dimension = self.fit_config['output_data'].shape[0]



        if self.fit_config['input_data'] is None:
            if self.fit_config['data_correlations']:
                era_ic = eigensystem_realization_algorithm_with_data_correlation_from_initial_condition_response(output_data=self.fit_config['output_data'],
                                                                                                                 state_dimension=self.state_dimension,
                                                                                                                 p=self.fit_config['p'],
                                                                                                                 q=self.fit_config['q'],
                                                                                                                 xi=self.fit_config['xi'],
                                                                                                                 zeta=self.fit_config['zeta'],
                                                                                                                 tau=self.fit_config['tau'])
                self.fit_config.update(era_ic)
                self.A = self.fit_config['A']
                self.C = self.fit_config['C']

            else:
                era_ic = eigensystem_realization_algorithm_from_initial_condition_response(output_data=self.fit_config['output_data'],
                                                                                           state_dimension=self.state_dimension,
                                                                                           p=self.fit_config['p'],
                                                                                           q=self.fit_config['q'])
                self.fit_config.update(era_ic)
                self.A = self.fit_config['A']
                self.C = self.fit_config['C']

        else:
            if self.fit_config['feedback_data'] is None:
                if self.fit_config['observer_order'] is None:
                    okid = observer_kalman_identification_algorithm(input_data=self.fit_config['input_data'],
                                                                    output_data=self.fit_config['output_data'],
                                                                    number_markov_parameters=self.fit_config['number_markov_parameters'],
                                                                    stable_order=self.fit_config['stable_order'])
                else:
                    okid = observer_kalman_identification_algorithm_with_observer(input_data=self.fit_config['input_data'],
                                                                                  output_data=self.fit_config['output_data'],
                                                                                  observer_order=self.fit_config['observer_order'],
                                                                                  stable_order=self.fit_config['stable_order'])

                    markov_parameters = markov_parameters_from_observer_markov_parameters(observer_markov_parameters=okid['observer_markov_parameters'],
                                                                                          number_markov_parameters=self.fit_config['number_markov_parameters'])

                    self.fit_config.update(markov_parameters)

                self.fit_config.update(okid)

                if self.fit_config['data_correlations']:
                    era = eigensystem_realization_algorithm_with_data_correlation(markov_parameters=self.fit_config['markov_parameters'],
                                                                                  state_dimension=self.state_dimension,
                                                                                  p=self.fit_config['p'],
                                                                                  q=self.fit_config['q'],
                                                                                  xi=self.fit_config['xi'],
                                                                                  zeta=self.fit_config['zeta'],
                                                                                  tau=self.fit_config['tau'])
                    self.fit_config.update(era)
                    self.A = self.fit_config['A']
                    self.B = self.fit_config['B']
                    self.C = self.fit_config['C']
                    self.D = self.fit_config['D']

                else:
                    era = eigensystem_realization_algorithm(markov_parameters=self.fit_config['markov_parameters'],
                                                            state_dimension=self.state_dimension,
                                                            p=self.fit_config['p'],
                                                            q=self.fit_config['q'])
                    self.fit_config.update(era)
                    self.A = self.fit_config['A']
                    self.B = self.fit_config['B']
                    self.C = self.fit_config['C']
                    self.D = self.fit_config['D']

            else:
                ocid = observer_controller_identification_algorithm(input_data=self.fit_config['input_data'],
                                                                    feedback_data=self.fit_config['feedback_data'],
                                                                    output_data=self.fit_config['output_data'],
                                                                    observer_order=self.fit_config['observer_order'],
                                                                    stable_order=self.fit_config['stable_order'])

                markov_controller_parameters = markov_controller_parameters_from_observer_controller_markov_parameters(observer_controller_markov_parameters=ocid['observer_controller_markov_parameters'],
                                                                                                                       number_markov_parameters=self.fit_config['number_markov_parameters'])
                self.fit_config.update(markov_controller_parameters)

                # ocera = observer_controller_eigensystem_realization_algorithm(markov_controller_parameters=self.fit_config['markov_controller_parameters'],
                #                                                               state_dimension=self.state_dimension,
                #                                                               p=self.fit_config['p'],
                #                                                               q=self.fit_config['q'])

                ocera = controller_eigensystem_realization_algorithm(markov_controller_parameters=self.fit_config['markov_controller_parameters'],
                                                                              state_dimension=self.state_dimension,
                                                                              p=self.fit_config['p'],
                                                                              q=self.fit_config['q'])

                self.fit_config.update(ocera)
                self.A = self.fit_config['A']
                self.B = self.fit_config['B']
                self.C = self.fit_config['C']
                self.D = self.fit_config['D']
                # self.G_observer = self.fit_config['G_observer']
                self.G_feedback = self.fit_config['G_feedback']



        self.fit_config['Training time'] = time.time() - t




    # Function for LTV fit
    def ltv_fit(self,
                forced_response_output_data: numpy.ndarray = None,
                input_data: numpy.ndarray = None,
                feedback_data: numpy.ndarray = None,
                free_response_output_data: numpy.ndarray = None,
                parameter_data: numpy.ndarray = None,
                observer_order: int = None,
                p: int = None,
                q: int = None,
                lifting_order: int = 1,
                data_correlations: bool = False,
                max_time_step: int = None,
                apply_transformation: bool = True,
                show_progress: bool = False
                ):

        t = time.time()
        self.fit_config = {}

        # if not isinstance(forced_response_output_data, numpy.ndarray) or \
        #         forced_response_output_data.ndim != 3 or \
        #         self.output_dimension is not None and forced_response_output_data.shape[0] != self.output_dimension:
        #     raise ValueError(
        #         "output_data must be a numpy.ndarray of shape (output_dimension, number_steps, number_experiments)")
        self.fit_config['forced_response_output_data'] = forced_response_output_data
        if forced_response_output_data is not None:
            self.output_dimension = forced_response_output_data.shape[0]
            self.fit_config['number_steps'] = forced_response_output_data.shape[1]
            self.fit_config['number_experiments'] = forced_response_output_data.shape[2]

        if input_data is not None and not (isinstance(input_data, numpy.ndarray) and input_data.ndim == 3) or \
                input_data is not None and self.input_dimension is not None and input_data.shape[
            0] != self.input_dimension or \
                input_data is not None and (
                input_data.shape[1] != self.fit_config['number_steps'] or input_data.shape[2] != self.fit_config[
            'number_experiments']):
            raise ValueError(
                "input_data must be a numpy.ndarray of shape (input_dimension, number_steps, number_experiments)")
        self.fit_config['input_data'] = input_data
        if input_data is not None:
            self.input_dimension = input_data.shape[0]

        self.fit_config['free_response_output_data'] = free_response_output_data
        # self.output_dimension = free_response_output_data.shape[0]
        # self.fit_config['number_steps'] = free_response_output_data.shape[1]
        # self.fit_config['number_experiments'] = free_response_output_data.shape[2]

        self.fit_config['feedback_data'] = feedback_data

        self.fit_config['parameter_data'] = parameter_data
        if self.fit_config['parameter_data'] is not None:
            self.parameter_dimension = parameter_data.shape[0]
        self.fit_config['observer_order'] = observer_order
        self.fit_config['p'] = p
        self.fit_config['q'] = q
        self.fit_config['lifting_order'] = lifting_order
        self.fit_config['data_correlations'] = data_correlations
        self.fit_config['max_time_step'] = max_time_step
        self.fit_config['apply_transformation'] = apply_transformation
        self.fit_config['show_progress'] = show_progress

        if self.fit_config['input_data'] is None:
            tvera_ic = time_varying_eigensystem_realization_algorithm_from_initial_condition_response(output_data=self.fit_config['free_response_output_data'],
                                                                                                      state_dimension=self.state_dimension,
                                                                                                      dt=self.dt,
                                                                                                      p=self.fit_config['p'],
                                                                                                      max_time_step=self.fit_config['max_time_step'])
            self.fit_config.update(tvera_ic)
            self.A = self.fit_config['A']
            self.C = self.fit_config['C']

        else:
            if self.fit_config['feedback_data'] is None:
                tvokid = time_varying_observer_kalman_identification_algorithm_with_observer(input_data=self.fit_config['input_data'],
                                                                                             output_data=self.fit_config['forced_response_output_data'],
                                                                                             observer_order=self.fit_config['observer_order'])

                self.fit_config.update(tvokid)

                tvera = time_varying_eigensystem_realization_algorithm(hki=self.fit_config['hki'],
                                                                       D=self.fit_config['D'],
                                                                       state_dimension=self.state_dimension,
                                                                       dt=self.dt,
                                                                       free_response_data=self.fit_config['free_response_output_data'],
                                                                       p=self.fit_config['p'],
                                                                       q=self.fit_config['q'],
                                                                       apply_transformation=self.fit_config['apply_transformation'],
                                                                       show_progress=self.fit_config['show_progress'])
                self.fit_config.update(tvera)
                self.A = self.fit_config['A']
                self.B = self.fit_config['B']
                self.C = self.fit_config['C']
                self.D = self.fit_config['D']

            else:
                tvocid = time_varying_observer_controller_identification_algorithm(input_data=self.fit_config['input_data'],
                                                                                   feedback_data=self.fit_config['feedback_data'],
                                                                                   output_data=self.fit_config['forced_response_output_data'],
                                                                                   observer_order=self.fit_config['observer_order'])
                self.fit_config.update(tvocid)

                tvocera = time_varying_observer_controller_eigensystem_realization_algorithm(hki=self.fit_config['hki_total'],
                                                                                             D=self.fit_config['D'],
                                                                                             state_dimension=self.state_dimension,
                                                                                             dt=self.dt,
                                                                                             free_response_data=self.fit_config['free_response_output_data'],
                                                                                             p=self.fit_config['p'],
                                                                                             q=self.fit_config['q'],
                                                                                             apply_transformation=self.fit_config['apply_transformation'],
                                                                                             show_progress=self.fit_config['show_progress'])

                self.fit_config.update(tvocera)
                self.A = self.fit_config['A']
                self.B = self.fit_config['B']
                self.C = self.fit_config['C']
                self.D = self.fit_config['D']
                self.G_feedback = self.fit_config['G_feedback']
                # self.G_observer = self.fit_config['G_observer']


        self.fit_config['Training time'] = time.time() - t


    def predict(self,
                number_steps: numpy.ndarray,
                x0: numpy.ndarray = None,
                parameter_data: numpy.ndarray = None,
                input_data: numpy.ndarray = None,
                observer_data: numpy.ndarray = None,
                process_noise_data: numpy.ndarray = None,
                measurement_noise_data: numpy.ndarray = None):

        self.predict_config = {}

        if (x0 is None) and (input_data is None) and (parameter_data is None):
            raise ValueError('x0, input_data and parameter_data cannot all be None.')

        if x0 is None and parameter_data is None:
            x0 = numpy.zeros(self.state_dimension)
        else:
            if x0 is None:
                x0 = (self.fit_config['X0']@numpy.linalg.pinv(self.fit_config['parameter_data']))@parameter_data

        y, x, x_observer, u_feedback = propagate_discrete_ss_model(model=self,
                                                                   number_steps=number_steps,
                                                                   x0=x0,
                                                                   input_data=input_data,
                                                                   observer_data=observer_data,
                                                                   process_noise_data=process_noise_data,
                                                                   measurement_noise_data=measurement_noise_data)

        self.predict_config['output_data'] = y
        self.predict_config['state_data'] = x
        self.predict_config['observer_data'] = x_observer
        self.predict_config['feedback_data'] = u_feedback






class continuous_ss_model(model):

    def __init__(self,
                 model_type: str,
                 state_dimension: int,
                 input_dimension: int = None,
                 output_dimension: int = None,
                 parameter_dimension: int = None,
                 f: Callable[[numpy.ndarray, float, numpy.ndarray], numpy.ndarray] = None,
                 h: Callable[[numpy.ndarray, float, numpy.ndarray], numpy.ndarray] = None,
                 g_feedback: Callable[[numpy.ndarray, float, numpy.ndarray], numpy.ndarray] = None,
                 g_observer: Callable[[numpy.ndarray, float, numpy.ndarray], numpy.ndarray] = None):

        super().__init__(model_type, output_dimension, input_dimension, parameter_dimension)

        check_arg_is_positive_integer(state_dimension)
        self.state_dimension = state_dimension

        check_arg_is_None_or_Callable(f)
        self.f = f

        check_arg_is_None_or_Callable(h)
        self.h = h

        self.g_feedback = g_feedback
        self.g_observer = g_observer


    def predict(self,
                tspan: numpy.ndarray,
                x0: numpy.ndarray = None,
                input_signal: Callable[[float], numpy.ndarray] = None,
                fixed_step_size: bool = False,
                integration_step: float = None,
                rtol: float = 1e-12,
                atol: float = 1e-12
                ):

        self.predict_config = {}

        y, x = propagate_continuous_ss_model(model=self,
                                             tspan=tspan,
                                             x0=x0,
                                             input_signal=input_signal,
                                             fixed_step_size=fixed_step_size,
                                             integration_step=integration_step,
                                             rtol=rtol,
                                             atol=atol)

        self.predict_config['output_data'] = y
        self.predict_config['state_data'] = x



