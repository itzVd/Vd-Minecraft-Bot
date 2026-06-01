import discord
from discord import app_commands
import aiohttp
import asyncio
import os
import threading
from flask import Flask
from groq import Groq

# ─── إعداد التوكنات والمفاتيح من البيئة الآمنة ───────────────────────────────
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GROQ_API_KEY  = os.environ.get("GROQ_API_KEY")

# ─── إعداد Groq AI ────────────────────────────────────────────────────────────
groq_client = Groq(api_key=GROQ_API_KEY)

GROQ_MODEL  = "llama-3.3-70b-versatile"
SYSTEM_PROMPT = (
    "أنت مساعد ذكي متخصص في لعبة Minecraft. تُجيب دائماً باللغة العربية الفصحى "
    "بشكل واضح ومنظم. لديك معرفة واسعة بكل جوانب اللعبة: صناعة الأدوات، البقاء، "
    "المودات، السيرفرات، والتحديثات. إذا سُئلت عن موضوع خارج Minecraft فأجب باختصار "
    "ثم أعِد توجيه المحادثة لمواضيع اللعبة."
)

# ─── إعداد البوت ─────────────────────────────────────────────────────────────
intents = discord.Intents.default()

class MinecraftBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("✅ تم مزامنة الأوامر مع Discord!")

    async def on_ready(self):
        await self.change_presence(
            activity=discord.Game(name="🎮 Minecraft | /help للمساعدة")
        )
        print(f"✅ البوت يعمل الآن: {self.user} (ID: {self.user.id})")

    async def on_message(self, message):
        if message.author.bot:
            return
        if self.user.mentioned_in(message) and not message.mention_everyone:
            content = message.content
            for mention in [f"<@{self.user.id}>", f"<@!{self.user.id}>"]:
                content = content.replace(mention, "").strip()

            if content:
                async with message.channel.typing():
                    answer = await get_ai_response(content)
                embed = discord.Embed(
                    title="🤖 مساعد Minecraft الذكي",
                    color=0x9B59B6,
                )
                for i, chunk in enumerate([answer[j:j+4000] for j in range(0, len(answer), 4000)]):
                    if i == 0:
                        embed.description = chunk
                    else:
                        embed.add_field(name=f"تابع ({i+1})", value=chunk, inline=False)
                embed.set_footer(
                    text=f"سؤال: {message.author.display_name} | مدعوم بـ Google Gemini ✨",
                    icon_url=message.author.display_avatar.url,
                )
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="👋 مرحباً!",
                    description="كيف يمكنني مساعدتك؟\nاكتب سؤالك بعد الإشارة لي، أو استخدم `/help` لعرض الأوامر.",
                    color=0x3498DB,
                )
                await message.channel.send(embed=embed)

bot = MinecraftBot()

# ─── ألوان الـ Embed ──────────────────────────────────────────────────────────
COLOR_GREEN  = 0x2ECC71
COLOR_RED    = 0xE74C3C
COLOR_BLUE   = 0x3498DB
COLOR_GOLD   = 0xF1C40F
COLOR_PURPLE = 0x9B59B6


# ══════════════════════════════════════════════════════════════════════════════
#  مساعد: الحصول على رد الذكاء الاصطناعي
# ══════════════════════════════════════════════════════════════════════════════
async def get_ai_response(question: str) -> str:
    loop = asyncio.get_event_loop()
    try:
        response = await loop.run_in_executor(
            None,
            lambda: groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": question},
                ],
                max_tokens=2048,
                temperature=0.7,
            ),
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ حدث خطأ: {str(e)[:300]}"


# ══════════════════════════════════════════════════════════════════════════════
#  أمر: /help — قائمة المساعدة
# ══════════════════════════════════════════════════════════════════════════════
@bot.tree.command(name="help", description="عرض جميع أوامر البوت")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📖 قائمة أوامر بوت Minecraft",
        description="مرحباً بك! فيما يلي جميع الأوامر المتاحة:",
        color=COLOR_GOLD,
    )
    embed.set_thumbnail(url="https://i.imgur.com/GhDnCPN.png")
    embed.add_field(
        name="🌐 فحص السيرفر",
        value=(
            "`/status ip:<عنوان>` — فحص سيرفر Java Edition\n"
            "`/bedrock ip:<عنوان>` — فحص سيرفر Bedrock Edition\n"
            "_مثال: `/status ip:mc.hypixel.net`_"
        ),
        inline=False,
    )
    embed.add_field(
        name="🤖 الذكاء الاصطناعي",
        value=(
            "`/ai سؤال:<سؤالك>` — اسأل مساعد Minecraft الذكي\n"
            "_أو أشِر للبوت مباشرةً في الشات_\n"
            "_مثال: `/ai سؤال:كيف أصنع سيف الماس؟`_"
        ),
        inline=False,
    )
    embed.add_field(
        name="🎨 السكين والملف الشخصي",
        value=(
            "`/skin اسم:<اسم اللاعب>` — عرض سكين اللاعب\n"
            "_مثال: `/skin اسم:Notch`_"
        ),
        inline=False,
    )
    embed.add_field(
        name="ℹ️ معلومات",
        value="`/ping` — قياس سرعة استجابة البوت",
        inline=False,
    )
    embed.set_footer(text="بوت Minecraft العربي | مدعوم بـ Google Gemini AI ✨")
    await interaction.response.send_message(embed=embed)


# ══════════════════════════════════════════════════════════════════════════════
#  أمر: /status — فحص سيرفر Java
# ══════════════════════════════════════════════════════════════════════════════
@bot.tree.command(name="status", description="فحص حالة سيرفر Minecraft Java Edition")
@app_commands.describe(ip="عنوان السيرفر (مثال: mc.hypixel.net)", port="رقم المنفذ (افتراضي: 25565)")
async def server_status(interaction: discord.Interaction, ip: str, port: int = 25565):
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.mcsrvstat.us/3/{ip}:{port}"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                data = await resp.json()
    except Exception:
        embed = discord.Embed(
            title="⚠️ فشل الاتصال",
            description="تعذّر الوصول إلى خدمة الفحص. حاول مجدداً لاحقاً.",
            color=COLOR_RED,
        )
        return await interaction.followup.send(embed=embed)

    online = data.get("online", False)

    if online:
        players_online = data.get("players", {}).get("online", 0)
        players_max    = data.get("players", {}).get("max", 0)
        version        = data.get("version", "غير معروف")
        motd_lines     = data.get("motd", {}).get("clean", [])
        motd           = " ".join(motd_lines) if motd_lines else "لا يوجد"
        icon_url       = f"https://api.mcsrvstat.us/icon/{ip}:{port}"

        bar_filled = int((players_online / players_max * 10) if players_max else 0)
        bar        = "🟩" * bar_filled + "⬜" * (10 - bar_filled)

        embed = discord.Embed(
            title=f"✅ السيرفر متاح — {ip}",
            color=COLOR_GREEN,
        )
        embed.set_thumbnail(url=icon_url)
        embed.add_field(name="📡 عنوان IP",    value=f"`{ip}:{port}`", inline=True)
        embed.add_field(name="🎮 الإصدار",      value=f"`{version}`",  inline=True)
        embed.add_field(name="👥 اللاعبون",
                        value=f"`{players_online} / {players_max}`\n{bar}", inline=False)
        embed.add_field(name="📝 وصف السيرفر", value=motd or "—",     inline=False)
        embed.set_footer(text="Java Edition | mcsrvstat.us")
    else:
        embed = discord.Embed(
            title=f"❌ السيرفر مغلق — {ip}",
            description="السيرفر غير متاح حالياً أو العنوان غير صحيح.",
            color=COLOR_RED,
        )
        embed.add_field(name="📡 العنوان المُدخَل", value=f"`{ip}:{port}`", inline=False)

    await interaction.followup.send(embed=embed)


# ══════════════════════════════════════════════════════════════════════════════
#  أمر: /bedrock — فحص سيرفر Bedrock
# ══════════════════════════════════════════════════════════════════════════════
@bot.tree.command(name="bedrock", description="فحص حالة سيرفر Minecraft Bedrock Edition")
@app_commands.describe(ip="عنوان السيرفر", port="رقم المنفذ (افتراضي: 19132)")
async def bedrock_status(interaction: discord.Interaction, ip: str, port: int = 19132):
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.mcsrvstat.us/bedrock/3/{ip}:{port}"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                data = await resp.json()
    except Exception:
        embed = discord.Embed(
            title="⚠️ فشل الاتصال",
            description="تعذّر الوصول إلى خدمة الفحص.",
            color=COLOR_RED,
        )
        return await interaction.followup.send(embed=embed)

    online = data.get("online", False)

    if online:
        players_online = data.get("players", {}).get("online", 0)
        players_max    = data.get("players", {}).get("max", 0)
        version        = data.get("version", "غير معروف")
        motd_lines     = data.get("motd", {}).get("clean", [])
        motd           = " ".join(motd_lines) if motd_lines else "لا يوجد"

        bar_filled = int((players_online / players_max * 10) if players_max else 0)
        bar        = "🟩" * bar_filled + "⬜" * (10 - bar_filled)

        embed = discord.Embed(
            title=f"✅ سيرفر Bedrock متاح — {ip}",
            color=COLOR_GREEN,
        )
        embed.add_field(name="📡 عنوان IP",    value=f"`{ip}:{port}`", inline=True)
        embed.add_field(name="🎮 الإصدار",      value=f"`{version}`",  inline=True)
        embed.add_field(name="👥 اللاعبون",
                        value=f"`{players_online} / {players_max}`\n{bar}", inline=False)
        embed.add_field(name="📝 وصف السيرفر", value=motd or "—",     inline=False)
        embed.set_footer(text="Bedrock Edition | mcsrvstat.us")
    else:
        embed = discord.Embed(
            title=f"❌ سيرفر Bedrock مغلق — {ip}",
            description="السيرفر غير متاح حالياً أو العنوان غير صحيح.",
            color=COLOR_RED,
        )

    await interaction.followup.send(embed=embed)


# ══════════════════════════════════════════════════════════════════════════════
#  أمر: /ai — الذكاء الاصطناعي
# ══════════════════════════════════════════════════════════════════════════════
@bot.tree.command(name="ai", description="اسأل مساعد Minecraft الذكي أي سؤال")
@app_commands.describe(سؤال="اكتب سؤالك هنا (مثال: كيف أصنع قوس؟)")
async def ai_chat(interaction: discord.Interaction, سؤال: str):
    await interaction.response.defer()

    answer = await get_ai_response(سؤال)

    chunks = [answer[i:i+4000] for i in range(0, len(answer), 4000)]
    for idx, chunk in enumerate(chunks):
        embed = discord.Embed(
            title="🤖 مساعد Minecraft الذكي" + (f" (جزء {idx+1})" if len(chunks) > 1 else ""),
            description=chunk,
            color=COLOR_PURPLE,
        )
        embed.set_footer(
            text=f"سؤال: {interaction.user.display_name} | مدعوم بـ Google Gemini ✨",
            icon_url=interaction.user.display_avatar.url,
        )
        if idx == 0:
            await interaction.followup.send(embed=embed)
        else:
            await interaction.channel.send(embed=embed)


# ══════════════════════════════════════════════════════════════════════════════
#  أمر: /skin — عرض سكين اللاعب
# ══════════════════════════════════════════════════════════════════════════════
@bot.tree.command(name="skin", description="عرض سكين وملف لاعب Minecraft")
@app_commands.describe(اسم="اسم اللاعب في Java Edition (مثال: Notch)")
async def player_skin(interaction: discord.Interaction, اسم: str):
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            # جلب UUID من Mojang API الرسمي
            mojang_url = f"https://api.mojang.com/users/profiles/minecraft/{اسم}"
            async with session.get(mojang_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status == 204 or resp.status == 404:
                    raise ValueError("اللاعب غير موجود")
                if resp.status != 200:
                    raise ValueError(f"خطأ في الاتصال ({resp.status})")
                data = await resp.json()

        uuid       = data.get("id", "")
        exact_name = data.get("name", اسم)
        if not uuid:
            raise ValueError("اللاعب غير موجود")

        avatar_url = f"https://crafatar.com/avatars/{uuid}?size=256&overlay"
        skin_url   = f"https://crafatar.com/skins/{uuid}"
        render_url = f"https://crafatar.com/renders/body/{uuid}?scale=6&overlay"

        # تنسيق UUID بالشكل الكامل مع الشرطات
        uuid_fmt = f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"

        embed = discord.Embed(
            title=f"🎨 ملف اللاعب — {exact_name}",
            color=COLOR_GOLD,
        )
        embed.set_thumbnail(url=avatar_url)
        embed.set_image(url=render_url)
        embed.add_field(name="👤 الاسم",  value=f"`{exact_name}`",  inline=True)
        embed.add_field(name="🆔 UUID",   value=f"`{uuid_fmt}`",    inline=True)
        embed.add_field(
            name="🔗 روابط",
            value=f"[تحميل السكين]({skin_url}) • [الصورة الرمزية]({avatar_url})",
            inline=False,
        )
        embed.set_footer(text="Mojang API + Crafatar | Java Edition فقط")
        await interaction.followup.send(embed=embed)

    except Exception:
        embed = discord.Embed(
            title="❌ اللاعب غير موجود",
            description=f"لم يتم العثور على اللاعب `{اسم}`.\nتأكد من صحة الاسم (حساسية الأحرف مهمة).",
            color=COLOR_RED,
        )
        await interaction.followup.send(embed=embed)


# ══════════════════════════════════════════════════════════════════════════════
#  أمر: /ping — قياس الاستجابة
# ══════════════════════════════════════════════════════════════════════════════
@bot.tree.command(name="ping", description="قياس سرعة استجابة البوت")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    color = COLOR_GREEN if latency < 100 else COLOR_GOLD if latency < 200 else COLOR_RED
    emoji = "🟢" if latency < 100 else "🟡" if latency < 200 else "🔴"

    embed = discord.Embed(
        title=f"{emoji} سرعة الاستجابة",
        description=f"**{latency} مللي ثانية**",
        color=color,
    )
    embed.set_footer(text="Pong! 🏓")
    await interaction.response.send_message(embed=embed)


# ══════════════════════════════════════════════════════════════════════════════
#  سيرفر Flask الصغير (للـ Uptime)
# ══════════════════════════════════════════════════════════════════════════════
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "<h2>🤖 Minecraft Discord Bot — يعمل بنجاح!</h2>", 200

@flask_app.route("/health")
def health():
    return {"status": "online", "bot": str(bot.user) if bot.user else "connecting"}, 200

def run_flask():
    port = int(os.environ.get("BOT_WEB_PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)


# ══════════════════════════════════════════════════════════════════════════════
#  نقطة الانطلاق الرئيسية
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ خطأ: DISCORD_TOKEN غير موجود في المتغيرات البيئية!")
        exit(1)
    if not GROQ_API_KEY:
        print("❌ خطأ: GROQ_API_KEY غير موجود في المتغيرات البيئية!")
        exit(1)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 سيرفر Flask يعمل للـ Uptime...")

    print("🚀 تشغيل بوت Discord...")
    bot.run(DISCORD_TOKEN)
