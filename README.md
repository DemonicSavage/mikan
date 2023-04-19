# SIFAS Card Downloader

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=bugs)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)

SIFAS Card Downloader automatically downloads and categorizes cards from the games Love Live! School Idol Festival ALL STARS (SIFAS) and Love Live! School Idol Festival (SIF).
SIFAS cards and stills are downloaded from [Idol Story](https://idol.st/).
SIF cards are downloaded from [School Idol Tomodachi](https://schoolido.lu/).

## Installation

(Note: this software requires [Python](https://www.python.org/)>=3.10 and [Poetry](https://python-poetry.org/))

1. Clone this GitHub repository (`git clone https://github.com/DemonicSavage/sifas_card_downloader.git`)
2. Go to the `sifas_card_downloader` directory (`cd sifas_card_downloader` on Unix).
3. Optionally, [configure the program to your liking](#configuration).
4. Run `poetry install` to grab the necessary dependencies.

## Configuration

The `config.cfg` currently only has one option, which is `data_dir`. Change that to the directory you want your cards to be downloaded to.

## Usage

This is a command line script. It first downloads (or updates) metadata files about the available cards (`cards.json`/`stills.json`/`sif.json`), and then downloads the image files themselves.

By default, running `sifas_card_downloader` without any arguments will download SIFAS cards. Using the `--stills` argument will download SIFAS stills instead, and `--sif` will download SIF cards.

## License

This software is released under the GNU GPLv3, and its dependencies are released under their respective licenses.
