#! /usr/bin/env bash

# Lints code:
#
#   # Lint tasque by default.
#   ./scripts/lint.sh
#   # Lint specific files.
#   ./scripts/lint.sh tasque/somefile/*.py

set -euo pipefail

lint() {
    flake8 "$@"
}

main() {
    if [[ "$#" -eq 0 ]]; then
        lint tasque
    else
        lint "$@"
    fi
}

main "$@"
