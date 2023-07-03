# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 14:28:42 2023

@author: Sergio Morales Machado, Daniel Sohm
"""

class Game:
    def __init__(self, name, price, discount, developer, publisher, tags, release_date, valoration, reviews, stock, download, f2p):
        self.name = name
        self.price = price
        self.discount = discount
        self.developer = developer
        self.publisher = publisher
        self.tags = tags
        self.release_date = release_date
        self.valoration = valoration
        self.reviews = reviews
        self.stock = stock
        self.download = download
        self.f2p = f2p
