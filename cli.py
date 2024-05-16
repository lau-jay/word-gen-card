import csv
import abc
from time import sleep
from pathlib import Path
import genanki
import edge_tts



class MyNote(genanki.Note):
  @property
  def guid(self):
    return genanki.guid_for(self.fields[0])


class GenAnki(abc.ABC):
    """
    """

    def __init__(self, deck: genanki.Deck, model: genanki.Model, source_data_path: str, to_path: str, 
                 lang: str ="en-US-JennyNeural") -> None:
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
        note =  genanki.Note(model=self.model, fields=fields)
        self.deck.add_note(note)

    def packge(self):
        self.process_data(self.source_path)
        self.package.write_to_file(self.to_path)

    @abc.abstractmethod
    def process_data(self, path):
        raise NotImplemented


class Eudic(GenAnki):
    def process_data(self, path):
        with open(path, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            next(datareader) # skip head
            for row in datareader:
                try:
                    int(row[0])
                except ValueError:
                    continue
                else:
                    voice = f"/tmp/{row[1]}.mp3"
                    file_path = Path(voice)
                    if file_path.exists():
                        print(f"skip {row[0]=}, {row[1]=}")
                    else:
                        voice = self.make_audio_file(row[1])
                        sleep(1)
                    self.package.media_files.append(voice)
                    print(row[0], voice)
                    voice = voice.rsplit("/")[-1]
                    fields = [row[1], row[2], "", f"[sound:{voice}]", row[3]]
                    self.gen_anki(fields=fields)


if __name__ == "__main__":
    my_deck = genanki.Deck(
        20240516,
    'Eudic新词'
    )
    my_model = genanki.Model(
        1442716959,
    'Jay Model',
    fields=[
        {'name': '单词'},
        {'name': '音标'},
        {'name': '图片'},
        {'name': '声音'},
        {'name': '基本释义'},
    ],
    templates=[
        {
        'name': 'Card 1',
        'qfmt': """
        <div style="font-size:50px;font-family:arial black">{{单词}}</div>
        <div style="font-size:15px; color: blue;">
            {{音标}}
        </div>
        <div class="image">{{图片}}</div>
        <br> {{声音}}""",
        'afmt': '{{FrontSide}}<hr id="answer">{{基本释义}}',
        },
    ]
    )

    eudic = Eudic(deck=my_deck, model=my_model, source_data_path="/Users/jay/Documents/我的学习记录_May 16, 2024.csv", to_path="/Users/jay/Downloads/output.apkg")
    eudic.packge()
