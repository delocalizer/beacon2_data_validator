# Description

Validate JSON data files against the beacon v2 data model.

# Usage

0. Help.

```
./beacon2-data-validator.py --help
```

1. Validate against latest beacon v2 default data model from github.

```
./beacon2-data-validator.py individuals individuals.json
```

2. Validate against some other schema version.

```
./beacon2-data-validator.py individuals individuals.json --baseuri https://path/to/schema/baseuri
```
