
from strawberry_jam.template import StrawberryJamTemplate
from strawberry_jam.utils import snake_case
from functools import cache
from pathlib import Path

TEMPLATE = """
from django.urls import path
from strawberry.django.views import GraphQLView

from {schema_app_label}.{api_folder_name}.schema import schema

urlpatterns = [
    path('', GraphQLView.as_view(schema=schema)),
]
"""


class Template(StrawberryJamTemplate):
    template: str = TEMPLATE

    @property
    @cache
    def module_name(self) -> str:
        return snake_case(self.__module__.split(".")[-1])
    

    @property
    @cache
    def module_dir(self) -> Path:
        return self.api_folder_path
    
    @property
    @cache
    def module_dir_name(self):
        return self.api_folder_name

    def validate_options(self, options: dict):
        return 