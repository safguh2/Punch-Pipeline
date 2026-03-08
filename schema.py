import asyncio
from pydantic import ValidationError, create_model, ConfigDict, BaseModel


class DynamicBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",  # forbid additional fields
    )


class SchemaValidator:
    def __init__(self, api):
        self.api = api
        self.schemas = dict()

        asyncio.create_task(self.schema_auto_loader())

    async def schema_auto_loader(self):
        while True:
            print("loading new schema")
            self.load_schemas()
            await asyncio.sleep(120)

    def load_schemas(self):
        self.schemas = dict()
        for schema in self.api.get_schemas():
            self.schemas[schema["label"]] = create_model(schema['label'], __base__=DynamicBase, **schema["fields"])
            print(schema)

    def verify(self, object: dict):
        if "label" not in object or "fields" not in object:
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
            validated = model(**object['fields'])
            return True

        except ValidationError as e:
            print(f"Invalid data for schema '{label}': {object}")
            return False
