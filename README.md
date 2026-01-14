<div align="center">

# <3 youtube meme uploader

youtube uploader using google api + oauth.  
client secrets stay local.

![python](https://img.shields.io/badge/python-3.x-ff78c8?style=for-the-badge)
![google](https://img.shields.io/badge/api-google-0b0b0b?style=for-the-badge)
![vibe](https://img.shields.io/badge/vibe-terminal--core-ff4db8?style=for-the-badge)

</div>

---

## setup

```bash
pip install -r requirements.txt
```

## google oauth

this project expects a local `client_secrets.json`.

do NOT upload your real secrets to github.

recommended:
- keep `client_secrets.json` only on your pc
- it’s already ignored by `.gitignore`

## run

```bash
python .\src\upload.py
```
