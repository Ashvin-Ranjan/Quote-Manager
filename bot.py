import discord
import json

key = ""

settings = {}

with open(".token", "r") as f:
    key = f.read().strip()

with open("settings.json", "r") as f:
    settings = json.loads(f.read())

client = discord.Client()


@client.event
async def on_ready():
    customActivity = discord.Game("Managing the quotebook")
    await client.change_presence(status=discord.Status.online, activity=customActivity)

    print("The bot is ready")


@client.event
async def on_message(message):
    global settings

    if message.author == client.user:
        return

    if (
        message.content.startswith("!mincount ")
        and len(message.content.split(" ")) == 2
    ):
        try:
            settings["removal_count"] = int(message.content.split(" ")[1])
            with open("settings.json", "w") as f:
                f.write(json.dumps(settings))
            await message.channel.send(
                f"Updated settings, `removal_count` set to {settings['removal_count']}",
                allowed_mentions=discord.AllowedMentions.none(),
            )
        except:

            await message.channel.send(
                "Unable to process your request.",
                allowed_mentions=discord.AllowedMentions.none(),
            )


@client.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == "👎" and reaction.count >= settings["removal_count"]:
        await reaction.message.delete()


client.run(key)
