# -*- coding: utf-8 -*-
"""
Created on Thu May 19 02:45:53 2022

@author: ACER
"""
from crawler.ListHotel import ListHotel
from crawler.ListHotelDetail import ListHotelDetail
from crawler.HotelDetail import HotelDetail

command_executor = 'http://172.17.0.2:4444'


def getAllListHotel(url):
    obj = ListHotel(url,command_executor)
    obj.get_Data()
    obj.exportCSV('./')
    print(len(obj.hotelList))
    
def getDetailHotel(url):
    detail = []
    listRoom = []
    obj = ListHotelDetail(url)
    obj.get_Data(command_executor,detail , listRoom)
    obj.exportCSV('./',detail , listRoom)
    
    