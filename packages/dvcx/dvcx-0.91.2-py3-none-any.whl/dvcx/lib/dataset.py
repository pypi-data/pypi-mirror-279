import inspect
from collections.abc import Iterator, Sequence
from typing import TYPE_CHECKING, Callable, Optional, Union

import sqlalchemy
from sqlalchemy.sql.elements import ColumnElement

from dvcx.lib.feature import Feature
from dvcx.lib.feature_types import FeatureLike, FeatureTypes
from dvcx.lib.feature_udf import FeatureConverter
from dvcx.lib.reader import FeatureReader
from dvcx.lib.udf import (
    Aggregator,
    BatchMapper,
    Generator,
    GroupMapper,
    Mapper,
    UDFBase,
)
from dvcx.lib.utils import convert_type_to_dvcx
from dvcx.query.dataset import (
    DatasetQuery,
    JoinPredicateType,
    PartitionByType,
    detach,
)
from dvcx.query.schema import Column

if TYPE_CHECKING:
    from typing_extensions import Self

C = Column


class Dataset(DatasetQuery):
    """DVCX DataFrame is a 2-dimensional table of rows and columns designed to work
    with AI datasets - datasets of unstructured data such as images, video audio, text,
    etc.

    Each row in the DataFrame acts as a reference to a file (or specific elements within
    a file) and is associated with various file parameters, represented as columns.
    These columns typically include labels, embeddings, or auto-generated labels,
    providing a comprehensive view of the file's attributes.
    """

    def apply(self, func, *args, **kwargs):
        return func(self, *args, **kwargs)

    def map(
        self,
        udf: Union[Callable, UDFBase],
        params=None,
        output=None,
        parallel: Optional[int] = None,
        workers: Union[bool, int] = False,
        min_task_size: Optional[int] = None,
        cache: bool = False,
    ) -> "Self":
        """Create a new dataframe by applying a function to each row to create new
        columns. The function should return a list of new column values corresponding
        to column names defined in the `output` parameter.

        Input-output relationship: 1:1

        Parameters:

        `udf` (Callable or UDFBase): Function or class applied to each row.
        `params`: List of column names used as input for the function. Default
                is taken from udf signature. `Stream()` (file object) can be included.
        `output`: Dictionary defining new columns and their corresponding data types.
                The order of the keys is important because it sets the format for the
                function's output.
        `parallel` (int): Enables parallel processing. Set >1 for multiple threads,
                `True` for using all CPU threads. Default is single-threaded.
        `workers` (int): Enables distributed processing if set >1. `True` means use all
                allowed workers. Only for dvc.ai platform setup.
        `min_task_size` (int): Minimum tasks per batch for distributed processing. Only
                for platform setup.
        `cache` (bool): If True, saves `Stream()`/file objects in local cache for future
                usage. Default is False.

        Returns:

        `DataFrame`: New dataframe with original rows but additional columns as
                specified in `output`.

        Example:
        >>> df.map(lambda name: name[:-4] + ".json", output={"json_file": String}) \
        >>>     .save("new_dataset")
        """

        self._validate_args("map()", parallel, workers, min_task_size)

        if output:
            output = {k: convert_type_to_dvcx(v) for k, v in output.items()}

        udf_obj = self._udf_to_obj(udf, Mapper, "map()", params, output, cache=cache)
        return self.add_signals(
            udf_obj.to_udf_wrapper(),
            parallel=parallel,
            workers=workers,
            min_task_size=min_task_size,
            cache=cache,
        )

    def generate(  # type: ignore[override]
        self,
        udf: Union[Callable, UDFBase],
        params=None,
        output=None,
        parallel: Optional[int] = None,
        workers: Union[bool, int] = False,
        min_task_size: Optional[int] = None,
        cache: bool = False,
    ) -> "Self":
        """Create a new dataframe by applying a function to each row to generate a new
        set of rows and columns.

        Input-output relationship: 1:N

        This method is similar to `map()`, uses the same list of parameters, but with
        two key differences:
        1. It produces multiple rows for each input row. This means several rows can be
           generated from a single file record (like extracting multiple files from a
           single archive).
        2. The function should return the complete set of columns, including both file
           columns and newly generated ones, not just the new columns.

        The function returns a nested list, where each inner list represents a set of
        column values (the same as `map()`).
        """
        self._validate_args("generate()", parallel, workers, min_task_size)

        udf_obj = self._udf_to_obj(
            udf, Generator, "generate()", params, output, cache=cache
        )
        return DatasetQuery.generate(
            self,
            udf_obj.to_udf_wrapper(),
            parallel=parallel,
            workers=workers,
            min_task_size=min_task_size,
            cache=cache,
        )

    def aggregate(
        self,
        udf: Union[Callable, UDFBase],
        params=None,
        output=None,
        partition_by: Optional[PartitionByType] = None,
        parallel: Optional[int] = None,
        workers: Union[bool, int] = False,
        min_task_size: Optional[int] = None,
        batch=1,
        cache: bool = False,
    ) -> "Self":
        """Create a new dataframe by aggregating a group of rows using a specified
        function, resulting in a new set of rows and columns.

        Input-output relationship: N:M

        This method bears similarity to `generate()`, employing a comparable set of
        parameters, yet differs in two crucial aspects:
        1. The `partition_by` parameter: This specifies the column name or a list of
           column names that determine the grouping criteria for aggregation.
        2. Group-based UDF function input: Instead of individual rows, the function
           receives a list all rows within each group defined by `partition_by`.
        """
        self._validate_args("aggregate()", parallel, workers, min_task_size)

        udf_obj = self._udf_to_obj(
            udf, Aggregator, "aggregate()", params, output, batch, cache=cache
        )
        return DatasetQuery.generate(
            self,
            udf_obj.to_udf_wrapper(),
            partition_by=partition_by,
            parallel=parallel,
            workers=workers,
            min_task_size=min_task_size,
            cache=cache,
        )

    def batch_map(
        self,
        udf: Union[Callable, UDFBase],
        params=None,
        output=None,
        parallel: Optional[int] = None,
        workers: Union[bool, int] = False,
        min_task_size: Optional[int] = None,
        batch=1000,
        cache: bool = False,
    ) -> "Self":
        """This is a batch version of map(). It accepts the same parameters plus an
        additional parameter:

        `batch` (int), which sets the batch size. The default batch size is 1000.

        Input-output relationship: N:N
        """
        self._validate_args("map()", parallel, workers, min_task_size)

        udf_obj = self._udf_to_obj(
            udf, BatchMapper, "batch_map()", params, output, batch, cache=cache
        )
        return self.add_signals(
            udf_obj.to_udf_wrapper(),
            parallel=parallel,
            workers=workers,
            min_task_size=min_task_size,
            cache=cache,
        )

    def group_map(
        self,
        udf: Union[Callable, UDFBase],
        params=None,
        output=None,
        partition_by: Optional[PartitionByType] = None,
        parallel: Optional[int] = None,
        workers: Union[bool, int] = False,
        min_task_size: Optional[int] = None,
        cache: bool = False,
    ) -> "Self":
        """Warning: experimental functionality!
        Create a new dataframe by applying a function to group of rows to create new
        columns. The function should return a nested list of new column values
        corresponding to columns defined in the `output` parameter.

        Input-output relationship: N:N

        This method is similar to `map()`, employing a comparable set of
        parameters, yet differs in two crucial aspects:
        1. The `partition_by` parameter: This specifies the column name or a list of
           column names that determine the grouping criteria.
        2. Group-based UDF function input: Instead of individual rows, the function
           receives a list all rows within each group defined by `partition_by`.
        3. Group-based UDF function output: Instead of returning a list of new columns
           values, the function returns nested list of the new columns. Each sub-list
           of the columns should correspond to input row in a given order.
        """
        self._validate_args(
            "group_map()", parallel, workers, min_task_size, partition_by
        )

        udf_obj = self._udf_to_obj(
            udf, GroupMapper, "group_map()", params, output, cache=cache
        )
        return self.add_signals(
            udf_obj.to_udf_wrapper(),
            parallel=parallel,
            workers=workers,
            min_task_size=min_task_size,
            partition_by=partition_by,
            cache=cache,
        )

    def _udf_to_obj(
        self,
        udf,
        target_class: type[UDFBase],
        name: str,
        params=None,
        output=None,
        batch: int = 1,
        cache: bool = False,
    ) -> UDFBase:
        if isinstance(udf, UDFBase):
            if not isinstance(udf, target_class):
                cls_name = target_class.__name__
                raise TypeError(
                    f"{name}: expected an instance derived from {cls_name}"
                    f", but received {udf.name}"
                )
            if params:
                raise ValueError(
                    f"params for BaseUDF class {udf.name} cannot be overwritten"
                )
            if output:
                raise ValueError(
                    f"output for BaseUDF class {udf.name} cannot be overwritten"
                )

            if isinstance(udf, UDFBase):
                udf.set_catalog(self.catalog)

                if cache:
                    udf.enable_caching()

            return udf

        if inspect.isfunction(udf):
            return target_class.from_func(udf, params, output, batch)

        if isinstance(udf, type):
            raise TypeError(
                f"{name} error: The class '{udf}' needs to be instantiated"
                f" as an object before you can use it as UDF"
            )

        if not callable(udf):
            raise TypeError(f"{name} error: instance {udf} must be callable for UDF")

        return target_class.from_func(udf, params, output, batch)

    def _validate_args(
        self, name, parallel, workers, min_task_size=None, partition_by=None
    ) -> None:
        msg = None
        if not isinstance(parallel, int) and parallel is not None:
            msg = (
                f"'parallel' argument must be int or None"
                f", {parallel.__class__.__name__} was given"
            )
        elif not isinstance(workers, bool) and not isinstance(workers, int):
            msg = (
                f"'workers' argument must be int or bool"
                f", {workers.__class__.__name__} was given"
            )
        elif min_task_size is not None and not isinstance(min_task_size, int):
            msg = (
                f"'min_task_size' argument must be int or None"
                f", {min_task_size.__class__.__name__} was given"
            )
        elif (
            partition_by is not None
            and not isinstance(partition_by, ColumnElement)
            and not isinstance(partition_by, Sequence)
        ):
            msg = (
                f"'partition_by' argument must be PartitionByType or None"
                f", {partition_by.__class__.__name__} was given"
            )

        if msg:
            raise TypeError(f"Dataset {name} error: {msg}")

    @classmethod
    def _args_to_columns(cls, *features):
        uniq_columns = {}
        for fr in features:
            col_dict = {col: None for col in cls._feature_to_columns(fr)}
            uniq_columns = uniq_columns | col_dict
        return list(uniq_columns)

    @classmethod
    def _feature_to_columns(cls, fr: FeatureLike) -> list[C]:
        if isinstance(fr, str):
            return [C(fr, str)]

        if isinstance(fr, C):
            return [fr]

        if isinstance(fr, FeatureReader):
            return cls._feature_to_columns(fr.fr_class)

        if not Feature.is_feature_class(fr):
            raise TypeError(f"feature or column '{fr}' has a wrong type '{type(fr)}'")

        return [C(name, typ) for name, typ in fr._to_udf_spec()]

    def _extend_features(self, method_name, *args):
        super_func = getattr(super(), method_name)

        columns = self._args_to_columns(*args)
        return super_func(*columns)

    @detach
    def select(self, *args, **kwargs) -> "Self":
        return self._extend_features("select", *args)

    @detach
    def select_except(self, *args) -> "Self":
        return self._extend_features("select_except", *args)

    def get_values(self, *fr_classes: FeatureLike) -> Iterator[Sequence]:
        """
        Iterate over dataset, getting feature values and applying reader calls.
        """
        # Get Feature classes and calls for each FeatureReader
        fr_classes_only, callers = zip(
            *[
                (f.fr_class, f) if isinstance(f, FeatureReader) else (f, lambda x: x)
                for f in fr_classes
            ]
        )
        for features in self.iterate(*fr_classes_only):
            yield [
                call(fr._get_value_with_check()) for fr, call in zip(features, callers)
            ]

    def iterate(self, *fr_classes: FeatureLike) -> Iterator[Sequence[Feature]]:
        fr_classes_only = FeatureTypes._to_features(*fr_classes)
        ds = self.select(*fr_classes_only)

        with ds.as_iterable() as rows_iter:
            params = FeatureConverter.get_flattened_params(fr_classes_only)
            for row in rows_iter:
                yield from FeatureConverter.deserialize(
                    [row], params, fr_classes_only, self.catalog, True
                )

    def to_pytorch(self, *fr_classes: FeatureLike, **kwargs):
        try:
            import torch  # noqa: F401
        except ImportError as exc:
            raise ImportError(
                "Missing required dependency 'torch' for Dataset.to_pytorch()"
            ) from exc
        from dvcx.lib.pytorch import PytorchDataset

        if self.attached:
            ds = self
        else:
            ds = self.save()
        assert ds.name is not None  # for mypy
        return PytorchDataset(
            fr_classes, ds.name, ds.version, catalog=self.catalog, **kwargs
        )

    @detach
    def merge(
        self,
        right_ds: "Dataset",
        on: Union[JoinPredicateType, Sequence[JoinPredicateType]],
        right_on: Union[JoinPredicateType, Sequence[JoinPredicateType], None] = None,
        inner=False,
        rname="{name}_right",
    ) -> "Self":
        if on is None:
            raise ValueError("'on' must be specified in merge()")

        list_on = [on] if not isinstance(on, (list, tuple)) else on
        on_columns = [cols for item in list_on for cols in self._args_to_columns(item)]

        if right_on is not None:
            list_right_on = (
                [right_on] if not isinstance(right_on, (list, tuple)) else right_on
            )
            right_on_columns = [
                cols for item in list_right_on for cols in self._args_to_columns(item)
            ]

            if len(right_on_columns) != len(on_columns):
                raise ValueError("'on' and 'right_on' must have the same length'")
        else:
            right_on_columns = on_columns

        ops = [
            self.c(left) == right_ds.c(right)
            for left, right in zip(on_columns, right_on_columns)
        ]

        return self.join(right_ds, sqlalchemy.and_(*ops), inner, rname)

    def sum(self, fr: FeatureLike):  # type: ignore[override]
        return self._extend_features("sum", fr)

    def avg(self, fr: FeatureLike):  # type: ignore[override]
        return self._extend_features("avg", fr)

    def min(self, fr: FeatureLike):  # type: ignore[override]
        return self._extend_features("min", fr)

    def max(self, fr: FeatureLike):  # type: ignore[override]
        return self._extend_features("max", fr)
