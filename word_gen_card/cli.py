import genanki
import argparse
from word_gen_card import Eudic

DICTIONARY_MAP = {
    "eudic": Eudic,
}

def main():
    parser = argparse.ArgumentParser(description="a generate anki card  tool from dictionary export csv file")

    parser.add_argument("source", help="dictionary export csv file absoulute path")
    parser.add_argument("to", help="generate anki apkg file save path")
    parser.add_argument("-d", "--dictionary", type=str, help="dictionary name", choices=["eudic"], default="eudic")
    parser.add_argument("-n", "--name", type=str, help="deck name", default="new_deck")
    args = parser.parse_args()

    dictionary_cls = DICTIONARY_MAP[args.dictionary]


    my_deck = genanki.Deck(
        20240516,
        args.name,
    )
    my_model = genanki.Model(
        1442716959,
        "Basic Model",
        fields=[
            {"name": "单词"},
            {"name": "音标"},
            {"name": "图片"},
            {"name": "声音"},
            {"name": "基本释义"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": """
                <div style="font-size:50px;font-family:arial black">{{单词}}</div>
                <div style="font-size:15px; color: blue;">
                    {{音标}}
                </div>
                <div class="image">{{图片}}</div>
                <br> {{声音}}""",
                "afmt": '{{FrontSide}}<hr id="answer">{{基本释义}}',
            },
        ],
    )

    eudic = dictionary_cls(deck=my_deck, model=my_model, source_data_path=args.source, to_path=args.to)
    eudic.packge()


if __name__ == "__main__":
    main()
