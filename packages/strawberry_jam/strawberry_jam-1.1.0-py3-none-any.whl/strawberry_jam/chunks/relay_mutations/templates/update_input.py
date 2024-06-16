from strawberry_jam.template import StrawberryJamTemplate
from functools import cache
from strawberry_jam.utils import pascal_case, snake_case, conv
from django.db.models import Field, OneToOneField, ManyToManyField, ForeignKey


ADD = conv("ADD_TO_COLLECTION_SUFFIX")
REMOVE = conv("REMOVE_FROM_COLLECTION_SUFFIX")

TYPE_CHECKING_IMPORTS = """
if TYPE_CHECKING:
{type_checking_imports}
"""

API_DEPENDANCY_IMPORT = """
    from {schema_app_label}.{api_folder_name}.{module_dir_name}.{field_input_module_name} import {field_input_name}
"""


FIELD = """
    {field_name}: strawberry.auto = strawberry_django.field()
"""

REL_TO_ONE = """
    {field_name}: strawberry.auto = strawberry_django.field()
"""

REL_TO_MANY = """
    {field_name}_{add_suffix}: List[strawberry.relay.GlobalID] = strawberry.field(
        default_factory=list,
    )
    {field_name}_{remove_suffix}: List[
        strawberry.relay.GlobalID
    ] = strawberry.field(
        default_factory=list, 
    )
    # alternative implemenattion 
    # {field_name}: strawberry.auto = strawberry_django.field()
"""

TEMPLATE = """
# TODO: Strawberry-Jam: review this file
import strawberry
import strawberry_django
from typing import List
from {model_app_label}.models import {model_name}



@strawberry_django.input({model_name}, partial=True)
class {module_class_name}:
    id: strawberry.auto
{fields}


"""

class Template(StrawberryJamTemplate):
    template: str = TEMPLATE


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
                    "field_input_module_name": snake_case(field.remote_field.model.__name__, "create_input"),
                    "field_input_name": pascal_case(field.remote_field.model.__name__, "create_input"),
                }))
        if imports.__len__() > 0:
            return TYPE_CHECKING_IMPORTS.format(type_checking_imports="".join(imports))
        return ""

    
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
                        "field_name": snake_case(field.name),
                        "schema_app_label": self.schema_app_label,
                        "api_folder_name": self.api_folder_name,
                        "module_dir_name": self.module_dir_name,
                        "field_input_module_name": snake_case(field.remote_field.model.__name__, "create_input"),
                        "field_input_name": pascal_case(field.remote_field.model.__name__, "create_input"),
                        "add_suffix": ADD,
                        "remove_suffix": REMOVE
                    }))
                else:
                    fields_chunks.append(REL_TO_ONE.format(**{
                        "field_name": field.name,
                        "schema_app_label": self.schema_app_label,
                        "api_folder_name": self.api_folder_name,
                        "module_dir_name": self.module_dir_name,
                        "field_input_module_name": snake_case(field.remote_field.model.__name__, "create_input"),
                        "field_input_name": pascal_case(field.remote_field.model.__name__, "create_input"),
                    }))
            else:
                if field.name != "id":
                    fields_chunks.append(FIELD.format(**{
                        "field_name": field.name
                    }))
        
        return "".join(fields_chunks)