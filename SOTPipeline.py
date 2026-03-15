import asyncio
import logging

from Communication.Communication import Communication


async def backup_pipeline(communication: Communication, interval: int = 21600):
    while True:
        try:
            communication.update_sot()
            await asyncio.sleep(interval)

        except Exception as e:
            print(f"backup failed, error:{str(e)}")
