import os
import re
import sys
from typing import Generator

from pyrogram import Client, enums, filters, types

from . import config

client = Client(
    name="Shorts",
    api_id=config.api_id,
    api_hash=config.api_hash,
    workdir=os.getenv("PYROGRAM_WORKDIR", Client.WORKDIR),
)


# Copied from aiogram:
# https://github.com/aiogram/aiogram/blob/0e7a9006b37bed4112e31f1b27772eaada5e1c63/aiogram/types/message_entity.py#L43-L57
def get_text(entity: types.MessageEntity, text: str | bytes) -> str:
    """
    Get value of entity

    :param text: full text
    :return: part of text
    """
    if sys.maxunicode == 0xFFFF:
        return text[entity.offset : entity.offset + entity.length]

    entity_text = text.encode("utf-16-le") if not isinstance(text, bytes) else text
    entity_text = entity_text[entity.offset * 2 : (entity.offset + entity.length) * 2]
    return entity_text.decode("utf-16-le")


# From here on, mostly copied from my Telegram bots
# https://github.com/SandaruKasa/SKTG/blob/6d0002a8786a0fc316ff819e140e874997f214fc/junior/features/shorts.py
def extract_links(message: types.Message) -> Generator[str, None, None]:
    # For the love of God, why do you have to treat captions and text differently?
    # They behave exactly the same in the API and both represent the text part of the message.
    # WHY WOULD YOU NEED TO PUT THEM IN DIFFERENT PLACES?
    # SO THAT API USERS HAVE TO WRITE MORE IF'S?
    for entity in message.entities or message.caption_entities or []:
        if entity.type == enums.MessageEntityType.TEXT_LINK:
            yield entity.url
        elif entity.type == enums.MessageEntityType.URL:
            yield get_text(entity, message.text or message.caption)


# [\w] gives [0-9a-zA-Z_] in ASCII mode
# `.*` in the beginning to prevent www.youtu.be from happening
# `.*` in the end to get rid of ?feature=share and other useless metrics
youtube_short_link = re.compile(r".*youtube\.com/shorts/([\w\-]{11}).*", flags=re.ASCII)
youtube_short_repl = r"https://youtu.be/\1"


@client.on_message(filters=filters.incoming & ~filters.channel)
async def reaction_handler(client: Client, message: types.Message):
    result = []
    for link in extract_links(message):
        substituted, subs = youtube_short_link.subn(youtube_short_repl, link)
        if subs != 0:
            result.append(substituted)
    if result:
        await message.reply(
            "Hello! This isn't me who is sending this message, "
            "it's a program I wrote to automatically convert YouTube Shorts into normal videos. "
            "Like this:\n" + "\n".join(result),
            disable_web_page_preview=True,
        )
