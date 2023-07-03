# TODO

* ~~CSV date format > human readable format~~
* ~~Add CSV headers~~
* ~~Fix crawling issues with certain URLs (e.g. https://www.instant-gaming.com/es/9064-comprar-juego-steam-wallace-gromit%e2%80%99s-grand-adventures/)~~
* Full-run and check whether there are any more errors
  * ~~'utf-8' codec can't decode byte 0xc3 in position 69825: invalid continuation byte~~
  * Handle unreleased game edge-case
  * Handle free-to-play game edge-case
  * ~~Handle out-of-stock game edge-case~~
* Refactoring
  * ~~Create csv first, and write data into csv after parsing it. Performance increase: avoid memory leak~~
  * Move crawling/parsing methods to other files
  * Improve game url fetching
  * Fix warnings
* Add comments to the code
