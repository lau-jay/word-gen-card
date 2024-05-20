import csv
from pathlib import Path
from time import sleep

from .base import GenAnki

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
