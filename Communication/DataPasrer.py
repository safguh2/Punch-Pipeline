def parse_data(raw: dict):
    relations = parse_relations(raw["relationships"])


def parse_relations(relations: list):
    parsed_relations = dict()
    for relation_type in relations:
        parsed_relation_type = list()
        for relation in relation_type["relationships"]:
            entity_from = relation.pop("from")
            entity_to = relation.pop("to")
            relation.update({
                "from": {
                    "entity_id": entity_from["entityId"],
                    "entity_type": entity_from["entityType"]
                },
                "to": {
                    "entity_id": entity_to["entityId"],
                    "entity_type": entity_to["entityType"]
                }
            })

            parsed_relation_type.append(relation)

        parsed_relations.update({
            relation_type["type"]: parsed_relation_type
        })

    return parsed_relations
