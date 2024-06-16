from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from strawberry_jam.utils import validate_model, process_template, finalize_schema
from tqdm import tqdm

class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            nargs="+",
            dest="models",
            help="The models to generate the schema for",
            )
        parser.add_argument(
            "--in-app", "-in",
            type=str,
            dest="schema_app_label",
            help="The app name to place the generated api modules in"
            )
        parser.add_argument(
            "--flavor", "-fl", "--workflow", "-wfl",
            type=str,
            dest="flavor",
            default="django_relay",
            help="The schema workflow to select for schema generation. "
            )
        
        parser.add_argument(
            "--package-name", "-pn",
            type=str,
            dest="api_folder_name",
            default="gql",
            help="The name of the package containing the endpoint. Basically this is a folder inside the endpoint app, that contains all the schema related files and folders",
            )
        parser.add_argument(
            "--overwrite", "-owt", 
            type=bool,
            required=False, 
            default=False, 
            dest="overwrite", 
            help="Overwrite existing files"
            )

    def handle(self, *args: Any, **options: Any) -> None:
        schema_app_label = options.get("schema_app_label")
        api_folder_name = options.get("api_folder_name")
        _options = {
                "schema_app_label": schema_app_label,
                "api_folder_name": api_folder_name,
                "overwrite": options.get("overwrite"),
        }
        models = options.get("models")

        # Use tqdm to show progress for each model
        for model in tqdm(models, colour="blue"):
            model_app_label, model_name = model.split(".")
            opts = {
                "model_app_label": model_app_label,
                "model_name": model_name,
                **_options
            }
            validate_model(opts)
            process_template(opts, options.get("flavor"))

        finalize_schema(options, options.get("flavor"))
