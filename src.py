import abc
import argparse
import csv
from pathlib import Path
from time import sleep

import edge_tts
import genanki


class MyNote(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


class GenAnki(abc.ABC):
    """ """

    def __init__(
        self,
        deck: genanki.Deck,
        model: genanki.Model,
        source_data_path: str,
        to_path: str,
        lang: str = "en-US-JennyNeural",
    ) -> None:
        self.deck = deck
        self.package = genanki.Package(self.deck)
        self.model = model
        self.source_path = source_data_path
        self.to_path = to_path
        self.lang = lang

    def make_audio_file(self, word):
        communicate = edge_tts.Communicate(word, self.lang)
        with open(f"/tmp/{word}.mp3", "wb") as output_file:
            for chunk in communicate.stream_sync():
                if chunk["type"] == "audio":
                    output_file.write(chunk["data"])
        return output_file.name

    def gen_anki(self, fields):
        note = genanki.Note(model=self.model, fields=fields)
        self.deck.add_note(note)

    def packge(self):
        self.process_data(self.source_path)
        self.package.write_to_file(self.to_path)

    @abc.abstractmethod
    def process_data(self, path):
        raise NotImplementedError


class Eudic(GenAnki):
    """
    Eudic dictionary new word to card
    """

    def process_data(self, path):
        with open(path, "r") as csvfile:
            datareader = csv.reader(csvfile)
            next(datareader)  # skip head
            for row in datareader:
                try:
                    int(row[0])
                except ValueError:
                    continue
                else:
                    audio_path = f"/tmp/{row[1]}.mp3"
                    file_path = Path(audio_path)
                    if file_path.exists():
                        print(f"skip {row[0]=}, {row[1]=}")
                    else:
                        audio_path = self.make_audio_file(row[1])
                        sleep(1)
                    self.package.media_files.append(audio_path)
                    print(row[0], audio_path)
                    audio_name = audio_path.rsplit("/")[-1]
                    fields = [row[1], row[2], "", f"[sound:{audio_name}]", row[3]]
                    self.gen_anki(fields=fields)


def main():
    parser = argparse.ArgumentParser(description="generate anki card from dict csv file")

    parser.add_argument("source", help="dict csv file absoulute path")
    parser.add_argument("to", help="generate anki apkg file save path")
    parser.add_argument("-d", "--deck", type=int, help="random deck id")
    parser.add_argument("-n", "--name", type=int, help="deck name", default="new_deck")
    args = parser.parse_args()

    if args.deck:
        deck_id = args.deck
    else:
        deck_id = 20240516

    my_deck = genanki.Deck(
        deck_id,
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

    eudic = Eudic(deck=my_deck, model=my_model, source_data_path=args.source, to_path=args.to)
    eudic.packge()


if __name__ == "__main__":
    main()
