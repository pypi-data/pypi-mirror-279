import numpy as np

pg_stride = 720

splits = ['number', 'object']
fmissing = np.nan
fdne = -np.inf
smissing = 'null'
sdne = '-'
string_type = np.str_
float_type = np.float32
int_type = np.int32
allowed_float_types = [np.float32, np.float64]
allowed_int_types = [np.int32, np.int64]
allowed_string_types = [np.str_, 'object']
allowed_dtypes = allowed_float_types + allowed_int_types + allowed_string_types
