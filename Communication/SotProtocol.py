code_dictionary = {"finish": 0, "entities": 1, "schemas": 2, "relations": 3}
response_dictionary = {"ready": True, "retry": False}


def parse_entity_request(entities: dict):
    requests = list()

    for label, entities_list in entities.items():
        for chunk in split_list(entities_list):
            requests.append({
                "code": 1,
                "data": {
                    "label": label,
                    "entities": chunk
                }
            })

    return requests


def parse_label_schema_request(schemas: dict):
    requests = list()
    schemas_data = list()

    for label, properties in schemas.items():
        schemas_data.append({
            "label": label,
            "properties": properties
        })

    for chunk in split_list(schemas_data):
        requests.append({
            "code": 2,
            "data": chunk
        })

    return requests


def parse_relation_schema_request(relations):
    requests = list()
    relations_data = list()

    for relationship_type, properties in relations.items():
        relations_data.append({
            "relationshipType": relationship_type,
            "properties": properties
        })

    for chunk in split_list(relations_data):
        requests.append({
            "code": 3,
            "data": chunk
        })

    return requests


def split_list(lst: list, size: int = 500):
    return [lst[i:i + size] for i in range(0, len(lst), size)]
