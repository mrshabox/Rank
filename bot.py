from pyrogram import Client , filters
from pymongo import MongoClient
import os

API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URL = os.environ.get("MONGO_URL")



bot = Client(
    "Level" ,
    api_id = API_ID ,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)

async def is_admins(client: bot, chat_id: int):
    return [
        member.user.id
        async for member in bot.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]

levellink =["https://kimnhungtoeic.com/wp-content/uploads/2020/09/animation-birthdays070517-02.gif", "https://kimnhungtoeic.com/wp-content/uploads/2020/09/animation-birthdays070517-02.gif", "https://kimnhungtoeic.com/wp-content/uploads/2020/09/animation-birthdays070517-02.gif", "https://kimnhungtoeic.com/wp-content/uploads/2020/09/animation-birthdays070517-02.gif", "https://kimnhungtoeic.com/wp-content/uploads/2020/09/animation-birthdays070517-02.gif", "https://kimnhungtoeic.com/wp-content/uploads/2020/09/animation-birthdays070517-02.gif", "https://kimnhungtoeic.com/wp-content/uploads/2020/09/animation-birthdays070517-02.gif", "https://kimnhungtoeic.com/wp-content/uploads/2020/09/animation-birthdays070517-02.gif", "https://kimnhungtoeic.com/wp-content/uploads/2020/09/animation-birthdays070517-02.gif"]
levelname = ["20.000đ", "50.000đ", "80.000đ", "110.000đ", "170.000đ", "190.000đ", "230.000đ", "500.000đ", "phần thưởng lớn nhất 1.000.000đ"]
levelnum = [5,10,15,20,30,40,50,70, 100]



@bot.on_message(
    filters.command("level", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def levelsystem(_, message): 
    leveldb = MongoClient(MONGO_URL)
   
    toggle = leveldb["ToggleDb"]["Toggle"] 
    if message.from_user:
        user = message.from_user.id
        chat_id = "-1001756651556" 
        if user not in (
            await is_admins(chat_id)
        ):
            return await message.reply_text(
                "You are not admin"
            )
    is_level = toggle.find_one({"chat_id": message.chat.id})
    if not is_level:
        toggle.insert_one({"chat_id": message.chat.id})
        await message.reply_text("Đã bật cày cấp ảo nhận tiền thật")
    else:
        toggle.delete_one({"chat_id": message.chat.id})
        await message.reply_text("Đã tắt cày cấp ảo nhận tiền thật")


@bot.on_message(
    (filters.text
    )
    & ~filters.private,
    group=8,
)
async def level(client, message):
    chat = message.chat.id
    user_id = message.from_user.id    

    leveldb = MongoClient(MONGO_URL)
    
    level = leveldb["LevelDb"]["Level"] 
    toggle = leveldb["ToggleDb"]["Toggle"] 

    is_level = toggle.find_one({"chat_id": message.chat.id})
    if is_level:
        xpnum = level.find_one({"level": user_id, "chatid": chat})

        if not message.from_user.is_bot:
            if xpnum is None:
                newxp = {"level": user_id, "chatid": chat, "xp": 5}
                level.insert_one(newxp)   
                    
            else:
                xp = xpnum["xp"] + 5
                level.update_one({"level": user_id, "chatid": chat}, {
                    "$set": {"xp": xp}})
                l = 0
                while True:
                    if xp < ((50*(l**2))+(50*(l))):
                         break
                    l += 1
                xp -= ((50*((l-1)**2))+(50*(l-1)))
                if xp == 0:
                    await message.reply_text(f"🌟 **Thông báo:** {message.from_user.mention} đã lên cấp {l}**")
    
                    for lv in range(len(levelname)) and range(len(levellink)):
                            if l == levelnum[lv]:            
                                Link = f"{levellink[lv]}"
                                await message.reply_video(video=Link, caption=f"Chúc mừng bạn **{message.from_user.mention}** đã chạm mốc và lĩnh được **{levelname[lv]}**. Gửi tin nhắn đến @ShaboxBot để lĩnh quà nhé. 💝🎁")
                  

                               
@bot.on_message(
    filters.command("rank", prefixes=["/", ".", "?", "-"])
    & ~filters.private)
async def rank(client, message):
    chat = message.chat.id
    user_id = message.from_user.id    
    
    leveldb = MongoClient(MONGO_URL)
    
    level = leveldb["LevelDb"]["Level"] 
    toggle = leveldb["ToggleDb"]["Toggle"] 

    is_level = toggle.find_one({"chat_id": message.chat.id})
    if is_level:
        xpnum = level.find_one({"level": user_id, "chatid": chat})
        xp = xpnum["xp"]
        l = 0
        r = 0
        while True:
            if xp < ((50*(l**2))+(50*(l))):
                break
            l += 1

        xp -= ((50*((l-1)**2))+(50*(l-1)))
        rank = level.find().sort("xp", -1)
        for k in rank:
            r += 1
            if xpnum["level"] == k["level"]:
                break                     
        await message.reply_text(f"{message.from_user.mention}:\n**Level:** {l}\n**EXP:** {xp}/{int(200 *((1/2) * l))}\n Đã nhận: {r}")




bot.run() 
