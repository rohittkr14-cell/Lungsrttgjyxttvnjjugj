# =========================================================
#            PCZ TOUR TRIAL MATCH BOT
# =========================================================
# INSTALL:
# pip install pyrogram tgcrypto

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

import json
import os

# =========================================================
# CONFIG
# =========================================================

API_ID = 37893084
API_HASH = "853a6c0f3be11009f667bc153244452e"
BOT_TOKEN = "8689193308:AAHUMVD5b43VPMbUqOq_w9vyPfJHM1cRIXk"

ADMIN_ID = 7691071175

FORCE_CHANNEL = "https://t.me/PCZ_registration_2"
PLAYGROUND_LINK = "https://t.me/+f7d7XEGMHAowNGE1"

# =========================================================
# BOT START
# =========================================================

app = Client(
    "pcz_trial_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =========================================================
# DATABASE
# =========================================================

DB_FILE = "playerszss.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({
            "Paltans": [],
            "Tigers": []
        }, f)


def load_data():
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# =========================================================
# FUNCTIONS
# =========================================================

def user_in_any_team(user_id):
    data = load_data()

    for team in data:
        for player in data[team]:
            if player["id"] == user_id:
                return True

    return False


def remove_user_everywhere(user_id):
    data = load_data()

    for team in data:
        data[team] = [
            p for p in data[team]
            if p["id"] != user_id
        ]

    save_data(data)


def get_profile_link(user):
    if user.username:
        return f"https://t.me/{user.username}"
    else:
        return f"tg://user?id={user.id}"


# =========================================================
# START COMMAND
# =========================================================

@app.on_message(filters.command("start"))
async def start(client, message):

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📢 Join Channel",
                url=FORCE_CHANNEL
            )
        ],
        [
            InlineKeyboardButton(
                "🏏 Join Playground",
                url=PLAYGROUND_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Joined",
                callback_data="joined"
            )
        ]
    ])

    txt = """
🏏 <b>WELCOME TO PCZ TOUR TRIAL MATCH</b>

<b>Before continuing please complete all steps below 👇</b>

<b>1. Join Official Channel</b>
<b>2. Join Playground Group</b>
<b>3. Click Joined Button</b>

<b>After that registration panel will open ✅</b>
"""

    await message.reply_text(
        txt,
        reply_markup=buttons
    )


# =========================================================
# JOINED BUTTON
# =========================================================

@app.on_callback_query(filters.regex("joined"))
async def joined_callback(client, callback):

    user = callback.from_user

    try:
        photo = await client.download_media(
            user.photo.big_file_id
        )

        caption = f"""
🏏 <b>PCZ TOUR TRIAL MATCH</b>

🔥 <b>PALTANS VS TIGERS</b>

━━━━━━━━━━━━━━━

<b>⚠️ ONLY SERIOUS PLAYERS REGISTER

📅 Match Date:
23-05-2025

⏰ Time:
1:00 PM

❌ Jo players online nahi rahenge wo register mat kare.

🏏 Match Format:
15 Overs Match

👥 Team Slots:
11 Players Per Team

📌 Instructions:

• Ek user sirf ek team join kar sakta hai.
• Match time par online rehna compulsory hai.
• Team full hone ke baad registration close ho jayega.
• Agar join karne ke baad leave karna ho to Leave Match button use kare.</b>

━━━━━━━━━━━━━━━

👇 Select Your Team
"""

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔥 Join Paltans",
                    callback_data="join_paltans"
                )
            ],
            [
                InlineKeyboardButton(
                    "🐯 Join Tigers",
                    callback_data="join_tigers"
                )
            ],
            [
                InlineKeyboardButton(
                    "❌ Leave Match",
                    callback_data="leave_match"
                )
            ],
            [
                InlineKeyboardButton(
                    "🚫 Cancel",
                    callback_data="cancel_match"
                )
            ]
        ])

        await callback.message.delete()

        await callback.message.reply_photo(
            photo=photo,
            caption=caption,
            reply_markup=buttons
        )

    except:

        caption = f"""
🏏 <b>PCZ TOUR TRIAL MATCH</b>

🔥 <b>PALTANS VS TIGERS</b>

━━━━━━━━━━━━━━━

<b>⚠️ ONLY SERIOUS PLAYERS REGISTER

📅 Match Date:
23-05-2025

⏰ Time:
1:00 PM

❌ Jo players online nahi rahenge wo register mat kare.

🏏 Match Format:
15 Overs Match

👥 Team Slots:
11 Players Per Team

📌 Instructions:

• Ek user sirf ek team join kar sakta hai.
• Match time par online rehna compulsory hai.
• Team full hone ke baad registration close ho jayega.
• Agar join karne ke baad leave karna ho to Leave Match button use kare.</b>

━━━━━━━━━━━━━━━

👇 Select Your Team
"""

        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔥 Join Paltans",
                    callback_data="join_paltans"
                )
            ],
            [
                InlineKeyboardButton(
                    "🐯 Join Tigers",
                    callback_data="join_tigers"
                )
            ],
            [
                InlineKeyboardButton(
                    "❌ Leave Match",
                    callback_data="leave_match"
                )
            ],
            [
                InlineKeyboardButton(
                    "🚫 Cancel",
                    callback_data="cancel_match"
                )
            ]
        ])

        await callback.message.delete()

        await callback.message.reply_text(
            caption,
            reply_markup=buttons
        )


# =========================================================
# JOIN PALTANS
# =========================================================

@app.on_callback_query(filters.regex("join_paltans"))
async def join_paltans(client, callback):

    user = callback.from_user
    data = load_data()

    if user_in_any_team(user.id):
        return await callback.answer(
            "❌ You already joined a team.",
            show_alert=True
        )

    if len(data["Paltans"]) >= 11:
        return await callback.answer(
            "❌ Paltans Team Full",
            show_alert=True
        )

    data["Paltans"].append({
        "id": user.id,
        "name": user.first_name
    })

    save_data(data)

    await callback.answer(
        "✅ Joined Paltans Successfully",
        show_alert=True
    )

    await callback.message.reply_text(
        f"""
<b>✅ Successfully Joined Paltans

⏰ Match Time:
1:00 PM

📅 Date:
23-05-2025

⚠️ Time par online aa jana.</b>
"""
    )


# =========================================================
# JOIN TIGERS
# =========================================================

@app.on_callback_query(filters.regex("join_tigers"))
async def join_tigers(client, callback):

    user = callback.from_user
    data = load_data()

    if user_in_any_team(user.id):
        return await callback.answer(
            "❌ You already joined a team.",
            show_alert=True
        )

    if len(data["Tigers"]) >= 11:
        return await callback.answer(
            "❌ Tigers Team Full",
            show_alert=True
        )

    data["Tigers"].append({
        "id": user.id,
        "name": user.first_name
    })

    save_data(data)

    await callback.answer(
        "✅ Joined Tigers Successfully",
        show_alert=True
    )

    await callback.message.reply_text(
        f"""
<b>✅ Successfully Joined Tigers

⏰ Match Time:
1:00 PM

📅 Date:
23-05-2025

⚠️ Time par online aa jana.</b>
"""
    )


# =========================================================
# LEAVE MATCH
# =========================================================

@app.on_callback_query(filters.regex("leave_match"))
async def leave_match(client, callback):

    user = callback.from_user

    if not user_in_any_team(user.id):
        return await callback.answer(
            "❌ You are not in any team.",
            show_alert=True
        )

    remove_user_everywhere(user.id)

    await callback.answer(
        "✅ Left Match Successfully",
        show_alert=True
    )


# =========================================================
# CANCEL
# =========================================================

@app.on_callback_query(filters.regex("cancel_match"))
async def cancel_match(client, callback):

    await callback.message.delete()


# =========================================================
# ADMIN LIST
# =========================================================

@app.on_message(filters.command("list"))
async def list_players(client, message):

    if message.from_user.id != ADMIN_ID:
        return

    data = load_data()

    text = "🏏 <b>PCZ TOUR MATCH LIST</b>\n\n"

    text += f"🔥 <b>PALTANS ({len(data['Paltans'])}/11)</b>\n\n"

    if data["Paltans"]:
        for x, player in enumerate(data["Paltans"], start=1):
            text += f"{x}. <a href='tg://user?id={player['id']}'>{player['name']}</a>\n"
    else:
        text += "No Players\n"

    text += "\n━━━━━━━━━━━━━━━\n\n"

    text += f"🐯 <b>TIGERS ({len(data['Tigers'])}/11)</b>\n\n"

    if data["Tigers"]:
        for x, player in enumerate(data["Tigers"], start=1):
            text += f"{x}. <a href='tg://user?id={player['id']}'>{player['name']}</a>\n"
    else:
        text += "No Players\n"

    await message.reply_text(
        text,
        disable_web_page_preview=True
    )


# =========================================================
# ADMIN ADD
# =========================================================

@app.on_message(filters.command("add"))
async def add_player(client, message):

    if message.from_user.id != ADMIN_ID:
        return

    try:
        args = message.text.split()

        user_id = int(args[1])
        team = args[2]

        data = load_data()

        if team not in ["Paltans", "Tigers"]:
            return await message.reply_text(
                "Use: /add user_id Paltans"
            )

        if len(data[team]) >= 11:
            return await message.reply_text(
                "❌ Team Full"
            )

        data[team].append({
            "id": user_id,
            "name": f"User {user_id}"
        })

        save_data(data)

        await message.reply_text(
            f"✅ Added {user_id} in {team}"
        )

    except:
        await message.reply_text(
            "Use:\n/add user_id Paltans"
        )


# =========================================================
# ADMIN REMOVE
# =========================================================

@app.on_message(filters.command("remove"))
async def remove_player(client, message):

    if message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(message.text.split()[1])

        remove_user_everywhere(user_id)

        await message.reply_text(
            "✅ User Removed"
        )

    except:
        await message.reply_text(
            "Use:\n/remove user_id"
        )


# =========================================================
# RUN BOT
# =========================================================

print("🏏 PCZ TOUR TRIAL MATCH BOT STARTED")

app.run()