from strawberry_jam.template import StrawberryJamTemplate
from functools import cache
from strawberry_jam.utils import pascal_case, snake_case


TEMPLATE = """
# TODO: Strawberry-Jam: review this file
import strawberry
import strawberry_django
from strawberry_jam.mutations import create, update
from typing import cast, TYPE_CHECKING, Annotated
from strawberry_django.permissions import (
    IsAuthenticated,
)

from {schema_app_label}.{api_folder_name}.inputs.{create_input_module_name} import {create_input_class_name}
from {schema_app_label}.{api_folder_name}.inputs.{update_input_module_name} import {update_input_class_name}

if TYPE_CHECKING:
    from {schema_app_label}.{api_folder_name}.nodes.{node_module_name} import {node_class_name}

@strawberry.type(name="Mutation")
class {module_class_name}:
    create_{field_name}: Annotated['{node_class_name}', strawberry.lazy(
        "{schema_app_label}.{api_folder_name}.nodes.{node_module_name}"
    )] = create(
        {create_input_class_name},
        extensions=[
            IsAuthenticated(),
        ]
    )

    update_{field_name}: Annotated['{node_class_name}', strawberry.lazy(
        "{schema_app_label}.{api_folder_name}.nodes.{node_module_name}"
    )] = update(
        {update_input_class_name},
        extensions=[
            IsAuthenticated(),
        ]
    )

    delete_{field_name}: Annotated['{node_class_name}', strawberry.lazy(
        "{schema_app_label}.{api_folder_name}.nodes.{node_module_name}"
    )] = strawberry_django.mutations.delete(
        strawberry_django.NodeInput,
        extensions=[
            IsAuthenticated(),
        ]

    )

"""

class Template(StrawberryJamTemplate):
    template: str = TEMPLATE    

    @property
    @cache
    def field_name(self) -> str:
        return snake_case(self.model_name)

    @property
    @cache
    def node_module_name(self):
        return snake_case(self.model_name, "node")
    
    @property
    @cache
    def node_class_name(self):
        return pascal_case(self.model_name, "node")
    
    @property
    @cache
    def create_input_module_name(self):
        return snake_case(self.model_name, "create_input")
    
    @property
    @cache
    def create_input_class_name(self):
        return pascal_case(self.model_name, "create_input")

    @property
    @cache
    def create_form_module_name(self):
        return snake_case(self.model_name, "create_form")

    @property
    @cache
    def create_form_class_name(self):
        return pascal_case(self.model_name, "create_form")


    @property
    @cache
    def update_input_module_name(self):
        return snake_case(self.model_name, "update_input")
    
    @property
    @cache
    def update_input_class_name(self):
        return pascal_case(self.model_name, "update_input")
    
    @property
    @cache
    def update_form_module_name(self):
        return snake_case(self.model_name, "update_form")
    
    @property
    @cache
    def update_form_class_name(self):
        return pascal_case(self.model_name, "update_form")

    