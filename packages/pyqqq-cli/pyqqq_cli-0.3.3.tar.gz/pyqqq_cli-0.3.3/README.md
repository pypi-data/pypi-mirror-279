## pyqqq-cli

### Installation

You can install `pyqqq-cli` via pip:

```bash
pip install pyqqq-cli
```

### Usage

After installation, the `qqq` command will be available. You can execute it with various subcommands:

```bash
qqq [OPTIONS] COMMAND [ARGS]...
```

#### Options

- `--help`: Show the help message and exit.

#### Commands

- `deploy`: Deploy a strategy.
- `delete`: Delete a deployed strategy.
- `list`: List deployed strategies.
- `logs`: Show logs of a deployed strategy.
- `pull`: Download an strategy from the registry.
- `run`: Run a strategy.
- `search`: Search for stock investment strategies.
- `version`: Show version number and quit.

### Example

```bash
qqq deploy my_strategy_name
```

This command deploys a strategy named `my_strategy_name`.

```bash
qqq list
```

This command lists all deployed strategies.

```bash
qqq logs my_strategy_name
```

This command shows logs of the deployed strategy named `my_strategy_name`.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


