api_type_dictionary = {"string": str, "integer": int, "float": int, "boolean": bool, "date": str, "dict": dict}


def parse_response(response):
    schemas = list()
    print(response)
    for schema in response:
        label = schema['label']

        fields = parse_fields(schema['properties'])

        schemas.append({"label": label, "properties": fields})

    return schemas


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
