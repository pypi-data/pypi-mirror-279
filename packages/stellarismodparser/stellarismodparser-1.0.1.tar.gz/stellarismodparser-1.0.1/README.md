# StellarisModParser

This package provides a simple parser for Stellaris's mod descriptor format.

## Usage

```python-repl
>>> import stellarismodparser
>>> path = "/home/seaswimmer/Projects/StellarisMods/No Menacing Ships.mod"
>>> mod = stellarismodparser.parse(path)
>>> mod.name
'No Menacing Ships'
>>> str(mod.supported_version)
'Andromeda 3.12.4'
>>> mod.tags
['Balance', 'Gameplay']
```
