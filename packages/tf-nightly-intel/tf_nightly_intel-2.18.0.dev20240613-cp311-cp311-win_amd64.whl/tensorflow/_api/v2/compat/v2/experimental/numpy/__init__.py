# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.experimental.numpy namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v2.experimental.numpy import random
from tensorflow.python.framework.tensor import Tensor as ndarray # line: 138
from tensorflow.python.ops.numpy_ops.np_array_ops import all # line: 420
from tensorflow.python.ops.numpy_ops.np_array_ops import amax # line: 672
from tensorflow.python.ops.numpy_ops.np_array_ops import amin # line: 689
from tensorflow.python.ops.numpy_ops.np_array_ops import any # line: 427
from tensorflow.python.ops.numpy_ops.np_array_ops import arange # line: 259
from tensorflow.python.ops.numpy_ops.np_array_ops import around # line: 820
from tensorflow.python.ops.numpy_ops.np_array_ops import array # line: 217
from tensorflow.python.ops.numpy_ops.np_array_ops import asanyarray # line: 246
from tensorflow.python.ops.numpy_ops.np_array_ops import asarray # line: 234
from tensorflow.python.ops.numpy_ops.np_array_ops import ascontiguousarray # line: 252
from tensorflow.python.ops.numpy_ops.np_array_ops import atleast_1d # line: 1293
from tensorflow.python.ops.numpy_ops.np_array_ops import atleast_2d # line: 1299
from tensorflow.python.ops.numpy_ops.np_array_ops import atleast_3d # line: 1305
from tensorflow.python.ops.numpy_ops.np_array_ops import broadcast_arrays # line: 1567
from tensorflow.python.ops.numpy_ops.np_array_ops import broadcast_to # line: 1192
from tensorflow.python.ops.numpy_ops.np_array_ops import compress # line: 434
from tensorflow.python.ops.numpy_ops.np_array_ops import copy # line: 465
from tensorflow.python.ops.numpy_ops.np_array_ops import cumprod # line: 483
from tensorflow.python.ops.numpy_ops.np_array_ops import cumsum # line: 500
from tensorflow.python.ops.numpy_ops.np_array_ops import diag # line: 305
from tensorflow.python.ops.numpy_ops.np_array_ops import diag_indices # line: 1338
from tensorflow.python.ops.numpy_ops.np_array_ops import diagflat # line: 389
from tensorflow.python.ops.numpy_ops.np_array_ops import diagonal # line: 347
from tensorflow.python.ops.numpy_ops.np_array_ops import dsplit # line: 1187
from tensorflow.python.ops.numpy_ops.np_array_ops import dstack # line: 1241
from tensorflow.python.ops.numpy_ops.np_array_ops import empty # line: 53
from tensorflow.python.ops.numpy_ops.np_array_ops import empty_like # line: 59
from tensorflow.python.ops.numpy_ops.np_array_ops import expand_dims # line: 875
from tensorflow.python.ops.numpy_ops.np_array_ops import eye # line: 98
from tensorflow.python.ops.numpy_ops.np_array_ops import flatten # line: 889
from tensorflow.python.ops.numpy_ops.np_array_ops import flip # line: 1433
from tensorflow.python.ops.numpy_ops.np_array_ops import fliplr # line: 1452
from tensorflow.python.ops.numpy_ops.np_array_ops import flipud # line: 1446
from tensorflow.python.ops.numpy_ops.np_array_ops import full # line: 136
from tensorflow.python.ops.numpy_ops.np_array_ops import full_like # line: 148
from tensorflow.python.ops.numpy_ops.np_array_ops import hsplit # line: 1184
from tensorflow.python.ops.numpy_ops.np_array_ops import hstack # line: 1214
from tensorflow.python.ops.numpy_ops.np_array_ops import identity # line: 130
from tensorflow.python.ops.numpy_ops.np_array_ops import imag # line: 517
from tensorflow.python.ops.numpy_ops.np_array_ops import isscalar # line: 1114
from tensorflow.python.ops.numpy_ops.np_array_ops import ix_ # line: 1534
from tensorflow.python.ops.numpy_ops.np_array_ops import max # line: 1667
from tensorflow.python.ops.numpy_ops.np_array_ops import mean # line: 657
from tensorflow.python.ops.numpy_ops.np_array_ops import min # line: 1673
from tensorflow.python.ops.numpy_ops.np_array_ops import moveaxis # line: 953
from tensorflow.python.ops.numpy_ops.np_array_ops import ndim # line: 1107
from tensorflow.python.ops.numpy_ops.np_array_ops import newaxis # line: 48
from tensorflow.python.ops.numpy_ops.np_array_ops import nonzero # line: 1324
from tensorflow.python.ops.numpy_ops.np_array_ops import ones # line: 83
from tensorflow.python.ops.numpy_ops.np_array_ops import ones_like # line: 91
from tensorflow.python.ops.numpy_ops.np_array_ops import pad # line: 1018
from tensorflow.python.ops.numpy_ops.np_array_ops import prod # line: 644
from tensorflow.python.ops.numpy_ops.np_array_ops import ravel # line: 772
from tensorflow.python.ops.numpy_ops.np_array_ops import real # line: 779
from tensorflow.python.ops.numpy_ops.np_array_ops import repeat # line: 788
from tensorflow.python.ops.numpy_ops.np_array_ops import reshape # line: 843
from tensorflow.python.ops.numpy_ops.np_array_ops import roll # line: 1458
from tensorflow.python.ops.numpy_ops.np_array_ops import rot90 # line: 1472
from tensorflow.python.ops.numpy_ops.np_array_ops import round # line: 1679
from tensorflow.python.ops.numpy_ops.np_array_ops import select # line: 1077
from tensorflow.python.ops.numpy_ops.np_array_ops import shape # line: 1095
from tensorflow.python.ops.numpy_ops.np_array_ops import sign # line: 1580
from tensorflow.python.ops.numpy_ops.np_array_ops import size # line: 615
from tensorflow.python.ops.numpy_ops.np_array_ops import split # line: 1152
from tensorflow.python.ops.numpy_ops.np_array_ops import squeeze # line: 882
from tensorflow.python.ops.numpy_ops.np_array_ops import stack # line: 1198
from tensorflow.python.ops.numpy_ops.np_array_ops import std # line: 759
from tensorflow.python.ops.numpy_ops.np_array_ops import sum # line: 631
from tensorflow.python.ops.numpy_ops.np_array_ops import swapaxes # line: 914
from tensorflow.python.ops.numpy_ops.np_array_ops import take # line: 1036
from tensorflow.python.ops.numpy_ops.np_array_ops import take_along_axis # line: 1602
from tensorflow.python.ops.numpy_ops.np_array_ops import transpose # line: 905
from tensorflow.python.ops.numpy_ops.np_array_ops import tri # line: 1353
from tensorflow.python.ops.numpy_ops.np_array_ops import tril # line: 1383
from tensorflow.python.ops.numpy_ops.np_array_ops import triu # line: 1408
from tensorflow.python.ops.numpy_ops.np_array_ops import vander # line: 1493
from tensorflow.python.ops.numpy_ops.np_array_ops import var # line: 706
from tensorflow.python.ops.numpy_ops.np_array_ops import vsplit # line: 1181
from tensorflow.python.ops.numpy_ops.np_array_ops import vstack # line: 1230
from tensorflow.python.ops.numpy_ops.np_array_ops import where # line: 1064
from tensorflow.python.ops.numpy_ops.np_array_ops import zeros # line: 65
from tensorflow.python.ops.numpy_ops.np_array_ops import zeros_like # line: 74
from tensorflow.python.ops.numpy_ops.np_config import enable_numpy_behavior as experimental_enable_numpy_behavior # line: 25
from tensorflow.python.ops.numpy_ops.np_dtypes import bool_ # line: 27
from tensorflow.python.ops.numpy_ops.np_dtypes import complex128 # line: 31
from tensorflow.python.ops.numpy_ops.np_dtypes import complex64 # line: 35
from tensorflow.python.ops.numpy_ops.np_dtypes import complex_ # line: 112
from tensorflow.python.ops.numpy_ops.np_dtypes import float16 # line: 39
from tensorflow.python.ops.numpy_ops.np_dtypes import float32 # line: 43
from tensorflow.python.ops.numpy_ops.np_dtypes import float64 # line: 47
from tensorflow.python.ops.numpy_ops.np_dtypes import float_ # line: 115
from tensorflow.python.ops.numpy_ops.np_dtypes import iinfo # line: 121
from tensorflow.python.ops.numpy_ops.np_dtypes import inexact # line: 51
from tensorflow.python.ops.numpy_ops.np_dtypes import int16 # line: 59
from tensorflow.python.ops.numpy_ops.np_dtypes import int32 # line: 63
from tensorflow.python.ops.numpy_ops.np_dtypes import int64 # line: 67
from tensorflow.python.ops.numpy_ops.np_dtypes import int8 # line: 71
from tensorflow.python.ops.numpy_ops.np_dtypes import int_ # line: 55
from tensorflow.python.ops.numpy_ops.np_dtypes import issubdtype # line: 126
from tensorflow.python.ops.numpy_ops.np_dtypes import object_ # line: 75
from tensorflow.python.ops.numpy_ops.np_dtypes import string_ # line: 80
from tensorflow.python.ops.numpy_ops.np_dtypes import uint16 # line: 84
from tensorflow.python.ops.numpy_ops.np_dtypes import uint32 # line: 88
from tensorflow.python.ops.numpy_ops.np_dtypes import uint64 # line: 92
from tensorflow.python.ops.numpy_ops.np_dtypes import uint8 # line: 96
from tensorflow.python.ops.numpy_ops.np_dtypes import unicode_ # line: 101
from tensorflow.python.ops.numpy_ops.np_math_ops import abs # line: 698
from tensorflow.python.ops.numpy_ops.np_math_ops import absolute # line: 704
from tensorflow.python.ops.numpy_ops.np_math_ops import add # line: 90
from tensorflow.python.ops.numpy_ops.np_math_ops import allclose # line: 542
from tensorflow.python.ops.numpy_ops.np_math_ops import angle # line: 852
from tensorflow.python.ops.numpy_ops.np_math_ops import append # line: 1417
from tensorflow.python.ops.numpy_ops.np_math_ops import arccos # line: 799
from tensorflow.python.ops.numpy_ops.np_math_ops import arccosh # line: 817
from tensorflow.python.ops.numpy_ops.np_math_ops import arcsin # line: 793
from tensorflow.python.ops.numpy_ops.np_math_ops import arcsinh # line: 811
from tensorflow.python.ops.numpy_ops.np_math_ops import arctan # line: 805
from tensorflow.python.ops.numpy_ops.np_math_ops import arctan2 # line: 402
from tensorflow.python.ops.numpy_ops.np_math_ops import arctanh # line: 823
from tensorflow.python.ops.numpy_ops.np_math_ops import argmax # line: 1405
from tensorflow.python.ops.numpy_ops.np_math_ops import argmin # line: 1411
from tensorflow.python.ops.numpy_ops.np_math_ops import argsort # line: 1340
from tensorflow.python.ops.numpy_ops.np_math_ops import array_equal # line: 1155
from tensorflow.python.ops.numpy_ops.np_math_ops import average # line: 1426
from tensorflow.python.ops.numpy_ops.np_math_ops import bitwise_and # line: 630
from tensorflow.python.ops.numpy_ops.np_math_ops import bitwise_not # line: 648
from tensorflow.python.ops.numpy_ops.np_math_ops import bitwise_or # line: 636
from tensorflow.python.ops.numpy_ops.np_math_ops import bitwise_xor # line: 642
from tensorflow.python.ops.numpy_ops.np_math_ops import cbrt # line: 868
from tensorflow.python.ops.numpy_ops.np_math_ops import ceil # line: 716
from tensorflow.python.ops.numpy_ops.np_math_ops import clip # line: 222
from tensorflow.python.ops.numpy_ops.np_math_ops import concatenate # line: 1298
from tensorflow.python.ops.numpy_ops.np_math_ops import conj # line: 728
from tensorflow.python.ops.numpy_ops.np_math_ops import conjugate # line: 879
from tensorflow.python.ops.numpy_ops.np_math_ops import cos # line: 763
from tensorflow.python.ops.numpy_ops.np_math_ops import cosh # line: 781
from tensorflow.python.ops.numpy_ops.np_math_ops import count_nonzero # line: 1334
from tensorflow.python.ops.numpy_ops.np_math_ops import cross # line: 289
from tensorflow.python.ops.numpy_ops.np_math_ops import deg2rad # line: 829
from tensorflow.python.ops.numpy_ops.np_math_ops import diff # line: 1054
from tensorflow.python.ops.numpy_ops.np_math_ops import divide # line: 144
from tensorflow.python.ops.numpy_ops.np_math_ops import divmod # line: 182
from tensorflow.python.ops.numpy_ops.np_math_ops import dot # line: 60
from tensorflow.python.ops.numpy_ops.np_math_ops import e # line: 51
from tensorflow.python.ops.numpy_ops.np_math_ops import einsum # line: 1543
from tensorflow.python.ops.numpy_ops.np_math_ops import equal # line: 1119
from tensorflow.python.ops.numpy_ops.np_math_ops import exp # line: 686
from tensorflow.python.ops.numpy_ops.np_math_ops import exp2 # line: 885
from tensorflow.python.ops.numpy_ops.np_math_ops import expm1 # line: 894
from tensorflow.python.ops.numpy_ops.np_math_ops import fabs # line: 710
from tensorflow.python.ops.numpy_ops.np_math_ops import fix # line: 900
from tensorflow.python.ops.numpy_ops.np_math_ops import float_power # line: 396
from tensorflow.python.ops.numpy_ops.np_math_ops import floor # line: 722
from tensorflow.python.ops.numpy_ops.np_math_ops import floor_divide # line: 150
from tensorflow.python.ops.numpy_ops.np_math_ops import gcd # line: 588
from tensorflow.python.ops.numpy_ops.np_math_ops import geomspace # line: 1259
from tensorflow.python.ops.numpy_ops.np_math_ops import greater # line: 1131
from tensorflow.python.ops.numpy_ops.np_math_ops import greater_equal # line: 1137
from tensorflow.python.ops.numpy_ops.np_math_ops import heaviside # line: 414
from tensorflow.python.ops.numpy_ops.np_math_ops import hypot # line: 430
from tensorflow.python.ops.numpy_ops.np_math_ops import inf # line: 55
from tensorflow.python.ops.numpy_ops.np_math_ops import inner # line: 273
from tensorflow.python.ops.numpy_ops.np_math_ops import isclose # line: 524
from tensorflow.python.ops.numpy_ops.np_math_ops import iscomplex # line: 909
from tensorflow.python.ops.numpy_ops.np_math_ops import iscomplexobj # line: 921
from tensorflow.python.ops.numpy_ops.np_math_ops import isfinite # line: 982
from tensorflow.python.ops.numpy_ops.np_math_ops import isinf # line: 988
from tensorflow.python.ops.numpy_ops.np_math_ops import isnan # line: 934
from tensorflow.python.ops.numpy_ops.np_math_ops import isneginf # line: 996
from tensorflow.python.ops.numpy_ops.np_math_ops import isposinf # line: 1004
from tensorflow.python.ops.numpy_ops.np_math_ops import isreal # line: 915
from tensorflow.python.ops.numpy_ops.np_math_ops import isrealobj # line: 928
from tensorflow.python.ops.numpy_ops.np_math_ops import kron # line: 436
from tensorflow.python.ops.numpy_ops.np_math_ops import lcm # line: 595
from tensorflow.python.ops.numpy_ops.np_math_ops import less # line: 1143
from tensorflow.python.ops.numpy_ops.np_math_ops import less_equal # line: 1149
from tensorflow.python.ops.numpy_ops.np_math_ops import linspace # line: 1205
from tensorflow.python.ops.numpy_ops.np_math_ops import log # line: 680
from tensorflow.python.ops.numpy_ops.np_math_ops import log10 # line: 1018
from tensorflow.python.ops.numpy_ops.np_math_ops import log1p # line: 1024
from tensorflow.python.ops.numpy_ops.np_math_ops import log2 # line: 1012
from tensorflow.python.ops.numpy_ops.np_math_ops import logaddexp # line: 482
from tensorflow.python.ops.numpy_ops.np_math_ops import logaddexp2 # line: 494
from tensorflow.python.ops.numpy_ops.np_math_ops import logical_and # line: 1180
from tensorflow.python.ops.numpy_ops.np_math_ops import logical_not # line: 1198
from tensorflow.python.ops.numpy_ops.np_math_ops import logical_or # line: 1186
from tensorflow.python.ops.numpy_ops.np_math_ops import logical_xor # line: 1192
from tensorflow.python.ops.numpy_ops.np_math_ops import logspace # line: 1246
from tensorflow.python.ops.numpy_ops.np_math_ops import matmul # line: 236
from tensorflow.python.ops.numpy_ops.np_math_ops import maximum # line: 188
from tensorflow.python.ops.numpy_ops.np_math_ops import meshgrid # line: 1514
from tensorflow.python.ops.numpy_ops.np_math_ops import minimum # line: 210
from tensorflow.python.ops.numpy_ops.np_math_ops import mod # line: 163
from tensorflow.python.ops.numpy_ops.np_math_ops import multiply # line: 108
from tensorflow.python.ops.numpy_ops.np_math_ops import nanmean # line: 965
from tensorflow.python.ops.numpy_ops.np_math_ops import nanprod # line: 960
from tensorflow.python.ops.numpy_ops.np_math_ops import nansum # line: 957
from tensorflow.python.ops.numpy_ops.np_math_ops import negative # line: 734
from tensorflow.python.ops.numpy_ops.np_math_ops import nextafter # line: 408
from tensorflow.python.ops.numpy_ops.np_math_ops import not_equal # line: 1125
from tensorflow.python.ops.numpy_ops.np_math_ops import outer # line: 472
from tensorflow.python.ops.numpy_ops.np_math_ops import pi # line: 47
from tensorflow.python.ops.numpy_ops.np_math_ops import polyval # line: 506
from tensorflow.python.ops.numpy_ops.np_math_ops import positive # line: 1030
from tensorflow.python.ops.numpy_ops.np_math_ops import power # line: 390
from tensorflow.python.ops.numpy_ops.np_math_ops import ptp # line: 1290
from tensorflow.python.ops.numpy_ops.np_math_ops import rad2deg # line: 838
from tensorflow.python.ops.numpy_ops.np_math_ops import reciprocal # line: 740
from tensorflow.python.ops.numpy_ops.np_math_ops import remainder # line: 176
from tensorflow.python.ops.numpy_ops.np_math_ops import signbit # line: 746
from tensorflow.python.ops.numpy_ops.np_math_ops import sin # line: 757
from tensorflow.python.ops.numpy_ops.np_math_ops import sinc # line: 1036
from tensorflow.python.ops.numpy_ops.np_math_ops import sinh # line: 775
from tensorflow.python.ops.numpy_ops.np_math_ops import sort # line: 1375
from tensorflow.python.ops.numpy_ops.np_math_ops import sqrt # line: 692
from tensorflow.python.ops.numpy_ops.np_math_ops import square # line: 1048
from tensorflow.python.ops.numpy_ops.np_math_ops import subtract # line: 102
from tensorflow.python.ops.numpy_ops.np_math_ops import tan # line: 769
from tensorflow.python.ops.numpy_ops.np_math_ops import tanh # line: 787
from tensorflow.python.ops.numpy_ops.np_math_ops import tensordot # line: 267
from tensorflow.python.ops.numpy_ops.np_math_ops import tile # line: 1313
from tensorflow.python.ops.numpy_ops.np_math_ops import trace # line: 1494
from tensorflow.python.ops.numpy_ops.np_math_ops import true_divide # line: 120
from tensorflow.python.ops.numpy_ops.np_math_ops import vdot # line: 379
from tensorflow.python.ops.numpy_ops.np_utils import finfo # line: 486
from tensorflow.python.ops.numpy_ops.np_utils import promote_types # line: 564
from tensorflow.python.ops.numpy_ops.np_utils import result_type # line: 518
