# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 16:23:41 2023

@author: Sergio Morales Machado, Daniel Sohm
"""

import urllib.request
import csv
import constants

def get_substring(text, substring_to_get_init, substring_to_get_end):
    first_string = text.find(substring_to_get_init)
    end_string = text.find(substring_to_get_end)
    return text[first_string + len(substring_to_get_init):end_string]


# Obtenemos la siguiente pagina para scrapear

def get_next_page_url(pages):
    if (len(pages) == 1):
        if ("title=\"Next\"" in str(pages[0])):
            return get_substring(str(pages[0]), constants.INIT_TEXT_PAGE, constants.END_TEXT_PAGE)
        else:
            return constants.END_LOOP
    elif (len(pages) == 2):
        if ("title=\"Next\"" in str(pages[1])):
            return get_substring(str(pages[1]), constants.INIT_TEXT_PAGE, constants.END_TEXT_PAGE)
        else:
            return constants.END_LOOP
    else:
        return constants.END_LOOP

# Obtención del contenido de la página pasada por parámetro
def make_request(url):
    request = urllib.request.Request(url, headers=constants.HEADERS)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8', 'ignore')

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    return soup

# Obtención de los distintos tags de los juegos: desarrollador, publicador y tags del juego
def get_game_tags(game_tags):
    game_publisher = ""
    game_developer = ""
    game_genres = []
    for tag in game_tags:
        if constants.CONTAINS_DEVELOPER in str(tag):
            game_developer = tag.find(string=True)
        elif constants.CONTAINS_PUBLISHER in str(tag):
            game_publisher = tag.find(string=True)
        else:
            game_genres.append(tag.find(string=True))
    return game_developer, game_publisher, game_genres

# Obtención de la valoración
def get_game_valoration(soup, game_number_reviews):
    if game_number_reviews != None:
        if int(game_number_reviews) == 0:
            game_valoration = None
        else:
            game_valoration = soup.find('div', {'class': 'ig-search-reviews-avg'})
            if game_valoration != None:
                game_valoration = game_valoration.get_text(strip=True)
    else:
        game_valoration = None
    return game_valoration

# Obtención si hay stock del juego
def check_if_game_is_in_stock(soup):
    is_any_stock = False
    has_stock = soup.find('div', {'class': 'stock'})
    if has_stock != None:
        is_any_stock = True

    return is_any_stock

# Ver si el juego es para hacer preorder
def is_preorder(soup):
    preorder = soup.find('div', {'class': 'preorder'})
    if preorder is None:
        return False
    else:
        return True

# Obtención de si es FTP o no
def is_free_play(soup):
    f2p = soup.find('span', {'class': 'free-to-play button'})
    if f2p == None:
        return False
    else:
        return True

# Obtener stock del juego
def get_game_stock(soup, is_preorder):
    is_any_stock = False
    if is_preorder:
        game_stock = ""
    else:
        is_stock = soup.find('div', {'class': 'stock'})
        if is_stock == None:
            game_stock = soup.find('div', {'class': 'nostock'})
            if game_stock != None:                
                game_stock = soup.find('div', {'class': 'nostock'}).get_text(strip=True)
        else:
            game_stock = soup.find('div', {'class': 'stock'}).get_text(strip=True)
            is_any_stock = True
    return game_stock, is_any_stock

#Obtener fecha de lanzamiento
def get_release_date(soup, is_preorder):
    if is_preorder:
        game_release_date = soup.find('div', {'class': 'preorder'}).get_text(strip=True).replace("Lanzamiento ", "")
    else:
        game_release_date = soup.find('div', {'class': 'table-cell release-date'})
        if game_release_date != None:
            game_release_date = game_release_date.find(string=True).strip()
    return game_release_date

#Obtener método de descarga
def get_download(soup, is_preorder, is_any_stock):
    if is_preorder:
        game_download = ''
    else:
        if is_any_stock:
            game_download = soup.find('div', {'class': 'download'})
            if game_download != None:
                game_download = game_download.get_text(strip=True)
        else:
            game_download = ''
    return game_download

#Obtención de la cantidad de reviews
def get_number_reviews(soup, is_preorder):
    if is_preorder:
        game_number_reviews = 0
    else:
        game_number_reviews = soup.find('a', {'class': 'visit'})

        if game_number_reviews != None:
            game_number_reviews = game_number_reviews.get_text(strip=True).replace(" reviews", "")
    return game_number_reviews

#Obtener precio
def get_price(soup):
    game_price = soup.find('div', {'class': 'total'})
    if game_price != None:
        game_price = game_price.get_text(strip=True)
    return game_price

#Obtener descuento
def get_discount(soup):
    game_discount = soup.find('div', {'class': 'discounted'})
    if game_discount != None:
        game_discount = game_discount.get_text(strip=True)
    return game_discount

#Inicializar CSV
def init_csv(now):
    csv_headers = ["title", "price", "discount", "developer", "publisher", "tags", "release_date", "valoration",
                   "reviews", "stock", "descarga", "f2p"]
    with open('../dataset/games-' + str(now) + '.csv', mode='w', newline='', encoding='utf-8') as games_csv:
        writer = csv.writer(games_csv, delimiter=';')
        writer.writerow(csv_headers)
        games_csv.close()

# Escribir en el csv
def write_csv_row(game, now):
    # TODO: ver porque se crea una columna rara en la 2
    with open('../dataset/games-' + str(now) + '.csv', mode='a', newline='', encoding='utf-8') as games_csv:
        writer = csv.writer(games_csv, delimiter=';')
        writer.writerow([game.name, game.price, game.discount,
                         game.developer, game.publisher, game.tags,
                         game.release_date, game.valoration,
                         game.reviews, game.stock, game.download, game.f2p])
        games_csv.close()
