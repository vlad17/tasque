# tasque

This module, `tasque`, classifies JIRAs based on their saved data, as they are exported from the JIRA CSV.

TODO better description 

## Setup

See `setup.py` for necessary python packages. Requires a linux x64 box.

```
conda create -y -n tasque-env python=3.6
source activate tasque-env
pip install --no-cache-dir --editable .
```

## Scripts

All scripts are available in `scripts/`, and should be run from the repo root in the `tasque-env`.

| script | purpose |
| ------ | ------- |
| `lint.sh` | invokes `pylint` with the appropriate flags for this repo |
| `format.sh` | auto-format the entire `tasque` directory |

## Example

All mainfiles are documented. Run `python -m tasque.main.* --help` for any `*` for details.

```{bash}
python -m tasque.main.jira_manual --help
```

## Dev Info

To update deps:

```
 pip freeze | awk -F '==' "{print \"'\"\$1\">=\"\$2\"',\"}" | xclip -in -selection clipboard # then paste in setup.py
```
