#!/usr/bin/env bash

set -e

export LC_ALL=en_US.UTF-8
export LANG=en_US.utf8
export PACKAGE_NAME=announcer

echo ""
echo "bandit"
echo "======"
bandit -ll $PACKAGE_NAME/*.py

echo ""
echo "flake8"
echo "======"
flake8 $PACKAGE_NAME

echo ""
echo "mypy"
echo "===="
mypy -p $PACKAGE_NAME --ignore-missing-imports
