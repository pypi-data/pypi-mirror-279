from strawberry_jam.template import StrawberryJamTemplate
from strawberry_jam.utils import snake_case
from functools import cache
from pathlib import Path

TEMPLATE = """
from {schema_app_label}.{api_folder_name}.schema import schema

def test_schema_is_valid():
    assert schema is not None
    assert hasattr(schema, 'query')
    assert hasattr(schema, 'mutation')

"""

class Template(StrawberryJamTemplate): 
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

