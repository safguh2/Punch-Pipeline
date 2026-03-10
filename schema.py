import asyncio
from pydantic import ValidationError, create_model, ConfigDict, BaseModel
from Communication.ModelParser import parse_to_model
from Communication.Neo4jApi import Neo4jApi


class DynamicBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",  # forbid additional fields
    )


class SchemaValidator:
    def __init__(self, api: Neo4jApi):
        self.api: Neo4jApi = api
        self.schemas: dict = dict()

        asyncio.create_task(self.schema_auto_loader())

    async def schema_auto_loader(self):
        while True:
            print("loading new schema")
            self.load_schemas()
            await asyncio.sleep(300)

    def load_schemas(self):
        self.schemas = dict()
        schemas: list = parse_to_model(self.api.get_schemas()["nodeLabels"])
        for schema in schemas:
            self.schemas[schema["label"]] = create_model(schema['label'], __base__=DynamicBase, **schema["properties"])

    def verify(self, object: dict):
        if "label" not in object or "properties" not in object:
            print("schema label in object doesn't exists")
            return False

        label = object['label']
        print(label)
        print(self.schemas)
        if label not in self.schemas:
            print("schema label doesn't exist in current schemas")
            return False

        model = self.schemas[label]

        try:
            validated = model(**object['properties'])
            return True

        except ValidationError as e:
            print(f"Invalid data for schema '{label}': {object}")
            return False
