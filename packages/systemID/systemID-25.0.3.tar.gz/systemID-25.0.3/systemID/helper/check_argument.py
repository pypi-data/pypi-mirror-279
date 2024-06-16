"""
Author: Damien GUEHO
Copyright: Copyright (C) 2023 Damien GUEHO
License: Public Domain
Version: 25
"""


import numpy
from typing import Callable

def check_arg_is_one_of(arg, args):
    if arg not in args:
        raise ValueError("{arg:} must be one of {args:}.".format(arg=arg, args=args))

def check_arg_is_bool(arg):
    if not isinstance(arg, bool):
        raise ValueError("{arg:} must be a bool.".format(arg=arg))

def check_arg_is_None_or_list(arg):
    if arg is not None and not isinstance(arg, list):
        raise ValueError("{arg:} must be None or a list.".format(arg=arg))

def check_arg_is_None_or_positive_integer(arg):
    if arg is not None and (not isinstance(arg, int) or arg <= 0):
        raise ValueError("{arg:} must be None or a positive integer.".format(arg=arg))

def check_arg_is_positive_integer(arg):
    if not isinstance(arg, int) or arg <= 0:
        raise ValueError("{arg:} must be a positive integer.".format(arg=arg))

def check_arg_is_positive_float(arg):
    if not isinstance(arg, float) or arg <= 0:
        raise ValueError("{arg:} must be a positive float.".format(arg=arg))

def check_arg_is_None_or_system_matrix_dims_01(arg, dim0, dim1):
    if arg is not None and not (isinstance(arg, Callable) and isinstance(arg(0), numpy.ndarray) and arg(0).shape == (dim0, dim1)):
        raise ValueError("{arg:} must be a callable function that returns a numpy.ndarray of shape ({dim_rows:}, {dim_columns}).".format(arg=arg, dim_rows=dim0, dim_columns=dim1))

def check_arg_is_None_or_system_matrix_dims_0(arg, dim0):
    if arg is not None and not (isinstance(arg, Callable) and isinstance(arg(0), numpy.ndarray) and arg(0).ndim == 2 and arg(0).shape[0] == dim0):
        raise ValueError("{arg:} must be a callable function that returns a numpy.ndarray of shape ({dim_rows:}, dim_axis_1).".format(arg=arg, dim0=dim0))

def check_arg_is_None_or_system_matrix_dims_1(arg, dim1):
    if arg is not None and not (isinstance(arg, Callable) and isinstance(arg(0), numpy.ndarray) and arg(0).ndim == 2 and arg(0).shape[1] == dim1):
        raise ValueError("{arg:} must be a callable function that returns a numpy.ndarray of shape (dim_axis_0, {dim_columns:}).".format(arg=arg, dim1=dim1))

def check_arg_is_None_or_system_matrix(arg):
    if arg is not None and not (isinstance(arg, Callable) and isinstance(arg(0), numpy.ndarray) and arg(0).ndim == 2):
        raise ValueError("{arg:} must be a callable function that returns a numpy.ndarray of shape (dim_axis_0, dim_axis_1).".format(arg=arg))

def check_arg_is_None_or_Callable(arg):
    if arg is not None and not isinstance(arg, Callable):
        raise ValueError("{arg:} must be a callable function that returns a numpy.ndarray of shape (dim_axis_0,).".format(arg=arg))

def check_arg_is_3Ddata_with_optional_dim0(arg, dim0):
    if not isinstance(arg, numpy.ndarray) or arg.ndim != 3 or (dim0 is not None and arg.shape[0] != dim0):
        raise ValueError("{arg:} must be a numpy.ndarray of shape ({dim0:}, number_steps, number_experiments)".format(arg=arg, dim0=dim0))

def check_arg_is_None_or_3Ddata_with_optional_dim0_and_dim12(arg, dim0, dim1, dim2):
    if arg is not None:
        if not (isinstance(arg, numpy.ndarray) and arg.ndim == 3) or (dim0 is not None and arg.shape[0] != dim0) or (arg.shape[1] != dim1 or arg.shape[2] != dim2):
            raise ValueError("{arg:} must be a numpy.ndarray of shape ({dim0:}, {dim1:}, {dim2:})".format(arg=arg, dim0=dim0, dim1=dim1, dim2=dim2))

def check_arg_is_None_or_3Ddata_with_dim1(arg, dim1):
    if arg is not None:
        if not isinstance(arg, numpy.ndarray) or arg.ndim == 2 or (arg.shape[1] != dim1):
            raise ValueError("{arg:} must be a numpy.ndarray of shape (_, {dim1:}, {dim2:})".format(arg=arg, dim1=dim1))
