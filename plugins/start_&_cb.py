import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from helper.database import codeflixbots
from config import *
from config import Config

# Start Command Handler
@Client.on_message(filters.private & filters.command("start"))
async def start(client, message: Message):
    user = message.from_user
    await codeflixbots.add_user(client, message)

    # Initial interactive text and sticker sequence
    m = await message.reply_text("Aʀᴀ ᴀʀᴀ ɪᴀᴍ Aʟɪsᴀ !, Hᴏᴡ ᴀʀᴇ ʏᴏᴜ \nWᴀɪᴛ ᴀ ᴍᴏᴍᴇɴᴛ. . .")
    await asyncio.sleep(0.4)
    await m.edit_text("🎊")
    await asyncio.sleep(0.5)
    await m.edit_text("⚡")
    await asyncio.sleep(0.5)
    await m.edit_text("Sᴛᴀʀᴛɪɴɢ Bᴀʙʏ...")
    await asyncio.sleep(0.4)
    await m.delete()

    # Send sticker after the text sequence
    await message.reply_sticker("CAACAgIAAxkBAAENiEJnjOPkz0obPy5_C3I1fNasUWjh0wACNlwAAkWwMUrVcpUgMBdNJDYE")

    # Define buttons for the start message
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Mʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs", callback_data='help')
        ],
        [
            InlineKeyboardButton('Uᴘᴅᴀᴛᴇs', url='https://t.me/EmitingStars_Botz'),
            InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ', url='https://t.me/Weebs_Weekends')
        ],
        [
            InlineKeyboardButton('Aʙᴏᴜᴛ', callback_data='about'),
            InlineKeyboardButton('Sᴏᴜʀᴄᴇ', callback_data='source')
        ]
    ])

    # Send start message with or without picture
    if Config.START_PIC:
        await message.reply_photo(
            Config.START_PIC,
            caption=Txt.START_TXT.format(user.mention),
            reply_markup=buttons
        )
    else:
        await message.reply_text(
            text=Txt.START_TXT.format(user.mention),
            reply_markup=buttons,
            disable_web_page_preview=True
        )


# Callback Query Handler
@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    print(f"Callback data received: {data}")  # Debugging line

    if data == "home":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Mʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs", callback_data='help')],
                [InlineKeyboardButton('Uᴘᴅᴀᴛᴇs', url='https://t.me/EmitingStars_Botz'), InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ', url='https://t.me/Weebs_Weekends')],
                [InlineKeyboardButton('Aʙᴏᴜᴛ', callback_data='about'), InlineKeyboardButton('Sᴏᴜʀᴄᴇ', callback_data='source')]
            ])
        )
    elif data == "caption":
        await query.message.edit_text(
            text=Txt.CAPTION_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url='https://t.me/Weebs_Weekends'), InlineKeyboardButton("Bᴀᴄᴋ", callback_data="help")]
            ])
        )

    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ •", callback_data='file_names')],
                [InlineKeyboardButton('• ᴛʜᴜᴍʙɴᴀɪʟ', callback_data='thumbnail'), InlineKeyboardButton('ᴄᴀᴘᴛɪᴏɴ •', callback_data='caption')],
                [InlineKeyboardButton('• ᴍᴇᴛᴀᴅᴀᴛᴀ', callback_data='meta'), InlineKeyboardButton('ᴅᴏɴᴀᴛᴇ •', callback_data='donate')],
                [InlineKeyboardButton('• ʜᴏᴍᴇ', callback_data='home')]
            ])
        )

    elif data == "meta":
        await query.message.edit_text(  # Change edit_caption to edit_text
            text=Txt.SEND_METADATA,  # Changed from caption to text
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close"), InlineKeyboardButton("Bᴀᴄᴋ", callback_data="help")]
            ])
        )
    elif data == "donate":
        await query.message.edit_text(
            text=Txt.DONATE_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="help"), InlineKeyboardButton("Oᴡɴᴇʀ", url='https://t.me/JeffySama')]
            ])
        )
    elif data == "file_names":
        format_template = await codeflixbots.get_format_template(user_id)
        await query.message.edit_text(
            text=Txt.FILE_NAME_TXT.format(format_template=format_template),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close"), InlineKeyboardButton("Bᴀᴄᴋ", callback_data="help")]
            ])
        )
    elif data == "thumbnail":
        await query.message.edit_caption(
            caption=Txt.THUMBNAIL_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close"), InlineKeyboardButton("Bᴀᴄᴋ", callback_data="help")]
            ])
        )
    elif data == "metadatax":
        await query.message.edit_caption(
            caption=Txt.SEND_METADATA,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close"), InlineKeyboardButton("Bᴀᴄᴋ", callback_data="help")]
            ])
        )
    elif data == "source":
        await query.message.edit_caption(
            caption=Txt.SOURCE_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close"), InlineKeyboardButton("Bᴀᴄᴋ", callback_data="home")]
            ])
        )
    elif data == "premiumx":
        await query.message.edit_caption(
            caption=Txt.PREMIUM_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="help"), InlineKeyboardButton("Bᴜʏ ᴘʀᴇᴍɪᴜᴍ •", url='https://t.me/JeffySama')]
            ])
        )
    elif data == "plans":
        await query.message.edit_caption(
            caption=Txt.PREPLANS_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close"), InlineKeyboardButton("Bᴜʏ ᴘʀᴇᴍɪᴜᴍ •", url='https://t.me/JeffySama')]
            ])
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url='https://t.me/Weebs_Weekends'), InlineKeyboardButton("Cᴏᴍᴍᴀɴᴅs", callback_data="help")],
                [InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url='https://t.me/JeffySama'), InlineKeyboardButton("Nᴇᴛᴡᴏʀᴋ", url='https://t.me/Eminence_Society')],
                [InlineKeyboardButton("Bᴀᴄᴋ", callback_data="home")]
            ])
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()

# Donation Command Handler
@Client.on_message(filters.command("donate"))
async def donation(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="Bᴀᴄᴋ", callback_data="help"), InlineKeyboardButton(text="Oᴡɴᴇʀ", url='https://t.me/JeffySama')]
    ])
    yt = await message.reply_photo(photo='https://envs.sh/N4z.jpg', caption=Txt.DONATE_TXT, reply_markup=buttons)
    await asyncio.sleep(300)
    await yt.delete()
    await message.delete()

# Premium Command Handler
@Client.on_message(filters.command("premium"))
async def getpremium(bot, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Oᴡɴᴇʀ", url="https://t.me/RexySama"), InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close")]
    ])
    yt = await message.reply_photo(photo='https://envs.sh/N43.jpg', caption=Txt.PREMIUM_TXT, reply_markup=buttons)
    await asyncio.sleep(300)
    await yt.delete()
    await message.delete()

# Plan Command Handler
@Client.on_message(filters.command("plan"))
async def premium(bot, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Sᴇɴᴅ ss", url="https://t.me/RexySama"), InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close")]
    ])
    yt = await message.reply_photo(photo='https://envs.sh/N4G.jpg', caption=Txt.PREPLANS_TXT, reply_markup=buttons)
    await asyncio.sleep(300)
    await yt.delete()
    await message.delete()

# Bought Command Handler
@Client.on_message(filters.command("bought") & filters.private)
async def bought(client, message):
    msg = await message.reply('Wait im checking...')
    replied = message.reply_to_message

    if not replied:
        await msg.edit("<b>Please reply with the screenshot of your payment for the premium purchase to proceed.\n\nFor example, first upload your screenshot, then reply to it using the '/bought' command</b>")
    elif replied.photo:
        await client.send_photo(
            chat_id=LOG_CHANNEL,
            photo=replied.photo.file_id,
            caption=f'<b>User - {message.from_user.mention}\nUser id - <code>{message.from_user.id}</code>\nUsername - <code>{message.from_user.username}</code>\nName - <code>{message.from_user.first_name}</code></b>',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Close", callback_data="close_data")]
            ])
        )
        await msg.edit_text('<b>Your screenshot has been sent to Admins</b>')

@Client.on_message(filters.private & filters.command("help"))
async def help_command(client, message):
    # Await get_me to get the bot's user object
    bot = await client.get_me()
    mention = bot.mention

    # Send the help message with inline buttons
    await message.reply_text(
        text=Txt.HELP_TXT.format(mention=mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Aᴜᴛᴏ ʀᴇɴᴀᴍᴇ ғᴏʀᴍᴀᴛ •", callback_data='file_names')],
            [InlineKeyboardButton('Tʜᴜᴍʙɴᴀɪʟ', callback_data='thumbnail'), InlineKeyboardButton('Cᴀᴘᴛɪᴏɴ', callback_data='caption')],
            [InlineKeyboardButton('Mᴇᴛᴀᴅᴀᴛᴀ', callback_data='meta'), InlineKeyboardButton('Dᴏɴᴀᴛᴇ', callback_data='donate')],
            [InlineKeyboardButton('Hᴏᴍᴇ', callback_data='home')]
        ])
    )
