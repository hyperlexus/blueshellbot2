from Tests.BDownloaderTests import BlueshellDownloaderTest
from Tests.BSpotifyTests import BlueshellSpotifyTest
from Tests.BDeezerTests import BlueshellDeezerTest


tester = BlueshellDownloaderTest()
tester.run()
tester = BlueshellSpotifyTest()
tester.run()
tester = BlueshellDeezerTest()
tester.run()
