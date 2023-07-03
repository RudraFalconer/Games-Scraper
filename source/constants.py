# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 12:10:13 2023

@author: Sergio Morales Machado, Daniel Sohm
"""


#CONSTANTES

#pages
INIT_TEXT_PAGE = "href=\""
END_TEXT_PAGE = "\" title="

INIT_TEXT_TITLE = "href=\""
END_TEXT_TITLE = "\" title="

URL = "https://www.instant-gaming.com"
SUBURL_STEAM = "/es/juegos/steam/"

END_LOOP = "FINAL"

CONTAINS_DEVELOPER = "content=\"Developers\""

CONTAINS_PUBLISHER = "content=\"Publishers\""

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "utf-8",
    "Accept-Language": "en-US,en;q=0.8",
    "Cache-Control": "no-cache",
    "dnt": "1",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}
