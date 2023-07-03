# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 14:28:42 2023

@author: Sergio Morales Machado, Daniel Sohm
"""

import time
from datetime import datetime

from game import Game
import constants
<<<<<<< HEAD


# TODO: separar los métodos a otro py
# Definimos las diferentes funciones que necesitamos

def get_substring(text, substring_to_get_init, substring_to_get_end):
    first_string = text.find(substring_to_get_init)
    end_string = text.find(substring_to_get_end)
    return text[first_string + len(substring_to_get_init):end_string]


# Get urls that contain steam games

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


#Request each game url

def make_request(url):
    request = urllib.request.Request(url, headers=constants.HEADERS)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8', 'ignore')

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    return soup

#Getting name tags for the game(multiplayer, genre, etc)

def get_game_tags(tags):
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

#Get average game valoration

def get_game_valoration(game_number_reviews):
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

#Check if game is in stock

def check_if_game_is_in_stock(soup):
    is_any_stock = False
    has_stock = soup.find('div', {'class': 'stock'})
    if has_stock != None:
        is_any_stock = True

    return is_any_stock

#Check if game is available for preorder

def is_preorder(soup):
    preorder = soup.find('div', {'class': 'preorder'})
    if preorder is None:
        return False
    else:
        return True

#Check for game being f2p

def is_free_play(soup):
    f2p = soup.find('span', {'class': 'free-to-play button'})
    if f2p == None:
        return False
    else:
        return True


def get_game_stock(soup, is_preorder):
    """
    is_any_stock = False
    if is_preorder:
        game_stock1 = "El juego no ha salido"
    else:
        is_stock = soup.find('div', {'class': 'stock'})
        if is_stock is None:
            game_stock1 = "No hay stock"
        else:
            #game_stock1 = soup.find('div', {'class': 'stock'}).get_text(strip=True)
            is_any_stock = True
            game_stock1 = True
    return game_stock1, is_any_stock
    """
    is_any_stock = False
    if is_preorder:
        game_stock = "El juego no ha salido"
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


def get_release_date(soup, is_preorder):
    if is_preorder:
        game_release_date = soup.find('div', {'class': 'preorder'}).get_text(strip=True).replace("Lanzamiento ", "")
    else:
        game_release_date = soup.find('div', {'class': 'table-cell release-date'})
        if game_release_date != None:
            game_release_date = game_release_date.find(string=True).strip()
    return game_release_date


def get_download(soup, is_preorder, is_any_stock):
    if is_preorder:
        game_download = 'El juego no ha salido'
    else:
        if is_any_stock:
            game_download = soup.find('div', {'class': 'download'})
            if game_download != None:
                game_download = game_download.get_text(strip=True)
        else:
            game_download = ''
    return game_download


def get_number_reviews(soup, is_preorder):
    if is_preorder:
        game_number_reviews = 0
    else:
        game_number_reviews = soup.find('a', {'class': 'visit'})

        if game_number_reviews != None:
            game_number_reviews = game_number_reviews.get_text(strip=True).replace(" reviews", "")
    return game_number_reviews


def get_price(soup):
    game_price = soup.find('div', {'class': 'total'})
    if game_price != None:
        game_price = game_price.get_text(strip=True)
    return game_price


def get_discount(soup):
    game_discount = soup.find('div', {'class': 'discounted'})
    if game_discount != None:
        game_discount = game_discount.get_text(strip=True)
    return game_discount


now = datetime.now().strftime('%Y-%m-%d__%H-%M-%S')


def init_csv():
    csv_headers = ["title", "price", "discount", "developer", "publisher", "tags", "release_date", "valoration",
                   "reviews", "stock", "f2p"]
    with open('../dataset/games-' + str(now) + '.csv', mode='w', newline='', encoding='utf-8') as games_csv:
        writer = csv.writer(games_csv, delimiter=';')
        writer.writerow(csv_headers)
        games_csv.close()


def write_csv_row(game):
    # TODO: ver porque se crea una columna rara en la 2
    with open('../dataset/games-' + str(now) + '.csv', mode='a', newline='', encoding='utf-8') as games_csv:
        writer = csv.writer(games_csv, delimiter=';')
        writer.writerow([game.name, game.price, game.discount,
                         game.developer, game.publisher, game.tags,
                         game.release_date, game.valoration,
                         game.reviews, game.stock, game.f2p])
        games_csv.close()
=======
import scrapper_functions
>>>>>>> 1154889d7d1097eb16a5233854d0156c6d9e88a7


######################################################
# INIT
######################################################

start_time = time.time()
url = constants.URL + constants.SUBURL_STEAM

keep_page_loop = True

games_url = []

print("Getting all the pages")

# Obtención de todas Urls de las distintas páginas de los juegos 

while keep_page_loop:
    soup = scrapper_functions.make_request(url)
    
    # Obtención de todos lo juegos de la página actual
    games = soup.find_all('a', {'class': 'cover video'})

    # Loop de todos los juegos de la página actual y lo almacenamos en una lista de URLs
    for game in games:
        url_juego = scrapper_functions.get_substring(str(game), constants.INIT_TEXT_TITLE, constants.END_TEXT_TITLE)
        games_url.append(url_juego)

    pages = soup.find_all('a', {'class': 'arrow'})

    # Obtencion de la url de la siguiente página para coger los juegos
    next_page_url = scrapper_functions.get_next_page_url(pages)

    # Paramos si hemos llegado a la última página
    if next_page_url in constants.END_LOOP:
        break
    
    #Actualizamos la Url para la siguiente ejecución del bucle
    url = next_page_url.replace("&amp;", "&")
    url = constants.URL + url
    
print(f"Hay un total de {len(games_url)} juegos")

game_urls_errors = []

# Timestamp para los csv
now = datetime.now().strftime('%Y-%m-%d__%H-%M-%S')
scrapper_functions.init_csv(now)


# Bucle de todas las urls para obtener los atributos
parsedGameCount = 0
for game_url in games_url:
    try:
        parsedGameCount += 1
        print(f'{str(parsedGameCount)} of {len(games_url)}: {game_url}')
        
        # Obtenemos la página con el make_request
        # Usamos BeautifulSoup para parsearlo a html y poder obtener cada uno de los componentes
        soup = scrapper_functions.make_request(game_url)
        
        # Obtención de cada uno de los atributos
        game_name = soup.find('h1').find(text=True)
        game_price = scrapper_functions.get_price(soup)
        game_discount = scrapper_functions.get_discount(soup)
        game_tags = soup.find_all('a', {'class': 'tag'})   
        game_developer, game_publisher, game_genres = scrapper_functions.get_game_tags(game_tags) 
        game_f2p = scrapper_functions.is_free_play(soup)
        game_preorder = scrapper_functions.is_preorder(soup)
        game_number_reviews = scrapper_functions.get_number_reviews(soup, game_preorder)
        game_valoration = scrapper_functions.get_game_valoration(soup, game_number_reviews)
        game_release_date = scrapper_functions.get_release_date(soup, game_preorder)
        game_stock, is_any_stock = scrapper_functions.get_game_stock(soup, game_preorder)
        game_download =  scrapper_functions.get_download(soup, game_preorder, is_any_stock)
        
        # Creación del objeto Game y guardar en csv
        game_obj = Game(game_name, game_price, game_discount, game_developer, game_publisher, game_genres,
                        game_release_date, game_valoration, game_number_reviews, game_stock, game_download, game_f2p)
        scrapper_functions.write_csv_row(game_obj, now)
        
    except Exception as e:
        # TODO: verificar los errores que salgan
        print(e)
        game_urls_errors.append(game_url)

# Mostrar mensaje final de tiempo transcurrido
end_time = time.time()
print("\nelapsed time: " + str(round(((end_time - start_time) / 60), 2)) + " minutes")