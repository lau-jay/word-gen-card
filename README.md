# word-gen-card
a generate anki card  tool from dictionary export csv file

## Installation

word-gen-card requires python version 3.10 or higher

```bash
pip install word-gen-card
```


## Quickstart
**Now Support Eudic export csv file**

```bash
card_cli source_file_path to_save_path -n dect_name -d deck_id

```

see more details

```bash
card_cli --help
```

## Support more csv formats

this tool default model fields like below:

```
fields=[
            {"name": "单词"},
            {"name": "音标"},
            {"name": "图片"},
            {"name": "声音"},
            {"name": "基本释义"},
        ],
```

your process_data method logic only put this struct data to `self.gen_anki` if  useing default model, like below:


```python
from word-gen-card.src import GenAnki

class OtherDict(GenAnki):
    def process_data(self, path):
        # do your something
        fields = [word, phonetic symbols, image, f'[sound:{audio_name]', basic meaning]
        self.gen_anki(fields=fields)

```

also you can custom your model, see below:

```
my_deck = genanki.Model(
      model_id,
        "Model NAME",
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
            "qfmt": "", # front side
            "afmt": "", # back side
        }
        ]
)
eudic = Eudic(deck=my_deck, model=my_model, source_data_path=args.source, to_path=args.to)
eudic.packge()
```
for more model detail see [genanki](https://github.com/kerrickstaley/genanki) repo

## License

This project is open sourced under MIT license, see the [LICENSE](LICENSE) file for more details.


