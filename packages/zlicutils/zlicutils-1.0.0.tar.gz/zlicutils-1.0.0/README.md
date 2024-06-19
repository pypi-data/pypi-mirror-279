# zlic-utils
A library for shared classes and functionalities in the ZLiC project.

## Installation

```bash
pip install zlicutils
```

## Installation for development purposes
```
pip install -e .   
```

## Tests
```
python -m pytest tests/
```

## Usage

### create Server
```
from zlicutils.server import Server

server = Server(host='0.0.0.0', port=8888)
server.router.add_api_route("/api/{id}", self._audio, methods=["GET"])

self.server.start()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors and acknowledgment

- For readme file I used format from https://www.makeareadme.com/

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
