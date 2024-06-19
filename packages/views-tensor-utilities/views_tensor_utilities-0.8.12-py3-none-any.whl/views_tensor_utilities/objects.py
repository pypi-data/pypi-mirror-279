import pandas as pd
import numpy as np
from . import defaults
from . import mappings


class ViewsDataframe():

    """
    ViewsDataframe

    Wrapper class for pandas dataframe which exposes methods to cast panel data into

    - 3D time-space-feature numpy tensors for regression-type models

    - 4D longitude-latitude-time-feature numpy tensors for neural-net-type models, or visualisation

    Two alternative casting methods are employed:

    - for trivially tensorisable data (where for every feature, every space unit is present at
      every time unit, e.g. pgm data) numpy stride-tricks is used, which is very fast as it uses
      pointer manipulation. Missing data is represented by the default missing values defined in
      defaults.

    - for data which cannot be simply tensorised (because not all space units are present in every
      time unit, e.g. cm data) an empty tensor initialised with default does-not-exist tokens defined
      in defaults is built with dimensions (total number of time units) x (total number of space units)
      x (total number of features). Data from the dataframe is filled in, using the dataframe index
      transformed to tuples. This is slow, but acceptable for cm-level data. Units of analysis not
      present in the input data retain the does-not-exist token. The transformer throws an error
      message if the does-not-exist token is actually present in the data.

    Methods:
        __split_by_dtype: Numeric and string data cannot be mixed in the same numpy tensor.
                          This method is used to break the data from the input dataframe up
                          into numeric and string parts.

        to_numpy_time_space: splits dataframe data into numeric and string parts and casts to
                             numpy time-space-feature feature tensors. The tensors are returned as
                             ViewsTensor objects inside a ViewsTensorContainer object.

        to_numpy_longlat: uses to_numpy_time_space to cast input data to time-space-feature
                          tensors, then casts these to longitude-latitude-time-feature tensors.
                          Cannot be used for data which is not simply tensorisable - an error
                          will be thrown if this is attempted. The tensors are returned as
                          ViewsTensor objects inside a ViewsTensorContainer object.

    """

    def __init__(self, df, cast_to_dtype=None, override_dne=None, override_missing=None):
        self.df = df
        self.index = df.index
        self.split_dfs = []
        self.cast_to_dtype = cast_to_dtype
        self.override_dne = override_dne
        self.override_missing = override_missing

        if mappings.is_strideable(self.index):
            self.transformer = mappings.df_to_numpy_time_space_strided
        else:
            self.transformer = mappings.df_to_numpy_time_space_unstrided

    def __split_by_dtype(self):

        """
        __split_by_dtype

        Protected method which splits input data into numeric and string parts as a list of
        dataframes. An error is thrown if the split fails to capture all the columns in the
        input dataframe.

        The input dataframe is then destroyed.
        """

        nsplit_columns = 0
        for split in defaults.splits:
            split_df = self.df.select_dtypes(include=[split])
            split_df = split_df.apply(pd.to_numeric, errors='ignore')
            self.split_dfs.append(split_df)

            nsplit_columns += len(self.split_dfs[-1].columns)

        if nsplit_columns != len(self.df.columns):
            raise RuntimeError(f'Failed to correctly split df by dtype into {defaults.splits}')

        self.df = None

    def to_numpy_time_space(self, broadcast_index=False):
        """
        to_numpy_time_space

        Method which splits input dataframe into numeric and string dataframes then casts the
        dataframes to time-space-feature tensors.

        Returns: ViewsTensorContainer object containing ViewsTensor objects

        """

        self.__split_by_dtype()

        tensors = []

        for split_df in self.split_dfs:

            if len(split_df.columns) > 0:

                dne = mappings.get_dne(split_df)
                missing = mappings.get_missing(split_df)

                try:

                    tensor_time_space = self.transformer(split_df, self.cast_to_dtype, self.override_dne,
                                                         self.override_missing)
                except:
                    raise RuntimeError('failed to cast at least one df to tensor')
#                    tensor_time_space = self.transformer(split_df)

                vnt = ViewsNumpy(tensor_time_space, split_df.columns, dne, missing)

                if broadcast_index:
                    vnt.index = split_df.index

                tensors.append(vnt)

        return ViewsTensorContainer(tensors, self.index)

    def to_numpy_longlat(self):

        """
        to_numpy_longlat

        Method which first casts input data to a ViewsTensorContainer object containing
        time-space-feature tensors as ViewsTensor objects.

        The tensors in the ViewsTensor objects are then cast to longitude-latitude-time-
        feature tensors and the ViewsTensorContainer object is returned.

        Cannot be used on non-simply-tensorisable dataframes.

        Returns: ViewsTensorContainer object containing ViewsTensor objects


        """

        if not(mappings.is_strideable(self.index)):
            raise RuntimeError(f'Unable to cast to long-lat - ntime x nspace != nobservations')

        tensor_container = self.to_numpy_time_space()

        for views_tensor in tensor_container.ViewsTensors:

            tensor_time_space = views_tensor.tensor

            views_tensor.tensor = mappings.numpy_time_space_to_longlat(tensor_time_space, self.index)

        return tensor_container

    def to_pytorch_time_space(self):
        pass

    def to_pytorch_lat_long_time(self):
        pass


class ViewsTensorContainer():

    """
    ViewsTensorContainer

    Wrapper class used to represent a multi-column pandas dataframe. The dataframe's data is represented
    by

    - a list of one or two ViewsTensor objects containing a numeric and/or a string tensor

    - the original index of the input dataframe (required if the dataframe needs to be reconstructed)

    Methods:

        to_pandas: if tensor container contains 3D tensors, casts split tensors back to dataframes
        and recombines to a single dataframe. If 4D tensors are wrapped, returns an error.

        space_time_to_panel: casts 3D split tensors back to a single dataframe

    """

    def __init__(self, tensors, index):
        self.ViewsTensors = tensors
        self.index = index

        if mappings.is_strideable(self.index):
            self.transformer = mappings.time_space_to_panel_strided
        else:
            self.transformer = mappings.time_space_to_panel_unstrided

    @classmethod
    def from_views_numpy_list(cls, list_of_views_tensors):

        index = list_of_views_tensors[0].index

        dtype_list = [vt.tensor.dtype for vt in list_of_views_tensors]

        dtype_set = set(dtype_list)

        merged_views_tensors = []

        for dtype in dtype_set:
            tensor_group = []
            group_columns = []
            group_dne = None
            group_missing = None
            for vt in list_of_views_tensors:
                if vt.tensor.dtype == dtype:
                    tensor_group.append(vt.tensor)
                    group_columns.append(vt.columns)
                    group_dne = vt.dne
                    group_missing = vt.missing

            merged_tensor = np.concatenate(tensor_group, axis=2)
            merged_views_tensors.append(ViewsNumpy(merged_tensor, group_columns, group_dne, group_missing))

        tensor_container = cls(tensors=merged_views_tensors, index=index)

        return tensor_container

    def to_pandas(self):

        """
        to_pandas

        Call space_time_to_panel if wrapped tensors are 3D, throws an error otherwise


        """

        if len(self.ViewsTensors[0].tensor.shape) != 3:
            raise RuntimeError(f'Not possible to cast ViewsTensorContainer to pandas unless D=3')
        else:
            return self.time_space_to_panel()

    def time_space_to_panel(self):

        """
        space_time_to_panel

        Casts all wrapped tensors to dataframes and combines to a single dataframe, which is returned

        """

        if len(self.ViewsTensors[0].tensor.shape) != 3:
            raise RuntimeError(f'Not possible to cast ViewsTensorContainer to pandas unless D=3')

        split_dfs = []
        for views_tensor in self.ViewsTensors:
            split_dfs.append(self.transformer(views_tensor.tensor, self.index, views_tensor.columns))

        return pd.concat(split_dfs, axis=1)

    def get_numeric_part(self):
        """
        get_numeric_part

        Get and return the numeric part of the container, if it exists

        """

        for views_tensor in self.ViewsTensors:
            tensor = views_tensor.tensor
            if tensor.dtype in defaults.allowed_float_types:
                return views_tensor
        else:
            return None

    def get_numeric_tensor(self):
        """
        get_numeric_tensor

        Get and return the numeric tensor from the container, if it exists

        """

        for views_tensor in self.ViewsTensors:
            tensor = views_tensor.tensor
            if tensor.dtype in defaults.allowed_float_types:
                return tensor
        else:
            return None

    def get_string_part(self):
        """
        get_string_part

        Get and return the string part of the container, if it exists

        """
        for views_tensor in self.ViewsTensors:
            tensor = views_tensor.tensor
            if tensor.dtype in ['str', 'object']:
                return views_tensor
        else:
            return None

    def get_string_tensor(self):
        """
        get_string_tensor

        Get and return the string tensor from the container, if it exists

        """
        for views_tensor in self.ViewsTensors:
            tensor = views_tensor.tensor
            if tensor.dtype in ['str', 'object']:
                return tensor
        else:
            return None


class ViewsNumpy():

    """
    ViewsNumpy

    Wrapper class for a single numpy tensor. Contains

    - a single tensor
    - a list of columns detailing what the features stored in the tensor's last (i.e. 3rd or 4th
      dimension) represent
    - a dne token indicating what value in the tensor represents units-of-analysis which do not exist
      (e.g. countries that do not exist in a particular month)
    - a missing token indicating what value in then tensor represents units-of-analysis which do
      exist but have no defined value

    """

    def __init__(self, tensor, columns, dne, missing):
        self.tensor = tensor
        self.columns = columns
        self.dne = dne
        self.missing = missing
        self.index = None


class ViewsPytorch():

    def __init__(self):
        pass
