# README

- `python3 -m pip install modal`
- `cd api`
- `python3 -m modal serve main.py`

Request format:

```
curl -X POST {modal_url} -F '--file=@sam-altman.mp3' # or whatever local file you want
```
