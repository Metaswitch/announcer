#!/bin/bash

set -ex

# Because poetry doesn't support dev-dependency extras, we need to install these
# tools outside of the tox poetry environment (because they're not required inside).
#
# python-coveralls is not specific enough about its dependencies so on Python 3.4
# forcibly specify pyYAML 5.2, as this was the last release to support Python 3.4.
ISNEW=$(python -c "print(1 if __import__('sys').version_info >= (3,5) else 0)")
if (( ISNEW ))
then
  COVERALLS="python-coveralls"
else
  COVERALLS="pyYAML==5.2 python-coveralls"
fi

pip install -U poetry tox-travis tomlq $COVERALLS
