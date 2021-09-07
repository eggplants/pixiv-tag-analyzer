# pixiv-tag-analyzer

[![PyPI version](https://img.shields.io/pypi/v/pixiv-tag-analyzer)](https://pypi.org/project/pixiv-tag-analyzer) [![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/eggplanter/pta)](https://hub.docker.com/r/eggplanter/pta) [![Maintainability](https://api.codeclimate.com/v1/badges/30545f499d5c82b19bcd/maintainability)](https://codeclimate.com/github/eggplants/pixiv-tag-analyzer/maintainability)

- 任意のpixivユーザの投稿,ブックマークの情報を収集しタグからその人の性癖を暴く
- 分析データは`data/`以下に保存

## DEMO

![image](https://user-images.githubusercontent.com/42153744/131588844-91678751-2a27-4e83-a26a-7eba74ba8df6.png)

## Run

Note: _In advance, please setup google-chrome-stable + selenium + webdriver_

### From PyPI

```bash
pip install pixiv-tag-analyzer
pta
```

### From Docker

```bash
docker run -it eggplanter/pta
```
