# pixiv-tag-analyzer

Pixiv の投稿とブックマークタグを集めて雑にランキングつくることで性癖を暴く

## DEMO

[WIP]

## Run

Note: _In advance, please setup google-chrome-stable + selenium + webdriver_

```bash
git clone https://github.com/eggplants/pixiv-tag-analyzer
cd pixiv-tag-analyzer
python -m pip install -r requirements.txt
cp client.sample.json client.json
editor $_ # set id & pass
python analyze.py
```
