from Utils.riichi.RiichiUtils import RiichiUtils
from Utils.riichi import PictureCombiner
from Utils.riichi.yakuchecker.YakuChecker import YakuChecker

"""
colour codes: m = man, s = sou, p = pin, d = dragons, w = winds
dragon codes: 1 = white, 2 = green, 3 = red (reverse italy)
wind codes: 1 = east, 2 = south, 3 = west, 4 = north
dora indicator: !
"""

example_hand = "124345!p444m444w22d"

def get_tiles_from_hand_string(mahjong_hand: str) -> list:
    tiles = RiichiUtils.handle_riichi_hand_errors(mahjong_hand)
    active_yaku_list = YakuChecker.check_for_yakus(tiles)
    github_list: list = RiichiUtils.get_github_names(tiles)
    github_links: list = RiichiUtils.get_links_from_github_list(github_list)
    return PictureCombiner.create_mahjong_hand(github_links)

if __name__ == "__main__":
    print(RiichiUtils.handle_riichi_hand_errors(example_hand))
