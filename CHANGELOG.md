# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 1.0.1 - 2024-07-03

### Added

- debug method to SimpleScribe

### Removed

- dependency importlib-metadata

## 1.0.0 - 2024-06-26

### Added

- SimpleScribe class
- delete_empty_dirs function

### Changed

- Refactored directory function into new dirs module (breaking change)

### Removed

- Scribe class (breaking change)

### Security

- Updated dependencies

## 0.8.4 - 2023-11-28

### Security

- Updated dependencies

## 0.8.2 - 2023-03-21

### Changed

- Log error when notify fails

## 0.8.1 - 2023-03-14

### Security

- Updated dependencies

## 0.8.0 - 2023-02-20

### Changed

- Support for backup versions in separate directory

## 0.7.1 - 2023-02-19

### Changed

- Added verbosity to tmplwrtr module

### Security

- Updated dependencies

## 0.7.0 - 2023-02-17

### Added

- Check file existence and raise if not function
- Update workflow name
- write_yaml_file function
- type aliases for StrStrDict, StrStrInt, StrStrIntBool

### Changed

- Update readme
- Options class

### Security

- Updated dependencies

## 0.6.0 - 2023-01-19

### Added

- ipv6 validation functions
- verify_directory function
- file permission/ownership functions

### Security

- Updated dependencies

## 0.5.0 - 2023-01-15

### Added

- function to convert ipv6 address to ipv6 network
- versioned backups

## 0.4.0 - 2023-01-10

### Added

- scribe module

## 0.3.0 - 2022-12-28

### Added

- versioned module

### Changed

- Updated README.md

### Fixed

- unlink issue for python 3.7

### Removed

- Wdict type

## 0.2.1 - 2022-12-15

### Added

- StrAnyDict in kinds module
- strtobool function

## 0.2.0 - 2022-11-10

### Security

- Updated dependencies
