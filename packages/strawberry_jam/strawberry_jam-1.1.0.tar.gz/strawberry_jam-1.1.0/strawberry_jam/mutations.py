import re
from django.core.exceptions import ValidationError
from django.db.models import Manager
from strawberry_jam.utils import conv
from strawberry.relay import GlobalID
from strawberry_django.mutations import update, resolvers
from strawberry_django.mutations.fields import DjangoCreateMutation, DjangoUpdateMutation, get_pk
from strawberry_django.permissions import get_with_perms
from strawberry_django.resolvers import django_resolver
from strawberry.annotation import StrawberryAnnotation
from django.db import transaction
from typing import (
    Type, 
    Any, 
    List, 
    Union, 
    Optional,
    Literal,
    Callable,
    Mapping,
    Sequence, 
    cast
)
from strawberry.unset import UNSET, UnsetType
from strawberry import UNSET
from strawberry.permission import BasePermission
from strawberry.field import UNRESOLVED
from strawberry.types import Info
from strawberry.extensions.field_extension import FieldExtension
import dataclasses

ADD = conv("ADD_TO_COLLECTION_SUFFIX")
REMOVE = conv("REMOVE_FROM_COLLECTION_SUFFIX")

REGEX = rf"^(.+)_({ADD}|{REMOVE})$"


def validate_relation_mutation_add_remove_fields_input(data: dict) -> dict:
    tracked_ids = {}

    # Populate the dictionary with sets of IDs for each unique suffix, distinguishing add and remove
    for key, value in data.items():
        match = re.match(REGEX, key)
        if match:
            field, suffix = match.groups()
            if field not in tracked_ids:
                tracked_ids[field] = {ADD: set(), REMOVE: set()}
            if suffix == ADD:
                tracked_ids[field][ADD].update(value)
            if suffix == REMOVE:
                tracked_ids[field][REMOVE].update(value)

    errors = {}
    # Check for conflicts in each suffix and add errors to the form
    for suffix, ids in tracked_ids.items():
        conflict_ids = ids[ADD].intersection(ids[REMOVE])
        if conflict_ids:
            errors[field + ADD] = errors[field + REMOVE] = f"Conflicting IDs in {
                field + ADD} and {field+REMOVE}: {conflict_ids}"    
    return errors


def resolve_vdata(data, instance):
    vdata = {}
    for maybe_connection_field_name, value in data.items():
        match = re.match(REGEX, maybe_connection_field_name)
        if match:
            value = [global_id.node_id for global_id in cast(List[GlobalID], value)]
            field, suffix = match.groups()
            relation: Manager = getattr(instance, field, None)
            if relation is None or not isinstance(relation, Manager):
                raise ValidationError({maybe_connection_field_name, f"Invalid field {maybe_connection_field_name}"})
            related_field_name, suffix = match.groups()
            if related_field_name not in vdata:
                vdata[related_field_name] = relation.values_list('id', flat=True)
            if suffix == ADD:
                vdata[related_field_name] = set(vdata[related_field_name]).union(value)
            elif suffix == REMOVE:
                vdata[related_field_name] = set(vdata[related_field_name]).difference(value)
            vdata[related_field_name] = list(vdata[related_field_name])
        else:
            vdata[maybe_connection_field_name] = value
    return vdata



class DjangoAddRemoveCreateMutation(DjangoCreateMutation):

    @django_resolver
    @transaction.atomic
    def resolver(
        self,
        source: Any,
        info: Info | None,
        args: list[Any],
        kwargs: dict[str, Any],
    ) -> Any:
        assert info is not None

        data: list[Any] | Any = kwargs.get(self.argument_name)

        if self.is_list:
            assert isinstance(data, list)
            data = [resolve_vdata(d) for d in data]
            return [
                self.create(
                    resolvers.parse_input(info, vars(d), key_attr=self.key_attr),
                    info=info,
                )
                for d in data
            ]

        assert not isinstance(data, list)
        data = resolve_vdata(data)
        return self.create(
            resolvers.parse_input(info, vars(data), key_attr=self.key_attr)
            if data is not None
            else {},
            info=info,
        )




class DjangoAddRemoveUpdateMutation(DjangoUpdateMutation):
    """
    DjangoAddRemoveUpdateMutation extends DjangoUpdateMutation, 
    overwrites resolver method to support add/remove style mutation.
    """

    @django_resolver
    @transaction.atomic
    def resolver(
        self,
        source: Any,
        info: Info | None,
        args: list[Any],
        kwargs: dict[str, Any],
    ) -> Any:
        """
        An overwrite of resolver method of DjangoUpdateMutation for add/remove style updating. 
        
        For more info see DjangoUpdateMutation.resolver

        Basically, we substitute the relation_add/relation_remove fields with model's relation field on data with merged values and 
        pass it back to the mutation, so everything is expected to work as normal.
        
        Since so, it is not possible to use the mutation with filter.

        IMPORTANT: We are not using relation.add and relation.remove methods for the/each instance,  
        because the relation update will be taken out of resolvers procedure, and global id to pk mapping 
        would need separate resolution and error handling.

        TODO: consider other implementation
        """

        assert info is not None

        model = self.django_model
        assert model is not None

        data: Any = kwargs.get(self.argument_name)
        vdata = vars(data).copy() if data is not None else {}
        errors = validate_relation_mutation_add_remove_fields_input(vdata)
        if errors and errors.values().__len__() > 0:
            raise ValidationError(errors)
        pk = get_pk(vdata, key_attr=self.key_attr)
        if pk not in (None, UNSET):  # noqa: PLR6201
            instance = get_with_perms(
                pk,
                info,
                required=True,
                model=model,
                key_attr=self.key_attr,
            )
        else:
            raise ValidationError("No GlobalID provided: updating via filter is not supported.")
        
        vdata = resolve_vdata(vdata, instance)

        return self.update(
            info, instance, resolvers.parse_input(info, vdata, key_attr=self.key_attr)
        )

def create(
    input_type: Optional[type] = None,
    *,
    name: Optional[str] = None,
    field_name: Optional[str] = None,
    is_subscription: bool = False,
    description: Optional[str] = None,
    init: Literal[True] = True,
    permission_classes: Optional[List[Type[BasePermission]]] = None,
    deprecation_reason: Optional[str] = None,
    default: Any = dataclasses.MISSING,
    default_factory: Union[Callable[..., object], object] = dataclasses.MISSING,
    metadata: Optional[Mapping[Any, Any]] = None,
    directives: Optional[Sequence[object]] = (),
    graphql_type: Optional[Any] = None,
    extensions: List[FieldExtension] = (),  # type: ignore
    argument_name: Optional[str] = None,
    handle_django_errors: Optional[bool] = None,
) -> Any:
    """Create mutation for django input fields.

    Automatically create data for django input fields.

    Examples
    --------
        >>> from strawberry_jam.mutations import create
        >>> @strawberry.django.input
        ... class ProductInput:
        ...     name: strawberry.auto
        ...     price: strawberry.auto
        ...
        >>> @strawberry.mutation
        >>> class Mutation:
        ...     create_product: ProductType = create(
        ...         ProductInput # input type where the to-many relations are declared with field-name + add_suffix and field-name + remove_suffix
        ...         handle_django_errors=True
        ...     )

    """
    return DjangoCreateMutation(
        input_type,
        python_name=None,
        django_name=field_name,
        graphql_name=name,
        type_annotation=StrawberryAnnotation.from_annotation(graphql_type),
        description=description,
        is_subscription=is_subscription,
        permission_classes=permission_classes or [],
        deprecation_reason=deprecation_reason,
        default=default,
        default_factory=default_factory,
        metadata=metadata,
        directives=directives,
        extensions=extensions or (),
        argument_name=argument_name,
        handle_django_errors=handle_django_errors,
    )


def update(
    input_type: Optional[type] = None,
    *,
    name: Optional[str] = None,
    field_name: Optional[str] = None,
    filters: Union[type, UnsetType, None] = UNSET,
    is_subscription: bool = False,
    description: Optional[str] = None,
    init: Literal[True] = True,
    permission_classes: Optional[List[Type[BasePermission]]] = None,
    deprecation_reason: Optional[str] = None,
    default: Any = dataclasses.MISSING,
    default_factory: Union[Callable[..., object], object] = dataclasses.MISSING,
    metadata: Optional[Mapping[Any, Any]] = None,
    directives: Optional[Sequence[object]] = (),
    graphql_type: Optional[Any] = None,
    extensions: List[FieldExtension] = (),  # type: ignore
    argument_name: Optional[str] = None,
    handle_django_errors: Optional[bool] = None,
    key_attr: Optional[str] = "pk",
) -> Any:
    """Add/remove style update mutation for django input fields.

    Examples
    --------
        >>> from strawberry_jam.mutations import update
        >>> @strawberry.django.input
        ... class ProductInput(IdInput):
        ...     name: strawberry.auto
        ...     price: strawberry.auto
        ...
        >>> @strawberry.mutation
        >>> class Mutation:
        ...     update_product: ProductType = update(
        ...         ProductInput # input type where the to-many relations are declared with field-name + add_suffix and field-name + remove_suffix
        ...         handle_django_errors=True
        ...     )

    """
    return DjangoAddRemoveUpdateMutation(
        input_type,
        python_name=None,
        django_name=field_name,
        graphql_name=name,
        type_annotation=StrawberryAnnotation.from_annotation(graphql_type),
        description=description,
        is_subscription=is_subscription,
        permission_classes=permission_classes or [],
        deprecation_reason=deprecation_reason,
        default=default,
        default_factory=default_factory,
        metadata=metadata,
        directives=directives,
        filters=filters,
        extensions=extensions or (),
        argument_name=argument_name,
        handle_django_errors=handle_django_errors,
        key_attr=key_attr,
    )