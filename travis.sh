set -ex

git clone --depth 1 https://github.com/aqualid/aqualid.git

PYTHONPATH=$PWD/aqualid coverage run --source=tools tests/run.py

flake8 --max-complexity=9 `find tools -name "[a-zA-Z]*.py"`
flake8 `find tests -name "[a-zA-Z]*.py"`

