import random
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import aiohttp
import asyncio
from json.decoder import JSONDecodeError



async def to_base(data, url):
  with open('base_top250.json', 'a+') as infile, open('base_top250.json', 'a+') as outfile:
    ss = {}
    try:
        movies = json.load(infile)
        print(movies)
        if not url in movies:
          movies[url] = data
          json.dump(movies, outfile)
    except JSONDecodeError:
      print("e")
      ss[url] = data
      json.dump(ss, outfile)
    
  return {"hello": "world"}
  
async def get_images(url, user_agent):
  url_image = url + 'mediaindex'
  print(url_image)
  async with aiohttp.ClientSession() as session:
    async with session.get(url_image, headers=user_agent) as response:
        html = await response.text()
        #print(html)
        soup = BeautifulSoup(html, 'lxml')

        images = soup.find("section", {"data-testid": "section-images"})

        imgs = images.find_all('img')
        links = []
        if len(imgs) > 5:
          for i in range(5):
            src_value = imgs[i].get('src')
            links.append(src_value)
        else:
          for tag in imgs:
            src_value = tag.get('src')
            links.append(src_value)
  return links


async def get_info(url, user_agent):
  async with aiohttp.ClientSession() as session:
    async with session.get(url, headers=user_agent) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'lxml')

        title_raw = soup.find("span", {"class":"hero__primary-text"}).get_text()

        box = soup.find("section", {"data-testid": "MoreLikeThis"})
        titles_like_this_raw = box.find_all("span", {"data-testid": "title"})
        titles_like_this = []
        for title in titles_like_this_raw:
            titles_like_this.append(title.text)
  images = await get_images(url, user_agent)
  #await to_base({"title": title_raw, "answers": titles_like_this, "images": images}, url)
  #print({"title": title_raw, "answers": titles_like_this, "images": images})
  return {"title": title_raw, "answers": titles_like_this, "images": images}

async def get_test_game_data():
  with open('test.json') as f:
    data = json.load(f)
    return data


async def get_game_data():
  movies = []
  with open('top250.json') as f:
    movies = json.load(f)
    #print(d)
  numbers = random.sample(range(249), 10)
  print(numbers)
  urls = [movies[i]['url'] for i in numbers]
  #urls = [movies[i]['url'] for i in range(10)]
  #print(urls)
  
  ua = UserAgent()
  user_agent = {
      'user-agent': ua.random 
  }
  total = []
  tasks = []
  for url in urls:
    task = asyncio.create_task(get_info(url, user_agent))
    tasks.append(task)
    #total.extend(await asyncio.gather(*tasks))
  total = await asyncio.gather(*tasks)
  #with open('test.json', 'a') as f:
      #json.dump(total, f)
  return total

async def get_numbers():
  movies = []
  with open('top250.json') as f:
    movies = json.load(f)
    #print(d)

  numbers = random.sample(range(249), 10)
  print(numbers)
  urls = [movies[i]['url'] for i in numbers]
  #urls = [movies[i]['url'] for i in movies]
  print(urls)
  
  url_movie_id = f"https://www.imdb.com/title/{id}"
  url_images = f"https://www.imdb.com/title/{id}/mediaindex"
  ua = UserAgent()
  user_agent = {
      'user-agent': ua.random 
  }
  total = []
  
  for url in urls:
    url_image = url + 'mediaindex'
    print(url_image)
    async with aiohttp.ClientSession() as session:
      async with session.get(url, headers=user_agent) as response:
          html = await response.text()
          soup = BeautifulSoup(html, 'lxml')
  
          title_raw = soup.find("span", {"class":"hero__primary-text"}).get_text()
  
          box = soup.find("section", {"data-testid": "MoreLikeThis"})
  
          titles_like_this_raw = box.find_all("span", {"data-testid": "title"})
          titles_like_this = []
          for title in titles_like_this_raw:
              titles_like_this.append(title.text)
              
    async with aiohttp.ClientSession() as session:
      async with session.get(url_image, headers=user_agent) as response:
          html = await response.text()
          #print(html)
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
      total.append(data)
  return total
#return data