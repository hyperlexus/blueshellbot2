from Music.BlueshellInitializer import BlueshellInitializer
from Config.Folder import Folder

# balls

if __name__ == '__main__':
    folder = Folder()
    initializer = BlueshellInitializer(willListen=True)
    blueshellBot = initializer.getBot()
    blueshellBot.startBot()
