import asyncio
import asyncpg


class DatabaseSource:

    def __init__(self, queue: asyncio.Queue, dsn: str, poll_interval: int = 600):
        self.queue = queue
        self.dsn = dsn
        self.poll_interval = poll_interval
        self.conn = None

    async def connect(self):
        self.conn = await asyncpg.connect(self.dsn)

    async def get_tables(self):
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public'
        """
        rows = await self.conn.fetch(query)
        return [r["table_name"] for r in rows]

    async def fetch_table_rows(self, table):
        query = f"SELECT * FROM \"{table}\""
        rows = await self.conn.fetch(query)
        return rows

    async def run(self):

        await self.connect()

        while True:
            try:
                tables = await self.get_tables()

                for table in tables:

                    rows = await self.fetch_table_rows(table)

                    for row in rows:
                        message = {
                            "label": table,
                            "properties": dict(row)
                        }

                        await self.queue.put(str(message).encode())

            except Exception as e:
                print("Database source error:", e)

            await asyncio.sleep(self.poll_interval)