# Tiles puzzle generator

Python script to generate a zip archive of an sliding tiles puzzle HTML page
from a provided image.


## install dependencies


### Debian

```bash
# apt install python3-dev python3-setuptools
# apt install libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev
$ python3 -m pip install --upgrade pip
$ python3 -m pip install --upgrade Pillow
```


## usage

```bash
$ ./tiles_puzzle_generator.py path_to_image_file
```

Generate a 3x3 sliding tiles puzzle (default value is 4x4)
```bash
$ ./tiles_puzzle_generator.py -s 3  path_to_image_file
```

Name the archive `surprise.zip` and set the value of the HTML tag `<title>` to
`surprise` (default value is `puzzle`)
```bash
$ ./tiles_puzzle_generator.py -t surprise path_to_image_file
```

Name the HTML page `open_me.html` (default name is `index.html`)
```bash
$ ./tiles_puzzle_generator.py -hn open_me path_to_image_file
```
