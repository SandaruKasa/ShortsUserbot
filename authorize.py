#!/usr/bin/env python3
import asyncio
import os

import pyrogram

# REPLACE WITH YOUR OWN
API_ID: int = 17349
API_HASH: str = "344583e45741c457fe1862106095a5eb"


async def main():
    client = pyrogram.Client(
        name="Shorts",
        api_id=API_ID,
        api_hash=API_HASH,
        workdir=os.getenv("PYROGRAM_WORKDIR", pyrogram.Client.WORKDIR),
    )
    async with client:
        print("You are now authorized!")
        print("Session file:", client.storage.database)


if __name__ == "__main__":
    asyncio.run(main())
