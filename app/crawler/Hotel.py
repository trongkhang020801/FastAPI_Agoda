# -*- coding: utf-8 -*-
"""
Created on Tue May 17 13:25:06 2022

@author: ACER
"""

class Hotel :
    
    def __init__(self, ID, name, star, adress, price, priceSale, 
                 url, review, numOfReview,ratingAverage, photo, status):
        self.ID = ID
        self.name = name
        self.star = star
        self.adress = adress
        self.price = price
        self.priceSale = priceSale
        self.url = url
        self.review = review
        self.numOfReview = numOfReview
        self.ratingAverage = ratingAverage
        self.photo = photo
        self.status = status
        
    