set -ex

coverage run --source=tools tests/run.py

flake8 --max-complexity=9 `find tools -name "[a-zA-Z]*.py"`
flake8 `find tests -name "[a-zA-Z]*.py"`

