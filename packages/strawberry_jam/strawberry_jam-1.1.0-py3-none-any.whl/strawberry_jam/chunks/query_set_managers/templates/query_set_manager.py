
from strawberry_jam.template import StrawberryJamTemplate

TEMPLATE = """
from strawberry_jam.queryset import QuerySetManager
from {model_app_label}.models import {model_name}


class {module_class_name}(QuerySetManager):
    model = {model_name}

    # implement your custom queryset here by overwriting def get_queryset
"""

class Template(StrawberryJamTemplate):
    template: str = TEMPLATE    
