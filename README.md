<!--Software that automatically downloads cards from various idol or idol-adjacent gacha mobile games.-->
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

Mikan automatically downloads cards from various idol or idol-adjacent gacha mobile games.

The following games are currently supported:

- Love Live! School Idol Festival (via [School Idol Tomodachi](https://schoolido.lu/))
- Love Live! School Idol Festival ALL STARS (via [Idol Story](https://idol.st/))
- Love Live! School Idol Festival 2 (via [Idol Story](https://idol.st/))
- BanG Dream! Girls Band Party! (via [Bandori Party](https://bandori.party/))
- Revue Starlight -Re LIVE- (via [Starlight Academy](https://starlight.academy/))
- IDOLM@STER Cinderella Girls Starlight Stage (via [Cinderella Producers](https://cinderella.pro/))

## Installation

To install Mikan, you need to install `pipx` ([see instructions](https://pypa.github.io/pipx/installation/)) and then run `pipx install mikan-card-downloader`.

To update it, run `pipx upgrade mikan-card-downloader`.

Installing through `pip` is also possible, but not recommended, and since Python 3.11 requires the `--break-system-packages` flag.

## Building by source

(Note: this software requires [Python](https://www.python.org/)>=3.10 and [Poetry](https://python-poetry.org/))

1. Clone this GitHub repository (`git clone https://github.com/DemonicSavage/mikan.git`)
2. Go to the `mikan` directory (`cd mikan` on Unix).
3. Run `poetry install` to grab the necessary dependencies.

## Configuration

The configuration file currently has the following options:

```cfg
# Path for the downloaded cards
[Paths]
data_dir = ~/Idol_Cards

# Other options
[Other]
# Formerly needed for SIF2 support
cookie = your_sessionid_cookie
# Maximum concurrent connections, default is 10
max_connections = 10
```

You can find this file in `$XDG_CONFIG_HOME/mikan` on Linux, `%APPDATA%\Local\mikan\mikan` on Windows, or `/Library/Application Support/mikan` on macOS.

## Usage

This is a command line script. It first creates (or updates) a metadata file about the available cards (`items.json`), and then downloads the image files themselves.

By default, running `mikan` without any arguments will create metadata and then download SIF2 cards.

Arguments can be passed to `mikan` to download cards from other games. Run `mikan --help` to see what arguments are available.

~~Note that for now, you need a `sessionid` cookie for an Idol Story account with beta-testing enabled for SIF2 support.~~
This is no longer the case.

Running it for the first time will prompt you for the directory cards and stills should be downloaded to.

## License

This software is released under the GNU GPLv3 license, and its dependencies are released under their respective licenses.

# Links

- [PyPI](https://pypi.org/project/mikan-card-downloader/)
- [GitHub](https://github.com/DemonicSavage/mikan)
