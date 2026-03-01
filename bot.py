from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import json, os
import time
from datetime import datetime, timedelta
from config import BOT_TOKEN
from telegram.ext import Updater
from admin import register_admin_commands
from user import register_user_commands
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from pytz import timezone
import json, os
import json
from datetime import datetime


USERS_PATH = "Data/Users.json"

def loads_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def saves_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
        
def load_jsons(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_jsons(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

PLAN_FILE = "Data/plan.json"

def log_command(update: Update, command_name: str):
    user = update.effective_user
    username = f"@{user.username}" if user.username else "NoUsername"
    logging.info(f"Command: /{command_name} | From: {username} ({user.id})")

def remove_expired_plans():
    try:
        plans = load_jsons("Data/plan.json")
        now = datetime.now(timezone("Asia/Kolkata"))
        changed = False

        for user_id, info in list(plans.items()):
            try:
                expiry_time = datetime.strptime(info["expiry"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone("Asia/Kolkata"))
                if expiry_time <= now:
                    print(f"[🔴] Plan expired for user {user_id}, removing...")
                    del plans[user_id]
                    changed = True
            except Exception as e:
                print(f"[❌] Error parsing expiry for {user_id}: {e}")

        if changed:
            save_jsons("Data/plan.json", plans)
            print("[✅] Expired plans removed.")
    except Exception as e:
        print(f"[❌] Plan auto-removal error: {e}")
        
# Start scheduler with timezone
scheduler = BackgroundScheduler(timezone=timezone("Asia/Kolkata"))
scheduler.add_job(remove_expired_plans, "interval", minutes=1)
scheduler.start()
print("✅ Auto-removal scheduler started.")


def load_json(path):
    import json
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return json.load(f)

USER_FILE = 'Data/Users.json'
os.makedirs("Data", exist_ok=True)
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as f:
        json.dump({}, f)


def is_registered(user_id):
    try:
        with open(USER_FILE) as f:
            data = json.load(f)
        return str(user_id) in data
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def register_user(user_id, name, username=None):
    with open(USER_FILE) as f:
        data = json.load(f)
    data[str(user_id)] = {
        "name": name,
        "username": username,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    with open(USER_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    name = user.first_name

    msg = (
        "✦ 𝑹𝑨𝑽𝑬𝑵 x 𝑪𝑯𝑬𝑪𝑲𝑬𝑹 ✦\n\n"
        f"⟡ 𝑵𝑨𝑴𝑬     ↯ {name}\n"
        f"⟡ 𝑺𝑻𝑨𝑻𝑼𝑺   ↯ 𝑵𝑬𝑾\n"
        f"⟡ 𝑪𝑶𝑴𝑴𝑨𝑵𝑫 ↯ /register\n\n"
        "━━━━━━━━━━━━━━━━━━"
    )

    buttons = [
        [InlineKeyboardButton("⟡ 𝑹𝑬𝑮𝑰𝑺𝑻𝑬𝑹 ⟡ ", callback_data="register")],
        [InlineKeyboardButton("⟡ 𝑴𝑨𝑰𝑵 𝑴𝑬𝑵𝑼 ⟡ ", callback_data="mainmenu")]
    ]

    update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(buttons))


def register(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = user.id
    name = user.first_name
    username = user.username or None

    if is_registered(user_id):
        msg = (
            "✦ 𝑹𝑬𝑮𝑰𝑺𝑻𝑬𝑹𝑬𝑫 ✦\n\n"
            f"⟡ 𝑵𝑨𝑴𝑬 ↯ {name}\n"
            f"⟡ 𝑺𝑻𝑨𝑻𝑼𝑺 ↯ 𝑨𝑳𝑹𝑬𝑨𝑫𝒀 𝑹𝑬𝑮𝑰𝑺𝑻𝑬𝑹𝑬𝑫\n"
            f"⟡ 𝑨𝑪𝑪𝑬𝑺𝑺   ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 𝑼𝑺𝑬𝑹\n"
            f"━━━━━━━━━━━━━━━━━━━"
        )
    else:
        register_user(user_id, name, username)
        msg = (
            "✦ 𝑹𝑬𝑮𝑰𝑺𝑻𝑬𝑹𝑬𝑫 𝑺𝑼𝑪𝑪𝑬𝑺𝑺 ✦\n\n"
            f"⟡ 𝑵𝑨𝑴𝑬 ↯ {name}\n"
            f"⟡ 𝑼𝑺𝑬𝑹𝑵𝑨𝑴𝑬 ↯ @{username if username else 'N/A'}\n"
            f"⟡ 𝑺𝑻𝑨𝑻𝑼𝑺 ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 𝑼𝑺𝑬𝑹\n"
            f"⟡ 𝑨𝑪𝑪𝑬𝑺𝑺   ↯ 𝑨𝑪𝑪𝑬𝑺𝑺 𝑮𝑹𝑨𝑵𝑻𝑬𝑫\n"
            f"━━━━━━━━━━━━━━━━━━━"
        )

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    
def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    user = query.from_user
    chat_id = query.message.chat.id
    user_id = str(user.id)
    name = user.first_name

    if data == "register":
        if is_registered(user_id):
            msg = (
                "✦ 𝑹𝑬𝑮𝑰𝑺𝑻𝑹𝑨𝑻𝑰𝑶𝑵 𝑭𝑨𝑰𝑳𝑬𝑫 ✦\n\n"
                f"⟡ 𝑵𝑨𝑴𝑬     ↯ {name}\n"
                f"⟡ 𝑺𝑻𝑨𝑻𝑼𝑺   ↯ 𝑨𝑳𝑹𝑬𝑨𝑫𝒀 𝑹𝑬𝑮𝑰𝑺𝑻𝑬𝑹𝑬𝑫\n"
                f"⟡ 𝑨𝑪𝑪𝑬𝑺𝑺   ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 𝑼𝑺𝑬𝑹\n\n"
                "━━━━━━━━━━━━━━━━━━━"
            )
        else:
            register_user(user_id, name)
            msg = (
                "✦ 𝑹𝑬𝑮𝑰𝑺𝑻𝑹𝑨𝑻𝑰𝑶𝑵 𝑺𝑼𝑪𝑪𝑬𝑺𝑺 ✦\n\n"
                f"⟡ 𝑵𝑨𝑴𝑬     ↯ {name}\n"
                f"⟡ 𝑺𝑻𝑨𝑻𝑼𝑺   ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 𝑼𝑺𝑬𝑹\n"
                f"⟡ 𝑨𝑪𝑪𝑬𝑺𝑺   ↯ 𝑨𝑪𝑪𝑬𝑺𝑺 𝑮𝑹𝑨𝑵𝑻𝑬𝑫\n\n"
                "━━━━━━━━━━━━━━━━━━━"
            )
        context.bot.send_message(chat_id=chat_id, text=msg)

    elif data == "mainmenu" or data == "backtomenu":
        if not is_registered(user_id):
            msg = (
                "✦ 𝗔𝗖𝗖𝗘𝗦𝗦 𝗗𝗘𝗡𝗜𝗘𝗗 ✦\n\n"
                f"⟡ 𝗡𝗔𝗠𝗘     ↯ {name}\n"
                f"⟡ 𝗦𝗧𝗔𝗧𝗨𝗦   ↯ 𝗨𝗡𝗥𝗘𝗚𝗜𝗦𝗧𝗘𝗥𝗘𝗗\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            )
            context.bot.send_message(chat_id=chat_id, text=msg)
        else:
            msg = (
                "✦ 𝑴𝑨𝑰𝑵 𝑴𝑬𝑵𝑼 ✦\n\n"
                f"⟡ 𝑾𝑬𝑳𝑪𝑶𝑴𝑬 ↯ {name}\n"
                f"⟡ 𝑺𝑻𝑨𝑻𝑼𝑺   ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 𝑼𝑺𝑬𝑹\n"
                f"⟡ 𝑨𝑪𝑪𝑬𝑺𝑺   ↯ 𝑫𝑨𝑺𝑯𝑩𝑶𝑨𝑹𝑫\n"
                f"⟡ 𝑴𝑶𝑫𝑬      ↯ 𝑳𝑰𝑽𝑬\n\n"
                "✧ 𝑪𝑯𝑶𝑶𝑺𝑬 𝑨𝑵 𝑶𝑷𝑻𝑰𝑶𝑵 𝑩𝑬𝑳𝑶𝑾\n\n"
                "━━━━━━━━━━━━━━━━━━"
            )
            buttons = [
                [InlineKeyboardButton("⟡ 𝑮𝑨𝑻𝑬𝑺 ⟡", callback_data="gates"),InlineKeyboardButton("⟡ 𝑷𝑹𝑰𝑪𝑬 𝑳𝑰𝑺𝑻 ⟡", callback_data="price")],
                [InlineKeyboardButton("⟡ 𝑺𝑼𝑷𝑷𝑶𝑹𝑻 ⟡", callback_data="support"),InlineKeyboardButton("⟡ 𝑷𝑹𝑶𝑭𝑰𝑳𝑬 ⟡", callback_data="profile")],
                [InlineKeyboardButton("⟡ 𝑼𝑷𝑫𝑨𝑻𝑬 𝑪𝑯𝑨𝑵𝑵𝑬𝑳 ⟡", url="https://t.me/+hfH9yadfjSYxZTdl")]
            ]
            query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "profile":
        username = f"@{user.username}" if user.username else "N/A"

        try:
            with open("data/Users.json", "r") as f:
                users = json.load(f)
            reg_date = users.get(user_id, {}).get("date", "N/A")
        except:
            reg_date = "N/A"

        try:
            with open("Data/plan.json", "r") as f:
                plans = json.load(f)
            plan_info = plans.get(user_id)
            plan = "PREMIUM" if plan_info else "FREE"
        except:
            plan = "FREE"

        msg = (
            f"✦ 𝑼𝑺𝑬𝑹 𝑰𝑵𝑭𝑶 ✦ \n\n"
            f"✦ 𝑵𝑨𝑴𝑬        ↯ {name}\n"
            f"✦ 𝑼𝑺𝑬𝑹         ↯ {username}\n"
            f"✦ 𝑼𝑺𝑬𝑹 𝑰𝑫     ↯ {user_id}\n"
            f"✦  𝑷𝑳𝑨𝑵        ↯ {plan}\n"                    "━━━━━━━━━━━━━━━━━━━━"
        )

        buttons = [[InlineKeyboardButton("⟡ 𝑩𝑨𝑪𝑲 ⟡", callback_data="backtomenu")]]
        query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))



    elif data == "gates":
        msg = (
            "✦ 𝑨𝑽𝑨𝑰𝑳𝑨𝑩𝑳𝑬 𝑮𝑨𝑻𝑬𝑺 ✦\n\n"
            "⟡ Choose a category below:\n\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        buttons = [
            [InlineKeyboardButton("⟡ 𝑨𝑼𝑻𝑯 ⟡", callback_data="authgates"), InlineKeyboardButton("⟡ 𝑪𝑯𝑨𝑹𝑮𝑬 ⟡", callback_data="chargegates")],
            [InlineKeyboardButton("⟡ 𝑻𝑶𝑶𝑳𝑺 ⟡", callback_data="tools"), InlineKeyboardButton("⟡ 𝑨𝑼𝑻𝑶 𝑺𝑯𝑶𝑷𝑰𝑭𝒀 ⟡", callback_data="shopify")],
            [InlineKeyboardButton("⟡ 𝑩𝑨𝑪𝑲 𝑻𝑶 𝑴𝑬𝑵𝑼 ⟡  ", callback_data="backtomenu")]
        ]
        query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "authgates":
        msg = (
            "✦ 𝑨𝑼𝑻𝑯 𝑮𝑨𝑻𝑬𝑺 ✦\n\n"
            "⟡ 𝑨𝑽𝑨𝑰𝑳𝑨𝑩𝑳𝑬 𝑪𝑶𝑴𝑴𝑨𝑵𝑫\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "[↯] /𝒄𝒉𝒌 ↯ 𝑺𝑻𝑹𝑰𝑷𝑬 𝑨𝑼𝑻𝑯 \n" 
            "[↯] 𝑺𝑻𝑨𝑻𝑼𝑺 ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 ✅\n"
            "[↯] 𝑷𝑳𝑨𝑵 ↯ 𝑭𝑹𝑬𝑬\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "[↯] /𝒃𝟑 ↯ 𝑩𝑹𝑨𝑰𝑵𝑻𝑹𝑬𝑬 𝑨𝑼𝑻𝑯\n"  
            "[↯] 𝑺𝑻𝑨𝑻𝑼𝑺 ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 ✅\n"
            "[↯] 𝑷𝑳𝑨𝑵 ↯ 𝑷𝑹𝑬𝑴𝑰𝑼𝑴\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
        )
        buttons = [
            [InlineKeyboardButton("⟡ 𝑩𝑨𝑪𝑲 ⟡  ", callback_data="gates")]
        ]
        query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "chargegates":
        msg = (
            "✦ 𝑪𝑯𝑨𝑹𝑮𝑬 𝑮𝑨𝑻𝑬𝑺 ✦\n\n"
            "⟡ 𝑨𝑽𝑨𝑰𝑳𝑨𝑩𝑳𝑬 𝑪𝑶𝑴𝑴𝑨𝑵𝑫\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "[↯] /𝒑𝒑 ↯ 𝑷𝑨𝒀𝑷𝑨𝑳 𝑫𝑰𝑹𝑬𝑪𝑻 𝑪𝑯𝑨𝑹𝑮𝑬 \n"
            "[↯] 𝑺𝑻𝑨𝑻𝑼𝑺 ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 ✅\n"
            "[↯] 𝑮𝑨𝑻𝑬 ↯ 𝑷𝑨𝒀𝑷𝑨𝑳 𝑫𝑰𝑹𝑬𝑪𝑻 \n"
            "[↯] 𝑨𝑴𝑶𝑼𝑵𝑻 ↯ 0.01$  \n"
            "[↯] 𝑷𝑳𝑨𝑵 ↯ 𝑷𝑹𝑬𝑴𝑰𝑼𝑴\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"              "[↯] /𝒎𝒑𝒑 ↯ 𝑴𝑨𝑺𝑺 𝑷𝑨𝒀𝑷𝑨𝑳 𝑫𝑰𝑹𝑬𝑪𝑻 𝑪𝑯𝑨𝑹𝑮𝑬  \n"
            "[↯] 𝑺𝑻𝑨𝑻𝑼𝑺 ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 ✅\n"
            "[↯] 𝑮𝑨𝑻𝑬 ↯ 𝑷𝑨𝒀𝑷𝑨𝑳 𝑫𝑰𝑹𝑬𝑪𝑻  \n"
            "[↯] 𝑨𝑴𝑶𝑼𝑵𝑻 ↯ 0.01$  \n"
            "[↯] 𝑷𝑳𝑨𝑵 ↯ 𝑷𝑹𝑬𝑴𝑰𝑼𝑴\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "[↯] /𝒔𝒇 ↯ 𝑺𝑯𝑶𝑷𝑰𝑭𝒀 𝑪𝑯𝑨𝑹𝑮𝑬\n"
            "[↯] 𝑺𝑻𝑨𝑻𝑼𝑺 ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 ✅\n"
            "[↯] 𝑮𝑨𝑻𝑬: 𝑺𝑻𝑹𝑰𝑷𝑬\n"
            "[↯] 𝑨𝑴𝑶𝑼𝑵𝑻: 3.49$  \n"
            "[↯] 𝑷𝑳𝑨𝑵 ↯ 𝑷𝑹𝑬𝑴𝑰𝑼𝑴\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "[↯] /𝒔𝒉𝒐  ↯ 𝑺𝑯𝑶𝑷𝑰𝑭𝒀 𝑪𝑯𝑨𝑹𝑮𝑬  \n"
            "[↯] 𝑺𝑻𝑨𝑻𝑼𝑺 ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 ✅\n"
            "[↯] 𝑮𝑨𝑻𝑬: 𝑨𝑼𝑻𝑯𝑵𝑬𝑻  \n"
            "[↯] 𝑨𝑴𝑶𝑼𝑵𝑻: 5.0$  \n"
            "[↯] 𝑷𝑳𝑨𝑵 ↯ 𝑷𝑹𝑬𝑴𝑰𝑼𝑴\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
        )
        buttons = [
            [InlineKeyboardButton("⟡ 𝑩𝑨𝑪𝑲 ⟡  ", callback_data="gates")]
        ]
        query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
        
    elif data == "tools":
        msg = (
            "✦ 𝑻𝑶𝑶𝑳𝑺 ✦\n\n"
            "⟡ 𝑨𝑽𝑨𝑰𝑳𝑨𝑩𝑳𝑬 𝑪𝑶𝑴𝑴𝑨𝑵𝑫\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "[↯] /gen ↯ 𝑮𝑬𝑵 𝑪𝑪 \n" 
            "[↯] 𝑺𝑻𝑨𝑻𝑼𝑺 ↯ 𝑰𝑵𝑨𝑪𝑻𝑰𝑽𝑬 ❌\n"
            "[↯] 𝑷𝑳𝑨𝑵 ↯ 𝑭𝑹𝑬𝑬\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "[↯] /sk ↯ 𝑺𝑲 𝑲𝑬𝒀 𝑪𝑯𝑬𝑪𝑲\n"  
            "[↯] 𝑺𝑻𝑨𝑻𝑼𝑺 ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 ✅\n"
            "[↯] 𝑷𝑳𝑨𝑵 ↯ 𝑭𝑹𝑬𝑬\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "[↯] /𝒗𝒃𝒗 ↯ 3DS 𝑳𝑶𝑶𝑲𝑼𝑷 / 𝑽𝑩𝑽 𝑳𝑶𝑶𝑲𝑼𝑷   \n" 
            "[↯] 𝑺𝑻𝑨𝑻𝑼𝑺 ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 ✅\n"
            "[↯] 𝑷𝑳𝑨𝑵 ↯ 𝑭𝑹𝑬𝑬\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
        )
        buttons = [
            [InlineKeyboardButton("⟡ 𝑩𝑨𝑪𝑲 ⟡  ", callback_data="gates")]
        ]
        query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
        
    elif data == "price":
        msg = (
            "✦ 𝑷𝑹𝑬𝑴𝑰𝑼𝑴 𝑷𝑳𝑨𝑵 ✦\n\n"
            "⟡ 20$ 𝑭𝑶𝑹 5 𝑫𝑨𝒀𝑺\n"
            "⟡ 30$ 𝑭𝑶𝑹 15 𝑫𝑨𝒀𝑺\n"
            "⟡ 50$ 𝑭𝑶𝑹 30 𝑫𝑨𝒀𝑺\n\n"
            "✦ 𝑨𝑽𝑨𝑰𝑳𝑨𝑩𝑳𝑬 𝑷𝑨𝒀𝑴𝑬𝑵𝑻 𝑴𝑬𝑻𝑯𝑶𝑫 ✦ \n"
            "⟡ 𝑼𝑷𝑰\n"
            "⟡ 𝑪𝑹𝒀𝑷𝑻𝑶\n\n"
            "✦ 𝑪𝑶𝑵𝑻𝑨𝑪𝑻 𝑨𝑫𝑴𝑰𝑵 𝑭𝑶𝑹 𝑩𝑼𝒀 𝑷𝑳𝑨𝑵 ✦\n"
            "⟡ 𝑨𝑫𝑴𝑰𝑵 ↯ @Darkboy22\n\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        buttons = [
            [InlineKeyboardButton("⟡ 𝑩𝑼𝒀 𝑵𝑶𝑾 ⟡  ", url="https://t.me/Darkboy22")],
            [InlineKeyboardButton("⟡ 𝑩𝑨𝑪𝑲 ⟡  ", callback_data="backtomenu")]
        ]
        query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))

    elif data == "support":
        msg = (
            "✦ 𝑪𝑼𝑺𝑻𝑶𝑴𝑬𝑹 𝑺𝑼𝑷𝑷𝑶𝑹𝑻 ✦\n\n"
            "⟡ 𝑨𝑫𝑴𝑰𝑵 ↯ @Darkboy22\n"
            "⟡ 𝑨𝑽𝑨𝑰𝑳𝑨𝑩𝑳𝑬 ↯ 24/7 𝑺𝑼𝑷𝑷𝑶𝑹𝑻\n\n"
            "⟡ 𝑵𝑶𝑻𝑬 ↯ 𝑪𝑶𝑵𝑻𝑨𝑪𝑻 𝑾𝑰𝑻𝑯 𝒀𝑶𝑼𝑹 𝑷𝑹𝑶𝑩𝑳𝑬𝑴 — 𝑫𝑶𝑵'𝑻 𝑪𝑶𝑴𝑬 𝑭𝑶𝑹 𝑻𝑰𝑴𝑬 𝑷𝑨𝑺𝑺\n\n"
            "✧ 𝑪𝑳𝑰𝑪𝑲 𝑶𝑵 𝑻𝑯𝑬 𝑼𝑺𝑬𝑹𝑵𝑨𝑴𝑬 𝑻𝑶 𝑪𝑯𝑨𝑻 𝑫𝑰𝑹𝑬𝑪𝑻𝑳𝒀\n"
            "━━━━━━━━━━━━━━━━━━━"
        )
        buttons = [
            [InlineKeyboardButton("⟡ 𝑩𝑨𝑪𝑲 ⟡  ", callback_data="backtomenu")]
        ]
        query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
        

    
    elif data == "shopify":
        msg = (
            "✦ 𝑨𝑼𝑻𝑶 𝑺𝑯𝑶𝑷𝑰𝑭𝒀 ✦\n\n"
            "⟡ 𝑨𝑽𝑨𝑰𝑳𝑨𝑩𝑳𝑬 𝑪𝑶𝑴𝑴𝑨𝑵𝑫\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "[↯] /𝒂𝒅𝒅 ↯ 𝑺𝑯𝑶𝑷𝑰𝑭𝒀 𝑺𝑰𝑻𝑬 𝑨𝑫𝑫\n"
            "[↯] 𝑬𝑿𝑨𝑴𝑷𝑳𝑬  ↯ /𝒂𝒅𝒅 https://example.com\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "[↯] /𝒔𝒉 ↯ 𝑨𝑼𝑻𝑶 𝑺𝑯𝑶𝑷𝑰𝑭𝒀 𝑺𝑰𝑵𝑮𝑳𝑬 𝑪𝑯𝑬𝑪𝑲\n"
            "[↯] 𝑺𝑻𝑨𝑻𝑼𝑺 ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 ✅\n"
            "[↯] 𝑷𝑳𝑨𝑵 ↯ 𝑷𝑹𝑬𝑴𝑰𝑼𝑴\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "[↯] /𝒎𝒔𝒉 ↯ 𝑨𝑼𝑻𝑶 𝑺𝑯𝑶𝑷𝑰𝑭𝒀 𝑴𝑨𝑺𝑺 𝑪𝑯𝑬𝑪𝑲\n"
            "[↯] 𝑺𝑻𝑨𝑻𝑼𝑺 ↯ 𝑨𝑪𝑻𝑰𝑽𝑬 ✅\n"
            "[↯] 𝑷𝑳𝑨𝑵 ↯ 𝑷𝑹𝑬𝑴𝑰𝑼𝑴\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
        )
        buttons = [
            [InlineKeyboardButton("⟡ 𝑩𝑨𝑪𝑲 ⟡", callback_data="gates")]
        ]
        query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
        
def main():
    # Create Updater and Dispatcher
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CallbackQueryHandler(button_handler))
        # Register ALL command handlers
    register_admin_commands(dp)
    register_user_commands(dp)

    # Confirm bot is active
    print("✅ Bot is running...")

    
    updater.start_polling()
    updater.idle()
    


if __name__ == "__main__":
    main()
    
