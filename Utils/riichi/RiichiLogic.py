from Utils.riichi.RiichiUtils import RiichiUtils
from Utils.riichi import PictureCombiner

"""
colour codes: m = man, s = sou, p = pin, d = dragons, w = winds
dragon codes: 0 = white, 1 = green, 2 = red (reverse italy)
wind codes: 0 = east, 1 = south, 2 = west, 3 = north
dora indicator: !
"""

example_hand = "123345!p444m444w22d"

def get_tiles_from_hand_string(mahjong_hand: str) -> list:
    tiles = RiichiUtils.handle_riichi_hand_errors(mahjong_hand)
    github_list: list = RiichiUtils.get_github_names(tiles)
    github_links: list = RiichiUtils.get_links_from_github_list(github_list)
    return PictureCombiner.create_mahjong_hand(github_links)

if __name__ == "__main__":
    get_tiles_from_hand_string(example_hand)
