<div align="center">

<h1 align="center">SULFUR Toolkit</h1>

**A toolkit to extract SULFUR oil and recipe data from `.bundle` files and unpack game assets.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/license/mit)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)
[![Python: 3.13](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![oils](examples/oils.png)
</div>

## Getting Started
Example output files (.xlsx and .json) are available in [examples](examples/).  
If you want to extract assets or parse the latest `.bundle` files, follow the guide below.

## Dependencies
```
uv sync
```

## Executing program
### Oil & Recipe Data
First, copy `onstartup_assets_all_*.bundle` this project directory, you can find it at:
```
C:\Program Files (x86)\Steam\steamapps\common\SULFUR\Sulfur_Data\StreamingAssets\aa\StandaloneWindows64\
```
And the project directory should look like this:
```
.
├── LICENSE
├── README.md
├── examples
├── onstartup_assets_all_*.bundle
├── pyproject.toml
├── requirements.txt
├── scripts
└── uv.lock
```

1. Extract data from the bundle and save it into `./tmp/data.json`.
```
uv run scripts/parse_bundle.py
```
2. Parse `./tmp/data.json` to generate `.json` and `.xlsx` output files, see [examples](examples/).
```
uv run scripts/parse_json.py
```

### Assets
Run the script below to unpack Sprite and Texture2D assets into `assets/`
```
uv run scripts/unpack_asset.py
```

## Acknowledgments
* [UnityPy](https://github.com/K0lb3/UnityPy/tree/master)