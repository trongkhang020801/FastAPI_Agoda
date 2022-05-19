from fastapi import FastAPI
import pymysql
con = pymysql.connect(db='DB_Angoda', user='root', passwd='', host='localhost', port=3306)
app=FastAPI()

# best way to make api
@app.get('/api/hotel')
async def index():
    with con.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM Hotel"
        cursor.execute(sql)
        result = cursor.fetchall()
    return {
        "success": True,
        "data":result
    }
# search data

@app.get('/api/search_price/{search_price}')
async def search(price1, price2):
    with con.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM Hotel where hotel_price>= "+price1+" and hotel_price<=" +price2 
        cursor.execute(sql)
        result = cursor.fetchall()
    return {
        "success": True,
        "data":result
    }

@app.get('/api/search_start/{search_start}')
async def search(start1, start2):
    with con.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM Hotel where hotel_start>= "+start1+" and hotel_start<=" +start2 
        cursor.execute(sql)
        result = cursor.fetchall()
    return {
        "success": True,
        "data":result
    }
