# Compile from source

## Prerequisite

- Python version >= 3.7

## Build

```
cd server
sh build.sh <version>
```

The output is like:

```
doris-sql-convertor-1.0.3-bin-x86
├── bin
│   ├── start.sh
│   └── stop.sh
├── conf
│   └── config.conf
├── lib
│   └── doris-sql-convertor-1.0.3-bin-x86
├── LICENSE
├── LICENSE_SQLGLOT
├── log
├── README.md
└── release-notes.md
```


## FAQ

- `ERROR: Could not find a version that satisfies the requirement blinker==1.6.3 (from versions: 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5)`

    Python or pip version is low. Upgrade Python or pip

    `python -m pip install --upgrade pip`

