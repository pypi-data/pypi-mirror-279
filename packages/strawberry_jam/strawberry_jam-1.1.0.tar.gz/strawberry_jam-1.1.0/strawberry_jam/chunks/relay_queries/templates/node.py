from strawberry_jam.template import StrawberryJamTemplate
from functools import cache
from strawberry_jam.utils import pascal_case, snake_case, conv
from django.db.models import Field, OneToOneField, ManyToManyField, ForeignKey

TYPE_CHECKING_IMPORTS = """
if TYPE_CHECKING:
{type_checking_imports}
"""

# from my_app.graphql.nodes.my_node import MyNode
API_DEPENDANCY_IMPORT = """
    from {schema_app_label}.{api_folder_name}.{module_dir_name}.{field_node_module_name} import {field_node_name}
"""


FIELD = """
    {field_name}: strawberry.auto = strawberry_django.field()
"""

REL_TO_ONE = """
    {field_name}: Annotated["{field_node_name}", strawberry.lazy(
        "{schema_app_label}.{api_folder_name}.{module_dir_name}.{field_node_module_name}"
    )] = strawberry_django.node()
"""

REL_TO_MANY = """
    {relay_field_name}: ListConnectionWithTotalCount[Annotated["{field_node_name}", strawberry.lazy(
        "{schema_app_label}.{api_folder_name}.{module_dir_name}.{field_node_module_name}"
    )]] = strawberry_django.connection(
        field_name="{field_name}",
    )
"""

TEMPLATE = """
# TODO: Strawberry-Jam: review this file
import strawberry
import strawberry_django
from strawberry.relay import Node
from strawberry_django.relay import ListConnectionWithTotalCount
from typing import TYPE_CHECKING, Annotated
from {model_app_label}.models import {model_name}
from {schema_app_label}.{api_folder_name}.filters.{filter_module_name} import {fileter_class_name}
from {schema_app_label}.{api_folder_name}.orders.{order_module_name} import {order_class_name}


{typechecking_imports}


@strawberry_django.type({model_name}, filters={fileter_class_name}, order={order_class_name}, fields=["id"])
class {module_class_name}(Node):
{fields}
"""

class Template(StrawberryJamTemplate):
    template: str = TEMPLATE

    @property
    @cache
    def fileter_class_name(self):
        return pascal_case(self.model_name, conv("FILTER_SUFFIX"))
    
    @property
    @cache
    def filter_module_name(self):
        return snake_case(self.model_name, conv("FILTER_SUFFIX"))
    @property
    @cache
    def order_class_name(self):
        return pascal_case(self.model_name, conv("ORDER_SUFFIX"))
    
    @property
    @cache
    def order_module_name(self):
        return snake_case(self.model_name, conv("ORDER_SUFFIX"))
    

    @property
    @cache
    def typechecking_imports(self) -> str:
        imports = []
        for field in self.model._meta.get_fields():
            if field.is_relation:
                field: OneToOneField | ManyToManyField | ForeignKey = field
                imports.append(API_DEPENDANCY_IMPORT.format(**{
                    "schema_app_label": self.schema_app_label,
                    "api_folder_name": self.api_folder_name,
                    "module_dir_name": self.module_dir_name,
                    "field_node_module_name": snake_case(field.remote_field.model.__name__, conv("NODE_SUFFIX")),
                    "field_node_name": pascal_case(field.remote_field.model.__name__, conv("NODE_SUFFIX")),
                }))
        if imports.__len__() > 0:
            return TYPE_CHECKING_IMPORTS.format(type_checking_imports="\n".join(imports))
        return "\n"

    
    @property
    @cache
    def fields(self) -> str:
        fields_chunks = []
        for field in self.model._meta.get_fields():
            field: Field = field

            if field.is_relation:
                field: OneToOneField | ManyToManyField | ForeignKey = field
                if field.many_to_many or field.one_to_many:
                    fields_chunks.append(REL_TO_MANY.format(**{
                        "field_name": field.name,
                        "relay_field_name": snake_case(field.name, conv("CONNECTION_SUFFIX")),
                        "schema_app_label": self.schema_app_label,
                        "api_folder_name": self.api_folder_name,
                        "module_dir_name": self.module_dir_name,
                        "field_node_module_name": snake_case(field.remote_field.model.__name__, conv("NODE_SUFFIX")),
                        "field_node_name": pascal_case(field.remote_field.model.__name__, conv("NODE_SUFFIX")),
                    }))
                else: 
                    fields_chunks.append(REL_TO_ONE.format(**{
                        "field_name": field.name,
                        "schema_app_label": self.schema_app_label,
                        "api_folder_name": self.api_folder_name,
                        "module_dir_name": self.module_dir_name,
                        "field_node_module_name": snake_case(field.remote_field.model.__name__, conv("NODE_SUFFIX")),
                        "field_node_name": pascal_case(field.remote_field.model.__name__, conv("NODE_SUFFIX")),
                    }))
            else:
                if field.name != "id":
                    fields_chunks.append(FIELD.format(**{
                        "field_name": field.name
                    }))
        
        return "\n".join(fields_chunks)
    