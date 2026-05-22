# =========================================================
#         PREMIUM LEAGUE ALL IN ONE BOT
# =========================================================

# INSTALL:
# pip install pyrogram tgcrypto

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import json
import os
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

API_ID = 37893084
API_HASH = "853a6c0f3be11009f667bc153244452e"
BOT_TOKEN = "8560529789:AAH55LSHmHaRYeypwW2fIXIUBcVgNShJYv4"

BOT_NAME = "PCZ TOUR"

# LOG CHANNEL USERNAME
LOG_CHANNEL = "@PCZ_registration_2"

# ADMINS
ADMINS = [7691071175]

# =========================================================
# FORCE JOIN SETTINGS
# =========================================================

CHANNEL_USERNAME = "PCZ_registration_2"
CHAT_USERNAME = "Panchayatgamezone"

CHANNEL_LINK = "https://t.me/PCZ_registration_2"
CHAT_LINK = "https://t.me/Panchayatgamezone"

# =========================================================
# FILES
# =========================================================

PLAYERS_DB = "userzs.json"
LEAGUE_DB = "leaguess.json"

# =========================================================
# CREATE FILES
# =========================================================

for file in [PLAYERS_DB, LEAGUE_DB]:

    if not os.path.exists(file):

        with open(file, "w") as f:
            json.dump({}, f)

# =========================================================
# LOAD / SAVE
# =========================================================

def load_json(file):

    try:
        with open(file, "r") as f:
            return json.load(f)

    except:
        return {}

def save_json(file, data):

    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# =========================================================
# DEFAULT PLAYER
# =========================================================

def default_player(role):

    return {
        "role": role
    }

# =========================================================
# BOT CLIENT
# =========================================================

app = Client(
    "premium_registrations_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =========================================================
# PROFILE PHOTO
# =========================================================

async def get_profile_photo(user):

    try:

        photos = []

        async for photo in app.get_chat_photos(user.id, limit=1):
            photos.append(photo.file_id)

        if photos:
            return photos[0]

        return f"https://ui-avatars.com/api/?name={user.first_name}&background=random"

    except:

        return f"https://ui-avatars.com/api/?name={user.first_name}&background=random"

# =========================================================
# START COMMAND
# =========================================================

@app.on_message(filters.command("start"))
async def start(client, message):

    user = message.from_user
    user_id = str(user.id)

    # =====================================
    # FORCE JOIN CHECK
    # =====================================

    try:

        channel = await app.get_chat_member(
            CHANNEL_USERNAME,
            user.id
        )

        chat = await app.get_chat_member(
            CHAT_USERNAME,
            user.id
        )

        if (
            str(channel.status) in ["left", "kicked"]
            or
            str(chat.status) in ["left", "kicked"]
        ):

            raise Exception

    except:

        text = f"""
<b>🏏 WELCOME TO {BOT_NAME}</b>

<b>🔥 To Use This Bot You Must Join Our Official Channel & Chat.</b>

<b>📌 After Joining Click On Joined Button Below.</b>
"""

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📢 JOIN CHANNEL",
                        url=CHANNEL_LINK
                    )
                ],
                [
                    InlineKeyboardButton(
                        "💬 JOIN CHAT",
                        url=CHAT_LINK
                    )
                ],
                [
                    InlineKeyboardButton(
                        "✅ JOINED",
                        callback_data="joined"
                    )
                ]
            ]
        )

        await message.reply_text(
            text,
            reply_markup=buttons
        )

        return

    # =====================================
    # NORMAL FLOW
    # =====================================

    db = load_json(PLAYERS_DB)

    profile_photo = await get_profile_photo(user)

    # =====================================
    # ALREADY REGISTERED
    # =====================================

    if user_id in db:

        role = db[user_id]["role"]

        text = f"""
<b>🏏 WELCOME BACK TO {BOT_NAME}</b>

<b>✅ You Are Already Registered</b>

<b>👤 Name:</b> {user.first_name}
<b>🏏 Role:</b> {role.upper()}

<b>🔥 Ready For Upcoming Leagues.</b>

<b>Use /register to Register in The Tour</b>
"""

        await message.reply_photo(
            photo=profile_photo,
            caption=text
        )

        return

    # =====================================
    # NEW USER
    # =====================================

    text = f"""
<b>🏏 WELCOME TO {BOT_NAME}</b>

<b>🔥 Official Pcz Registration Bot</b>

<b>📌 Select Your Role Below</b>

<b>🏏 Batsman</b>
<b>🎯 Bowler</b>
<b>⚡ All Rounder</b>
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🏏 Batsman",
                    callback_data="role_batsman"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎯 Bowler",
                    callback_data="role_bowler"
                )
            ],
            [
                InlineKeyboardButton(
                    "⚡ All Rounder",
                    callback_data="role_allrounder"
                )
            ]
        ]
    )

    await message.reply_photo(
        photo=profile_photo,
        caption=text,
        reply_markup=buttons
    )

# =========================================================
# JOINED BUTTON CHECK
# =========================================================

@app.on_callback_query(filters.regex("joined"))
async def joined(client, query):

    user = query.from_user
    user_id = str(user.id)

    try:

        channel = await app.get_chat_member(
            CHANNEL_USERNAME,
            user.id
        )

        chat = await app.get_chat_member(
            CHAT_USERNAME,
            user.id
        )

        if (
            str(channel.status) in ["left", "kicked"]
            or
            str(chat.status) in ["left", "kicked"]
        ):

            raise Exception

    except:

        await query.answer(
            "Please Join Channel & Chat First!",
            show_alert=True
        )

        return

    await query.message.delete()

    db = load_json(PLAYERS_DB)

    profile_photo = await get_profile_photo(user)

    # =====================================
    # ALREADY REGISTERED
    # =====================================

    if user_id in db:

        role = db[user_id]["role"]

        text = f"""
<b>🏏 WELCOME BACK TO {BOT_NAME}</b>

<b>✅ You Are Already Registered</b>

<b>👤 Name:</b> {user.first_name}
<b>🏏 Role:</b> {role.upper()}

<b>🔥 Ready For Upcoming Leagues.</b>

<b>Use /register to Register in The Tour</b>
"""

        await query.message.reply_photo(
            photo=profile_photo,
            caption=text
        )

        return

    # =====================================
    # NEW USER
    # =====================================

    text = f"""
<b>🏏 WELCOME TO {BOT_NAME}</b>

<b>🔥 Official Premium League Registration Bot</b>

<b>📌 Select Your Role Below</b>

<b>🏏 Batsman</b>
<b>🎯 Bowler</b>
<b>⚡ All Rounder</b>
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🏏 Batsman",
                    callback_data="role_batsman"
                )
            ],
            [
                InlineKeyboardButton(
                    "🎯 Bowler",
                    callback_data="role_bowler"
                )
            ],
            [
                InlineKeyboardButton(
                    "⚡ All Rounder",
                    callback_data="role_allrounder"
                )
            ]
        ]
    )

    await query.message.reply_photo(
        photo=profile_photo,
        caption=text,
        reply_markup=buttons
    )

# =========================================================
# ROLE SELECT
# =========================================================

@app.on_callback_query(filters.regex("role_"))
async def role_select(client, query):

    user = query.from_user
    user_id = str(user.id)

    db = load_json(PLAYERS_DB)

    if user_id in db:

        await query.answer(
            "Already Registered!",
            show_alert=True
        )

        return

    role = query.data.replace("role_", "")

    db[user_id] = default_player(role)

    save_json(PLAYERS_DB, db)

    text = f"""
<b>🏆 REGISTRATION SUCCESSFUL</b>

<b>👤 Name:</b> {user.first_name}
<b>🆔 ID:</b> {user.id}

<b>🏏 Role:</b> {role.upper()}

<b>🔥 Welcome To Official Premium League.</b>
"""

    await query.message.edit_caption(
        caption=text,
        reply_markup=None
    )

# =========================================================
# OPEN LEAGUE
# =========================================================

@app.on_message(filters.command("open"))
async def open_league(client, message):

    if message.from_user.id not in ADMINS:
        return

    try:

        args = message.text.split()

        league_name = args[1]
        time = args[2]

    except:

        await message.reply_text(
            "<b>❌ Usage:\n/open IPL_LEAGUE 10D</b>"
        )

        return

    league_db = load_json(LEAGUE_DB)

    league_db["active"] = {
        "league": league_name,
        "time": time,
        "players": [],
        "extra_players": [],
        "extra": False
    }

    save_json(LEAGUE_DB, league_db)

    await message.reply_text(
        f"""
<b>🏆 {league_name} REGISTRATION OPENED</b>

<b>⏰ Time:</b> {time}

<b>🔥 Players Can Now Register Using /register</b>
"""
    )

# =========================================================
# REMOVE PLAYER
# =========================================================

@app.on_message(filters.command("remove"))
async def remove_player(client, message):

    if message.from_user.id not in ADMINS:
        return

    try:

        args = message.text.split()

        remove_id = int(args[1])

    except:

        await message.reply_text(
            "<b>❌ Usage:\n/remove USER_ID</b>"
        )

        return

    league_db = load_json(LEAGUE_DB)

    if "active" not in league_db:

        await message.reply_text(
            "<b>❌ No Active League</b>"
        )

        return

    active = league_db["active"]

    removed = False

    for player in active["players"]:

        if player["id"] == remove_id:

            active["players"].remove(player)

            removed = True

            break

    for player in active["extra_players"]:

        if player["id"] == remove_id:

            active["extra_players"].remove(player)

            removed = True

            break

    save_json(LEAGUE_DB, league_db)

    if removed:

        await message.reply_text(
            f"<b>✅ Player Removed Successfully\n🆔 {remove_id}</b>"
        )

    else:

        await message.reply_text(
            "<b>❌ Player Not Found</b>"
        )

# =========================================================
# EXTRA REGISTRATION
# =========================================================

@app.on_message(filters.command("extra"))
async def extra_league(client, message):

    if message.from_user.id not in ADMINS:
        return

    league_db = load_json(LEAGUE_DB)

    if "active" not in league_db:

        await message.reply_text(
            "<b>❌ No Active League</b>"
        )

        return

    try:

        args = message.text.split()

        extra_time = args[2]

    except:

        await message.reply_text(
            "<b>❌ Usage:\n/extra IPL 1D</b>"
        )

        return

    league_db["active"]["extra"] = True
    league_db["active"]["extra_time"] = extra_time

    save_json(LEAGUE_DB, league_db)

    await message.reply_text(
        f"""
<b>🔥 EXTRA REGISTRATION OPENED</b>

<b>⏰ Extra Time:</b> {extra_time}
"""
    )

# =========================================================
# CLEAR LEAGUE
# =========================================================

@app.on_message(filters.command("clear"))
async def clear_league(client, message):

    if message.from_user.id not in ADMINS:
        return

    save_json(LEAGUE_DB, {})

    await message.reply_text(
        "<b>🗑 League Cleared Successfully</b>"
    )

# =========================================================
# REGISTER FOR LEAGUE
# =========================================================

@app.on_message(filters.command("register"))
async def register(client, message):

    user = message.from_user
    user_id = str(user.id)

    players_db = load_json(PLAYERS_DB)
    league_db = load_json(LEAGUE_DB)

    if user_id not in players_db:

        await message.reply_text(
            "<b>❌ First Start The Bot & Select Your Role</b>"
        )

        return

    if "active" not in league_db:

        await message.reply_text(
            "<b>❌ No Active League Right Now</b>"
        )

        return

    active = league_db["active"]

    all_ids = []

    for p in active["players"]:
        all_ids.append(p["id"])

    for p in active["extra_players"]:
        all_ids.append(p["id"])

    if user.id in all_ids:

        await message.reply_text(
            "<b>⚠️ You Already Registered In This League</b>"
        )

        return

    role = players_db[user_id]["role"]

    now = datetime.now().strftime("%d-%m-%Y %H:%M")

    player_data = {
        "name": user.first_name,
        "id": user.id,
        "username": user.username,
        "role": role,
        "time": now
    }

    if active.get("extra"):

        active["extra_players"].append(player_data)

    else:

        active["players"].append(player_data)

    save_json(LEAGUE_DB, league_db)

    profile_photo = await get_profile_photo(user)

    text = f"""
<b>🏆 {active['league']} REGISTRATION</b>

<b>✅ Successfully Registered</b>

<b>👤 Name:</b> {user.first_name}
<b>🆔 ID:</b> {user.id}

<b>🏏 Role:</b> {role.upper()}

<b>⏰ Time:</b> {now}

<b>🔥 Welcome To Official League.</b>
"""

    await message.reply_photo(
        photo=profile_photo,
        caption=text
    )

    log_text = f"""
<b>🏆 NEW REGISTRATION</b>

<b>👤 Name:</b> {user.first_name}
<b>🆔 ID:</b> {user.id}

<b>🏏 Role:</b> {role.upper()}

<b>⏰ Time:</b> {now}

<b>🏆 League:</b> {active['league']}</b>
"""

    try:

        await app.send_message(
            LOG_CHANNEL,
            log_text
        )

    except Exception as e:

        print(f"LOG ERROR: {e}")

# =========================================================
# PLAYER LIST
# =========================================================

@app.on_message(filters.command("list"))
async def list_players(client, message):

    league_db = load_json(LEAGUE_DB)

    if "active" not in league_db:

        await message.reply_text(
            "<b>❌ No Active League</b>"
        )

        return

    active = league_db["active"]

    players = active["players"]
    extra_players = active["extra_players"]

    text = f"<b>🏆 {active['league']} PLAYER LIST</b>\n"

    count = 1
    list_number = 1

    for player in players:

        if count == 1:

            text += f"\n\n<b>📋 LIST {list_number}</b>\n"

        if player.get("username"):

            name = f"<a href='https://t.me/{player['username']}'>{player['name']}</a>"

        else:

            name = f"<a href='tg://user?id={player['id']}'>{player['name']}</a>"

        text += (
            f"\n<b>{count}. "
            f"{name} "
            f"({player['role'].upper()})</b>"
        )

        if count == 15:

            count = 0
            list_number += 1

        count += 1

    if extra_players:

        text += "\n\n<b>🔥 EXTRA PLAYERS</b>\n"

        extra_count = 1

        for player in extra_players:

            if player.get("username"):

                name = f"<a href='https://t.me/{player['username']}'>{player['name']}</a>"

            else:

                name = f"<a href='tg://user?id={player['id']}'>{player['name']}</a>"

            text += (
                f"\n<b>{extra_count}. "
                f"{name} "
                f"({player['role'].upper()})</b>"
            )

            extra_count += 1

    await message.reply_text(
        text,
        disable_web_page_preview=True
    )

# =========================================================
# RUN BOT
# =========================================================

print("🏏 Premium League Bot Started Successfully")

app.run()