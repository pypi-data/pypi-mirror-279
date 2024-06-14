# Invidious.py

A Python wrapper for Invidious API

# Installation

## With pip 

`$ pip install invidious.py`

## With Git

```sh
$ git clone https://codeberg.org/librehub/invidious.py
$ cd invidious.py
$ pip install .
```

# Getting Started

```python
from invidious.enums import ContentType
from invidious import *

iv = Invidious()
searched = iv.search("distrotube", ctype=ContentType.CHANNEL)

for item in searched:
    print(item.author) 
    # Print names of all channels
    # in first page of result 'distrotube'
```

# Links

* PyPi: https://pypi.org/project/invidious.py/
* Git repo: https://codeberg.org/librehub/invidious.py
* Matrix: https://matrix.to/#/#librehub:cutefunny.art

## Support

Any contacts and crytpocurrency wallets you can find on my [profile page](https://warlock.codeberg.page).

