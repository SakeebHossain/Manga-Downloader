# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.1] - 2019-08-17
### Added
- Support for `mangareader.net`.
- `requirements.txt` and `install.sh` to make installing the 
tool easier.

### Changed
- Went from using `cx-freeze` to `pyinstaller` because we were 
experiencing SSL issues, wasn't making much progress with it. 

### Removed
- Everything to do with `https://mangahere.cc`, it was too much 
trouble trying to download the images because of the way it has 
to "load" images, hiding the image link. Besides it's pulling
the image from other manga sites anyway!

[Unreleased]: https://github.com/SakeebHossain/Manga-Downloader/compare/v0.0.1...HEAD
[0.0.2]: https://github.com/SakeebHossain/Manga-Downloader/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/SakeebHossain/Manga-Downloader/releases/tag/v0.0.1
