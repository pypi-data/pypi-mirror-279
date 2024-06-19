# ClickNLoad2FeedCrawler
ClickNLoad2FeedCrawler fängt Click'n'Load ab, entschlüsselt die Payload und übergibt diese dem FeedCrawler.

[![PyPI version](https://badge.fury.io/py/cnl2feedcrawler.svg)](https://badge.fury.io/py/cnl2feedcrawler)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/cnl2feedcrawler)](https://img.shields.io/pypi/dm/cnl2feedcrawler)
[![Github Sponsorship](https://img.shields.io/badge/support-me-red.svg)](https://github.com/users/rix1337/sponsorship)

####  Voraussetzungen
* Linux basierte Laufzeitumgebung (inkompatibel mit Windows)
* [Python 3.6](https://www.python.org/downloads/) oder neuer
* [pip](https://pip.pypa.io/en/stable/installing/)
* [openssl](https://www.openssl.org/)
* [Node.js](https://nodejs.org/)
* [FeedCrawler](https://github.com/rix1337/FeedCrawler)

#### Update

```pip install -U cnl2feedcrawler```

#### Starten

```cnl2feedcrawler --url=192.168.1.1:9090``` in der Konsole (Python muss im System-PATH hinterlegt sein)

# Docker
```
docker run -d \
  --name="ClickNLoad2FeedCrawler" \
  -p 9666:9666 \
  -e 'URL'='192.168.1.1:9090'
  rix1337/docker-cnl2feedcrawler:latest
  ```


#### Pflichtparameter

| Parameter         | Erläuterung                                                        |
|-------------------|--------------------------------------------------------------------|
| ```--url=<URL>``` | Die lokale URL des FeedCrawlers - bspw. `http://192.168.1.1:9090`) |



## Click'n'Load auf Windows umleiten

`netsh interface portproxy add v4tov4 listenport=9666 connectaddress=<Docker Host> connectport=9666 listenaddress=127.0.0.1`

#### Umleitung entfernen:

`netsh interface portproxy delete v4tov4 listenport=9666 listenaddress=127.0.0.1`


## Credits

* [drwilly](https://github.com/drwilly)
