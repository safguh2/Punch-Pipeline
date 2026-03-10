def parse_schema(raw):
    label_schemas = parse_label_schemas(raw["nodeLabels"])

def parse_label_schemas(schemas: list):
    parsed_schemas = dict()
    for schema in schemas:
        for schema_property in schema["properties"]:
            schema_property["type"] = schema_property["type"].lower()

        parsed_schemas.update({
            schema["label"]: schema["properties"]
        })

    return parsed_schemas

def parse_relation_schemas(schemas):
    pass