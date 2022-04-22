# Changelog

All notable changes to this project will be documented in this file.

This file's format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/). The
version number is tracked in the file `pyproject.toml`.

## [Unreleased]

### Breaking Changes
- Set the minimum Python version to 3.7.
  - 3.5 and 3.6 are EOL.

### Added

### Fixed

## [3.0.2] - 2021-06-10

### Fixed
- Fix up docker deploy so that we wait until the package is in pypi before building.

## [3.0.1] - 2021-06-10

- Fix up docker deploy that was still using TRAVIS_TAG

## [3.0.0] - 2021-06-10

### Changed
- Switch from Travis to Github Actions
- Remove Python 3.4 support.
- Upgrade to python 3.9-alpine3.13

### Added
- Add Microsoft Teams support to announcer
  - Some commandline options are not supported in announcer when using Teams.
    - --iconurl
    - --iconemoji
    - --username

## [2.3.0] - 2019-08-12

### Changed
- Fix after_deploy.sh so that the current directory is mounted in when calling announce
- Handle references that don't match the changelog version

### Added

## [2.2.0] - 2019-07-16

### Changed
- Dependency updates:
  - mypy from "^0.701.0" to "^0.720"
  - yamllint from "^1.15" to "^1.16"
  - pytest from "^4.5" to "^4.6"
  - tox from "^3.12" to "^3.13"

### Added
- Add coveralls support
- Add deeper indents for sublists and triangular bullets
- Dependency additions:
  - pytest-cov added at "^2.7"

## [2.1.0] - 2019-05-31

### Changed
- Do Docker deploys on tagged builds

### Added

## [2.0.0] - 2019-05-31

### Changed
- First public release! :tada:

### Added

[unreleased]: https://github.com/Metaswitch/announcer/compare/3.0.2...HEAD
[3.0.2]: https://github.com/Metaswitch/announcer/compare/3.0.1...3.0.2
[3.0.1]: https://github.com/Metaswitch/announcer/compare/3.0.0...3.0.1
[3.0.0]: https://github.com/Metaswitch/announcer/compare/2.3.0...3.0.0
[2.3.0]: https://github.com/Metaswitch/announcer/compare/2.2.0...2.3.0
[2.2.0]: https://github.com/Metaswitch/announcer/compare/2.1.0...2.2.0
[2.1.0]: https://github.com/Metaswitch/announcer/compare/2.0.0...2.1.0
[2.0.0]: https://github.com/Metaswitch/announcer/tree/2.0.0
