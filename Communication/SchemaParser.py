def parse_schema(raw):
    label_schemas = parse_label_schemas(raw["nodeLabels"])
    relation_schemas = parse_relation_schemas(raw["relationshipTypes"])

    return label_schemas, relation_schemas

def parse_label_schemas(schemas: list):
    parsed_schemas = dict()
    for schema in schemas:
        parse_types(schema["properties"])

        parsed_schemas.update({
            schema["label"]: schema["properties"]
        })

    return parsed_schemas


def parse_relation_schemas(schemas):
    parsed_schemas = dict()
    for schema in schemas:
        parse_types(schema["properties"])

        parsed_schemas.update({
            schema["relationshipType"]: schema["properties"]
        })

    return parsed_schemas


def parse_types(properties):
    for schema_property in properties:
        schema_property["type"] = schema_property["type"].lower()
