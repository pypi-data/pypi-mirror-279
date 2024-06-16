from django.db.models import Model
from pathlib import Path
from django.apps import apps
from strawberry_jam.utils import extract_docstring_variables, create_directory, create_module, snake_case, pascal_case
from functools import cache


OPTIONS = {
    "schema_app_label": str,
    "api_folder_name": str,
    "model_app_label": str,
    "model_name": str,
    "overwrite": bool or None,
}

OPTIONAL_OPTIONS = ["overwrite"]


DEFAULT_MODULE_DIR_NAMES = {
    "node": "nodes",
    "filter": "filters",
    "order": "orders",
    "create_form": "forms",
    "update_form": "forms",
    "create_input": "inputs",
    "update_input": "inputs",
    "query": "queries",
    "query_set_manager": "query_set_managers",
    "mutation": "mutations"
}

class StrawberryJamTemplate:
    options: dict
    """The options passed for initialization"""
    # configurable via instantiation
    # required
    schema_app_label: str
    """The django app that will contain the graphql endpoint package, i.e. the folder with 'api_folder_name'"""

    api_folder_name: str
    """The package name for the all the strawberry types to reside in"""
    model_app_label: str
    """The app_label of the model"""
    model_name: str
    """The name of the model"""

    # configurable on subclass
    # required
    template: str
    """The template string containing formattable chunks"""


    #optional
    overwrite: bool = False

    def __init__(self, options: dict) -> None:
        self.validate_options(options)
        self.options = options
        self.schema_app_label = options.get("schema_app_label")
        self.api_folder_name = options.get("api_folder_name")
        self.model_app_label = options.get("model_app_label")
        self.model_name = options.get("model_name")
        self.overwrite = options.get("overwrite", self.overwrite)
        assert self.template and isinstance(self.template, str), f"'template' must be configured on {self.__class__.__name__}"
        if not "urls" in self.module_name or not "schema" in self.module_name:
            assert self.module_dir_name and isinstance(self.module_dir_name, str), f"'module_dir_name' must be configured on {self.module_name}"

    def validate_options(self, options: dict):
        required = set([k for k in OPTIONS if k not in OPTIONAL_OPTIONS])
        options_keys = set([k for k in options.keys() if k not in OPTIONAL_OPTIONS])
        assert required == options_keys, f"Missing required options {required.symmetric_difference(options_keys)}"


    @property 
    @cache
    def schema_app_path(self) -> Path:
        return Path(self.schema_app_label)
    
    @property
    @cache
    def api_folder_path(self) -> Path:
        return self.schema_app_path / Path(self.api_folder_name)
    
    @property
    @cache
    def model(self) -> Model:
        return apps.get_model(self.model_app_label, self.model_name)
    
    @property
    @cache
    def module_name(self) -> str:
        return snake_case(self.model_name, self.__module__.split(".")[-1])
    

    @property
    @cache
    def module_class_name(self) -> str:
        return pascal_case(self.module_name)


    @property
    def module_dir_name(self) -> str: 
        """
        The name of package the module will be created inside
        """
        return DEFAULT_MODULE_DIR_NAMES.get(self.__module__.split(".")[-1])


    
    @property
    @cache
    def module_dir(self) -> Path:
        return self.api_folder_path / Path(self.module_dir_name)
    
    @property
    @cache
    def template_variables(self) -> list[str]:
        return extract_docstring_variables(self.template)
    
    

    def generate_module(self) -> None:
        context = {}
        for var_name in self.template_variables:
            attr_value = getattr(self, var_name)
            assert isinstance(attr_value, str), "All values for template variables must be string"
            context[var_name] = attr_value
        content = self.template.format(**context)
        create_directory(self.module_dir)
        create_module(self.module_name, self.module_dir, content, self.overwrite)


    class Meta:
        abstract = True

