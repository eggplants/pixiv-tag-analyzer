# pixiv-tag-analyzer

任意のpixivユーザの投稿,ブックマークの情報を収集しタグからその人の性癖を暴く

## DEMO

![image](https://user-images.githubusercontent.com/42153744/131588844-91678751-2a27-4e83-a26a-7eba74ba8df6.png)

## Run

Note: _In advance, please setup google-chrome-stable + selenium + webdriver_

### From PyPI

```bash
pip install pixiv-tag-analyzer
cat <<'A' > client.json
{
  "pixiv_id": "<mail address or userid>",
  "password": "<password>"
}
A
pta
```

### From source

```bash
git clone https://github.com/eggplants/pixiv-tag-analyzer
cd pixiv-tag-analyzer
python -m pip install -r requirements.txt
cp client.sample.json client.json
editor $_ # set id & pass
python analyze.py
```
