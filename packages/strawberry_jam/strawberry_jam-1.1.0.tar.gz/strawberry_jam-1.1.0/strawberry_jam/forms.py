from django.forms import ModelForm
from strawberry_jam.queryset import QuerySetManager
from strawberry_jam.utils import conv
import re
from typing import Dict, Any
from strawberry.relay import GlobalID
from typing import cast, List
from strawberry_jam.mutations import validate_relation_mutation_add_remove_fields_input

ADD = conv("ADD_TO_COLLECTION_SUFFIX")
REMOVE = conv("REMOVE_FROM_COLLECTION_SUFFIX")

REGEX = rf"^(.+)({ADD}|{REMOVE})$"

def check_add_remove_conflict(data: Dict[str, Any], form: ModelForm) -> None:
    errors = validate_relation_mutation_add_remove_fields_input(data)
    for key, val in errors.items():
        form.add_error(key, val)


class ModelForm(ModelForm):
    queryset_manager: QuerySetManager

    class Meta:
        abstract = True

    def __init__(self, info, data, *args, **kwargs) -> None:
        self.info = info
        super().__init__(data, *args, **kwargs)

    def validate(self, data):
        check_add_remove_conflict(data, self)
        return super().validate(data)

    def get_queryset(self):
        return self.queryset_manager.get_queryset(self.info)

    def clean(self):
        cleaned_data = {**super().clean()}
        modified_cleaned_data = {}

        for maybe_connection_field_name, value in cleaned_data.items():
            value = [global_id.id for global_id in cast(List[GlobalID], value)]
            match = re.match(
                REGEX, maybe_connection_field_name)
            if match:
                related_field_name, suffix = match.groups()
                if related_field_name not in self.instance.__dict__:
                    self.add_error(maybe_connection_field_name, f"Invalid related field: {related_field_name}")
                    continue
                if suffix == ADD:
                    modified_cleaned_data[related_field_name] = value
                elif suffix == REMOVE:
                    modified_cleaned_data[related_field_name] = [id for id in getattr(
                        self.instance, related_field_name).values_list('id', flat=True) if id not in value]
                cleaned_data.pop(maybe_connection_field_name)

        return {**cleaned_data, **modified_cleaned_data}
