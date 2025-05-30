hiragana_dict = {
    "a": "あ", "i": "い", "u": "う", "e": "え", "o": "お",
    "ka": "か", "ki": "き", "ku": "く", "ke": "け", "ko": "こ",
    "sa": "さ", "shi": "し", "su": "す", "se": "せ", "so": "そ",
    "ta": "た", "chi": "ち", "tsu": "つ", "te": "て", "to": "と",
    "na": "な", "ni": "に", "nu": "ぬ", "ne": "ね", "no": "の",
    "ha": "は", "hi": "ひ", "fu": "ふ", "he": "へ", "ho": "ほ",
    "ma": "ま", "mi": "み", "mu": "む", "me": "め", "mo": "も",
    "ya": "や", "yu": "ゆ", "yo": "よ",
    "ra": "ら", "ri": "り", "ru": "る", "re": "れ", "ro": "ろ",
    "wa": "わ", "wo": "を", "n": "ん",

    "ga": "が", "gi": "ぎ", "gu": "ぐ", "ge": "げ", "go": "ご",
    "za": "ざ", "ji": "じ", "zu": "ず", "ze": "ぜ", "zo": "ぞ",
    "da": "だ", "de": "で", "do": "ど",
    "ba": "ば", "bi": "び", "bu": "ぶ", "be": "べ", "bo": "ぼ",

    "pa": "ぱ", "pi": "ぴ", "pu": "ぷ", "pe": "ぺ", "po": "ぽ",

    "kya": "きゃ", "kyu": "きゅ", "kyo": "きょ",
    "sha": "しゃ", "shu": "しゅ", "sho": "しょ",
    "cha": "ちゃ", "chu": "ちゅ", "cho": "ちょ",
    "nya": "にゃ", "nyu": "にゅ", "nyo": "にょ",
    "hya": "ひゃ", "hyu": "ひゅ", "hyo": "ひょ",
    "mya": "みゃ", "myu": "みゅ", "myo": "みょ",
    "rya": "りゃ", "ryu": "りゅ", "ryo": "りょ",

    "gya": "ぎゃ", "gyu": "ぎゅ", "gyo": "ぎょ",
    "ja": "じゃ", "ju": "じゅ", "jo": "じょ",
    "bya": "びゃ", "byu": "びゅ", "byo": "びょ",

    "pya": "ぴゃ", "pyu": "ぴゅ", "pyo": "ぴょ",

    "small_tsu": "っ"
}

katakana_dict = {
    "a": "ア", "i": "イ", "u": "ウ", "e": "エ", "o": "オ",
    "ka": "カ", "ki": "キ", "ku": "ク", "ke": "ケ", "ko": "コ",
    "sa": "サ", "shi": "シ", "su": "ス", "se": "セ", "so": "ソ",
    "ta": "タ", "chi": "チ", "tsu": "ツ", "te": "テ", "to": "ト",
    "na": "ナ", "ni": "ニ", "nu": "ヌ", "ne": "ネ", "no": "ノ",
    "ha": "ハ", "hi": "ヒ", "fu": "フ", "he": "ヘ", "ho": "ホ",
    "ma": "マ", "mi": "ミ", "mu": "ム", "me": "メ", "mo": "モ",
    "ya": "ヤ", "yu": "ユ", "yo": "ヨ",
    "ra": "ラ", "ri": "リ", "ru": "ル", "re": "レ", "ro": "ロ",
    "wa": "ワ", "wo": "ヲ", "n": "ン",

    "ga": "ガ", "gi": "ギ", "gu": "グ", "ge": "ゲ", "go": "ゴ",
    "za": "ザ", "ji": "ジ", "zu": "ズ", "ze": "ゼ", "zo": "ゾ",
    "da": "ダ", "de": "デ", "do": "ド",
    "ba": "バ", "bi": "ビ", "bu": "ブ", "be": "ベ", "bo": "ボ",

    "pa": "パ", "pi": "ピ", "pu": "プ", "pe": "ペ", "po": "ポ",

    "kya": "キャ", "kyu": "キュ", "kyo": "キョ",
    "sha": "シャ", "shu": "シュ", "sho": "ショ",
    "cha": "チャ", "chu": "チュ", "cho": "チョ",
    "nya": "ニャ", "nyu": "ニュ", "nyo": "ニョ",
    "hya": "ヒャ", "hyu": "ヒュ", "hyo": "ヒョ",
    "mya": "ミャ", "myu": "ミュ", "myo": "ミョ",
    "rya": "リャ", "ryu": "リュ", "ryo": "リョ",

    "gya": "ギャ", "gyu": "ギュ", "gyo": "ギョ",
    "ja": "ジャ", "ju": "ジュ", "jo": "ジョ",
    "bya": "ビャ", "byu": "ビュ", "byo": "ビョ",

    "pya": "ピャ", "pyu": "ピュ", "pyo": "ピョ",

    "small_tsu": "ッ"
}

# reverse cursed technique
reverse_hiragana_dict = {v: k for k, v in hiragana_dict.items()}
reverse_katakana_dict = {v: k for k, v in katakana_dict.items()}


def get_hiragana(input_str):
    if input_str in hiragana_dict:
        return hiragana_dict[input_str]
    elif input_str in reverse_hiragana_dict:
        return reverse_hiragana_dict[input_str]
    else:
        return False

def get_katakana(input_str):
    if input_str in katakana_dict:
        return katakana_dict[input_str]
    elif input_str in reverse_katakana_dict:
        return reverse_katakana_dict[input_str]
    else:
        return False

def conv_multiple_kana(kana_type, to_conv):
    if not to_conv:
        return False

    converting, output = "", ""
    groupings = []
    input_as_list = list(to_conv)

    for count, character in enumerate(input_as_list):
        current_item = character
        if current_item == " ":
            continue
        converting += current_item

        if count+1 < len(input_as_list):  # edge case: small tsu when two consonants != n in a row
            if converting.isascii() and converting == input_as_list[count+1] and converting not in ['a', 'e', 'i', 'o', 'u'] and input_as_list[count+1] != "n":
                groupings.append("small_tsu")
                converting = ""
                continue

        if converting == "n":  # edge case: standalone n character should not be converted if followed by vowel
            if len(input_as_list) != count+1 and input_as_list[count+1] in ['a', 'e', 'i', 'o', 'u']:
                continue

        if kana_type == 'h':
            if converting in hiragana_dict.keys() or converting in hiragana_dict.values():
                groupings.append(converting)
                converting = ""
        elif kana_type == 'k':
            if converting in katakana_dict.keys() or converting in katakana_dict.values():
                groupings.append(converting)
                converting = ""

    if kana_type == 'h':
        for count, character in enumerate(groupings):
            if character == "っ":
                output += get_hiragana(groupings[count+1])[0]
                continue
            output += get_hiragana(character)
    elif kana_type == 'k':
        for count, character in enumerate(groupings):
            if character == "ッ":
                output += get_katakana(groupings[count + 1])[0]
                continue
            output += get_katakana(character)
    else:
        return False

    if converting != "":
        if output == "":
            return "found no results", 1
        return f"Found: {output}, not found: {converting}", 2
    return output, 0
