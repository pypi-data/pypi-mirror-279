# Ponfig

Ponfig is a simple Python package to read configuration values from the project root's `config` directory.

## Installation

pip install ponfig


## Usage

```python
from ponfig import config

value = config('app.example')
print(value)  # Outputs the value of `example` key in `app.config`
```

## License
This project is licensed under the MIT License.