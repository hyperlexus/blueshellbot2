import math
from datetime import datetime
from mpmath import mp, mpf, exp
from Music.BlueshellBot import BlueshellBot
from Music.BlueshellBot import blueshell_entire_bot_startup_timestamp
from discord import ApplicationContext, Option, OptionChoice
from discord.ext.commands import slash_command, Cog
from Config.Helper import Helper
from Config.Embeds import BEmbeds
from Config.Colors import BColors
from Config.Configs import BConfigs
from Utils.Utils import Utils
from Utils.rr_api import calculate_average_vr, readable_average_vr

helper = Helper()

class MiscSlashCog(Cog):
    def __init__(self, bot: BlueshellBot) -> None:
        self.__bot: BlueshellBot = bot
        self.__embeds = BEmbeds()
        self.__colors = BColors()
        self.__config = BConfigs()

    @slash_command(name='uptime', description="get time since last restart")
    async def uptime(self, ctx: ApplicationContext) -> None:
        await ctx.respond(embed=self.__embeds.UPTIME(str(datetime.now() - blueshell_entire_bot_startup_timestamp)[:-7]))

    @slash_command(name='festgelegte_vertrege', description='vertrag mit der bank ausrechnen')
    async def vertrege(self, ctx: ApplicationContext,
                       geld: Option(int, "Geld"),
                       rate: Option(int, "Rückzahlrate in %")
                       ) -> None:
        if rate > 100 or rate < 1:
            await ctx.respond("prozent von 1 bis 100")
        if geld < 1000:
            await ctx.respond("1000 ist untergrenze für geld bratan")
        if geld > 1000000:
            await ctx.respond("du kannst dir nicht mehr als 1e6 geld leihen")

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
                                      root_rules: Option(str, "Root rules. Enter like this: '2,3,5'") = None
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

            sum_no_rules = goal_money
            vanilla_number_goal = math.ceil((-1 + math.sqrt(1 + 8 * goal_money)) / 2)
            if vanilla_number is not None:
                sum_no_rules = vanilla_number * (vanilla_number + 1) // 2

            def divcheck(num):
                return any(num % divisor == 0 for divisor in div_rules)

            def digsumcheck(num):
                return any(sum(int(n) for n in str(num)) == m for m in digsum_rules)

            def rootcheck(num):
                return any(int(num ** (1 / n)) ** n == num for n in root_rules)

            number = 1
            sum_rules = 0
            amount_numbers = 0
            while sum_rules < sum_no_rules:
                number += 1
                if divcheck(number) or digsumcheck(number) or rootcheck(number):
                    continue
                amount_numbers += 1
                sum_rules += number

            efficiency = vanilla_number_goal / amount_numbers - 1
            efficiency = int(efficiency*10000) / 100  # disgusting rounding because floats are stupid

            answer_string = f"you would need to count up to number {number} to get more than "
            answer_string += f"the equivalent of {vanilla_number} in vanilla" if goal_money is None else f"{goal_money} money"
            answer_string += f"\nThe following rules were applied: div: {div_rules}, digsum: {digsum_rules}, root: {root_rules}" if there_are_rules else ""
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
            result = (
                    mpf('200') +
                    mpf('600') * exp(mpf('-0.045') * mpf(n)) +
                    mpf('225') * exp(mpf('-0.0015') * mpf(n))
            )
            return 1 / result if inverse else result

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
            return -1, 200 if inverse else 0.005

        result = get_trophy_chance(number, False)
        result_inverse = get_trophy_chance(number, True)
        if result[0] == -1:
            await ctx.respond("this is so precise, 1500 digits of precision couldn't handle it, the message would've been too long")
            return

        output_string = f"chance for a trophy for number {number} is {result_inverse[1]}%, or 1 in {result[1]} with precision of {result[0]} digits"
        if number > 10000:
            output_string = "This is a big number so the numbers can get very huge and long. Be careful\n" + output_string
        await ctx.respond(output_string)

    @slash_command(name='good_rooms', description='returns good rr rooms')
    async def good_rooms(self, ctx: ApplicationContext):
        vr_data = readable_average_vr(calculate_average_vr())
        await ctx.respond(vr_data)


def setup(bot):
    bot.add_cog(MiscSlashCog(bot))
