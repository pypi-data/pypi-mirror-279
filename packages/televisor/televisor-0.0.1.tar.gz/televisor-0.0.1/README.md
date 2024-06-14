# televisor

<p align="center">
    <img src="assets/logo.png"/>
</p>


## Usage

First, configure your telegram chat id and bot token in `.bashrc`:

```sh
export TELEVISOR_TOKEN='foo'
export MY_CHAT_ID=12345
```

To call the module:

```sh
python -m tv send 'foo.mp4'
```

## Installation

To install from `pip`:

```sh
pip install televisor
```

To create environment and install all dependencies:

```sh
./setup.sh
```
