# from zoneinfo import ZoneInfo
# import discord
# from discord.ext.commands import slash_command, Cog
# from discord import ApplicationContext
# import re
# import math
# from datetime import datetime, timedelta
#
#
# def extract(pattern, text, default="0", group=1):
#     match = re.search(pattern, text)
#     return match.group(group) if match else default
#
#
# def format_relative(t):
#     if not t or t == "0":
#         return "0m"
#     t = t.strip()
#     if "h" in t and " " in t:
#         return t.replace("h ", ":") + "h"
#     elif "h" in t:
#         return t
#     else:
#         return t + "m"
#
#
# def format_absolute(t, tz_name="Europe/Berlin"):
#     now = datetime.now(ZoneInfo(tz_name))
#     if not t or t == "0":
#         return now.strftime("%H:%M")
#     t = t.strip()
#     hrs = 0
#     mins = 0
#     if "h" in t:
#         parts = t.split("h")
#         hrs = int(parts[0].strip() or 0)
#         if len(parts) > 1 and parts[1].strip():
#             minutes_str = parts[1].replace("m", "").strip()
#             mins = int(minutes_str) if minutes_str else 0
#     else:
#         minutes_str = t.replace("m", "").strip()
#         mins = int(minutes_str) if minutes_str else 0
#     dt = now + timedelta(hours=hrs, minutes=mins)
#     hours_diff = (dt.date() - now.date()).seconds // 3600
#     time_str = dt.strftime("%H:%M")
#     if hours_diff > 24:
#         return f"{time_str} +{hours_diff//24}d"
#     return time_str
#
#
# def format_power_time(minutes, tz_name, is_absolute):
#     if minutes <= 0:
#         return "MAX"
#     if is_absolute:
#         now = datetime.now(ZoneInfo(tz_name))
#         dt = now + timedelta(minutes=minutes)
#         days_diff = (dt.date() - now.date()).days
#         time_str = dt.strftime("%H:%M")
#         if days_diff > 1:
#             return f"{time_str} +{days_diff}d"
#         return time_str
#     else:
#         hrs = minutes // 60
#         mins = minutes % 60
#         if hrs > 0 and mins > 0:
#             return f"{hrs}:{mins:02d}h"
#         elif hrs > 0:
#             return f"{hrs}h"
#         else:
#             return f"{mins}m"
#
#
# def get_power_display(current_power, target, tz_name, is_absolute, is_cap=False):
#     if current_power >= target:
#         return "max" if is_cap else str(int(current_power // target))
#     mins_needed = math.ceil((target - current_power) * 3)
#     return format_power_time(mins_needed, tz_name, is_absolute)
#
#
# def get_o_value(content, o_type):
#     match = re.search(r'\*\*(\d+)\*\*\s*' + o_type + r'(?:[^*(]*\(\+\*\*(\d+)\*\*\s*stored\))?', content)
#     if match:
#         base = int(match.group(1))
#         stored = int(match.group(2)) if match.group(2) else 0
#         return str(base + stored)
#     return "0"
#
#
# key_emoji = "<:goldKey:1532460704676708495>"
# kakera_emoji = "<:kakera:1506799052745080833>"
# spheres_emoji = "<:spheres:1506804921444601913>"
# sphere_w8 = "<:spW8:1532463911175983265>"
# sphere_8 = "<:sp8:1532460836176531467>"
# sphere_9 = "<:sp9:1532460813359513790>"
# kekmark_emoji = "<:kekmark:1506816979804229752>"
# stack_rolls_emoji = "<:stackedrolls:1506817470357442650>"
# dollar_rt_emoji = "<:rolltimer:1506817938420924426>"
# add_roll_emoji = "<:addroll:1506819400169427128>"
# omega_emoji = "<:omegakey:1529169719192588379>"
# mega_emoji = "<:megasphere:1529174573315129514>"
# poke_emoji = "<:slugma:1529176216517607565>"
# chaos_key = "<:chaosKey:1532460675366912152>"
#
# class MudaeCog(Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.target_users = ["hyperlexus", "ad.infernum"]  # yes this is hardcoded no im too lazy
#         self.mudae_id = 432610292342587392
#         self.servers_to_search = [1486857971060445186, 995966314877300737, 1494713422271746139]
#         self.last_message_reacted_to = 0
#         self.absolute_toggle = True
#         self.max_power = {
#             "hyperlexus": 110,
#             "ad.infernum": 110
#         }
#
#     @Cog.listener()
#     async def on_message(self, message):
#         if self.bot.voice_clients: return None
#         if message.guild is None or message.guild.id is None or (message.guild.id not in self.servers_to_search): return
#         if message.author.id != self.mudae_id:
#             if not message.author.name.lower().startswith("mudae"): return None
#
#         content = message.content
#         current_user = None
#         for user in self.target_users:
#             if content.startswith(f"**{user}**,"):
#                 current_user = user
#                 break
#
#         if not current_user: return None
#         if "rolls left" not in content and "rolls reset" not in content: return None
#
#         try:
#             await message.delete()
#         except discord.Forbidden:
#             pass
#         except discord.NotFound:
#             pass
#
#         current_tz = "America/New_York" if current_user == "ad.infernum" else "Europe/Berlin"
#         rolls = extract(r'You have \*\*(\d+)\*\* rolls left', content)
#         rolls_time_raw = extract(r'Next rolls reset in \*\*([^*]+)\*\*', content, default="0")
#         rolls_time_abs = format_absolute(rolls_time_raw, current_tz)
#         rolls_time_rel = format_relative(rolls_time_raw)
#
#         rt_stock = extract(r'You have \*\*(\d+)\*\* rolls reset', content)
#
#         claim_yes = re.search(r'next claim reset is in \*\*([^*]+)\*\*', content)
#         claim_no = re.search(r'you can\'t claim for another \*\*([^*]+)\*\*', content)
#
#         if claim_yes:
#             claim_str_rel = f"{format_relative(claim_yes.group(1))}{kekmark_emoji}"
#             claim_str_abs = f"{format_absolute(claim_yes.group(1), current_tz)}{kekmark_emoji}"
#         elif claim_no:
#             claim_str_rel = f"{format_relative(claim_no.group(1))}:x:"
#             claim_str_abs = f"{format_absolute(claim_no.group(1), current_tz)}:x:"
#         else: claim_str_rel = claim_str_abs = ":question:"
#
#         dk_match = re.search(r'Next \$dk in \*\*([^*]+)\*\*', content)
#         dk_rel = format_relative(dk_match.group(1)) if dk_match else kekmark_emoji
#         dk_abs = format_absolute(dk_match.group(1), current_tz) if dk_match else kekmark_emoji
#
#         vote_match = re.search(r'vote again in \*\*([^*]+)\*\*', content)
#         vote_rel = format_relative(vote_match.group(1)) if vote_match else kekmark_emoji
#         vote_abs = format_absolute(vote_match.group(1), current_tz) if vote_match else kekmark_emoji
#
#         daily_match = re.search(r'Next \$daily reset in \*\*([^*]+)\*\*', content)
#         daily_rel = format_relative(daily_match.group(1)) if daily_match else kekmark_emoji
#         daily_abs = format_absolute(daily_match.group(1), current_tz) if daily_match else kekmark_emoji
#
#         rt_cd_match = re.search(r'The cooldown of \$rt is not over\. Time left: \*\*([^*]+)\*\*', content)
#         if re.search(r'\$rt is available!', content):
#             rt_rel = rt_abs = kekmark_emoji
#         elif rt_cd_match:
#             rt_rel = format_relative(rt_cd_match.group(1))
#             rt_abs = format_absolute(rt_cd_match.group(1), current_tz)
#         else:
#             rt_rel = rt_abs = ":question:"
#
#         p_cd_match = re.search(r'Remaining time before your next \$p: \*\*([^*]+)\*\*', content)
#         if re.search(r'\$p is available!', content):
#             p_rel = p_abs = kekmark_emoji
#         elif p_cd_match:
#             p_rel = format_relative(p_cd_match.group(1))
#             p_abs = format_absolute(p_cd_match.group(1), current_tz)
#         else:
#             p_rel = p_abs = ":question:"
#
#         keys_val = extract(r'\*\*([\d,]+)\*\*\s*<:kakera[^>]+>to collect', content).replace(",", "").replace(".", "")
#         keys_time_raw = extract(r'to collect before the next reset \(\*\*([^*]+)\*\*', content, default="0")
#         keys_time_rel = format_relative(keys_time_raw)
#         keys_time_abs = format_absolute(keys_time_raw, current_tz)
#
#         bku_prob = extract(r'\$bku on your next \$sw: \*\*([^*]+)\*\*', content, default="0%")
#         omega_keys = extract(r'\*\*([\d,]+)\*\*\s*<:omegakey', content, default="0").replace(",", "")
#
#         k_stock = extract(r'Stock: \*\*([\d,]+)\*\*\s*<:kakera', content)
#         sp_stock = extract(r'Stock: \*\*([\d,]+)\*\*\s*<:sp', content, default="0")
#
#         oh_val = get_o_value(content, r'\$oh')
#         oc_val = get_o_value(content, r'\$oc')
#         oq_val = get_o_value(content, r'\$oq')
#         ot_val = get_o_value(content, r'\$ot')
#         o_string = f"👨‍🌾{oh_val}♟️{oc_val}💣{oq_val}🚢{ot_val}"
#
#         mega_match = re.search(r'Next <:spM:\d+> has \*\*([^*]+)\*\* chance', content)
#         no_mega = re.search(r'No <:spM:\d+> left today\.', content)
#
#         if mega_match: mega_str = f"{mega_emoji}{mega_match.group(1)}{kekmark_emoji}"
#         elif no_mega: mega_str = f"{mega_emoji}:x:"
#         else: mega_str = f"{mega_emoji}:question:"
#
#         p8_match = re.search(r'\(Perk 8\).*?Clicked today:\s*\*\*(\d+)\*\*/(\d+)\.\s*Rolled today:\s*\*\*(\d+)\*\*/(\d+)', content)
#         p8_str = f"{p8_match.group(1)}/{p8_match.group(2)} | {p8_match.group(3)}/{p8_match.group(4)}" if p8_match else "0/40 | 0/?"
#
#         buttons_match = re.search(r'\*\*(\d+)/(\d+)\*\*\s*buttons clicked', content)
#         buttons_str = f"{buttons_match.group(1)}/{buttons_match.group(2)}" if buttons_match else "0/10"
#
#         p9_match = re.search(r'\(Perk 9\).*?Rolled today:\s*\*\*(\d+)\*\*/(\d+)', content)
#         p9_str = f"{p9_match.group(1)}/{p9_match.group(2)}" if p9_match else "0/6"
#
#         perks_string = f"{sphere_8}: {p8_str}, {sphere_9}: {buttons_str} | {p9_str}"
#
#         if current_user in ["hyperlexus", "ad.infernum"]:
#             if self.absolute_toggle:
#                 keys_time = keys_time_abs
#             else:
#                 keys_time = keys_time_rel
#             key_string = "" if int(
#                 keys_val) == 4500 else f"{key_emoji}{keys_val}, {keys_time}, {bku_prob} {omega_emoji}{omega_keys}\n"
#             power_match = re.search(r'Power: \*\*(\d+)%\*\*', content)
#             current_power = int(power_match.group(1)) if power_match else 100
#             cost_match = re.search(r'Each kakera button consumes (\d+)% of your reaction power', content)
#             base_cost = float(cost_match.group(1)) if cost_match else 34.0
#
#             cost_quarter = base_cost / 4.0
#             cost_half = base_cost / 2.0
#             cost_full = base_cost
#             max_p = self.max_power.get(current_user, 110)
#
#             p8_c_val = get_power_display(current_power, cost_quarter, current_tz, self.absolute_toggle)
#             p8_val = get_power_display(current_power, cost_half, current_tz, self.absolute_toggle)
#             full_val = get_power_display(current_power, cost_full, current_tz, self.absolute_toggle)
#             max_val = get_power_display(current_power, max_p, current_tz, self.absolute_toggle, is_cap=True)
#
#             power_line = f"{k_stock}{kakera_emoji}{current_power}% | {sphere_w8}{p8_c_val}, {sphere_8}{p8_val},{kakera_emoji}{full_val}, :warning:{max_val}\n"
#
#             result = (
#                 f"**{current_user}**:\n"
#                 f"{rolls}{stack_rolls_emoji} {rolls_time_abs}🕐 {rt_stock}{add_roll_emoji} {claim_str_abs}\n"
#                 f"{daily_abs}📅 {vote_abs}🗳️ {dk_abs}💸 {rt_abs}{dollar_rt_emoji} {p_abs}{poke_emoji}\n"
#                 f"{key_string}"
#                 f"{power_line}"
#                 f"{sp_stock}{spheres_emoji} | {o_string} | {mega_str}\n"
#                 f"{perks_string}"
#             ) if self.absolute_toggle else (
#                 f"**{current_user}**:\n"
#                 f"{rolls}{stack_rolls_emoji} {rolls_time_rel}🕐 {rt_stock}{add_roll_emoji} {claim_str_rel}\n"
#                 f"{daily_rel}📅 {vote_rel}🗳️ {dk_rel}💸 {rt_rel}{dollar_rt_emoji} {p_rel}{poke_emoji}\n"
#                 f"{key_string}"
#                 f"{power_line}"
#                 f"{sp_stock}{spheres_emoji} | {o_string} | {mega_str}\n"
#                 f"{perks_string}"
#             )
#         else: return None  # artefact from when we had different users with different code. might need it again
#
#         if message.id != self.last_message_reacted_to:
#             self.last_message_reacted_to = message.id
#             return await message.channel.send(result)
#         return None
#
#     @slash_command(name='toggle_tu_message')
#     async def flip_tu_message(self, ctx: ApplicationContext):
#         if ctx.author.id != 422800248935546880:
#             await ctx.respond("you are not authorised to use this command.")
#             return
#
#         self.absolute_toggle = not self.absolute_toggle
#         await ctx.respond(kekmark_emoji)
#         return
#
#
# def setup(bot):
#     bot.add_cog(MudaeCog(bot))

import io
import re
import math
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

import discord
from discord.ext.commands import Cog, slash_command
from discord import ApplicationContext
from html2image import Html2Image
from jinja2 import Template


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


def format_absolute(t, tz_name="Europe/Berlin"):
    now = datetime.now(ZoneInfo(tz_name))
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
    hours_diff = (dt.date() - now.date()).seconds // 3600
    time_str = dt.strftime("%H:%M")
    if hours_diff > 24:
        return f"{time_str} +{hours_diff // 24}d"
    return time_str


def format_power_time(minutes, tz_name, is_absolute):
    if minutes <= 0:
        return "max"
    if is_absolute:
        now = datetime.now(ZoneInfo(tz_name))
        dt = now + timedelta(minutes=minutes)
        hours_diff = (dt.date() - now.date()).seconds // 3600
        time_str = dt.strftime("%H:%M")
        if hours_diff > 24:
            return f"{time_str} +{hours_diff // 24}d"
        return time_str
    else:
        hrs = minutes // 60
        mins = minutes % 60
        if hrs > 0 and mins > 0:
            return f"{hrs}:{mins:02d}h"
        elif hrs > 0:
            return f"{hrs}h"
        else:
            return f"{mins}m"


def get_power_display(current_power, target, tz_name, is_absolute, mode="count"):
    """
    mode:
      - "count": returns '2x', '4x' when reached, timer when not.
      - "check": returns '✓' when reached, timer when not.
      - "cap": returns 'max' when reached, timer when not.
    """
    if current_power >= target:
        if mode == "cap":
            return "max"
        elif mode == "check":
            return "✓"
        count = int(current_power // target)
        return f"{count}x"
    mins_needed = math.ceil((target - current_power) * 3)
    return format_power_time(mins_needed, tz_name, is_absolute)


def get_o_value(content, o_type):
    match = re.search(r'\*\*(\d+)\*\*\s*' + o_type + r'(?:[^*(]*\(\+\*\*(\d+)\*\*\s*stored\))?', content)
    if match:
        base = int(match.group(1))
        stored = int(match.group(2)) if match.group(2) else 0
        return str(base + stored)
    return "0"


class MudaeCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_users = ["hyperlexus", "ad.infernum"]
        self.mudae_id = 432610292342587392
        self.servers_to_search = [1486857971060445186, 995966314877300737, 1494713422271746139]
        self.last_message_reacted_to = 0
        self.absolute_toggle = True

        self.max_power = {
            "hyperlexus": 110,
            "ad.infernum": 100
        }

        self.hti = Html2Image(size=(540, 380))
        self.template_path = "Storage/mudae/mudaeTemplate.html"

    def render_card_to_bytes(self, context: dict) -> io.BytesIO:
        """Reads template, injects variables via Jinja2, and returns in-memory PNG bytes."""
        with open(self.template_path, "r", encoding="utf-8") as f:
            template_str = f.read()

        template = Template(template_str)
        rendered_html = template.render(**context)

        raw_png = self.hti.screenshot(
            html_str=rendered_html,
            save_as="mudae_card_temp.png"
        )[0]

        with open(raw_png, "rb") as f:
            buffer = io.BytesIO(f.read())
        buffer.seek(0)
        return buffer

    @Cog.listener()
    async def on_message(self, message):
        if self.bot.voice_clients: return None
        if message.guild is None or message.guild.id is None or (message.guild.id not in self.servers_to_search): return
        if message.author.id != self.mudae_id:
            if not message.author.name.lower().startswith("mudae"): return None

        content = message.content
        current_user = None
        for user in self.target_users:
            if content.startswith(f"**{user}**,"):
                current_user = user
                break

        if not current_user: return None
        if "rolls left" not in content and "rolls reset" not in content: return None

        try:
            await message.delete()
        except (discord.Forbidden, discord.NotFound):
            pass

        current_tz = "America/New_York" if current_user == "ad.infernum" else "Europe/Berlin"

        current_time_str = datetime.now(ZoneInfo(current_tz)).strftime("%H:%M")

        rolls = extract(r'You have \*\*(\d+)\*\* rolls left', content)
        rt_stock = extract(r'You have \*\*(\d+)\*\* rolls reset', content)

        rolls_class = "ready-bg" if int(rolls.replace(",", "") or 0) > 0 else ""

        claim_yes = re.search(r'next claim reset is in \*\*([^*]+)\*\*', content)
        claim_no = re.search(r'you can\'t claim for another \*\*([^*]+)\*\*', content)
        if claim_yes:
            claim_text = format_absolute(claim_yes.group(1), current_tz) if self.absolute_toggle else format_relative(
                claim_yes.group(1))
            claim_class = "ready"
        elif claim_no:
            claim_text = format_absolute(claim_no.group(1), current_tz) if self.absolute_toggle else format_relative(
                claim_no.group(1))
            claim_class = "cooldown"
        else:
            claim_text = "ready"
            claim_class = "ready"

        dk_match = re.search(r'Next \$dk in \*\*([^*]+)\*\*', content)
        dk_time = (format_absolute(dk_match.group(1), current_tz) if self.absolute_toggle else format_relative(
            dk_match.group(1))) if dk_match else "r"

        vote_match = re.search(r'vote again in \*\*([^*]+)\*\*', content)
        vote_time = (format_absolute(vote_match.group(1), current_tz) if self.absolute_toggle else format_relative(
            vote_match.group(1))) if vote_match else "ready"

        daily_match = re.search(r'Next \$daily reset in \*\*([^*]+)\*\*', content)
        daily_time = (format_absolute(daily_match.group(1), current_tz) if self.absolute_toggle else format_relative(
            daily_match.group(1))) if daily_match else "ready"

        rt_cd_match = re.search(r'The cooldown of \$rt is not over\. Time left: \*\*([^*]+)\*\*', content)
        if re.search(r'\$rt is available!', content):
            rt_time = "ready"
        elif rt_cd_match:
            rt_time = format_absolute(rt_cd_match.group(1), current_tz) if self.absolute_toggle else format_relative(
                rt_cd_match.group(1))
        else:
            rt_time = "?"

        p_cd_match = re.search(r'Remaining time before your next \$p: \*\*([^*]+)\*\*', content)
        if re.search(r'\$p is available!', content):
            p_time = "ready"
        elif p_cd_match:
            p_time = format_absolute(p_cd_match.group(1), current_tz) if self.absolute_toggle else format_relative(
                p_cd_match.group(1))
        else:
            p_time = "?"

        k_stock = extract(r'Stock: \*\*([\d,]+)\*\*\s*<:kakera', content)
        sp_stock = extract(r'Stock: \*\*([\d,]+)\*\*\s*<:sp', content, default="0")

        keys_val = extract(r'\*\*([\d,]+)\*\*\s*<:kakera[^>]+>to collect', content).replace(",", "").replace(".", "")
        bku_prob = extract(r'\$bku on your next \$sw: \*\*([^*]+)\*\*', content, default="0%")
        omega_keys = extract(r'\*\*([\d,]+)\*\*\s*<:omegakey', content, default="0").replace(",", "")

        oh_val = get_o_value(content, r'\$oh')
        oc_val = get_o_value(content, r'\$oc')
        oq_val = get_o_value(content, r'\$oq')
        ot_val = get_o_value(content, r'\$ot')

        oh_class = "ready-bg" if int(oh_val) > 0 else ""
        oc_class = "ready-bg" if int(oc_val) > 0 else ""
        oq_class = "ready-bg" if int(oq_val) > 0 else ""
        ot_class = "ready-bg" if int(ot_val) > 0 else ""

        mega_match = re.search(r'Next <:spM:\d+> has \*\*([^*]+)\*\* chance', content)
        no_mega = re.search(r'No <:spM:\d+> left today\.', content)
        mega_disabled = bool(no_mega)
        mega_text = mega_match.group(1) if mega_match else ("0%" if no_mega else "?")

        p8_match = re.search(r'\(Perk 8\).*?Clicked today:\s*\*\*(\d+)\*\*/(\d+)\.\s*Rolled today:\s*\*\*(\d+)\*\*/(\d+)', content)
        p8_str = f"{p8_match.group(3)}/{p8_match.group(4)}, {p8_match.group(1)}/{p8_match.group(2)}" if p8_match else "?, 0/40"

        buttons_match = re.search(r'\*\*(\d+)/(\d+)\*\*\s*buttons clicked', content)
        buttons_str = f"{buttons_match.group(1)}/{buttons_match.group(2)}" if buttons_match else "0/10"

        p9_match = re.search(r'\(Perk 9\).*?Rolled today:\s*\*\*(\d+)\*\*/(\d+)', content)
        p9_str = f"{p9_match.group(1)}/{p9_match.group(2)}" if p9_match else "?"

        power_match = re.search(r'Power: \*\*(\d+)%\*\*', content)
        current_power = int(power_match.group(1)) if power_match else 100
        cost_match = re.search(r'Each kakera button consumes (\d+)% of your reaction power', content)
        base_cost = float(cost_match.group(1)) if cost_match else 34.0

        cost_quarter = base_cost / 4.0
        cost_half = base_cost / 2.0
        cost_full = base_cost
        cost_double = base_cost * 2.0

        max_p = float(self.max_power.get(current_user, 110.0))

        bar_fill_pct = min((current_power / max_p) * 100.0, 100.0)
        pos_quarter = min((cost_quarter / max_p) * 100.0, 100.0)
        pos_half = min((cost_half / max_p) * 100.0, 100.0)
        pos_full = min((cost_full / max_p) * 100.0, 100.0)
        pos_double = min((cost_double / max_p) * 100.0, 100.0)

        q_val = get_power_display(current_power, cost_quarter, current_tz, self.absolute_toggle, mode="count")
        h_val = get_power_display(current_power, cost_half, current_tz, self.absolute_toggle, mode="count")
        f_val = get_power_display(current_power, cost_full, current_tz, self.absolute_toggle, mode="count")
        d_val = get_power_display(current_power, cost_double, current_tz, self.absolute_toggle, mode="check")
        m_val = get_power_display(current_power, max_p, current_tz, self.absolute_toggle, mode="cap")

        kakera_box_class = "ready-bg"
        react_class = "ready"
        react_status = "?"
        if current_power == max_p:
            react_status = "max"
        elif current_power >= cost_double:
            react_status = "ready"
        elif current_power >= cost_full:
            react_status = "valuable"
        elif current_power >= cost_half:
            react_status = "p8 / " + f_val
            react_class = "cooldown"
        elif current_power >= cost_quarter:
            react_status = "p8 + y10 / " + h_val + " / " + f_val
            react_class = "cooldown"
        elif current_power < cost_quarter:
            react_status = "cooked"
            kakera_box_class = "warning-bg"
            react_class = "cooldown"

        context = {
            "user": current_user,
            "current_time": current_time_str,
            "rolls": rolls,
            "rt_stock": rt_stock,
            "rolls_class": rolls_class,
            "claim_class": claim_class,
            "claim_text": claim_text,
            "react_class": react_class,
            "react_status": react_status,
            "kakera_box_class": kakera_box_class,
            "daily_time": daily_time,
            "vote_time": vote_time,
            "dk_time": dk_time,
            "rt_time": rt_time,
            "p_time": p_time,
            "bku_amount": keys_val,
            "bku_prob": bku_prob,
            "omega_keys": omega_keys,
            "k_stock": k_stock,
            "current_power": current_power,
            "max_p_lbl": f"{max_p:g}%",
            "bar_fill_pct": f"{bar_fill_pct:.1f}",
            "pos_quarter": f"{pos_quarter:.1f}",
            "pos_half": f"{pos_half:.1f}",
            "pos_full": f"{pos_full:.1f}",
            "pos_double": f"{pos_double:.1f}",
            "reached_q": current_power >= cost_quarter,
            "reached_h": current_power >= cost_half,
            "reached_f": current_power >= cost_full,
            "reached_d": current_power >= cost_double,
            "q_val": q_val,
            "h_val": h_val,
            "f_val": f_val,
            "d_val": d_val,
            "m_val": m_val,
            "oh_val": oh_val,
            "oc_val": oc_val,
            "oq_val": oq_val,
            "ot_val": ot_val,
            "oh_class": oh_class,
            "oc_class": oc_class,
            "oq_class": oq_class,
            "ot_class": ot_class,
            "sp_stock": sp_stock,
            "p8_str": p8_str,
            "p9_str": f"{buttons_str}",
            "mega_disabled": mega_disabled,
            "mega_text": mega_text
        }

        if message.id != self.last_message_reacted_to:
            self.last_message_reacted_to = message.id

            img_buffer = self.render_card_to_bytes(context)
            discord_file = discord.File(fp=img_buffer, filename="mudae_status.png")

            return await message.channel.send(file=discord_file)
        return None

    @slash_command(name='toggle_tu_message')
    async def flip_tu_message(self, ctx: ApplicationContext):
        if ctx.author.id != 422800248935546880:
            await ctx.respond("you are not authorised to use this command.")
            return

        self.absolute_toggle = not self.absolute_toggle
        await ctx.respond("<:kekmark:1506816979804229752>")
        return


def setup(bot):
    bot.add_cog(MudaeCog(bot))