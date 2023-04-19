[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=bugs)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=DemonicSavage_sifas_card_downloader&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=DemonicSavage_sifas_card_downloader)

SYNOPSIS:
./sifas_card_downloader [OPTIONS...]

DESCRIPTION:
The program automatically downloads and categorizes cards from the game Love Live! School Idol Festival ALL STARS.
Images are downloaded from https://idol.st/. Also works with School Idol Festival cards, with images downloaded
from https://schoolido.lu/.

USAGE:
Just run ./sifas_card_downloader. Use "--stills" to download stills instead of cards, or use "--sif" to download
School Idol Festival cards.

OPTIONS:
-h, --help
Outputs this message and exits

    --stills
            Works with stills instead of cards (won't organize the stills)

    --sif
            Works with SIF cards instead of SIFAS cards (won't organize the cards)
