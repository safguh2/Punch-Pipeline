api_type_dictionary = {"string": str, "integer": int, "float": int, "boolean": bool, "date": str, "dict": dict}
def parse_to_model(schemas):
    model_schemas = list()
    print(schemas)
    for schema in schemas:
        label = schema['label']

        fields = parse_fields(schema['properties'])

        model_schemas.append({"label": label, "properties": fields})

    return model_schemas


def parse_fields(raw_fields):
    fields = dict()
    print(raw_fields)
    for field in raw_fields:
        type = api_type_dictionary[field["type"].lower()]
        fields[field['name']] = (type, ...)

    return fields


def get_mock_data():
    with open("../mock_data.json") as data:
        binary = data.read()
        return binary
