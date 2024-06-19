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

### create Server with tun access
```
from fastapi import Depends

from zlicutils.server import Server
from zlicutils.tan import TanManager

server = Server(host='0.0.0.0', port=8888)

tan_manager = TanManager()

server.router.add_api_route("/api/{id}", _api methods=["GET"])

server.router.add_api_route("/tan", tan_manager.tans_as_html, methods=["GET"])
server.router.add_api_route("/api/verified/{source_id}", self._api_verified_, methods=["GET"], dependencies=[Depends(tan_manager.verify_tan)])

server.start()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors and acknowledgment

- For readme file I used format from https://www.makeareadme.com/

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
