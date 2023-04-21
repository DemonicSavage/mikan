# Mikan

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=coverage)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=bugs)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)

Mikan automatically downloads cards from the games Love Live! School Idol Festival ALL STARS (SIFAS) and Love Live! School Idol Festival (SIF).

SIFAS cards and stills are downloaded from [Idol Story](https://idol.st/).

SIF cards are downloaded from [School Idol Tomodachi](https://schoolido.lu/).

## Installation

To install Mikan, just `pip install mikan-card-downloader`.

## Building by source

(Note: this software requires [Python](https://www.python.org/)>=3.10 and [Poetry](https://python-poetry.org/))

1. Clone this GitHub repository (`git clone https://github.com/DemonicSavage/mikan.git`)
2. Go to the `mikan` directory (`cd mikan` on Unix).
3. Run `poetry install` to grab the necessary dependencies.

## Configuration

The `config.cfg` currently only has one option, which is `data_dir`. Change that to the directory you want your cards to be downloaded to.
You can find this file in `$XDG_CONFIG_HOME/mikan` on Linux, `%APPDATA%\Local\mikan\mikan` on Windows, or `/Library/Application Support/mikan` on macOS.

## Usage

This is a command line script. It first creates (or updates) metadata files about the available cards (`cards.json`/`stills.json`/`sif.json`), and then downloads the image files themselves.

By default, running `mikan` without any arguments will create metadata and then download SIFAS cards. Using the `--stills` argument will download SIFAS stills instead, and `--sif` will download SIF cards.

Running it for the first time will prompt you for the directory cards and stills should be downloaded to.

## License

This software is released under the GNU GPLv3, and its dependencies are released under their respective licenses.
