from strawberry_jam.template import StrawberryJamTemplate
from functools import cache
from strawberry_jam.utils import get_modules_and_classes, snake_case, conv, create_directory
from pathlib import Path


DEPENDENCY_IMPORT = """
from {schema_app_label}.{api_folder_name}.{module_dir_name}.{type_module_name} import {type_class_name}
"""

TEMPLATE = """
import strawberry
{dependency_imports}

@strawberry.type
class Query(
{queries_list}
    ): 
    node: strawberry.relay.Node = strawberry.relay.node()
    
@strawberry.type
class Mutation(
{mutations_list}
): pass
    
schema = strawberry.Schema({include_queries}, {include_mutations})

"""

class Template(StrawberryJamTemplate):
    template: str = TEMPLATE

    overwrite: bool = True  

    query_class_names: list[str] = []

    @property
    @cache
    def module_name(self) -> str:
        return snake_case(self.__module__.split(".")[-1])
    
    @property
    @cache
    def module_dir_name(self):
        return self.api_folder_name

    @property
    @cache
    def module_dir(self) -> Path:
        return self.api_folder_path


    def validate_options(self, options: dict):
        return 

    @property
    @cache
    def queries(self):
        dir = self.api_folder_path / Path(conv("QUERIES_FOLDER_NAME"))
        if not dir.is_dir():
            create_directory(dir)
        return get_modules_and_classes(dir, conv("QUERY_SUFFIX"))

    @property
    @cache
    def mutations(self):
        dir = self.api_folder_path / Path(conv("MUTATIONS_FOLDER_NAME"))
        if not dir.is_dir():
            create_directory(dir)
        return get_modules_and_classes(dir, conv("MUTATION_SUFFIX"))

    @property
    @cache
    def dependency_imports(self) -> str:
        content = []
        for module_name, class_name in self.queries.items():
            content.append(DEPENDENCY_IMPORT.format(
                schema_app_label=self.schema_app_label,
                api_folder_name=self.api_folder_name,
                module_dir_name = conv("QUERIES_FOLDER_NAME"),
                type_module_name = module_name,
                type_class_name = class_name
            ))
        for module_name, class_name in self.mutations.items():
            content.append(DEPENDENCY_IMPORT.format(
                schema_app_label=self.schema_app_label,
                api_folder_name=self.api_folder_name,
                module_dir_name = conv("MUTATIONS_FOLDER_NAME"),
                type_module_name = module_name,
                type_class_name = class_name
            ))
        return "".join(content)
    
    @property
    @cache
    def queries_list(self) -> str:
        return ",\n".join([f"    {v}" for v in self.queries.values()])
    
    @property
    @cache
    def mutations_list(self) -> str:
        return ",\n".join([f"    {v}" for v in self.mutations.values()])

    @property
    @cache
    def include_queries(self):
        return "query=Query" if self.queries.keys().__len__() > 0 else ""
    @property
    @cache
    def include_mutations(self):
        return "mutation=Mutation" if self.mutations.keys().__len__() > 0 else ""