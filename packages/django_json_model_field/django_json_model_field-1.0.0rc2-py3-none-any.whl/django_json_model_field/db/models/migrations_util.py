from __future__ import annotations

from importlib import import_module
from typing import Any, TYPE_CHECKING, Tuple, Type, TypeVar, overload

from django.db.models import Field

if TYPE_CHECKING:
    from .json_model import JSONModel

TType = TypeVar("TType", bound=type)

DeconstructedJSONModel = Tuple[str, Tuple[type, ...], dict[str, Any]]


def deconstruct(model_class: Type[JSONModel]) -> DeconstructedJSONModel:
    """
    Deconstructs a JSONModel class into a tuple of its name, bases, and attributes to be used as a model state
    representation in migrations.
    """

    bases = tuple(
        (
            _get_deconstructed_parent(parent)
            for parent in model_class.__mro__[1:-1]  # __mro__ starts with the class itself and ends with object
        )
    )
    opts = model_class._meta
    attrs = {"fields": tuple(field.deconstruct() for field in opts.get_fields(include_parents=False))}
    attrs.update(
        __module__=model_class.__module__,
    )
    if hasattr(model_class, "__classcell__"):
        attrs["__classcell__"] = model_class.__classcell__
    if opts.abstract:
        attrs["abstract"] = True

    return model_class.__name__, bases, attrs


def _get_deconstructed_parent(parent: type) -> type | tuple:
    from .json_model import JSONModel

    if parent == JSONModel:
        return parent

    if issubclass(parent, JSONModel):
        return deconstruct(parent)

    return parent


@overload
def reconstruct(cls: DeconstructedJSONModel) -> Type[JSONModel]:
    ...


@overload
def reconstruct(cls: TType) -> TType:
    ...


def reconstruct(cls: DeconstructedJSONModel | TType) -> Type[JSONModel] | TType:
    """
    Reconstructs a JSONModel class from a deconstructed representation. Used when reconstructing JSONModelField
    instances from migration files during Django migration commands.

    For convenience, type classes can be passed directly to this function, in which case they are returned as-is.
    """

    if isinstance(cls, tuple):
        name, bases, attrs = cls
        bases = tuple(reconstruct(base) for base in bases)
        fields = [_reconstruct_field(field) for field in attrs.pop("fields")]
        attrs.update({name: field for name, field in fields})
        reconstructed_cls = type(name, bases, attrs)
        setattr(reconstructed_cls, "_reconstructed", True)
        return reconstructed_cls

    return cls


def _reconstruct_field(field: tuple) -> tuple[str, Field]:
    name, path, args, kwargs = field
    module_name, field_class_name = path.rsplit(".", 1)
    field_module = import_module(module_name)
    field_class = getattr(field_module, field_class_name)

    return name, field_class(*args, **kwargs)
