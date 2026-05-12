import discord
from discord.ext import commands
import re


def extract(pattern, text, default="0", group=1):
    match = re.search(pattern, text)
    return match.group(group) if match else default

def clean_time(t):
    if not t or t == "0":
        return "0m"
    t = t.strip()
    if "h" in t and " " in t:
        return t.replace("h ", ":") + "h"
    elif "h" in t:
        return t
    else:
        return t + "m"

class MudaeCondenser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_users = ["hyperlexus", "ad.infernum"]
        self.mudae_id = 432610292342587392
        self.servers_to_search = [1486857971060445186, 995966314877300737, 1494713422271746139]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.mudae_id:
            if not message.author.name.lower().startswith("mudae"): return

        if message.guild.id not in self.servers_to_search: return

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
        rolls_time = clean_time(rolls_time_raw)

        rt_stock = extract(r'You have \*\*(\d+)\*\* rolls reset', content)

        claim_yes = re.search(r'next claim reset is in \*\*([^*]+)\*\*', content)
        claim_no = re.search(r'you can\'t claim for another \*\*([^*]+)\*\*', content)

        if claim_yes: claim_str = f"{clean_time(claim_yes.group(1))}:white_check_mark:"
        elif claim_no: claim_str = f"{clean_time(claim_no.group(1))}:x:"
        else: claim_str = ":question:"

        dk_match = re.search(r'Next \$dk in \*\*([^*]+)\*\*', content)
        dk_str = clean_time(dk_match.group(1)) if dk_match else ":white_check_mark:"

        vote_match = re.search(r'vote again in \*\*([^*]+)\*\*', content)
        vote_str = clean_time(vote_match.group(1)) if vote_match else ":white_check_mark:"

        daily_match = re.search(r'Next \$daily reset in \*\*([^*]+)\*\*', content)
        daily_str = clean_time(daily_match.group(1)) if daily_match else ":white_check_mark:"

        keys_val = extract(r'\*\*([\d,]+)\*\*\s*<:kakera[^>]+>to collect', content)
        keys_time_raw = extract(r'to collect before the next reset \(\*\*([^*]+)\*\*', content, default="0")
        keys_time = clean_time(keys_time_raw)

        bku_prob = extract(r'\$bku on your next \$sw: \*\*([^*]+)\*\*', content, default="0%")
        power = extract(r'Power: \*\*([^*]+)\*\*', content, default="100%")

        can_react = "You __can__ react to kakera" in content
        cant_react_match = re.search(r"You can't react to kakera for \*\*([^*]+)\*\*", content)

        if can_react: react_str = ":white_check_mark:"
        elif cant_react_match: react_str = f":x: {self.clean_time(cant_react_match.group(1))}"
        else: react_str = ":x:"

        k_stock = extract(r'Stock: \*\*([\d,]+)\*\*\s*<:kakera', content)
        sp_stock = extract(r'Stock: \*\*([\d,]+)\*\*\s*<:sp', content, default="0")

        result = (
            f"**{current_user}**:\n"
            f"{rolls}:slot_machine: {rolls_time}:clock1: {rt_stock}:arrows_counterclockwise: {claim_str}\n"
            f"{daily_str}:date: {vote_str}:ballot_box: {dk_str}:money_with_wings:\n"
            f":key:{keys_val}, {keys_time}, {bku_prob}\n"
            f":gem:{power}{react_str}, {k_stock}\n"
            f":red_circle:{sp_stock}"
        )

        await message.channel.send(result)

def setup(bot):
    bot.add_cog(MudaeCondenser(bot))