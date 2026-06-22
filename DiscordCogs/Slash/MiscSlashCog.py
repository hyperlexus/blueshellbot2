import asyncio
import json
import math
import os
import time
import urllib
from datetime import datetime
import aiohttp
from mpmath import mp, mpf, exp
from Music.BlueshellBot import BlueshellBot
from Music.BlueshellBot import blueshell_entire_bot_startup_timestamp
from discord import ApplicationContext, Option, Member
from discord.ext import tasks
from discord.ext.commands import slash_command, Cog
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
from Utils.Utils import Utils
from Utils import rr_api

helper = Helper()

def save_alerts(alerts_list):
    file_path = "alerts.json"
    with open(file_path, "w") as f:
        json.dump(alerts_list, f, indent=4)

def get_alerts():
    file_path = "alerts.json"
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        return json.load(f)


class MiscSlashCog(Cog):
    def __init__(self, bot: BlueshellBot) -> None:
        self.__bot: BlueshellBot = bot
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()
        self.check_alerts.start()

    @slash_command(name='uptime', description="get time since last restart")
    async def uptime(self, ctx: ApplicationContext) -> None:
        await ctx.respond(embed=self.__embeds.UPTIME(str(datetime.now() - blueshell_entire_bot_startup_timestamp)[:-7]))
        return

    @slash_command(name='alert', description="set a reminder for yourself or others")
    async def alert(self, ctx: ApplicationContext, time_input: str = Option(description="time (10m, 1h, t20:00, etc.)",),
                    message: str = Option(description="alert description"),
                    target_user: Member = Option(Member, description="target user", default=None)):
        await ctx.defer()

        time_str = Utils.seconds_until(time_input[1:]) if time_input.startswith('t') else time_input
        seconds = Utils.convert_to_s(time_str)

        if seconds is None:
            return await ctx.respond(embed=self.__embeds.BAD_ALERT(time_input))

        send_at = time.time() + seconds
        target_id = target_user.id if target_user else ctx.author.id

        alerts = get_alerts()
        alerts.append({
            "user_id": target_id,
            "author_id": ctx.author.id,
            "channel_id": ctx.channel_id,
            "text": message,
            "send_at": send_at,
            "original_time": time_str
        })
        save_alerts(alerts)

        return await ctx.respond(embed=self.__embeds.ALERT_SET(time_str))


    @slash_command(name='festgelegte_vertrege', description='vertrag mit der bank ausrechnen')
    async def vertrege(self, ctx: ApplicationContext,
                       geld: Option(int, "Geld"),
                       rate: Option(int, "Rückzahlrate in %")
                       ) -> None:
        if rate > 100 or rate < 1:
            await ctx.respond("prozent von 1 bis 100")
            return
        if geld < 1000:
            await ctx.respond("1000 ist untergrenze für geld bratan")
            return
        if geld > 1000000:
            await ctx.respond("du kannst dir nicht mehr als 1e6 geld leihen")
            return

        def regerplatz(geld2, rate2):
            return math.ceil(geld2 ** 0.5 / 10) / (4 * rate2)

        result = geld, rate, int(regerplatz(geld, rate)*100), int(geld*(1+regerplatz(geld, rate)))
        await ctx.respond(embed=self.__embeds.FESTGELEGTE_VERTREGE_EMBED(result[0], result[1], result[2], result[3]))
        return

    @slash_command(name='money_calculator', description='check to what number you have to count to get a certain amount of money')
    async def rule_vanilla_equivalent(self, ctx: ApplicationContext,
                                      goal_money: Option(int,"Money you want to reach."),
                                      vanilla_number: Option(int, "Vanilla number. If you use this, goal money is disregarded.") = None,
                                      div_rules: Option(str, "Division rules. Enter like this: '2,3,5'") = None,
                                      digsum_rules: Option(str, "Digsum rules. Enter like this: '2,3,4'") = None,
                                      root_rules: Option(str, "Root rules. Enter like this: '2,3,5'") = None,
                                      total_bonus_factor: Option(float, "Your total bonus factor when counting. e.g. 1.5") = 1.0
                                      ):
        try:
            if div_rules in ("1", "0", "1,", ",1"):
                await ctx.respond("you can't do that, and you know you can't. so don't do it. easy.")
                return
            div_rules = Utils.convert_rules_to_list(div_rules, "div")
            digsum_rules = Utils.convert_rules_to_list(digsum_rules, "dig")
            root_rules = Utils.convert_rules_to_list(root_rules, "root")

            there_are_rules = bool(div_rules) or bool(digsum_rules) or bool(root_rules)

            if div_rules == -1 or digsum_rules == -1 or root_rules == -1:
                await ctx.respond("something went wrong when parsing rules. please try again and make sure to follow the format.")
                return

            digsum_rules_set = set(digsum_rules) if digsum_rules else set()

            raw_target_money = goal_money
            if vanilla_number is not None:
                raw_target_money = vanilla_number * (vanilla_number + 1) // 2

            sum_no_rules = raw_target_money / total_bonus_factor
            vanilla_number_goal = math.ceil((-1 + math.sqrt(1 + 8 * goal_money)) / 2)
            if vanilla_number is not None:
                sum_no_rules = vanilla_number * (vanilla_number + 1) // 2

            def divcheck(num):
                return any(num % divisor == 0 for divisor in div_rules)

            def digsumcheck(num):
                if not digsum_rules_set: return False
                total = 0
                while num > 0:
                    total += num % 10
                    num //= 10
                return total in digsum_rules_set

            def rootcheck(num):
                return any(round(num ** (1.0 / n)) ** n == num for n in root_rules)

            number = 1
            sum_rules = 0
            amount_numbers = 0
            while sum_rules < sum_no_rules:
                number += 1
                if divcheck(number) or rootcheck(number) or digsumcheck(number):
                    continue
                amount_numbers += 1
                sum_rules += number

            efficiency = vanilla_number_goal / amount_numbers - 1
            efficiency = round(efficiency * 100, 2)  # no longer disgusting rounding, yay

            answer_string = f"you would need to count up to number {number} to get more than "
            answer_string += f"the equivalent of {vanilla_number} in vanilla" if goal_money is None else f"{goal_money} money"
            answer_string += f"\nThe following rules were applied: div: {div_rules}, digsum: {digsum_rules}, root: {root_rules}" if there_are_rules else ""
            answer_string += f"\n calculated with a {total_bonus_factor}x multiplier." if total_bonus_factor != 1.0 else ""
            answer_string += f"\nThis equals {amount_numbers+1} actual counts in total. This is {efficiency}% more efficient than without any rules." if there_are_rules else ""
            answer_string += f"\nPlease keep in mind that this is total money, and you only get a maximum of 50% ~~+1~~ of that when counting"
            await ctx.respond(answer_string)
            return
        except Exception as e:
            await ctx.respond("ich war zu faul für vernünftiges error handling. machs bitte einfach richtig bro")
            await ctx.respond(e)
            return

    @slash_command(name='trophy_chance_calculator', description='check how likely you are to win a trophy')
    async def trophy_chance_calculator(self, ctx: ApplicationContext, number: Option(int, "number to calculate rate for")) -> None:
        if number < 1 or number > 25000000:
            await ctx.respond("zahl von 1 bis 2.5e7 bitte")
            return

        def formula(n, precision, inverse):
            mp.dps = precision
            formula_result = (
                    mpf('150') +
                    mpf('1000') * exp(mpf('-0.02') * mpf(n)) +
                    mpf('100') * exp(mpf('-0.001') * mpf(n))
            )
            return 1 / formula_result if inverse else formula_result

        def get_trophy_chance(n, inverse):
            precision = 1500
            value = formula(n, precision, inverse)
            value_string = mp.nstr(value, precision)
            for i, digit in enumerate(value_string):
                if i < 4 and not inverse or i < 5 and inverse:
                    continue
                else:
                    if not inverse:
                        if digit != "0":
                            return i + 5, str(formula(n, i + 5, inverse))
                    else:
                        if digit != "9":
                            return i + 5, str(formula(n, i + 5, inverse))
            return -1, str(mpf('1') / mpf('150')) if inverse else "150"

        result = get_trophy_chance(number, False)
        result_inverse = get_trophy_chance(number, True)
        if result[0] == -1:
            await ctx.respond("this is so precise, 1500 digits of precision couldn't handle it, the message would've been too long")
            return

        output_string = f"chance for a trophy for number {number} is {result_inverse[1]}%, or 1 in {result[1]} with precision of {result[0]} digits"
        if number > 10000:
            output_string = "This is a big number so the numbers can get very huge and long. Be careful\n" + output_string
        await ctx.respond(output_string)

    @slash_command(name='rr_rooms', description='returns good rr rooms')
    async def good_rooms(self, ctx: ApplicationContext):
        vr_data = rr_api.readable_average_vr(rr_api.calculate_average_vr())
        await ctx.respond(vr_data)
        return

    @slash_command(name='join_best_room', description='provides all fcs of the best room with open host on')
    async def join_best_room(self, ctx: ApplicationContext):
        best_room = rr_api.get_room_by_id(rr_api.get_highest_room_id())
        if not best_room:
            await ctx.respond("the api seems to be down or there are no players at the moment, please start a room!")
            return
        openhost_codes = rr_api.get_all_openhost_fcs_by_room(best_room)
        best_room_vr_count = rr_api.get_average_room_vr(best_room)
        best_room_player_count = rr_api.get_room_player_count(best_room)
        output_string = f"fcs in the room (Avg VR: {round(best_room_vr_count)}, {best_room_player_count} players) with openhost on:\n"
        output_string += "\n".join(openhost_codes) if openhost_codes else "no codes have openhost on in this room."
        await ctx.respond(output_string)
        return

    @slash_command(name='join_a_room', description='lists all fcs with openhost on in a specific room')
    async def join_a_room(self, ctx: ApplicationContext, room_id: Option(str, "Room ID (6 digits)")):
        room = rr_api.get_room_by_id(room_id)
        openhost_codes = rr_api.get_all_openhost_fcs_by_room(room)
        room_vr_count = rr_api.get_average_room_vr(room)
        is_private_room = True if room_vr_count == -1 else False
        room_player_count = rr_api.get_room_player_count(room)
        output_string = f"fcs in the room (Avg VR: {round(room_vr_count)}, {room_player_count} players) with openhost on:\n"
        output_string += "\n".join(openhost_codes) if openhost_codes else "no codes have openhost on in this room."
        if is_private_room:
            output_string += "\nnote that this is a private room and maybe a mogi!"
        await ctx.respond(output_string)
        return

    @slash_command(name='clean', description=helper.HELP_CLEAN)
    async def clean(self, ctx: ApplicationContext,
                    limit = Option(int, "How many messages to delete?", default=20),
                    who = Option(str, "whose messages to clean?", choices=["all", "bot", "user", "saul", "any"], default="all")):
        if Utils.check_if_banned(ctx.author.id, self.__config.PROJECT_PATH):
            await ctx.respond(embed=self.__embeds.BANNED())
            return
        if not ctx.guild:
            await ctx.respond("this command is restricted to servers.")
            return
        if who == "any" and not (ctx.guild.id == 995966314877300737 or ctx.author.guild_permissions.administrator):
            await ctx.respond("you are not authorised to delete everyone's messages, only your own and the bot's.")
            return
        if limit > self.__config.CLEAN_AMOUNT:
            await ctx.respond(embed=self.__embeds.TOO_MANY_CLEAN_QUERIES(limit))
            return

        await ctx.defer(ephemeral=True)

        def should_delete(msg):
            # only delete messages from the bot itself
            if who in ("bot", "all") and msg.author.id == ctx.bot.user.id:
                return True
            if who in ("user", "all") and msg.content.startswith(self.__config.BOT_PREFIX):
                return True
            if who == "any":
                return True
            return False

        inspect_amount = limit if who == "any" else self.__config.CLEAN_AMOUNT
        to_delete = []

        async for message in ctx.channel.history(limit=inspect_amount):
            if len(to_delete) >= limit:
                break
            if should_delete(message):
                to_delete.append(message)

        if to_delete:
            from datetime import datetime, timedelta, timezone
            two_weeks_ago = datetime.now(timezone.utc) - timedelta(days=14)

            bulk_deletable = [m for m in to_delete if m.created_at > two_weeks_ago]
            manual_deletable = [m for m in to_delete if m.created_at <= two_weeks_ago]

            if bulk_deletable:
                await ctx.channel.delete_messages(bulk_deletable)

            if manual_deletable:
                for i, msg in enumerate(manual_deletable):
                    await msg.delete()
                    if (i + 1) % 5 == 0:
                        await asyncio.sleep(1)

        await ctx.channel.send(embed=self.__embeds.CLEANED(limit, len(to_delete), who, inspect_amount), delete_after=10)
        await ctx.respond("messages cleaned.")
        return

    @tasks.loop(seconds=10)
    async def check_alerts(self):
        now = time.time()
        alerts = get_alerts()
        if not alerts: return

        updated_alerts = []
        if_sent_alerts = False

        for alert in alerts:
            if now >= alert['send_at']:
                if_sent_alerts = True
                channel = self.__bot.get_channel(alert['channel_id'])

                if channel:
                    mention = f"<@{alert['user_id']}>"
                    embed = self.__embeds.ALERT_DONE(
                        time_str=alert['original_time'],
                        message=alert['text'],
                    )
                    try:
                        await channel.send(content=mention, embed=embed)
                    except:
                        pass  # leel, maybe she was right and i really shouldn't code

            else:
                updated_alerts.append(alert)

        if if_sent_alerts:
            save_alerts(updated_alerts)

    @check_alerts.before_loop
    async def before_check_alerts(self):
        await self.__bot.wait_until_ready()

    @slash_command(name='restart_compcount',
                   description='compcount gets restarted and all streaks are saved. only runnable by admin')
    async def restart_compcount(self, ctx: ApplicationContext):
        if ctx.interaction.user.id not in (422800248935546880, 468786219258740756):
            await ctx.respond("you are not authorised to do this.")
            return
        await ctx.defer()
        env_variables = os.environ.copy()

        message = await ctx.followup.send("deploying...\n```bash\n\n```", wait=True)

        path = os.getcwd()
        target_path = os.path.abspath(os.path.join(path, "..", "compcountdeploy.sh"))

        process = await asyncio.create_subprocess_exec(
            'sh', target_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            env=env_variables
        )

        async def HURRAH_ICH_VERWENDE_DAS_WAS_MAGGDA_GEZEIGT_HAT(stdout):
            while True:
                line = await stdout.readline()
                if not line:
                    break
                yield line.decode('utf-8')  # leeeeeeeel

        log_lines = []
        last_update_time = asyncio.get_event_loop().time()
        update_interval = 1.5

        async for line in HURRAH_ICH_VERWENDE_DAS_WAS_MAGGDA_GEZEIGT_HAT(process.stdout):
            log_lines.append(line)
            current_time = asyncio.get_event_loop().time()

            if current_time - last_update_time > update_interval:
                full_log = "".join(log_lines)
                
                if len(full_log) > 1900:
                    full_log = "...\n" + full_log[-1850:]
                
                try:
                    await message.edit(content=f"deploying...\n```bash\n{full_log}```")
                except Exception as e:
                    print(f"reingeschissen: {e}")
                
                last_update_time = current_time

        await process.wait()

        full_log = "".join(log_lines)
        if len(full_log) > 1900:
            full_log = "...\n" + full_log[-1850:]
            
        await message.edit(content=f"deployment completed with code {process.returncode}:\n```bash\n{full_log}```")

    async def restart_blueshellbot(self, ctx: ApplicationContext):
        await ctx.defer()
        if ctx.interaction.user.id != 422800248935546880:
            await ctx.respond("you are not authorised to run this command as you are not the bot admin.")
            return

        await ctx.respond("restarting...")
        await asyncio.sleep(0.25)
        path = os.getcwd()
        target_path = os.path.abspath(os.path.join(path, "..", "restart-blueshelly.sh"))

        process = await asyncio.create_subprocess_exec(
            'sh', target_path,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )

    @slash_command(name="base_kakera_calculator",
                       description="calculate a character's ka value based on rank, claims, and keys.")
    async def base_kakera_calculator(self, ctx: ApplicationContext,
            r = Option(int, "claim rank ($top)", min_value=1),
            l = Option(int, "like rank ($topl)", min_value=1),
            left = Option(int, "total number of claimed characters (with $left), 0 for base value", min_value=0),
            keys = Option(int, "number of keys on the character", min_value=0)
    ):
        if keys == 0: ym = 1.0
        elif 1 <= keys < 3: ym = 1.0 + 0.1 * (keys - 1)
        elif 3 <= keys < 6: ym = 1.1 + 0.1 * (keys - 3)
        elif 6 <= keys < 10: ym = 1.3 + 0.1 * (keys - 6)
        else: ym = 1.6 + 0.05 * (keys - 10)
        rl = (r + l) / 2.0
        cm = 1.0 + (left / 5500.0)
        inner_val = 25000 * math.pow(rl + 70, -0.75) + 20
        bv = math.floor(inner_val * cm + 0.5)
        kv = math.floor(bv * ym + 0.5)
        await ctx.respond(f"r: {r}, rl: {rl}, l: {l}, $left: {left}, y: {keys}\n"f"value: {kv}")

    @slash_command(name="lounge_role_request", guild_ids=[1494713422271746139])
    async def lounge_role_request(self, ctx: ApplicationContext,
                                  leaderboard_name = Option(str, "leaderboard name")):

        if Utils.check_if_banned(ctx.author, self.__config.PROJECT_PATH):
            await ctx.respond(embed=self.__embeds.BANNED())
            return
        await ctx.defer(ephemeral=True)

        api_url = "https://gb.hlorenzi.com/api/v1/graphql"
        headers = {
            "Content-Type": "text/plain",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
        }
        graphql_query = f"""{{
            team(teamId: "k3_uU0") {{
                tiers {{
                    name
                    lowerBound
                }}
                player(name: "{leaderboard_name}") {{
                    name
                    rating
                }}
            }}
        }}"""

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, data=graphql_query, headers=headers) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        print(f"API error status {response.status}: {error_text} trying to submit lounge role request")
                        await ctx.respond(f"the leaderboard api is returning an error (code {response.status}).")
                        return
                    data = await response.json()
                    team_data = data.get("data", {}).get("team", {})
                    player_data = team_data.get("player")

                    if not team_data or player_data is None:
                        await ctx.respond(
                            f"couldn't find a player named `{leaderboard_name}` on the leaderboard. double-check the spelling on <https://gb.hlorenzi.com/reg/k3_uU0>.\n"
                            f"leaderboard names are case-sensitive!")
                        return
                    player_rating = player_data.get("rating", 0)
                    tiers = team_data.get("tiers", [])
                    tiers.sort(key=lambda t: t.get("lowerBound", -99999), reverse=True)

                    player_rank = "unknown"
                    for tier in tiers:
                        if player_rating >= tier.get("lowerBound", -99999):
                            player_rank = tier.get("name")
                            break

            except aiohttp.ClientError as e:
                print(f"Network error trying to submit lounge role request: {e}")
                await ctx.respond("the leaderboard site is currently unreachable. try again later.")
                return

        target_channel_id = 1512468097649348658
        target_user_ids = 422800248935546880, 640985620948189186
        safe_name = urllib.parse.quote(leaderboard_name)
        check_url = f"https://gb.hlorenzi.com/reg/k3_uU0/player/{safe_name}"

        await self.__bot.get_channel(target_channel_id).send(
            f"<@{target_user_ids[0]}> <@{target_user_ids[1]}>\n"
            f"<@{ctx.author.id}> has submitted a lounge role request with leaderboard name **{leaderboard_name}**.\n"
            f"their rank is {player_rank} with a rating of {round(player_rating)}.\n"
            f"You can check this player's rating here: <{check_url}>"
        )

        await ctx.respond("your request has been submitted successfully. please be patient as it has to be processed manually.")

def setup(bot):
    bot.add_cog(MiscSlashCog(bot))
