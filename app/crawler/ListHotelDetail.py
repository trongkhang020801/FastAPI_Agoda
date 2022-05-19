# -*- coding: utf-8 -*-
"""
Created on Thu May 19 03:04:36 2022

@author: ACER
"""

import time
from selenium import webdriver
from bs4 import BeautifulSoup
from crawler.HotelRoom import HotelRoom
from crawler.HotelDetail import HotelDetail
import os
import pandas as pd
from selenium.webdriver.chrome.service import Service

class ListHotelDetail:
    
    def __init__(self, url_data):
        self.url_data = url_data
        
    def scrollPage(self,driver):
        i = 5
        scroll_pause_time = 1
        screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
        while True:
            # scroll one screen height each time
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause_time)
            button_add = driver.find_elements_by_class_name('MasterRoom-showMoreLessButton')
            for s in button_add:
                if(s.get_attribute('data-element-name') == 'room-grid-show-more'):
                    driver.execute_script("arguments[0].click();",s)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = driver.execute_script("return document.body.scrollHeight;")  
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if(screen_height) * i > scroll_height:
                time.sleep(2)
                break


    def checkNullData(self,index):
        if(index != None):
            return index.text
        else:
            return '0 '

    def get_Data(self,commandExecutor,detailHotel,listRoom):
        
        s = Service('E:/python/export_files/chromedriver.exe')
        driver = webdriver.Chrome(service=s)
        
        
        driver.get(self.url_data)
        time.sleep(2)
        
        while True:
            
            self.scrollPage(driver)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            idh= soup.find("div",{"class":"MapCompact"})
            hotel_id = idh.get('data-provider-id')
            describe = soup.find("p",{"class":"Typographystyled__TypographyStyled-sc-j18mtu-0 fHvoAu kite-js-Typography"}).text
            address = soup.find("span",{"class":"Spanstyled__SpanStyled-sc-16tp9kb-0 gwICfd kite-js-Span HeaderCerebrum__Address"}).text
            images = soup.find_all("img",{"class":"SquareImage"})
         
            url_img = ''
            for i in images:
                url_img = url_img +","+i['src']
            url_img = url_img + ","
            
        
            room = soup.find_all("div",{"class":"MasterRoom MasterRoom--withMoreLess"})
            master_room_id = []
            room_names = []
            child_room_price = []
            child_room_capacity = []
            room_image = []
            child_detail_room = []
            hotel_room = []
            select_count = []
            for i in room:
                hotel_room.append(hotel_id)
                master_room_id.append(i.get('id'))
                id_room = i.get('id')
                child_room = i.find_all("div",{"class":"ChildRoomsList-room-contents"})
                room_name = i.find("span",{"class":"MasterRoom__HotelName"}).text
                room_names.append(room_name)
                images = i.find_all("img")
                url_img = ''
                for i in images:
                    url_img = url_img +","+i['src']
                url_img = url_img + ","
                room_image.append(url_img)
                detail = '~'
                for y in child_room:
                    price_child = y.find("h1").text[:-2]
                    child_room_price.append(price_child)
                    capacity = y.find("span",{"class":"Capacity-iconGroup"})
                    count = capacity.find_all("i")
                    child_room_capacity.append(len(count))
                    detail = detail + "price = "+price_child + "-capacity = " + str(len(count)) + '~'
                select_count.append(len(child_room)) 
                child_detail_room.append(detail)
                
                child = HotelRoom(hotel_id, id_room, room_name, url_img, len(child_room), detail)
                listRoom.append(child)
            break
       
        d = HotelDetail(hotel_id, address, describe, url_img, len(room), len(child_room_price))
        detailHotel.append(d)
    
        
        
         
            
    
    def exportCSV(self,path,detailHotel,listRoom):
        check_detail = os.path.exists(path + '/hotel_detail.csv')
        check_room = os.path.exists(path + '/hotel_room.csv')
        
        
        
               
            
        
        d = detailHotel[0]
       
        d = {'hotel_id': d.hotelId,
             'address' : d.address,
             'describe': d.describe,
             'img' : d.img,
             'room_count' : d.roomCount,
             'select_count_sum': d.selectCountSum}
        df = pd.DataFrame(d,index=[0])
        if(check_detail == False):
            df.to_csv(path + '/hotel_detail.csv',mode = 'ab',encoding='utf-8-sig',index=False)
        else:
            df.to_csv(path + '/hotel_detail.csv',mode = 'ab', header=False,encoding='utf-8-sig',index=False)
        
        hotel_room = []   
        master_room_id = [] 
        room_names = []  
        room_image = []   
        select_count = []  
        child_detail = []                                 
        for i in listRoom:   
            hotel_room.append(i.hotelId)
            master_room_id.append(i.masterRoomId)
            room_names.append(i.roomName)
            room_image.append(i.img)
            select_count.append(i.selectCount)
            child_detail.append(i.roomDetail)
        d2 = {'hotel_id': hotel_room,
             'master_room_id' : master_room_id,
             'room_names': room_names,
             'img' : room_image,
             'select_count' : select_count,
             'room_detail' : child_detail}
        
        df2 = pd.DataFrame(d2)
        if(check_room == False):
            df2.to_csv(path + '/hotel_room.csv', mode='ab',encoding='utf-8-sig',index=False)
        else:
            df2.to_csv(path + '/hotel_room.csv', mode='ab', header=False,encoding='utf-8-sig',index=False)