import abc

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
