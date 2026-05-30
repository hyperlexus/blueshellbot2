import discord
from discord.ext.commands import slash_command, Cog
from discord import ApplicationContext
import re
from datetime import datetime, timedelta


def extract(pattern, text, default="0", group=1):
    match = re.search(pattern, text)
    return match.group(group) if match else default

def format_relative(t):
    if not t or t == "0":
        return "0m"
    t = t.strip()
    if "h" in t and " " in t:
        return t.replace("h ", ":") + "h"
    elif "h" in t:
        return t
    else:
        return t + "m"

def format_absolute(t):
    now = datetime.now()
    if not t or t == "0":
        return now.strftime("%H:%M")
    t = t.strip()
    hrs = 0
    mins = 0
    if "h" in t:
        parts = t.split("h")
        hrs = int(parts[0].strip() or 0)
        if len(parts) > 1 and parts[1].strip():
            minutes_str = parts[1].replace("m", "").strip()
            mins = int(minutes_str) if minutes_str else 0
    else:
        minutes_str = t.replace("m", "").strip()
        mins = int(minutes_str) if minutes_str else 0
    dt = now + timedelta(hours=hrs, minutes=mins)
    return dt.strftime("%H:%M")

key_emoji = "<:keys:1506802471568277584>"
kakera_emoji = "<:kakera:1506799052745080833>"
spheres_emoji = "<:spheres:1506804921444601913>"
kekmark_emoji = "<:kekmark:1506816979804229752>"
stack_rolls_emoji = "<:stackedrolls:1506817470357442650>"
dollar_rt_emoji = "<:rolltimer:1506817938420924426>"
add_roll_emoji = "<:addroll:1506819400169427128>"

class MudaeCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_users = ["hyperlexus", "ad.infernum", "tokyobre"]  # yes this is hardcoded no im too lazy
        self.mudae_id = 432610292342587392
        self.servers_to_search = [1486857971060445186, 995966314877300737, 1494713422271746139]
        self.last_message_reacted_to = 0
        self.absolute_toggle = True

    @Cog.listener()
    async def on_message(self, message):
        if self.bot.voice_clients: return
        if message.guild is None or message.guild.id is None or (message.guild.id not in self.servers_to_search):
            return
        if message.author.id != self.mudae_id:
            if not message.author.name.lower().startswith("mudae"): return

        content = message.content
        current_user = None
        for user in self.target_users:
            if content.startswith(f"**{user}**,"):
                current_user = user
                break

        if not current_user: return

        if "rolls left" not in content and "rolls reset" not in content: return

        try: await message.delete()
        except discord.Forbidden: pass
        except discord.NotFound: pass

        rolls = extract(r'You have \*\*(\d+)\*\* rolls left', content)
        rolls_time_raw = extract(r'Next rolls reset in \*\*([^*]+)\*\*', content, default="0")
        rolls_time_abs = format_absolute(rolls_time_raw)
        rolls_time_rel = format_relative(rolls_time_raw)

        rt_stock = extract(r'You have \*\*(\d+)\*\* rolls reset', content)

        claim_yes = re.search(r'next claim reset is in \*\*([^*]+)\*\*', content)
        claim_no = re.search(r'you can\'t claim for another \*\*([^*]+)\*\*', content)

        if claim_yes:
            claim_str_rel = f"{format_relative(claim_yes.group(1))}{kekmark_emoji}"
            claim_str_abs = f"{format_absolute(claim_yes.group(1))}{kekmark_emoji}"
        elif claim_no:
            claim_str_rel = f"{format_relative(claim_no.group(1))}:x:"
            claim_str_abs = f"{format_absolute(claim_no.group(1))}:x:"
        else: claim_str_rel = claim_str_abs = ":question:"

        dk_match = re.search(r'Next \$dk in \*\*([^*]+)\*\*', content)
        dk_rel = format_relative(dk_match.group(1)) if dk_match else kekmark_emoji
        dk_abs = format_absolute(dk_match.group(1)) if dk_match else kekmark_emoji

        vote_match = re.search(r'vote again in \*\*([^*]+)\*\*', content)
        vote_rel = format_relative(vote_match.group(1)) if vote_match else kekmark_emoji
        vote_abs = format_absolute(vote_match.group(1)) if vote_match else kekmark_emoji

        daily_match = re.search(r'Next \$daily reset in \*\*([^*]+)\*\*', content)
        daily_rel = format_relative(daily_match.group(1)) if daily_match else kekmark_emoji
        daily_abs = format_absolute(daily_match.group(1)) if daily_match else kekmark_emoji

        keys_val = extract(r'\*\*([\d,]+)\*\*\s*<:kakera[^>]+>to collect', content).replace(",", "").replace(".", "")
        keys_time_raw = extract(r'to collect before the next reset \(\*\*([^*]+)\*\*', content, default="0")
        keys_time_rel = format_relative(keys_time_raw)
        keys_time_abs = format_absolute(keys_time_raw)

        bku_prob = extract(r'\$bku on your next \$sw: \*\*([^*]+)\*\*', content, default="0%")
        power = extract(r'Power: \*\*([^*]+)\*\*', content, default="100%")

        can_react = "You __can__ react to kakera" in content
        cant_react_match = re.search(r"You can't react to kakera for \*\*([^*]+)\*\*", content)

        if can_react: react_rel = react_abs = kekmark_emoji
        elif cant_react_match:
            react_rel = f":x: {format_relative(cant_react_match.group(1))}"
            react_abs = f":x: {format_absolute(cant_react_match.group(1))}"
        else: react_rel = react_abs = ":x:"

        k_stock = extract(r'Stock: \*\*([\d,]+)\*\*\s*<:kakera', content)
        sp_stock = extract(r'Stock: \*\*([\d,]+)\*\*\s*<:sp', content, default="0")

        if current_user in ["hyperlexus", "ad.infernum"]:
            key_string = "" if int(keys_val) == 4500 else f"{key_emoji}{keys_val}, {keys_time_abs}, {bku_prob}\n"
            result = (
                f"**{current_user}**:\n"
                f"{rolls}{stack_rolls_emoji} {rolls_time_abs}🕐 {rt_stock}{add_roll_emoji} {claim_str_abs}\n"
                f"{daily_abs}📅 {vote_abs}🗳️ {dk_abs}💸\n"
                f"{key_string}"
                f"{k_stock}{kakera_emoji}, {power}{react_abs}\n"
                f"{sp_stock}{spheres_emoji}"
            ) if self.absolute_toggle else (
                f"**{current_user}**:\n"
                f"{rolls}{stack_rolls_emoji} {rolls_time_rel}🕐 {rt_stock}{add_roll_emoji} {claim_str_rel}\n"
                f"{daily_rel}📅 {vote_rel}🗳️ {dk_rel}💸\n"
                f"{key_string}"
                f"{k_stock}{kakera_emoji}, {power}{react_rel}\n"
                f"{sp_stock}{spheres_emoji}"
            )
        elif current_user == "tokyobre":
            finished_rolls_string = f"You have **{rolls_time_rel}** left to use your **{rolls}** remaining Rolls.\n"\
                if int(rolls) > 0 else f"**YOU IDIOT ALREADY ROLLED THIS HOUR**\nCome back in {rolls_time_rel}."
            result = (
                f"**{current_user}** gets a new Claim in **{claim_str_rel}**\n\n"
                f"{finished_rolls_string}\n"
                f"**{rt_stock}**:arrows_counterclockwise:\n\n"
                f"$daily in **{daily_rel}**.\n"
                f"$dk in **{dk_rel}**.\n"
                f"$vote in **{vote_rel}**.\n\n"
                f"React to Kakera in **{react_rel}**.\n"
                f"**{k_stock}** {kakera_emoji}\n"
                f"**{sp_stock}** {spheres_emoji}\n"
                f"||**{keys_val}**, **{keys_time_rel}**, **{bku_prob}**||\n"
            )
        else: result = ""

        if message.id != self.last_message_reacted_to:
            self.last_message_reacted_to = message.id
            await message.channel.send(result)

    @slash_command(name='toggle_tu_message')
    async def flip_tu_message(self, ctx: ApplicationContext):
        if ctx.author.id != 422800248935546880:
            await ctx.respond("you are not authorised to use this command.")
            return

        self.absolute_toggle = not self.absolute_toggle
        await ctx.respond(kekmark_emoji)
        return

def setup(bot):
    bot.add_cog(MudaeCog(bot))