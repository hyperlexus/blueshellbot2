from Utils.riichi.RiichiUtils import RiichiUtils
from yaku_utils import YakuUtils

def pinfu(tile_dict: dict) -> bool:  # todo
    possible_possible_chis = YakuUtils.extract_possible_possible_chis(tile_dict)
    chi_amount_dict = {}
    for colour, chi_list in possible_possible_chis.items():
        most_chis_in_this_hand = 0
        for chi in chi_list:
            most_chis_in_this_hand = len(chi) if len(chi) > most_chis_in_this_hand else most_chis_in_this_hand
        chi_amount_dict[colour] = most_chis_in_this_hand
    return chi_amount_dict

def iipeikou(tile_dict: dict) -> bool:
    possible_possible_chis = YakuUtils.extract_possible_possible_chis(tile_dict)
    for colour, chi_list in possible_possible_chis.items():
        for chis in chi_list:
            found_chis = []
            for chi in chis:
                if chi in found_chis:
                    return True
                else:
                    found_chis.append(chi)
    return False

def tanyao(tile_str: str) -> bool:  # bomboclaat
    for blud in ('1', '9', 'w', 'd'):
        if blud in tile_str:
            return False
    return True

def yakuhai(tile_dict: dict) -> int:
    pons = YakuUtils.extract_sets(tile_dict, 3)
    for pon in pons:
        if 'd' in pon:
            return 1
        elif 'w' in pon:
            return 2
    return 0

example_hand = "222w"

if __name__ == "__main__":
    hand_tiles = RiichiUtils.handle_riichi_hand_errors(example_hand)
    print(yakuhai(hand_tiles))