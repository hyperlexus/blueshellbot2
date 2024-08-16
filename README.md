# blueshellbot
## music bot and some other shit

started as a music bot, now doing other commands i feel like doing for my personal server\
dockerfile included, but not really structured and just for personal use. does NOT work with amd64 architecture

feel free to fork or steal and shit idc

note: use python3.11\
3.12 breaks like 8 packages because it's not supported with some old ones.\
some of these are `aiohttp`, `Brotli` and more. if you see it say it failed to build those then you're using 3.12

### for .env (an example):
```
BOT_TOKEN=Your_Own_Bot_Token
SPOTIFY_ID=Your_Own_Spotify_ID
SPOTIFY_SECRET=Your_Own_Spotify_Secret
BOT_PREFIX=Your_Wanted_Prefix_For_Blueshell
SHOULD_AUTO_DISCONNECT_WHEN_ALONE=True
```
and you can set every variable you can find in `/Config/Configs.py` in the .env file.\
the default values are set as the second number or stat in the brackets there.\
this .env file also has to be included when you build the docker image.\
if you use a web portal instead of docker desktop to run the image, you have to pass the variables one by one.\
if you do that, i recommend changing the default values so you have to pass less variables manually :)

### known issues and other small bits:
1. if someone runs `b.alert "`, the bot returns an error. why this happens is sorta known but\
it's sort of a running gag among my friends to make it produce a 🥶 emoji this easily, so i didnt fix it yet
2. `b.alert` also does not work with roles or bot users.
3. the `b.restart` command has to be manually changed to include your filepath **AND** discord user ID, and is kind of buggy on different systems.\
this can be found on lines 235 and 246 in `/DiscordCogs/MiscCog.py`.
4. after a `b.restart`, the bot sometimes has to be started manually after the command is run, because of who knows why.
5. the discord user id on line 235 is the one of the bot owner, and/or of the user(s) you want to allow to kill the bot from within discord.\
if you want to allow multiple users, you can just change it to the following:\
`if ctx.author.id == <id 1> or ctx.author.id == <id 2>:`\
you can get your discord user id by enabling developer mode in discord settings, right-clicking your name and clicking "copy id".
6. you can add new commands by adding a new command in the MiscCog.py file and following the rough structure of what I did.\
If you know what you're doing, you'll figure it out.\
The reason I'm adding this is because this command will automatically be added to the `b.help` command.

Enjoy! :D