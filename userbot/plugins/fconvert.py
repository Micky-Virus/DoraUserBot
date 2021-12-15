import asyncio
import os
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path

import os
from datetime import datetime

import requests

from LEGENDBOT.utils import admin_cmd, edit_or_reply, sudo_cmd
from userbot.cmdhelp import CmdHelp

from . import *

from telethon import functions, types
from telethon.errors import PhotoInvalidDimensionsError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import SendMediaRequest

from LEGENDBOT.utils import admin_cmd, edit_or_reply, progress, sudo_cmd
from userbot.cmdhelp import CmdHelp
from userbot.helpers.funct import unzip

if not os.path.isdir("./temp"):
    os.makedirs("./temp")


@bot.on(admin_cmd(pattern="stim$"))
@bot.on(sudo_cmd(pattern="stim$", allow_sudo=True))
async def _(LEGEND):
    if LEGEND.fwd_from:
        return
    reply_to_id = LEGEND.message.id
    if LEGEND.reply_to_msg_id:
        reply_to_id = LEGEND.reply_to_msg_id
    event = await edit_or_reply(LEGEND, "Converting.....")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        filename = "hi.jpg"
        file_name = filename
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await LEGEND.client.download_media(
            reply_message, downloaded_file_name
        )
        if os.path.exists(downloaded_file_name):
            caat = await LEGEND.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=reply_to_id,
            )
            os.remove(downloaded_file_name)
            await event.delete()
        else:
            await event.edit("Can't Convert")
    else:
        await event.edit("Syntax : `.stoi` reply to a Telegram normal sticker")


@bot.on(admin_cmd(pattern="itom$"))
@bot.on(sudo_cmd(pattern="itom$", allow_sudo=True))
async def _(LEGEND):
    if LEGEND.fwd_from:
        return
    reply_to_id = LEGEND.message.id
    if LEGEND.reply_to_msg_id:
        reply_to_id = LEGEND.reply_to_msg_id
    event = await edit_or_reply(LEGEND, "Converting.....")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        filename = "hi.webp"
        file_name = filename
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await LEGEND.client.download_media(
            reply_message, downloaded_file_name
        )
        if os.path.exists(downloaded_file_name):
            caat = await LEGEND.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=reply_to_id,
            )
            os.remove(downloaded_file_name)
            await event.delete()
        else:
            await event.edit("Can't Convert")
    else:
        await event.edit("Syntax : `.itos` reply to a Telegram normal sticker")


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


@bot.on(admin_cmd(pattern="ttf ?(.*)"))
@bot.on(sudo_cmd(pattern="ttf ?(.*)", allow_sudo=True))
async def get(event):
    if event.fwd_from:
        return
    name = event.text[5:]
    if name is None:
        await edit_or_reply(event, "reply to text message as `.ttf <file name>`")
        return
    m = await event.get_reply_message()
    if m.text:
        with open(name, "w") as f:
            f.write(m.message)
        await event.delete()
        await event.client.send_file(event.chat_id, name, force_document=True)
        os.remove(name)
    else:
        await edit_or_reply(event, "reply to text message as `.ttf <file name>`")


@bot.on(admin_cmd(pattern="ftoi$"))
@bot.on(sudo_cmd(pattern="ftoi$", allow_sudo=True))
async def on_file_to_photo(event):
    if event.fwd_from:
        return
    target = await event.get_reply_message()
    hbot = await edit_or_reply(event, "Converting.....")
    try:
        image = target.media.document
    except AttributeError:
        return
    if not image.mime_type.startswith("image/"):
        return  # This isn't an image
    if image.mime_type == "image/webp":
        return  # Telegram doesn't let you directly send stickers as photos
    if image.size > 10 * 1024 * 1024:
        return  # We'd get PhotoSaveFileInvalidError otherwise
    file = await event.client.download_media(target, file=BytesIO())
    file.seek(0)
    img = await event.client.upload_file(file)
    img.name = "image.png"
    try:
        await event.client(
            SendMediaRequest(
                peer=await event.get_input_chat(),
                media=types.InputMediaUploadedPhoto(img),
                message=target.message,
                entities=target.entities,
                reply_to_msg_id=target.id,
            )
        )
    except PhotoInvalidDimensionsError:
        return
    await hbot.delete()


@bot.on(admin_cmd(pattern="gif$"))
@bot.on(sudo_cmd(pattern="gif$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    LEGENDreply = await event.get_reply_message()
    if not LEGENDreply or not LEGENDreply.media or not LEGENDreply.media.document:
        return await edit_or_reply(event, "`Stupid!, This is not animated sticker.`")
    if LEGENDreply.media.document.mime_type != "application/x-tgsticker":
        return await edit_or_reply(event, "`Stupid!, This is not animated sticker.`")
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    chat = "@tgstogifbot"
    LEGENDevent = await edit_or_reply(event, "`Converting to gif ...`")
    async with event.client.conversation(chat) as conv:
        try:
            await silently_send_message(conv, "/start")
            await event.client.send_file(chat, LEGENDreply.media)
            response = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            if response.text.startswith("Send me an animated sticker!"):
                return await LEGENDevent.edit("`This file is not supported`")
            LEGENDresponse = response if response.media else await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            LEGENDfile = Path(
                await event.client.download_media(LEGENDresponse, "./temp/")
            )
            LEGENDgif = Path(await unzip(LEGENDfile))
            legend = await event.client.send_file(
                event.chat_id,
                LEGENDgif,
                support_streaming=True,
                force_document=False,
                reply_to=reply_to_id,
            )
            await event.client(
                functions.messages.SaveGifRequest(
                    id=types.InputDocument(
                        id=legend.media.document.id,
                        access_hash=legend.media.document.access_hash,
                        file_reference=legend.media.document.file_reference,
                    ),
                    unsave=True,
                )
            )
            await LEGENDevent.delete()
            for files in (LEGENDgif, LEGENDfile):
                if files and os.path.exists(files):
                    os.remove(files)
        except YouBlockedUserError:
            await LEGENDevent.edit("Unblock @tgstogifbot")
            return


@bot.on(admin_cmd(pattern="nfc ?(.*)"))
@bot.on(sudo_cmd(pattern="nfc ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "```Reply to any media file.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "reply to media file")
        return
    input_str = event.pattern_match.group(1)
    if input_str is None:
        await edit_or_reply(event, "try `.nfc voice` or`.nfc mp3`")
        return
    if input_str in ["mp3", "voice"]:
        event = await edit_or_reply(event, "converting...")
    else:
        await edit_or_reply(event, "try `.nfc voice` or`.nfc mp3`")
        return
    try:
        start = datetime.now()
        c_time = time.time()
        downloaded_file_name = await event.client.download_media(
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to download")
            ),
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit(
            "Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms)
        )
        new_required_file_name = ""
        new_required_file_caption = ""
        command_to_run = []
        voice_note = False
        supports_streaming = False
        if input_str == "voice":
            new_required_file_caption = "voice_" + str(round(time.time())) + ".opus"
            new_required_file_name = (
                Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-map",
                "0:a",
                "-codec:a",
                "libopus",
                "-b:a",
                "100k",
                "-vbr",
                "on",
                new_required_file_name,
            ]
            voice_note = True
            supports_streaming = True
        elif input_str == "mp3":
            new_required_file_caption = "mp3_" + str(round(time.time())) + ".mp3"
            new_required_file_name = (
                Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-vn",
                new_required_file_name,
            ]
            voice_note = False
            supports_streaming = True
        else:
            await event.edit("not supported")
            os.remove(downloaded_file_name)
            return
        logger.info(command_to_run)
        # TODO: re-write create_subprocess_exec 😉
        process = await asyncio.create_subprocess_exec(
            *command_to_run,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        os.remove(downloaded_file_name)
        if os.path.exists(new_required_file_name):
            force_document = False
            await event.client.send_file(
                entity=event.chat_id,
                file=new_required_file_name,
                allow_cache=False,
                silent=True,
                force_document=force_document,
                voice_note=voice_note,
                supports_streaming=supports_streaming,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "trying to upload")
                ),
            )
            os.remove(new_required_file_name)
            await event.delete()

            
            
            
import os
from datetime import datetime

import requests

from LEGENDBOT.utils import admin_cmd, edit_or_reply, sudo_cmd
from userbot.cmdhelp import CmdHelp

from . import *


@bot.on(admin_cmd(pattern=r"open", outgoing=True))
async def _(event):
    b = await event.client.download_media(await event.get_reply_message())
    a = open(b, "r")
    c = a.read()
    a.close()
    a = await event.reply("Reading file...")
    if len(c) >= 4096:
        await event.edit("output file too large lemme paste it 😜😜")  # hehe
        out = c
        url = "https://del.dog/documents"
        r = requests.post(url, data=out.encode("UTF-8")).json()
        url = f"https://del.dog/{r['key']}"
        await event.edit(
            f" Output file is too large Not supported By Telegram\n**So Pasted to** [Dog Bin]({url}) 😁😁",
            link_preview=False,
        )
        await a.delete()
    else:
        await event.client.send_message(event.chat_id, f"{c}")
        await a.delete()
    os.remove(b)


@bot.on(admin_cmd(pattern="doc ?(.*)"))
async def get(event):
    name = event.text[5:]
    if name is None:
        await event.edit("reply to text message as .ttf <file name>")
        return
    m = await event.get_reply_message()
    if m.text:
        with open(name, "w") as f:
            f.write(m.message)
        await event.delete()
        await event.client.send_file(event.chat_id, name, force_document=True)
        os.remove(name)
    else:
        await event.edit("reply to text message as .doc <file name.extension>")


thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "thumb_image.jpg"


@bot.on(admin_cmd(pattern="stoi"))
@bot.on(sudo_cmd(pattern="stoi", allow_sudo=True))
async def danish(hehe):
    if hehe.fwd_from:
        return
    thumb = None
    hehe.message.id
    if hehe.reply_to_msg_id:
        hehe.reply_to_msg_id
    cobra = await edit_or_reply(hehe, "Converting.....")

    input_str = "dc.jpeg"
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if cobra.reply_to_msg_id:
        datetime.datetime.now()
        file_name = input_str
        reply_message = await cobra.get_reply_message()

        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await hehe.client.download_media(
            reply_message, downloaded_file_name
        )

        try:
            thumb = await reply_message.download_media(thumb=-1)
        except Exception:
            thumb = thumb
        if os.path.exists(downloaded_file_name):

            dc = await hehe.client.send_file(
                hehe.chat_id,
                downloaded_file_name,
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                reply_to=reply_message,
                thumb=thumb,
            )

            os.remove(downloaded_file_name)
            await cobra.delete()
        else:
            await cobra.edit("Something went wrong")
    else:
        await cobra.edit("reply to a non animated sticker")


# hehe


@bot.on(admin_cmd(pattern="itos"))
@bot.on(sudo_cmd(pattern="itos", allow_sudo=True))
async def teamcobra(hehe):
    if hehe.fwd_from:
        return
    thumb = None
    hehe.message.id
    if hehe.reply_to_msg_id:
        hehe.reply_to_msg_id
    cobra = await edit_or_reply(hehe, "Converting.....")

    input_str = "dc.webp"
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if cobra.reply_to_msg_id:
        datetime.datetime.now()
        file_name = input_str
        reply_message = await cobra.get_reply_message()

        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await hehe.client.download_media(
            reply_message, downloaded_file_name
        )

        try:
            thumb = await reply_message.download_media(thumb=-1)
        except Exception:
            thumb = thumb
        if os.path.exists(downloaded_file_name):

            dc = await hehe.client.send_file(
                hehe.chat_id,
                downloaded_file_name,
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                reply_to=reply_message,
                thumb=thumb,
            )

            os.remove(downloaded_file_name)
            await cobra.delete()
        else:
            await cobra.edit("Something went wrong")
    else:
        await cobra.edit("reply to a non animated sticker")
        
        

CmdHelp("fileconvert").add_command(
    "stim", "<reply to a sticker", "Converts the replied sticker into an image"
).add_command(
    "itom", "<reply to a image>", "Converts the replied image to sticker"
).add_command(
    "ftoi", "<reply to a image file", "Converts the replied file image to normal image"
).add_command(
    "gif",
    "<reply to a animated sticker",
    "Converts the replied animated sticker into gif",
).add_command(
    "ttf",
    "<reply to text>",
    "Converts the given text message to required file(given file name)",
).add_command(
    "nfc voice",
    "<reply to media to extract voice>",
    "Converts the replied media file to voice",
).add_command(
    "nfc mp3",
    "<reply to media to extract mp3>",
    "Converts the replied media file to mp3",
).add_command("open", None, "open files as text "
).add_command(
    ".doc <file name.extension> <reply to any text/media>",
    None,
    "Create a document of anything (example:- .doc dc.mp4, .doc dc.txt, .doc dc.webp)",
).add_command("stoi", None, "★  Convert sticker to image"
).add_command(
    "itos", None, "Convert Image to Sticker"
).add()
