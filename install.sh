#!/bin/bash

set -ex

# Because poetry doesn't support dev-dependency extras, we need to install these
# tools outside of the tox poetry environment (because they're not required inside).
#
pip install -U poetry tox-gh-actions yq
