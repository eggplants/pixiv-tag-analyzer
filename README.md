# pixiv-tag-analyzer

任意のpixivユーザの投稿,ブックマークの情報を収集しタグからその人の性癖を暴く

## DEMO

![image](https://user-images.githubusercontent.com/42153744/131588558-e877db6b-1105-4966-be16-80ecf1f1b199.png)

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
