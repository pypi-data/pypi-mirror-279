# -*- coding: utf-8 -*-
"""
Linopy variables module.

This module contains variable related definitions of the package.
"""

import functools
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional, Sequence, Union
from warnings import warn

import numpy as np
import pandas as pd
import polars as pl
from numpy import floating, issubdtype
from xarray import DataArray, Dataset, broadcast
from xarray.core.types import Dims

import linopy.expressions as expressions
from linopy.common import (
    LocIndexer,
    as_dataarray,
    check_has_nulls,
    check_has_nulls_polars,
    filter_nulls_polars,
    format_string_as_variable_name,
    generate_indices_for_printout,
    get_label_position,
    has_optimized_model,
    is_constant,
    print_coord,
    print_single_variable,
    save_join,
    to_dataframe,
    to_polars,
)
from linopy.config import options
from linopy.constants import TERM_DIM
from linopy.solvers import set_int_index

logger = logging.getLogger(__name__)


def varwrap(method, *default_args, **new_default_kwargs):
    @functools.wraps(method)
    def _varwrap(var, *args, **kwargs):
        for k, v in new_default_kwargs.items():
            kwargs.setdefault(k, v)
        return var.__class__(
            method(var.data, *default_args, *args, **kwargs), var.model, var.name
        )

    _varwrap.__doc__ = (
        f"Wrapper for the xarray {method.__qualname__} function for linopy.Variable"
    )
    if new_default_kwargs:
        _varwrap.__doc__ += f" with default arguments: {new_default_kwargs}"

    return _varwrap


def _var_unwrap(var):
    return var.data if isinstance(var, Variable) else var


class Variable:
    """
    Variable container for storing variable labels.

    The Variable class is a subclass of xr.DataArray hence most xarray functions
    can be applied to it. However most arithmetic operations are overwritten.
    Like this one can easily combine variables into a linear expression.


    Examples
    --------
    >>> from linopy import Model
    >>> import pandas as pd
    >>> m = Model()
    >>> x = m.add_variables(pd.Series([0, 0]), 1, name="x")
    >>> y = m.add_variables(4, pd.Series([8, 10]), name="y")

    Add variable together:

    >>> x + y  # doctest: +SKIP
    Linear Expression with 2 term(s):
    ----------------------------------
    <BLANKLINE>
    Dimensions:  (dim_0: 2, _term: 2)
    Coordinates:
      * dim_0    (dim_0) int64 0 1
    Dimensions without coordinates: _term
    Data:
        coeffs   (dim_0, _term) int64 1 1 1 1
        vars     (dim_0, _term) int64 0 2 1 3

    Multiply them with a coefficient:

    >>> 3 * x  # doctest: +SKIP
    Linear Expression with 1 term(s):
    ----------------------------------
    <BLANKLINE>
    Dimensions:  (dim_0: 2, _term: 1)
    Coordinates:
      * dim_0    (dim_0) int64 0 1
    Dimensions without coordinates: _term
    Data:
        coeffs   (dim_0, _term) int64 3 3
        vars     (dim_0, _term) int64 0 1


    Further operations like taking the negative and subtracting are supported.
    """

    __slots__ = ("_data", "_model")
    __array_ufunc__ = None

    _fill_value = {"labels": -1, "lower": np.nan, "upper": np.nan}

    def __init__(self, data: Dataset, model: Any, name: str):
        """
        Initialize the Variable.

        Parameters
        ----------
        labels : xarray.Dataset
            data of the variable.
        model : linopy.Model
            Underlying model.
        """
        from linopy.model import Model

        if not isinstance(data, Dataset):
            raise ValueError(f"data must be a Dataset, got {type(data)}")

        if not isinstance(model, Model):
            raise ValueError(f"model must be a Model, got {type(model)}")

        # check that `labels`, `lower` and `upper`, `sign` and `mask` are in data
        for attr in ("labels", "lower", "upper"):
            if attr not in data:
                raise ValueError(f"missing '{attr}' in data")

        data = data.assign_attrs(name=name)
        (data,) = broadcast(data)
        for attr in (
            "lower",
            "upper",
        ):  # convert to float, important for  operations like "shift"
            if not issubdtype(data[attr].dtype, floating):
                data[attr] = data[attr].astype(float)

        if "label_range" not in data.attrs:
            data.assign_attrs(label_range=(data.labels.min(), data.labels.max()))

        self._data = data
        self._model = model

    def __getitem__(self, selector) -> Union["Variable", "ScalarVariable"]:

        keys = selector if isinstance(selector, tuple) else (selector,)
        if all(map(pd.api.types.is_scalar, keys)):
            warn(
                "Accessing a single value with `Variable[...]` and return type "
                "ScalarVariable is deprecated. In future, this will return a Variable."
                "To get a ScalarVariable use `Variable.at[...]` instead.",
                FutureWarning,
            )
            return self.at[keys]

        else:
            # return selected Variable
            data = Dataset(
                {k: self.data[k][selector] for k in self.data}, attrs=self.attrs
            )
            return self.__class__(data, self.model, self.name)

    @property
    def attrs(self):
        """
        Get the attributes of the variable.
        """
        return self.data.attrs

    @property
    def coords(self):
        """
        Get the coordinates of the variable.
        """
        return self.data.coords

    @property
    def indexes(self):
        """
        Get the indexes of the variable.
        """
        return self.data.indexes

    @property
    def sizes(self):
        """
        Get the sizes of the variable.
        """
        return self.data.sizes

    @property
    def shape(self):
        """
        Get the shape of the variable.
        """
        return self.labels.shape

    @property
    def size(self):
        """
        Get the size of the variable.
        """
        return self.labels.size

    @property
    def dims(self):
        """
        Get the dimensions of the variable.
        """
        return self.labels.dims

    @property
    def ndim(self):
        """
        Get the number of dimensions of the variable.
        """
        return self.labels.ndim

    @property
    def at(self):
        """
        Access a single value of the variable.

        This method is a wrapper around the `__getitem__` method and allows
        to access a single value of the variable.

        Examples
        --------
        >>> from linopy import Model
        >>> import pandas as pd
        >>> m = Model()
        >>> x = m.add_variables(pd.Series([0, 0]), 1, name="x")
        >>> x.at[0]
        ScalarVariable: x[0]
        """
        return AtIndexer(self)

    @property
    def loc(self):
        return LocIndexer(self)

    def to_pandas(self):
        return self.labels.to_pandas()

    def to_linexpr(
        self,
        coefficient: Union[
            np.number, pd.Series, pd.DataFrame, np.ndarray, DataArray
        ] = 1,
    ) -> "expressions.LinearExpression":
        """
        Create a linear expression from the variables.

        Parameters
        ----------
        coefficient : array-like, optional
                Coefficient for the linear expression. This can be a numeric value, numpy array,
                pandas series/dataframe or a DataArray. Default is 1.
        Returns
        -------
        linopy.LinearExpression
            Linear expression with the variables and coefficients.
        """
        coefficient = as_dataarray(coefficient, coords=self.coords, dims=self.dims)
        ds = Dataset({"coeffs": coefficient, "vars": self.labels}).expand_dims(
            TERM_DIM, -1
        )
        return expressions.LinearExpression(ds, self.model)

    def __repr__(self):
        """
        Print the variable arrays.
        """
        max_lines = options["display_max_rows"]
        dims = list(self.sizes.keys())
        dim_sizes = list(self.sizes.values())
        masked_entries = (~self.mask).sum().values
        lines = []

        if dims:
            for indices in generate_indices_for_printout(dim_sizes, max_lines):
                if indices is None:
                    lines.append("\t\t...")
                else:
                    coord = [
                        self.data.indexes[dims[i]][ind] for i, ind in enumerate(indices)
                    ]
                    label = self.labels.values[indices]
                    line = (
                        print_coord(coord)
                        + ": "
                        + print_single_variable(self.model, label)
                    )
                    lines.append(line)
            # lines = align_lines_by_delimiter(lines, "∈")

            shape_str = ", ".join(f"{d}: {s}" for d, s in zip(dims, dim_sizes))
            mask_str = f" - {masked_entries} masked entries" if masked_entries else ""
            lines.insert(
                0,
                f"Variable ({shape_str}){mask_str}\n{'-'* (len(shape_str) + len(mask_str) + 11)}",
            )
        else:
            lines.append(
                f"Variable\n{'-'*8}\n{print_single_variable(self.model, self.labels.item())}"
            )

        return "\n".join(lines)

    def print(self, display_max_rows=20):
        """
        Print the linear expression.

        Parameters
        ----------
        display_max_rows : int
            Maximum number of rows to be displayed.
        display_max_terms : int
            Maximum number of terms to be displayed.
        """
        with options as opts:
            opts.set_value(display_max_rows=display_max_rows)
            print(self)

    def __neg__(self):
        """
        Calculate the negative of the variables (converts coefficients only).
        """
        return self.to_linexpr(-1)

    def __mul__(self, other):
        """
        Multiply variables with a coefficient.
        """
        if isinstance(other, (expressions.LinearExpression, Variable, ScalarVariable)):
            return self.to_linexpr() * other
        else:
            return self.to_linexpr(other)

    def __pow__(self, other):
        """
        Power of the variables with a coefficient. The only coefficient allowed is 2.
        """
        if not other == 2:
            raise ValueError("Power must be 2.")
        return self * self

    def __rmul__(self, other):
        """
        Right-multiply variables with a coefficient.
        """
        return self.to_linexpr(other)

    def __matmul__(self, other):
        """
        Matrix multiplication of variables with a coefficient.
        """
        return self.to_linexpr() @ other

    def __div__(self, other):
        """
        Divide variables with a coefficient.
        """
        if isinstance(other, (expressions.LinearExpression, Variable)):
            raise TypeError(
                "unsupported operand type(s) for /: "
                f"{type(self)} and {type(other)}. "
                "Non-linear expressions are not yet supported."
            )
        return self.to_linexpr(1 / other)

    def __truediv__(self, coefficient):
        """
        True divide variables with a coefficient.
        """
        return self.__div__(coefficient)

    def __add__(self, other):
        """
        Add variables to linear expressions or other variables.
        """
        return self.to_linexpr() + other

    def __radd__(self, other):
        # This is needed for using python's sum function
        return self if other == 0 else NotImplemented

    def __sub__(self, other):
        """
        Subtract linear expressions or other variables from the variables.
        """
        return self.to_linexpr() - other

    def __le__(self, other):
        return self.to_linexpr().__le__(other)

    def __ge__(self, other):
        return self.to_linexpr().__ge__(other)

    def __eq__(self, other):
        return self.to_linexpr().__eq__(other)

    def __gt__(self, other):
        raise NotImplementedError(
            "Inequalities only ever defined for >= rather than >."
        )

    def __lt__(self, other):
        raise NotImplementedError(
            "Inequalities only ever defined for >= rather than >."
        )

    def __contains__(self, value):
        return self.data.__contains__(value)

    def add(self, other):
        """
        Add variables to linear expressions or other variables.
        """
        return self.__add__(other)

    def sub(self, other):
        """
        Subtract linear expressions or other variables from the variables.
        """
        return self.__sub__(other)

    def mul(self, other):
        """
        Multiply variables with a coefficient.
        """
        return self.__mul__(other)

    def div(self, other):
        """
        Divide variables with a coefficient.
        """
        return self.__div__(other)

    def pow(self, other):
        """
        Power of the variables with a coefficient. The only coefficient allowed is 2.
        """
        return self.__pow__(other)

    def dot(self, other):
        """
        Generalized dot product for linopy and compatible objects. Like np.einsum if performs a
        multiplaction of the two objects with a subsequent summation over common dimensions.
        """
        return self.__matmul__(other)

    def groupby(
        self,
        group,
        squeeze: "bool" = True,
        restore_coord_dims: "bool" = None,
    ):
        """
        Returns a LinearExpressionGroupBy object for performing grouped
        operations.

        Docstring and arguments are borrowed from `xarray.Dataset.groupby`

        Parameters
        ----------
        group : str, DataArray or IndexVariable
            Array whose unique values should be used to group this array. If a
            string, must be the name of a variable contained in this dataset.
        squeeze : bool, optional
            If "group" is a dimension of any arrays in this dataset, `squeeze`
            controls whether the subarrays have a dimension of length 1 along
            that dimension or if the dimension is squeezed out.
        restore_coord_dims : bool, optional
            If True, also restore the dimension order of multi-dimensional
            coordinates.

        Returns
        -------
        grouped
            A `LinearExpressionGroupBy` containing the xarray groups and ensuring
            the correct return type.
        """
        return self.to_linexpr().groupby(
            group=group, squeeze=squeeze, restore_coord_dims=restore_coord_dims
        )

    def rolling(
        self,
        dim: "Mapping[Any, int]" = None,
        min_periods: "int" = None,
        center: "bool | Mapping[Any, bool]" = False,
        **window_kwargs: "int",
    ) -> "expressions.LinearExpressionRolling":
        """
        Rolling window object.

        Docstring and arguments are borrowed from `xarray.Dataset.rolling`

        Parameters
        ----------
        dim : dict, optional
            Mapping from the dimension name to create the rolling iterator
            along (e.g. `time`) to its moving window size.
        min_periods : int, default: None
            Minimum number of observations in window required to have a value
            (otherwise result is NA). The default, None, is equivalent to
            setting min_periods equal to the size of the window.
        center : bool or mapping, default: False
            Set the labels at the center of the window.
        **window_kwargs : optional
            The keyword arguments form of ``dim``.
            One of dim or window_kwargs must be provided.

        Returns
        -------
        linopy.expression.LinearExpressionRolling
        """
        return self.to_linexpr().rolling(
            dim=dim, min_periods=min_periods, center=center, **window_kwargs
        )

    def cumsum(
        self,
        dim: Dims = None,
        *,
        skipna: Optional[bool] = None,
        keep_attrs: Optional[bool] = None,
        **kwargs: Any,
    ) -> "expressions.LinearExpression":
        """
        Cumulated sum along a given axis.

        Docstring and arguments are borrowed from `xarray.Dataset.cumsum`

        Parameters
        ----------
        dim : str, Iterable of Hashable, "..." or None, default: None
            Name of dimension[s] along which to apply ``cumsum``. For e.g. ``dim="x"``
            or ``dim=["x", "y"]``. If "..." or None, will reduce over all dimensions.
        skipna : bool or None, optional
            If True, skip missing values (as marked by NaN). By default, only
            skips missing values for float dtypes; other dtypes either do not
            have a sentinel missing value (int) or ``skipna=True`` has not been
            implemented (object, datetime64 or timedelta64).
        keep_attrs : bool or None, optional
            If True, ``attrs`` will be copied from the original
            object to the new one.  If False, the new object will be
            returned without attributes.
        **kwargs : Any
            Additional keyword arguments passed on to the appropriate array
            function for calculating ``cumsum`` on this object's data.
            These could include dask-specific kwargs like ``split_every``.

        Returns
        -------
        linopy.expression.LinearExpression
        """
        return self.to_linexpr().cumsum(
            dim=dim, skipna=skipna, keep_attrs=keep_attrs, **kwargs
        )

    @property
    def name(self):
        """
        Return the name of the variable.
        """
        return self.attrs["name"]

    @property
    def labels(self):
        """
        Return the labels of the variable.
        """
        return self.data.labels

    @property
    def data(self):
        """
        Get the data of the variable.
        """
        # Needed for compatibility with linopy.merge
        return self._data

    @property
    def model(self):
        """
        Return the model of the variable.
        """
        return self._model

    @property
    def type(self):
        """
        Type of the variable.

        Returns
        -------
        str
            Type of the variable.
        """
        if self.attrs["integer"]:
            return "Integer Variable"
        elif self.attrs["binary"]:
            return "Binary Variable"
        else:
            return "Continuous Variable"

    @property
    def range(self):
        """
        Return the range of the variable.
        """
        return self.data.attrs["label_range"]

    @classmethod
    @property
    def fill_value(cls):
        """
        Return the fill value of the variable.
        """
        return cls._fill_value

    @property
    def mask(self):
        """
        Get the mask of the variable.

        The mask indicates on which coordinates the variable array is enabled
        (True) and disabled (False).

        Returns
        -------
        xr.DataArray
        """
        return (self.labels != self._fill_value["labels"]).astype(bool)

    @property
    def upper(self):
        """
        Get the upper bounds of the variables.

        The function raises an error in case no model is set as a
        reference.
        """
        return self.data.upper

    @upper.setter
    @is_constant
    def upper(self, value):
        """
        Set the upper bounds of the variables.

        The function raises an error in case no model is set as a
        reference.
        """
        value = DataArray(value).broadcast_like(self.upper)
        if not set(value.dims).issubset(self.model.variables[self.name].dims):
            raise ValueError("Cannot assign new dimensions to existing variable.")
        self.data["upper"] = value

    @property
    def lower(self):
        """
        Get the lower bounds of the variables.

        The function raises an error in case no model is set as a
        reference.
        """
        return self.data.lower

    @lower.setter
    @is_constant
    def lower(self, value):
        """
        Set the lower bounds of the variables.

        The function raises an error in case no model is set as a
        reference.
        """
        value = DataArray(value).broadcast_like(self.lower)
        if not set(value.dims).issubset(self.model.variables[self.name].dims):
            raise ValueError("Cannot assign new dimensions to existing variable.")
        self.data["lower"] = value

    @property
    @has_optimized_model
    def solution(self):
        """
        Get the optimal values of the variable.

        The function raises an error in case no model is set as a
        reference or the model is not optimized.
        """
        return self.data["solution"]

    @solution.setter
    def solution(self, value):
        """
        Set the optimal values of the variable.
        """
        value = DataArray(value).broadcast_like(self.labels)
        self.data["solution"] = value

    @property
    @has_optimized_model
    def sol(self):
        """
        Get the optimal values of the variable.

        The function raises an error in case no model is set as a
        reference or the model is not optimized.
        """
        warn(
            "`Variable.sol` is deprecated. Use `Variable.solution` instead.",
            DeprecationWarning,
        )
        return self.solution

    @has_optimized_model
    def get_solver_attribute(self, attr):
        """
        Get an attribute from the solver model.

        Parameters
        ----------
        attr : str
            Name of the attribute to get.

        Returns
        -------
        xr.DataArray
        """
        solver_model = self.model.solver_model
        if self.model.solver_name != "gurobi":
            raise NotImplementedError(
                "Solver attribute getter only supports the Gurobi solver for now."
            )

        vals = pd.Series(
            {v.VarName: getattr(v, attr) for v in solver_model.getVars()}, dtype=float
        )
        vals = set_int_index(vals)

        idx = np.ravel(self.labels)
        try:
            vals = vals[idx].values.reshape(self.labels.shape)
        except KeyError:
            vals = vals.reindex(idx).values.reshape(self.labels.shape)

        return DataArray(vals, self.coords)

    @property
    def flat(self):
        """
        Convert the variable to a pandas DataFrame.

        The resulting DataFrame represents a long table format of the variable
        with columns `labels`, `lower`, `upper` which are not masked.

        Returns
        -------
        df : pandas.DataFrame
        """
        ds = self.data

        def mask_func(data):
            return data["labels"] != -1

        df = to_dataframe(ds, mask_func=mask_func)
        check_has_nulls(df, name=f"{self.type} {self.name}")
        return df

    def to_polars(self) -> pl.DataFrame:
        """
        Convert all variables to a single polars DataFrame.

        The resulting dataframe is a long format of the variables
        with columns `labels`, `lower`, 'upper` and `mask`.

        Returns
        -------
        pl.DataFrame
        """
        df = to_polars(self.data)
        df = filter_nulls_polars(df)
        check_has_nulls_polars(df, name=f"{self.type} {self.name}")
        return df

    def sum(self, dim=None, **kwargs):
        """
        Sum the variables over all or a subset of dimensions.

        This stack all terms of the dimensions, that are summed over, together.
        The function works exactly in the same way as ``LinearExpression.sum()``.

        Parameters
        ----------
        dim : str/list, optional
            Dimension(s) to sum over. The default is None which results in all
            dimensions.
        dims : str/list, optional
            Deprecated. Use ``dim`` instead.

        Returns
        -------
        linopy.LinearExpression
            Summed expression.
        """
        if dim is None and "dims" in kwargs:
            dim = kwargs.pop("dims")
            warn(
                "The `dims` argument is deprecated. Use `dim` instead.",
                DeprecationWarning,
            )
        if kwargs:
            raise ValueError(f"Unknown keyword argument(s): {kwargs}")

        return self.to_linexpr().sum(dim)

    def diff(self, dim, n=1):
        """
        Calculate the n-th order discrete difference along the given dimension.

        This function works exactly in the same way as ``LinearExpression.diff()``.

        Parameters
        ----------
        dim : str
            Dimension over which to calculate the finite difference.
        n : int, default: 1
            The number of times values are differenced.

        Returns
        -------
        linopy.LinearExpression
            Finite difference expression.
        """
        return self.to_linexpr().diff(dim, n)

    def isnull(self):
        """
        Get a boolean mask with true values where there is missing values.
        """
        return self.labels == -1

    def where(self, cond, other=None, **kwargs):
        """
        Filter variables based on a condition.

        This operation call ``xarray.DataArray.where`` but sets the default
        fill value to -1 and ensures preserving the linopy.Variable type.

        Parameters
        ----------
        cond : DataArray or callable
            Locations at which to preserve this object's values. dtype must be `bool`.
            If a callable, it must expect this object as its only parameter.
        other : scalar, DataArray, Variable, optional
            Value to use for locations in this object where ``cond`` is False.
            By default, these locations filled with -1.
        **kwargs :
            Keyword arguments passed to ``xarray.DataArray.where``

        Returns
        -------
        linopy.Variable
        """
        if other is None:
            other = self._fill_value
        elif isinstance(other, Variable):
            other = other.data
        elif isinstance(other, ScalarVariable):
            other = {"labels": other.label, "lower": other.lower, "upper": other.upper}
        elif not isinstance(other, (dict, Dataset)):
            warn(
                "other argument of Variable.where should be a Variable, ScalarVariable or dict. "
                "Other types will not be supported in the future.",
                FutureWarning,
            )
        return self.__class__(
            self.data.where(cond, other, **kwargs), self.model, self.name
        )

    def fillna(self, fill_value):
        """
        Fill missing values with a variable.

        This operation call ``xarray.DataArray.fillna`` but ensures preserving
        the linopy.Variable type.

        Parameters
        ----------
        fill_value : Variable/ScalarVariable
            Variable to use for filling.
        """
        return self.where(~self.isnull(), fill_value)

    def ffill(self, dim, limit=None):
        """
        Forward fill the variable along a dimension.

        This operation call ``xarray.DataArray.ffill`` but ensures preserving
        the linopy.Variable type.

        Parameters
        ----------
        dim : str
            Dimension over which to forward fill.
        limit : int, optional
            Maximum number of consecutive NaN values to forward fill. Must be greater than or equal to 0.

        Returns
        -------
        linopy.Variable
        """
        data = (
            self.data.where(self.labels != -1)
            # .ffill(dim, limit=limit)
            # breaks with Dataset.ffill, use map instead
            .map(DataArray.ffill, dim=dim, limit=limit).fillna(self._fill_value)
        )
        data = data.assign(labels=data.labels.astype(int))
        return self.__class__(data, self.model, self.name)

    def bfill(self, dim, limit=None):
        """
        Backward fill the variable along a dimension.

        This operation call ``xarray.DataArray.bfill`` but ensures preserving
        the linopy.Variable type.

        Parameters
        ----------
        dim : str
            Dimension over which to backward fill.
        limit : int, optional
            Maximum number of consecutive NaN values to backward fill. Must be greater than or equal to 0.

        Returns
        -------
        linopy.Variable
        """
        data = (
            self.data.where(~self.isnull())
            # .bfill(dim, limit=limit)
            # breaks with Dataset.bfill, use map instead
            .map(DataArray.bfill, dim=dim, limit=limit).fillna(self._fill_value)
        )
        data = data.assign(labels=data.labels.astype(int))
        return self.__class__(data, self.model, self.name)

    def sanitize(self):
        """
        Sanitize variable by ensuring int dtype with fill value of -1.

        Returns
        -------
        linopy.Variable
        """
        if issubdtype(self.labels.dtype, floating):
            data = self.data.assign(labels=self.labels.fillna(-1).astype(int))
            return self.__class__(data, self.model, self.name)
        return self

    def equals(self, other):
        return self.labels.equals(_var_unwrap(other))

    # Wrapped function which would convert variable to dataarray
    assign_attrs = varwrap(Dataset.assign_attrs)

    assign_coords = varwrap(Dataset.assign_coords)

    broadcast_like = varwrap(Dataset.broadcast_like)

    compute = varwrap(Dataset.compute)

    # drop = varwrap(Dataset.drop)

    drop_sel = varwrap(Dataset.drop_sel)

    drop_isel = varwrap(Dataset.drop_isel)

    expand_dims = varwrap(Dataset.expand_dims)

    sel = varwrap(Dataset.sel)

    isel = varwrap(Dataset.isel)

    shift = varwrap(Dataset.shift, fill_value=_fill_value)

    swap_dims = varwrap(Dataset.swap_dims)

    set_index = varwrap(Dataset.set_index)

    rename = varwrap(Dataset.rename)

    roll = varwrap(Dataset.roll)

    stack = varwrap(Dataset.stack)


class AtIndexer:
    __slots__ = ("object",)

    def __init__(self, obj):
        self.object = obj

    def __getitem__(self, keys) -> "ScalarVariable":

        keys = keys if isinstance(keys, tuple) else (keys,)
        object = self.object

        if not all(map(pd.api.types.is_scalar, keys)):
            raise ValueError("Only scalar keys are allowed.")
        # return single scalar
        if not object.labels.ndim:
            return ScalarVariable(object.labels.item(), object.model)
        assert object.labels.ndim == len(
            keys
        ), f"expected {object.labels.ndim} keys, got {len(keys)}."
        key = dict(zip(object.labels.dims, keys))
        keys = [object.labels.get_index(k).get_loc(v) for k, v in key.items()]
        return ScalarVariable(object.labels.data[tuple(keys)], object.model)


@dataclass(repr=False)
class Variables:
    """
    A variables container used for storing multiple variable arrays.
    """

    data: Dict[str, Variable] = field(default_factory=dict)
    model: Any = None  # Model is not defined due to circular imports

    dataset_attrs = ["labels", "lower", "upper"]
    dataset_names = ["Labels", "Lower bounds", "Upper bounds"]

    def _formatted_names(self):
        """
        Get a dictionary of formatted names to the proper variable names.
        This map enables a attribute like accession of variable names which
        are not valid python variable names.
        """
        return {format_string_as_variable_name(n): n for n in self}

    def __getitem__(
        self, names: Union[str, Sequence[str]]
    ) -> Union[Variable, "Variables"]:
        if isinstance(names, str):
            return self.data[names]

        return self.__class__({name: self.data[name] for name in names}, self.model)

    def __getattr__(self, name: str):
        # If name is an attribute of self (including methods and properties), return that
        if name in self.data:
            return self.data[name]
        else:
            if name in (formatted_names := self._formatted_names()):
                return self.data[formatted_names[name]]
        raise AttributeError(
            f"Variables has no attribute `{name}` or the attribute is not accessible / raises an error."
        )

    def __dir__(self):
        base_attributes = super().__dir__()
        formatted_names = [
            n for n in self._formatted_names() if n not in base_attributes
        ]
        return base_attributes + formatted_names

    def __repr__(self):
        """
        Return a string representation of the linopy model.
        """
        r = "linopy.model.Variables"
        line = "-" * len(r)
        r += f"\n{line}\n"

        for name, ds in self.items():
            coords = " (" + ", ".join(ds.coords) + ")" if ds.coords else ""
            r += f" * {name}{coords}\n"
        if not len(list(self)):
            r += "<empty>\n"
        return r

    def __len__(self):
        return self.data.__len__()

    def __iter__(self):
        return self.data.__iter__()

    def items(self):
        return self.data.items()

    def _ipython_key_completions_(self):
        """
        Provide method for the key-autocompletions in IPython.

        See
        http://ipython.readthedocs.io/en/stable/config/integrating.html#tab-completion
        For the details.
        """
        return list(self)

    def add(self, variable):
        """
        Add a variable to the variables container.
        """
        self.data[variable.name] = variable

    def remove(self, name):
        """
        Remove variable `name` from the variables.
        """
        self.data.pop(name)

    @property
    def attrs(self):
        """
        Get the attributes of all variables.
        """
        return self.labels.attrs

    @property
    def coords(self):
        """
        Get the coordinates of all variables.
        """
        return self.labels.coords

    @property
    def indexes(self):
        """
        Get the indexes of all variables.
        """
        return self.labels.indexes

    @property
    def sizes(self):
        """
        Get the sizes of all variables.
        """
        return self.labels.sizes

    @property
    def labels(self):
        """
        Get the labels of all variables.
        """
        return save_join(
            *[v.labels.rename(k) for k, v in self.items()], integer_dtype=True
        )

    @property
    def lower(self):
        """
        Get the lower bounds of all variables.
        """
        return save_join(*[v.lower.rename(k) for k, v in self.items()])

    @property
    def upper(self):
        """
        Get the upper bounds of all variables.
        """
        return save_join(*[v.upper.rename(k) for k, v in self.items()])

    @property
    def nvars(self):
        """
        Get the number all variables effectively used by the model.

        These excludes variables with missing labels.
        """
        return len(self.flat.labels.unique())

    @property
    def binaries(self):
        """
        Get all binary variables.
        """
        keys = [v for v in self if self[v].attrs["binary"]]
        return self[keys]

    @property
    def integers(self):
        """
        Get all integers variables.
        """
        keys = [v for v in self if self[v].attrs["integer"]]
        return self[keys]

    @property
    def continuous(self):
        """
        Get all continuous variables.
        """
        keys = [
            v
            for v in self
            if not self[v].attrs["integer"] and not self[v].attrs["binary"]
        ]
        return self[keys]

    @property
    def solution(self):
        """
        Get the solution of variables.
        """
        return save_join(*[v.solution.rename(k) for k, v in self.items()])

    @has_optimized_model
    def get_solver_attribute(self, attr):
        """
        Get an attribute from the solver model.

        Parameters
        ----------
        attr : str
            Name of the attribute to get.

        Returns
        -------
        xr.DataArray
        """
        return save_join(
            *[v.get_solver_attribute(attr).rename(k) for k, v in self.items()]
        )

    def get_name_by_label(self, label):
        """
        Get the variable name of the variable containing the passed label.

        Parameters
        ----------
        label : int
            Integer label within the range [0, MAX_LABEL] where MAX_LABEL is the last assigned
            variable label.

        Raises
        ------
        ValueError
            If label is not contained by any variable.

        Returns
        -------
        name : str
            Name of the containing variable.
        """
        if not isinstance(label, (float, int, np.integer)) or label < 0:
            raise ValueError("Label must be a positive number.")
        for name, labels in self.labels.items():
            if label in labels:
                return name
        raise ValueError(f"No variable found containing the label {label}.")

    def get_label_range(self, name: str):
        """
        Get starting and ending label for a variable.
        """
        return self[name].range

    def get_label_position(self, values):
        """
        Get tuple of name and coordinate for variable labels.
        """
        return get_label_position(self, values)

    def print_labels(self, values):
        """
        Print a selection of labels of the variables.

        Parameters
        ----------
        values : list, array-like
            One dimensional array of constraint labels.
        """
        res = [print_single_variable(self.model, v) for v in values]
        print("\n".join(res))

    @property
    def flat(self) -> pd.DataFrame:
        """
        Convert all variables to a single pandas Dataframe.

        The resulting dataframe is a long format of the variables
        with columns `labels`, `lower`, 'upper` and `mask`.

        Returns
        -------
        pd.DataFrame
        """
        df = pd.concat([self[k].flat for k in self], ignore_index=True)
        unique_labels = df.labels.unique()
        map_labels = pd.Series(np.arange(len(unique_labels)), index=unique_labels)
        df["key"] = df.labels.map(map_labels)
        return df

    def reset_solution(self):
        """
        Reset the stored solution of variables.
        """
        for k, v in self.items():
            if "solution" in v:
                v._data = v.data.drop_vars("solution")

    def set_blocks(self, blocks: DataArray):
        """
        Get a dataset of same shape as variables.labels indicating the blocks.
        """
        dim = blocks.dims[0]
        assert dim in self.labels.dims, "Block dimension not in variables."

        for name, variable in self.items():
            if dim in variable.dims:
                variable.data["blocks"] = blocks.broadcast_like(variable.labels)

    def get_blockmap(self, dtype=np.int8):
        """
        Get a one-dimensional array mapping the variables to blocks.
        """
        df = self.flat
        res = np.full(self.model._xCounter + 1, -1, dtype=dtype)
        res[df.labels] = df.blocks
        return res


class ScalarVariable:
    """
    A scalar variable container.

    In contrast to the Variable class, a ScalarVariable only contains
    only one label. Use this class to create a expression or constraint
    in a rule.
    """

    __slots__ = ("_label", "_model")

    def __init__(self, label: int, model: Any):
        self._label = label
        self._model = model

    def __repr__(self) -> str:
        if self.label == -1:
            return "ScalarVariable: None"
        name, coord = self.model.variables.get_label_position(self.label)
        coord_string = print_coord(coord)
        return f"ScalarVariable: {name}{coord_string}"

    @property
    def label(self):
        """
        Get the label of the variable.
        """
        return self._label

    @property
    def lower(self):
        """
        Get the lower bound of the variable.
        """
        name, position = self.model.variables.get_label_position(self.label)
        return self.model.variables[name].lower.sel(position).item()

    @property
    def upper(self):
        """
        Get the upper bound of the variable.
        """
        name, position = self.model.variables.get_label_position(self.label)
        return self.model.variables[name].upper.sel(position).item()

    @property
    def model(self):
        """
        Get the model to which the variable belongs.
        """
        return self._model

    def to_scalar_linexpr(self, coeff=1):
        if not isinstance(coeff, (int, np.integer, float)):
            raise TypeError(f"Coefficient must be a numeric value, got {type(coeff)}.")
        return expressions.ScalarLinearExpression((coeff,), (self.label,), self.model)

    def to_linexpr(self, coeff=1):
        return self.to_scalar_linexpr(coeff).to_linexpr()

    def __neg__(self):
        return self.to_scalar_linexpr(-1)

    def __add__(self, other):
        return self.to_scalar_linexpr(1) + other

    def __radd__(self, other):
        # This is needed for using python's sum function
        return self if other == 0 else NotImplemented

    def __sub__(self, other):
        return self.to_scalar_linexpr(1) - other

    def __mul__(self, coeff):
        return self.to_scalar_linexpr(coeff)

    def __rmul__(self, coeff):
        return self.to_scalar_linexpr(coeff)

    def __div__(self, coeff):
        return self.to_scalar_linexpr(1 / coeff)

    def __truediv__(self, coeff):
        return self.__div__(coeff)

    def __le__(self, other):
        return self.to_scalar_linexpr(1).__le__(other)

    def __ge__(self, other):
        return self.to_scalar_linexpr(1).__ge__(other)

    def __eq__(self, other):
        return self.to_scalar_linexpr(1).__eq__(other)

    def __gt__(self, other):
        raise NotImplementedError(
            "Inequalities only ever defined for >= rather than >."
        )

    def __lt__(self, other):
        raise NotImplementedError(
            "Inequalities only ever defined for >= rather than >."
        )
