import io
import re
import math
import functools
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
        self.target_users = ["hyperlexus", "alvideiectiones", "julisus"]
        self.mudae_id = 432610292342587392
        self.servers_to_search = [1486857971060445186, 995966314877300737, 1494713422271746139]
        self.last_message_reacted_to = 0
        self.absolute_toggle = True

        self.max_power = {
            "hyperlexus": 115,
            "ad.infernum": 110,
            "alvideiectiones": 110,
            "julisus": 100
        }

        self.hti = Html2Image(
            size=(540, 400),
            custom_flags=[
                '--disable-gpu',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--headless=new',
                '--hide-scrollbars',
                '--force-device-scale-factor=1',
                '--default-background-color=00000000'
            ]
        )
        self.template_path = "Storage/mudae/mudaeTemplate.html"
        with open(self.template_path, "r", encoding="utf-8") as f:
            self.template = Template(f.read())

    def render_card_to_bytes(self, context: dict) -> io.BytesIO:
        """Reads template, injects variables via Jinja2, and returns in-memory PNG bytes."""
        rendered_html = self.template.render(**context)

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

        match current_user:
            case "ad.infernum":
                current_tz = "Pacific/Honolulu"
            case "alvideiectiones":
                current_tz = "Asia/Tokyo"
            case _:
                current_tz = "Europe/Berlin"

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
            claim_text = format_absolute(claim_no.group(1), current_tz) if self.absolute_toggle else format_relative(claim_no.group(1))
            claim_class = "cooldown"
        else:
            claim_text = "ready"
            claim_class = "ready"

        dk_match = re.search(r'Next \$dk in \*\*([^*]+)\*\*', content)
        dk_time = (format_absolute(dk_match.group(1), current_tz) if self.absolute_toggle else format_relative(
            dk_match.group(1))) if dk_match else "ready"

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
        react_status = "?"  # this is currently unused and not displayed anywhere
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
            "react_status": react_status,  # unused
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

            render_function = functools.partial(self.render_card_to_bytes, context)

            img_buffer = await self.bot.loop.run_in_executor(None, render_function)
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