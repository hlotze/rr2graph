# Changelog

All notable changes to this project will be documented in this file.

The format is inspired by Keep a Changelog
and the project loosely follows Semantic Versioning.

---

## [Unreleased]

### Added
- Extended automated test coverage for bump_version.py
- Added multi-version CI testing for Python 3.11 and 3.12
- Added requirements.txt and cleaned development dependency handling
- Added manpage improvements and CLI documentation consistency

### Changed
- Converted all README documentation to English
- Refactored helpers.py to fully English messages and comments
- Improved .gitignore and .dockerignore structure
- Simplified and modernized development tooling
- Replaced legacy lint stack with ruff + black
- Improved CI workflow reliability and Python compatibility
- Updated typing compatibility for Python 3.11/3.12

### Fixed
- Fixed typing incompatibility using pd.NaT in union annotations
- Fixed CI failures caused by Python version mismatches
- Fixed missing test discovery for tests/tools/
- Fixed coverage gaps in bump_version.py

### Documentation
- Updated README.md
- Updated README_DOCKER.md
- Updated README_UV.md
- Updated README_VENV.md
- Improved developer-oriented documentation structure

---

## [0.3.1]

### Added
- Initial public project structure
- Excel import and preprocessing
- Monthly aggregation support
- Plot generation system
- YAML configuration support
- CLI interface
- Docker support
- Automated testing and CI setup
