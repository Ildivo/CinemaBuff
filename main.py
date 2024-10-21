from typing import Union
from bs4 import BeautifulSoup
import aiohttp
from fastapi import FastAPI, Request
import asyncio
import json
#from imdby.imdb import imdb
from fake_useragent import UserAgent
from game import get_numbers, get_game_data, get_test_game_data
import random
import schema
import model

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, JSON, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import os

#from imdb import Cinemagoer
#from kinopoisk.movie import Movie
#movie_list = Movie.objects.search('matrix')
#print(movie_list)
#movie = Movie(id=278229)
#movie.get_content('posters')
#movie.get_content('main_page')
#print(movie)
#ia = Cinemagoer()
#h = ia.get_movie('0094226')
#print(h.videos)
#print(dir(h)) #['photo sites'][0])
#<span class=\"hero__primary-text\" data-testid=\"hero__primary-text\">Fight Club</span>

# print the names of the directors of the movie
#print('Directors:', details.movie_poster_url)
#section data-testid=\"section-images\"
 
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request, ):
    data = await get_game_data()
    return templates.TemplateResponse(
        request=request, name="game.html", context={"data": data}
    )

@app.get("/game", response_class=HTMLResponse)
async def game(request: Request, ):
    data = await get_game_data()
    return templates.TemplateResponse(
        request=request, name="game.html", context={"data": data}
    )
    
@app.post("/newgame")
async def newgame():
    data = await get_numbers()
    return data

@app.get("/r")
async def r():
    #movies = []
    with open('top250.json') as f:
        movies = json.load(f)
        
    numbers = random.sample(range(249), 10)
    print(numbers)
    urls = [movies[i]['url'] for i in numbers]
    print(urls)
    return {"message": movies}

@app.get("/top250")
async def top():
    url_images = f"https://www.imdb.com/chart/top/?sort=rank%2Casc"
    ua = UserAgent()
    user_agent = {
        'user-agent': ua.random,
        'accept': 'text/html'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url_images, headers=user_agent) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')
            script = soup.select_one("script[type='application/ld+json']")
            data = json.loads(script.text)
            
            movies = []

            for movie in data["itemListElement"]:
                movies.append({k: movie["item"][k] for k in ["name", "url", "image", "genre", "duration"]})

            print(movies)
            with open('test.json', 'w') as f:
                json.dump(movies, f)

    return {"html":movies}

    
@app.get("/1")
async def main():
    #section data-testid=\"MoreLikeThis
    url_images = f"https://www.imdb.com/title/tt0137523"
    ua = UserAgent()
    user_agent = {
        'user-agent': ua.random #'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.465 (Edition Yx GX)',
    }

    async with aiohttp.ClientSession() as session:
        
            
        async with session.get(url_images, headers=user_agent) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')
            #box = soup.find_all('section', data-testid='section-images')
            title_raw = soup.find("span", {"class":"hero__primary-text"}).get_text()
            #print(title_raw)
            box = soup.find("section", {"data-testid": "MoreLikeThis"})
            #span data-testid=\"title\">Inception</span>
            #<span class=\"hero__primary-text\" data-testid=\"hero__primary-text\">Fight Club</span>
            
            
            titles_like_this_raw = box.find_all("span", {"data-testid": "title"})
            titles_like_this = []
            for title in titles_like_this_raw:
                titles_like_this.append(title.text)
            print(title_raw)
            print(titles_like_this)
    return {"html": html}

@app.get("/movie/{id}")
async def read_root(id:str):
    #tt0137523
    url_movie_id = f"https://www.imdb.com/title/{id}"
    url_images = f"https://www.imdb.com/title/{id}/mediaindex"
    ua = UserAgent()
    user_agent = {
        'user-agent': ua.random 
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url_movie_id, headers=user_agent) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')

            title_raw = soup.find("span", {"class":"hero__primary-text"}).get_text()

            box = soup.find("section", {"data-testid": "MoreLikeThis"})

            titles_like_this_raw = box.find_all("span", {"data-testid": "title"})
            titles_like_this = []
            for title in titles_like_this_raw:
                titles_like_this.append(title.text)
            
        async with session.get(url_images, headers=user_agent) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')

            images = soup.find("section", {"data-testid": "section-images"})
            
            imgs = images.find_all('img')
            links = []
            for tag in imgs:
                  src_value = tag.get('src')
                  links.append(src_value)
            
    data = {
        "title": title_raw,
        "answers": titles_like_this,
        "images": links
    }
    print(data)
    return data

@app.get("/img")
async def get_img():
    return {"Hello": "world"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}







@app.post("/games/")
async def create_game(game: GameData, db: SessionLocal = Depends(get_db)):
    db_game = Game(data=game.data, answers=game.answers)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return {"message": "Game created successfully", "id": str(db_game.id)}