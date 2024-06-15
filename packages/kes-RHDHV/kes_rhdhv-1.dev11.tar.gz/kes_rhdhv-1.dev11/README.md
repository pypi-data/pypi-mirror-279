# Kes Python Client

## Description

This repository contains a python client which can be used to programatically access and modify your activity data through an abstraction called tables. The [documentation](https://royalhaskoningdhv.github.io/kes-python-client/build/html/index.html#) explains this in in more detail.

Generally speaking you would first create your data model in Kes and, publish it, download the Python representation of it and use that in your own Python code by creating a client like this:

```
config = Config(kes_service_address='localhost:50051')
client = Client(config)
project = client.open_project("Preview Python client example")
```

## Requirements

Python 3.10 and higher.
## Installation

Install using pip: `pip install kes-RHDHV`

You will need a token which you can obtain from the project page in Kes. The [example](https://github.com/RoyalHaskoningDHV/kes-python-client/blob/main/examples/example.py#L10) shows how to use the token.

Each project has its own unique tokens for your user account in Kes.
## Examples

See the [examples](examples)

## Documentation

See the [online documentation](https://royalhaskoningdhv.github.io/kes-python-client/build/html/index.html)

## License

This library is distributed under the [MIT license](LICENSE)
