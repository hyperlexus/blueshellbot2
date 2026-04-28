import discord
from discord.ext.commands import slash_command, Cog
from Config.Configs import BConfigs
import sqlite3
import re

SCORE_PATTERN = re.compile(r'(?:👑\s*)?([1-6X])/6:')
PING_PATTERN = re.compile(r'<@!?(\d+)>')
BROKEN_PING_PATTERN = re.compile(r'(?<!<)@([^\s<]+)')
STREAK_PATTERN = re.compile(r'on a (\d+) day streak', re.IGNORECASE)

name_fix_dict = {
    "MAGG🦒À": 468786219258740756,
    "Alvi Deiectiones": 649457215564152852,
    "Yoon fanboy <3": 422800248935546880,
    "his plug <3": 290148556776407050,
    "his hole <3": 712625082169688094,
    "Alex fangirl <3": 1291879618282000466,
    "Jiaxing Fu femboy <3": 649457215564152852,
    "his eva <3": 1291879618282000466,
    "her hitler <3": 422800248935546880,
    "his booktok girl <3": 1291879618282000466,
    "her biker boy <3": 422800248935546880,
    "their nigger <3": 649457215564152852,  # not my bad he named himself that
    "Polo G": 593025049775308810,
    "Saito": 422800248935546880,
    "bin kein schinese": 422800248935546880,
}

GUILD_ID = 995966314877300737
WORDLE_CHANNEL_ID = 1412420988037107723
WORDLE_BOT_ID = 1211781489931452447

class WordleCog(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.__config = BConfigs()

        self.conn = sqlite3.connect('wordle_stats.db')
        self.cursor = self.conn.cursor()
        self._setup_db()

    def _setup_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                user_id TEXT PRIMARY KEY,
                played INTEGER DEFAULT 0,
                score_1 INTEGER DEFAULT 0,
                score_2 INTEGER DEFAULT 0,
                score_3 INTEGER DEFAULT 0,
                score_4 INTEGER DEFAULT 0,
                score_5 INTEGER DEFAULT 0,
                score_6 INTEGER DEFAULT 0,
                score_x INTEGER DEFAULT 0
            )
        ''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS server_data (key TEXT PRIMARY KEY, value INTEGER)''')
        self.conn.commit()

    def _update_db_for_user(self, user_id: str, score: str):
        self.cursor.execute('INSERT OR IGNORE INTO stats (user_id) VALUES (?)', (user_id,))
        self.cursor.execute('UPDATE stats SET played = played + 1 WHERE user_id = ?', (user_id,))

        score_column = f'score_{score.lower()}'
        self.cursor.execute(f'UPDATE stats SET {score_column} = {score_column} + 1 WHERE user_id = ?', (user_id,))
        self.conn.commit()

    async def _parse_wordle_summary(self, message: discord.Message):
        streak_match = STREAK_PATTERN.search(message.content)
        if streak_match:
            streak = int(streak_match.group(1))
            self.cursor.execute('SELECT value FROM server_data WHERE key = "total_days"')
            row = self.cursor.fetchone()
            current_streak = row[0] if row else 0

            if streak > current_streak:
                self.cursor.execute('INSERT OR REPLACE INTO server_data (key, value) VALUES (?, ?)',("total_days", streak))
                self.conn.commit()

        lines = message.content.split('\n')

        for line in lines:
            score_match = SCORE_PATTERN.search(line)
            if not score_match:
                continue

            score = score_match.group(1)

            for broken_name, actual_id in name_fix_dict.items():
                if f"@{broken_name}" in line:
                    self._update_db_for_user(actual_id, score)
                    line = line.replace(f"@{broken_name}", "")

            proper_pings = PING_PATTERN.findall(line)
            for user_id in proper_pings:
                self._update_db_for_user(user_id, score)

            broken_pings = BROKEN_PING_PATTERN.findall(line)
            for username in broken_pings:
                member = discord.utils.find(
                    lambda m: m.name.lower() == username.lower() or m.display_name.lower() == username.lower(),
                    message.guild.members if message.guild else []
                )
                if member:
                    self._update_db_for_user(str(member.id), score)
                else:
                    return False, username

        return True, None

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id != WORDLE_CHANNEL_ID:
            return

        if message.author.id == WORDLE_BOT_ID and "Here are yesterday's results:" in message.content:
            success, bad_name = await self._parse_wordle_summary(message)

            if not success: await message.channel.send(f" <@422800248935546880> name not in ping or in dict: {bad_name}")

    @slash_command(name="sync_wordle", description="sync wordle", guild_ids=[GUILD_ID])
    @discord.default_permissions(administrator=True)
    async def sync_wordle(self, ctx: discord.ApplicationContext) -> None:
        if ctx.channel.id != WORDLE_CHANNEL_ID:
            await ctx.respond(f"error: not in <#{WORDLE_CHANNEL_ID}>.", ephemeral=True)
            return
        await ctx.defer()

        self.cursor.execute('DELETE FROM stats')
        self.cursor.execute('DELETE FROM server_data')
        self.conn.commit()

        count = 0
        async for message in ctx.channel.history(limit=None, oldest_first=True):
            if message.author.id == WORDLE_BOT_ID and "Here are yesterday's results:" in message.content:

                success, bad_name = await self._parse_wordle_summary(message)

                if not success:
                    await ctx.respond(f"{bad_name}, {message}")
                    return

                count += 1

        await ctx.respond(f"{count}")

    @slash_command(name="wordle_stats", description="Show server wordle statistics", guild_ids=[GUILD_ID, 964302006091128893, 1494713422271746139])
    async def wordle_stats(
            self,
            ctx: discord.ApplicationContext,
            target_user: discord.Member = discord.Option(discord.Member, "specific user", required=False, default=None)
    ) -> None:

        self.cursor.execute('SELECT value FROM server_data WHERE key = "total_days"')
        streak_result = self.cursor.fetchone()

        total_days = streak_result[0] if streak_result else 1

        if target_user:
            self.cursor.execute('SELECT * FROM stats WHERE user_id = ?', (str(target_user.id),))
            row = self.cursor.fetchone()

            if not row:
                await ctx.respond(f"no stats for {target_user.display_name}.")
                return

            user_id, played, s1, s2, s3, s4, s5, s6, sx = row
            wins = s1 + s2 + s3 + s4 + s5 + s6

            # x = 7 guesses according to nyt
            total_geses = (s1 * 1) + (s2 * 2) + (s3 * 3) + (s4 * 4) + (s5 * 5) + (s6 * 6) + (sx * 7)

            avg_score = total_geses / played if played > 0 else 0
            win_rate = (wins / played) * 100 if played > 0 else 0
            play_rate = (played / total_days) * 100 if total_days > 0 else 0

            embed = discord.Embed(title=f"User Stats for {target_user.display_name}", color=discord.Color.blue())

            summary = f"Wins: **{wins}**\nPlayed: {played}\nWin Rate: {win_rate:.1f}%\nPlay rate: {play_rate:.1f}%\nAverage Guesses: **{avg_score:.2f}**/6"
            embed.add_field(name="statistics", value=summary, inline=False)

            breakdown_breakdown = (
                f"1️⃣ {s1}\n"
                f"2️⃣ {s2}\n"
                f"3️⃣ {s3}\n"
                f"4️⃣ {s4}\n"
                f"5️⃣ {s5}\n"
                f"6️⃣ {s6}\n"
                f"❌ {sx}"
            )
            embed.add_field(name="g♭ distribution", value=breakdown_breakdown, inline=False)

            total_geses = (s1 * 1) + (s2 * 2) + (s3 * 3) + (s4 * 4) + (s5 * 5) + (s6 * 6) + (sx * 7)
            embed.add_field(name="total guesses all time", value=str(total_geses), inline=False)

            await ctx.respond(embed=embed)

        else:
            self.cursor.execute('SELECT * FROM stats ORDER BY played DESC')
            rows = self.cursor.fetchall()

            if not rows:
                await ctx.respond("No stats found! Run `/sync_wordle` first.")
                return

            embed = discord.Embed(title=f"#wördle Leaderboard", color=discord.Color.green())
            leaderboard_text = "-# explanation: wins / played / total (win % | play %), avg guesses/6\n\n"

            for row in rows:
                user_id, played, s1, s2, s3, s4, s5, s6, sx = row
                wins = s1 + s2 + s3 + s4 + s5 + s6
                total_geses = (s1 * 1) + (s2 * 2) + (s3 * 3) + (s4 * 4) + (s5 * 5) + (s6 * 6) + (sx * 7)

                avg_score = total_geses / played if played > 0 else 0
                win_rate = (wins / played) * 100 if played > 0 else 0
                play_rate = (played / total_days) * 100 if total_days > 0 else 0

                leaderboard_text += f"<@{user_id}>: {wins} / {played} / {total_days:04d} ({win_rate:.1f}% | {play_rate:.1f}%), {avg_score:.2f}/6\n"

            embed.description = leaderboard_text
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(WordleCog(bot))