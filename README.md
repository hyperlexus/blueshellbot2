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
BOT_ADMINS="<userid1>,<userid2>"

PROJECT_PATH="C:\\Users\\HyperLexus\\PycharmProjects\\blueshellbot2"
PROJECT_URL="https://github.com/hyperlexus/blueshellbot2"
```
and you can set every variable you can find in `/Config/Configs.py` in the .env file.\
the default values are set as the second number or stat in the brackets there.\
this .env file also has to be included when you build the docker image.\
if you use a web portal instead of docker desktop to run the image, you have to pass the variables one by one.\
if you do that, i recommend changing the default values so you have to pass less variables manually :)

### known issues and other small bits:
1. if someone runs `b.alert "`, the bot returns an error. why this happens is sorta known but
it's sort of a running gag among my friends to make it produce a 🥶 emoji this easily, so i didnt fix it yet
2. `b.alert` also does not work with roles or bot users.\
3. A lot of the `b.restart` problems have been FIXED, now what you need to do to get it to work is the following:\
Change the necessary config in `.env`, mainly `PROJECT_PATH` and `BAT_PATH`, which point to where your project root and where the executable for the bot is.
4. Any admin commands (those in the `ModCog.py` file) can only be executed by "Bot admins". These are to be defined by **USER ID** in the .env file.\
As shown above, it should be like `BOT_ADMINS="<id1>,<id2>"` with no space in between.
5. you can add new commands by adding a new command in the MiscCog.py file and following the rough structure of what I did.\
If you know what you're doing, you'll figure it out.\
The reason I'm adding this is because this command will automatically be added to the `b.help` command.

Enjoy! :D