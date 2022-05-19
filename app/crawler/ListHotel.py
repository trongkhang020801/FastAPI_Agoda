# -*- coding: utf-8 -*-
"""
Created on Tue May 17 13:38:40 2022

@author: ACER
"""
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from pathlib import Path
from crawler.Hotel import Hotel
import pandas as pd
from selenium.webdriver.chrome.service import Service

class ListHotel:
    
    hotelList =  []
    def __init__(self, url_data):
        self.url_data = url_data
        
    def scrollPage(self,driver):
        i = 1
        scroll_pause_time = 1
        screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
        while True:
            # scroll one screen height each time
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = driver.execute_script("return document.body.scrollHeight;")
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height) * i > scroll_height:
                time.sleep(2)
                break

    def checkNullData(self,index):
        if(index != None):
            return index.text
        else:
            return '0 '

    def get_Data(self,commandExecutor):
        
        s = Service('E:/python/export_files/chromedriver.exe')
        driver = webdriver.Chrome(service=s)
        
        
        driver.get(self.url_data)
        time.sleep(2)
        
        while True:
            
            self.scrollPage(driver)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            li = soup.find_all("li", {"class": "PropertyCard PropertyCardItem"})
            print('count = ', len(li))
            
            try:
                #Thêm khach san
                for item in li:
                    if(self.getIndex(item) != None):
                        obj = self.getIndex(item)
                        self.hotelList.append(obj)
            except Exception as e:
                print('error funct getData: ',e)
                
    
            button_next = driver.find_elements_by_class_name('pagination2__next')
            if len(button_next) > 0:
                button_next = button_next[0]
            else:
                time.sleep(2)
                driver.quit()
                break
            time.sleep(2)
            driver.execute_script("arguments[0].click();", button_next)
            
         
            
    def getIndex(self,hotel):
        for s in self.hotelList:
            if(hotel.get('data-hotelid') == s.ID ):
                return None
 
        #Lấy dữ liệu
        try:
            idh = hotel.get('data-hotelid')
            name = hotel.find("h3",{"class":"PropertyCard__HotelName"}).text
            star = hotel.find("i",{"id":"NHAWEB-2124"}).get('title')
            adress = hotel.find("span",{"class":"Address__Text"}).text
            price = self.checkNullData(hotel.find("div",{"class":"PropertyCardPrice"}))
            price_sale = self.checkNullData(hotel.find("span",{"class":"PropertyCardPrice__Value"}))
            url =  hotel.find("a", {"class":"PropertyCard__Link"})['href']
            review = self.checkNullData(hotel.find("span",{"class":"Spanstyled__SpanStyled-sc-16tp9kb-0 kkSkZk kite-js-Span Box-sc-kv6pi1-0 eRxXoo"}))
            num_of_review = self.checkNullData(hotel.find("span",{"class":"Spanstyled__SpanStyled-sc-16tp9kb-0 jYmZbG kite-js-Span Box-sc-kv6pi1-0 jjmSNA"}))
            rating_average = self.checkNullData(hotel.find("p",{"class":"Typographystyled__TypographyStyled-sc-j18mtu-0 Hkrzy kite-js-Typography"}))
            status = self.checkNullData(hotel.find("button",{"class":"Buttonstyled__ButtonStyled-sc-5gjk6l-0 evAQLf"}))
            photo = hotel.find("div",{"class":"Overlay"}).find('img')['src']
        
            #Xử lý dữ liệu
            star = float(star[:star.find(" ")] if (star[:star.find(" ")].strip()) else 0)
            price = price[:price.find(" ")].replace('.', '')
            price_sale = price_sale[:price_sale.find(" ")].replace('.', '')
            num_of_review = int(num_of_review[:num_of_review.find(" ")].replace('.', ''))
            rating_average = rating_average.replace(',', '.')
            url = 'https://www.agoda.com/' + url
        
            #Thêm dữ liệu
            item = Hotel(idh,name,star,adress,price,price_sale,url,
                         rating_average,num_of_review,review,photo,status)
            
            return item

        except Exception as e:
            print('id-hotel=',idh, ',error getIndex: ',e)
            return None
    
    def exportCSV(self,path):
        hotel_id = []
        hotel_name = []
        hotel_star = []
        hotel_adress = []
        hotel_price = []
        hotel_price_sale = []
        hotel_url = []
        hotel_review = []
        hotel_num_of_review = []
        hotel_rating_average = []
        hotel_status = []
        hotel_photo = []
        
        for i in self.hotelList:
            hotel_id.append(i.ID)
            hotel_name.append(i.name)
            hotel_star.append(i.star)
            hotel_adress.append(i.adress)
            hotel_price.append(i.price)
            hotel_price_sale.append(i.priceSale)
            hotel_url.append(i.url)
            hotel_rating_average.append(i.ratingAverage)
            hotel_num_of_review.append(i.numOfReview)
            hotel_review.append(i.review)
            hotel_status.append(i.status)
            hotel_photo.append(i.photo)
        d = { 'hotel_id' : hotel_id
             ,'hotel_name' : hotel_name
             ,'hotel_start' : hotel_star
             ,'hotel_adress' : hotel_adress
             ,'hotel_price' : hotel_price
             ,'hotel_price_sale' : hotel_price_sale
             ,'hotel_url' : hotel_url
             ,'hotel_rating_average' : hotel_rating_average
             ,'hotel_review' : hotel_review
             ,'hotel_num_of_review' : hotel_num_of_review
             ,'hotel_active' : hotel_status
             ,'hotel_image' : hotel_photo}
        # Ghi vào data
        dFrame = pd.DataFrame(d)
        # lọc các dòng trùng nhau
        dFrame = dFrame.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)  
        
        #Ghi vào CSV
        filepath = Path(path +'/hotel_agoda.csv')  
        filepath.parent.mkdir(parents=True, exist_ok=True)
        dFrame.to_csv(filepath,encoding='utf-8-sig',index=False) 
