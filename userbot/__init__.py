import logging
import os
import re
import sys
from typing import Generator

from pyrogram import Client, enums, errors, filters, types

from . import config

logger = logging.getLogger(__name__)

client = Client(
    name="Shorts",
    api_id=config.api_id,
    api_hash=config.api_hash,
    workdir=os.getenv("PYROGRAM_WORKDIR", Client.WORKDIR),
)


async def im_in_chat(me: types.User, chat: types.Chat):
    match chat.type:
        case enums.ChatType.PRIVATE | enums.ChatType.BOT:
            # I don't think it's possible to get your hands on any messages from a private chat you're not a part of. (*)
            return True

        case enums.ChatType.CHANNEL:
            # IDC.
            # Fetching members won't work I guess (you can only do that if you're an admin and even then there's a hard limit of 200). (*)
            # Maybe fetching permissions is something you can try, (or is that admin permissions? then it probably won't work either).
            # There might actually be some sort of `.am_joined` flag, but I'm too lazy to check.
            # In the end, it doesn't even matter: I filter out channel messages for this userbot anyways.
            raise NotImplementedError(
                "Can't be bothered to check whether I'm a part of a channel"
            )

        case enums.ChatType.GROUP:
            # I guess some weird shit can happen when the message is from a group that has been converted to a supergroup.
            # Or you're viewing a message from an old group you're no longer a part of.
            # But let's hope Telegram won't send you updates about those.
            return True

        case enums.ChatType.SUPERGROUP:
            # Telegram will actually send you _ALL_ the updates from a discussion group as soon as you open comments. (*)
            # У команды Дурова мало того, что руки из жопы растут, так ещё видимо и ЧСВ люто прёт, раз они вместо того,
            # чтобы использовать уже существующие TLS/BSON, пилят СвОи СоБсТвЕнНыЕ MTProto/TypeLanguage.
            try:
                me_as_member = await chat.get_member(user_id=me.id)
                return True
            except errors.UserNotParticipant:
                return False

        case other:
            raise NotImplementedError(f"Hooray! New chat type: {other}")

    # (*) At least for now. God knows what awful code Telegram will introduce in the future updates.


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


@client.on_message(
    ~filters.channel  # don't react to channel posts (you're probably not an admin there anyways)
    & ~filters.scheduled  # don't react to messages that have just been scheduled but not yet sent
)
async def shorts_handler(client: Client, message: types.Message):
    logger.debug("New message: %s", repr(message))
    result = []
    for link in extract_links(message):
        substituted, subs = youtube_short_link.subn(youtube_short_repl, link)
        if subs != 0:
            result.append(substituted)
    # Sadly the return value of all filters is discarded by pyrogram,
    # so it's impossible to turn the code above into a Filter.__call__
    # and then use its return value here.
    if (
        # there were some links that got converted
        result
        # and I'm actually in this chat
        # (i.e. this message didn't come from a discussion group I'm not a part of)
        and (await im_in_chat(client.me, message.chat))
    ):
        logger.info("Converted in chat %s: %s", repr(message.chat), ", ".join(result))
        await message.reply(
            "Hello! This message isn't sent by me. "
            "It's sent by [a program I wrote](https://github.com/SandaruKasa/ShortsUserbot) "
            "to automatically convert YouTube Shorts into normal videos:\n"
            + "\n".join(result),
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
