import subprocess
subprocess.run(["pip", "install", "discord.py", "flask"])

import discord
from discord.ext import commands
import os
import re
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

rules = {
    1: "**1. Be Respectful**\nTreat everyone with kindness.\nNo harassment, slurs, bullying, threats, or targeting others.\nDisagreements are fine—disrespect is not.",
    2: "**2. Keep It PG-13**\nNo NSFW content, sexual content, gore, extreme violence, or overly explicit language.\nVR clips must also follow PG-13 guidelines.",
    3: "**3. No Cheating, Exploits, or Hacks**\nDo not use, share, or promote cheats, exploits, or game-breaking mods.\nAttempting to bypass bans or restrictions is also prohibited.",
    4: "**4. No Impersonation**\nDo not pretend to be staff, moderators, developers, or other community members.\nFake admin tags or misleading nicknames are not allowed.",
    5: "**5. Follow Channel Topics**\nPost only in the appropriate channels.\nRead channel descriptions before sending messages.\nYou're allowed to talk about other things, but don't make the entire chat about a completely off-topic thing.\nYou can talk about yeeps or grace in any channel!",
    6: "**6. No Spam**\nNo message spam, emoji spam, ping spam, or mic spam.\nDo not repeatedly ask for the same thing after being answered.\nNo mass-DMing members.",
    7: "**7. VR Gameplay Clips Allowed**\nClips must be appropriate and follow all server rules.\nNo exposing private info accidentally shown in your footage.\nNo drama-baiting or targeted calling-out.",
    8: "**8. Protect Your Privacy**\nDo not share personal information (yours or others').\nNo IPs, emails, addresses, real names, or private conversations.\nDo not record voice chats or screenshare users without permission.",
    9: "**9. No Toxic Behavior**\nNo starting arguments, drama, or instigating fights.\nKeep the community fun, friendly, and drama-free.",
    10: "**10. Age Requirement**\nYou must be 13+ to use Discord and be in this server.\nAnyone admitting to being under the required age will be removed.",
    11: "**11. No Advertising Without Permission**\nNo promoting other servers, social media, or products unless explicitly allowed by staff.\nPosting invite links without approval is considered advertising.",
    12: "**12. Use Common Sense**\nIf you think something might break the rules, don't do it.\nJust because a rule isn't written doesn't mean harmful behavior is allowed.",
    13: "**13. Staff Decisions Are Final**\nListen to moderators and admins.\nIf you feel you were punished unfairly, appeal respectfully.\nArguing with staff can lead to additional consequences.",
    14: "**14. Reporting Issues**\nReport rule-breakers or problems to staff privately.\nDo not mini-mod or start fights in chat over issues.",
    15: "**15. Have Fun & Be Cool**\nWe're here to enjoy VR and hang out.\nHelp new players, stay positive, and don't ruin the vibe.",
}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Match ?rule followed immediately by a number (no space allowed)
    match = re.match(r'^\?rule(\d+)$', message.content.strip())
    if match:
        number = int(match.group(1))
        if number in rules:
            embed = discord.Embed(description=rules[number], color=discord.Color.blue())
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(f"❌ Rule `{number}` doesn't exist. There are **15 rules** total.")
        return

    await bot.process_commands(message)

@bot.command(name='ping')
@commands.has_role('Moderator')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Bot latency is **{latency}ms**.')

@ping.error
async def ping_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("❌ You need the **Moderator** role to use this command.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

bot.run(os.environ['DISCORD_TOKEN'])
