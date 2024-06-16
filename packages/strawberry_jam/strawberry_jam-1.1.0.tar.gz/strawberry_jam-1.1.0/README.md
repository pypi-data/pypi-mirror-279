# Strawberry Jam 🍓

Codegen django command for strawberry-django for rapid schema boilerplate generation from given models

## Installation

```txt
pip3 install strawberry_jam
```

or using uv

```txt
uv pip install strawberry_jam
```

Add `'strawberry_jam'` to your project's `settings.py`.

```py
INSTALLED_APPS = [
    # ... other apps
    'strawberry_jam',
]
```

Configure strawberry django to handle GlobalIds automatically.

```py
STRAWBERRY_DJANGO = {
    "MAP_AUTO_ID_AS_GLOBAL_ID": True
}
```

## Usage

```zsh
python3 manage.py configure-schema <app_label.ModelName1> <app_label.ModelName2> <app_label.ModelNameN> -in <my_graphql_app_label> -fl <flavor_name>
```

### Arguments

#### Required

1. list of models in form of `app_label.ModelName`
2. `--in-app`, `-in`: the `app_label` where the schema modules will be generated
3. `--flavor`, `-fl`, `--workflow`, `-wfl`: the name of the workflow that will generate the necessary modules

#### Optional

1. `--package-name`, `-pn`: the name of the package, defaults to `gql`
2. `--overwrite`, `-owt`: if true, will overwrite everything

## Falvors/Workflows

This addon comes with the following flavors:

- `relay_queries`: generates relay style types(nodes), query, filter, order
- `relay_mutations`: generates relay style create/partial-update input types, mutations
- `query_set_managers`: A simple class with get_queryset, to help manage querysets in one place, normally not needed
- `tests`: coming soon

IMPORTANT!

**Running a flavor with `overwrite` flag will replace the necessary modules made with other flavors to work with the currenty run flavor.**

## Under the hood and things to know

### StrawberryJamTemplate

The addon has implemented a simple `StrawberryJamTemplate` class. The command looks for modules in the `chunks/flavor_name/templates/` and initializes the Template subclass of `StrawberryJamTemplate`, which generates the necessary modules in the schema.

### Mutations

The relay_mutations flavor comes with extra. Instead of exposing to-many relations as a field, it exposes them via `<field_name>_add` and `<field_name>_remove` fields of type `list[GlobalID]`, which let add remove fields by simply passing ids that need to be added or removed.

## TODO

- Add generation of test modules
- Maybe add ability to run multiple flavors consecutively
- The generated schema will not work, if the types for relations are not generated. So maybe skip the fields for models that are not supplied to the command.
