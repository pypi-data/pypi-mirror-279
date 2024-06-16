# Ponfig

Ponfig 是一个简单的 Python 包，用于从项目根目录的 `config` 目录中读取配置值，以及从项目根目录的 `env` 目录中读取环境变量值。

## Installation 安装

```sh
pip install ponfig
```

## Before implement 实施前准备

确保你的项目根目录中有以下结构。

```
├── config/
│   ├── app.config
│   ├── other.config
│   └── ***.config
└── env/
    ├── app.env
    ├── other.env
    └── ***.env
```

## Basic Usage 基本用法

```python
from ponfig import get_config

value = get_config('app.example')
print(value)  # 输出 `app.config` 文件中 `example` 键的值
```

## License 许可证

This project is licensed under the MIT License.

该项目使用 MIT 许可证。