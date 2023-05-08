from os import environ
from builtins import print as _print
from re import search
import lightbulb
import hikari
import dotenv


dotenv.load_dotenv(".env")
bot = lightbulb.BotApp(
    token=environ.get("DISCORD_TOKEN"),
    prefix="~",
    intents=hikari.Intents.ALL_UNPRIVILEGED + hikari.Intents.MESSAGE_CONTENT,
    help_class=None,
    owner_ids=[174200708818665472, 266751215767912463])


@bot.command
@lightbulb.command("ping", "Calls the bot with its delay")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Pong! Bot ping is {round(ctx.bot.heartbeat_latency*1000, 1)}ms")


@bot.command
@lightbulb.command("reload", "reloads all extensions")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def reload(ctx: lightbulb.Context) -> None:
    message = await ctx.respond(embed=hikari.Embed(description="**Reloading all extensions**", color=0x8aadff))
    try:
        for i in extensions:
            bot.reload_extensions(i)
        await message.edit(embed=hikari.Embed(description="**:white_check_mark: Reloaded**", color=0x29ff70))
    except Exception as e:
        await message.edit(embed=hikari.Embed(description=f"**:x: Error reloading**\n{e}", color=0xff3838))




bot.load_extensions_from("cogs")
extensions = bot.extensions
bot.run()

from server import app, add_token

app.run(host='0.0.0.0',port=8080)
