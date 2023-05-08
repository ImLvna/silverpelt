from os import environ
from builtins import print as _print
from re import search
import lightbulb
import hikari
import dotenv

from server import add_token

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
        bot.reload_extensions()
        await message.edit(embed=hikari.Embed(description="**:white_check_mark: Reloaded**", color=0x29ff70))
    except Exception as e:
        await message.edit(embed=hikari.Embed(description=f"**:x: Error reloading**\n{e}", color=0xff3838))

@bot.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("eval", "evaluates code")
@lightbulb.implements(lightbulb.PrefixCommand)
async def eval(ctx: lightbulb.Context) -> None: # pylint: disable=redefined-builtin
    code = ctx.event.content[len(ctx.prefix) + 5:]
    match_blockquote = search(r"^```(?:(?:py|python)\n)?([^`]+?)```", code)
    match_inline = search(r"^`([^`]+)`", code)
    if match_blockquote is not None:
        code = match_blockquote.group(1)
    elif match_inline is not None:
        code = match_inline.group(1)
    message = await ctx.respond(embed=hikari.Embed(description="**Evaluating code...**", color=0x8aadff))
    logs = []
    def print(*args, **kwargs): # pylint: disable=unused-variable, redefined-builtin
        _print(*args, **kwargs)
        logs.append(''.join([str(i) for i in args]))
        desc = '\n'.join(logs)
        if desc != "":
            message.edit(embed=hikari.Embed(description=desc, color=0x8aadff))
    try:
        exec(code) # pylint: disable=exec-used
        desc = '\n'.join(logs)
        if desc != "":
            await message.edit(embed=hikari.Embed(description=desc, color=0x73eb79))
        else:
            await message.edit(embed=hikari.Embed(description="**No output**", color=0x73eb79))
    except Exception as e:
        logs.append("")
        logs.append(str(e))
        desc = '\n'.join(logs)
        await message.edit(embed=hikari.Embed(description=desc, color=0xcc4968))



bot.load_extensions_from("cogs")
bot.run()
