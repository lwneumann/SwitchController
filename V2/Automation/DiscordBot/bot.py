import os
import discord
import threading
import asyncio
from discord.ext import commands
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import screenshot


# Load token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
USER_ID = int(os.getenv("USER_ID")) 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
user = None

app = Flask(__name__)

# Store pending user input requests
pending_request = None

# -----------------------------
# Flask routes
# -----------------------------
@app.route("/update", methods=["POST"])
def update():
    data = request.json
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if not channel:
        return jsonify({"status": "error", "message": "Channel not found"}), 404

    # One-way update
    if "message" in data and data.get("id") != "ask":
        msg = data["message"]
        try:
            future = asyncio.run_coroutine_threadsafe(channel.send(msg), bot.loop)
            future.result(timeout=10)
            return jsonify({"status": "ok", "result": "Message sent"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    # Post screenshot
    if data.get("id") == "screenshot":
        ping = data['ping']
        path = data['path']
        try:
            if ping:
                future = asyncio.run_coroutine_threadsafe(channel.send(user.mention, file=discord.File(path)), bot.loop)
            else:
                future = asyncio.run_coroutine_threadsafe(channel.send(file=discord.File(path)), bot.loop)
            future.result(timeout=10)

            return jsonify({"status": "ok", "result": "Message sent"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    # Ask for user input
    if data.get("id") == "ask":
        global pending_request
        if pending_request is not None and not pending_request.done():
            return jsonify({"status": "error", "message": "Another request is pending"}), 429
        prompt = data.get("prompt", "Please provide input:")
        fut = bot.loop.create_future()
        pending_request = fut

        async def send_prompt_with_reactions():
            msg = await channel.send(prompt)
            emoji_map = {
                "✅": "yes",
                "❌": "no",
                "🔁": "repeat",
                "🛑": "stop"
            }
            for emoji in emoji_map.keys():
                await msg.add_reaction(emoji)
            fut.msg_id = msg.id
            fut.emoji_map = emoji_map

        asyncio.run_coroutine_threadsafe(send_prompt_with_reactions(), bot.loop)
        return jsonify({"status": "ok"})


@app.route("/result", methods=["GET"])
def get_result():
    global pending_request
    if pending_request is None:
        return jsonify({"status": "error", "message": "No pending request"}), 404
    if pending_request.done():
        reply = pending_request.result()
        pending_request = None
        return jsonify({"status": "ok", "reply": reply})
    else:
        return jsonify({"status": "pending", "reply": None})


# -----------------------------
# Discord events
# -----------------------------
@bot.event
async def on_ready():
    global user
    user = await bot.fetch_user(USER_ID)

    print(f"> Logged in as {bot.user}")
    return user

# Handle emoji reactions for user input
@bot.event
async def on_reaction_add(reaction, user):
    global pending_request
    if user == bot.user:
        return
    if pending_request and hasattr(pending_request, "msg_id") and reaction.message.id == pending_request.msg_id:
        emoji_map = getattr(pending_request, "emoji_map", {})
        if str(reaction.emoji) in emoji_map:
            reply_text = emoji_map[str(reaction.emoji)]
            if not pending_request.done():
                pending_request.set_result(reply_text)
            await reaction.message.channel.send(f"✅ Got your reply: {reply_text}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

# Commands
@bot.command(pass_context=True)
async def screen(ctx):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    ret = screenshot.screenshot()
    await ctx.send('Here is the current screen:', file=discord.File('screen.png'))
    return

# -----------------------------
# Run Flask in background
# -----------------------------
def run_flask():
    app.run(port=5000)

threading.Thread(target=run_flask, daemon=True).start()
bot.run(TOKEN)
