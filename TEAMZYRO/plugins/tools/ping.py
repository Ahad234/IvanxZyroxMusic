import time
import psutil
import asyncio
from pyrogram import filters
from TEAMZYRO import app

start_time = time.time()

def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time


@app.on_message(filters.command("ping") & filters.group)
async def ping(_, message):
    start = time.time()
    reply = await message.reply_text("Pinging...")
    end = time.time()
    await reply.edit_text(f"Pong! `{round((end - start) * 1000)}ms`")


@app.on_message(filters.command("stats") & filters.group)
async def stats(_, message):
    uptime = get_readable_time(time.time() - start_time)
    cpu_usage = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    ram_usage = mem.percent
    disk = psutil.disk_usage("/")
    disk_usage = disk.percent

    text = (
        f"**Bot Statistics:**\n"
        f"⏱️ Uptime: `{uptime}`\n"
        f"⚡ CPU Usage: `{cpu_usage}%`\n"
        f"🖥️ RAM Usage: `{ram_usage}%`\n"
        f"💾 Disk Usage: `{disk_usage}%`"
    )

    await message.reply_text(text)
