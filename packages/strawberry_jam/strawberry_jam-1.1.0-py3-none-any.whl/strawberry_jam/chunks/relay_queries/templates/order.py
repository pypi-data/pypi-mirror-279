from strawberry_jam.template import StrawberryJamTemplate
from functools import cache
from strawberry_jam.utils import snake_case, pascal_case, conv
from django.db.models import Field

TYPE_CHECKING_IMPORTS = """
if TYPE_CHECKING:
{type_checking_imports}
"""

# from my_app.graphql.nodes.my_node import MyNode
API_DEPENDANCY_IMPORT = """
    from {schema_app_label}.{api_folder_name}.{module_dir_name}.{field_order_module_name} import {field_order_name}
"""

FIELD = """
    {field_name}: auto
"""

REL_TO_ONE = """
    {field_name}: Annotated["{field_order_name}", strawberry.lazy(
        "{schema_app_label}.{api_folder_name}.{module_dir_name}.{field_order_module_name}"
    )] | None
"""

REL_TO_MANY = """
    {field_name}: List[Annotated["{field_order_name}", strawberry.lazy(
        "{schema_app_label}.{api_folder_name}.{module_dir_name}.{field_order_module_name}"
    )]] | None
"""



TEMPLATE = """
# TODO: Strawberry-Jam: review this file
import strawberry_django
import strawberry
from strawberry import auto, relay
from typing import TYPE_CHECKING, List, Annotated

from {model_app_label}.models import {model_name}

{dependancy_imports}

@strawberry_django.order({model_name})
class {module_class_name}:
{fields}
"""


class Template(StrawberryJamTemplate):
    template: str = TEMPLATE

    @property
    @cache
    def fields(self) -> str:
        fields_chunks = []
        for field in self.model._meta.get_fields():
            field: Field = field
            if field.is_relation: 
                if field.many_to_many or field.one_to_many:
                    fields_chunks.append(REL_TO_MANY.format(**{
                        'field_name': snake_case(field.name, conv("CONNECTION_SUFFIX")),
                        'field_order_name': pascal_case(field.remote_field.model.__name__, conv("ORDER_SUFFIX")),
                        'schema_app_label': self.schema_app_label,
                        'api_folder_name': self.api_folder_name,
                        'module_dir_name': self.module_dir_name,
                        'field_order_module_name': snake_case(field.remote_field.model.__name__, conv("ORDER_SUFFIX")),
                    }))
                else:
                    fields_chunks.append(REL_TO_MANY.format(**{
                        'field_name': field.name,
                        'field_order_name': pascal_case(field.remote_field.model.__name__, conv("ORDER_SUFFIX")),
                        'schema_app_label': self.schema_app_label,
                        'api_folder_name': self.api_folder_name,
                        'module_dir_name': self.module_dir_name,
                        'field_order_module_name': snake_case(field.remote_field.model.__name__, conv("ORDER_SUFFIX")),
                    }))
            else:
                fields_chunks.append(FIELD.format(field_name=field.name))

        return "".join(fields_chunks)

    @property
    @cache
    def dependancy_imports(self):
        imports = []
        for field in self.model._meta.get_fields():
            if field.is_relation:
                imports.append(API_DEPENDANCY_IMPORT.format(**{
                    "schema_app_label": self.schema_app_label,
                    "api_folder_name": self.api_folder_name,
                    "module_dir_name": self.module_dir_name,
                    "field_order_module_name": snake_case(field.remote_field.model.__name__, conv("ORDER_SUFFIX")),
                    "field_order_name": pascal_case(field.remote_field.model.__name__, conv("ORDER_SUFFIX")),
                }))
        if imports.__len__() > 0:
            return TYPE_CHECKING_IMPORTS.format(type_checking_imports="".join(imports))
        return ""
