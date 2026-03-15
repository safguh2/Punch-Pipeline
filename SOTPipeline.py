import asyncio
import logging

from Communication.Communication import Communication


async def backup_pipeline(communication: Communication, interval: int = 21600):
    while True:
        try:
            # await asyncio.sleep(interval)
            communication.update_sot()
            await asyncio.sleep(30)

        except Exception as e:
            print(e)
