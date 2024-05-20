# word-gen-card
a generate anki card  tool from dictionary export csv file

## Installation

word-gen-card requires python version 3.10 or higher

```bash
pip install word_gen_card
```

## Quickstart
**Now Support Eudic export csv file**

see usage details

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

your process_data method logic only put this fields list to `self.gen_anki` if  using default model, like below:


```python
from word_gen_card import GenAnki

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
