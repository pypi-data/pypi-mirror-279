# Dream Machine API
Fork from https://github.com/danaigc/DreamMachineAPI
About High quality video generation by lumalabs.ai. Reverse engineered API.

![image](./a.png)


https://github.com/yihong0618/LumaDreamCreator/assets/15976103/a55ee848-ab50-4769-8014-76ace41e330b


## How to
- Login https://lumalabs.ai/ and generate video.
- Use `Chrome` or other browsers to inspect the network requests (F12 -> XHR).
- Clone this REPO -> `git clone https://github.com/yihong0618/LumaDreamCreator.git`
- Copy the cookie.
 Export LUMA_COOKIE='xxxxx'.

## Usage

```
python -m luma --prompt 'make this picture alive' -I a.png
```

or
```
pip install -U luma-creator 
```

```python
from luma import VideoGen
i = VideoGen('cookie', 'image_url' ) # Replace 'cookie', image_url with your own
print(i.get_limit_left())
i.save_video("a blue cyber dream", './output')
```

## Thanks

- [DreamMachineAPI](https://github.com/danaigc/DreamMachineAPI)
