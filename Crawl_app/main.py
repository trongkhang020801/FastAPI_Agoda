# -*- coding: utf-8 -*-
"""
Created on Tue May 17 14:43:57 2022

@author: ACER
"""

from crawler.Crawl import *
import pandas as pd
import numpy as np


'''
data = pd.read_csv('./crawler/hotel_agoda.csv')

y = data["hotel_url"]
url_array = y.values

h = 0
for i in url_array:
    h+=1;
    if(h == 10):
        break
    try:
        getDetailHotel(i)
    except Exception as e:
        print('url',i, ',error getDetail: ',e)
'''
getAllListHotel('https://www.agoda.com/vi-vn/search?city=16440')
