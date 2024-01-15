import requests, json
from bs4 import BeautifulSoup
#   FOOTBALL NEWS
result_football = []
def get_football():
    url = "https://tribuna.uz"
    base_url = "https://tribuna.uz"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    container = soup.select_one(".daily-news")
    products = container.find_all("div", {"class":"ddd"})
    for product in products:
        url = base_url + product.select_one("a")["href"]
        photo = base_url + product.select_one('img')['src']
        title = product.select_one('.news-title').text
        result_football.append({
            "title" : title,
            "photo" : photo,
            "url" : url
        })
        
    with open("data/football.json", "w", encoding="utf-8") as file:
        json.dump(result_football, file, indent=4, ensure_ascii=False)


#   UZB NEWS
result_uzb = []
def get_uzb():
    url = "https://kun.uz/news/category/uzbekiston"
    base_url = "https://kun.uz"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    container = soup.select_one(".top-news")
    
    products_container = container.find("div", {"class":"top-news__small-items"}).find("div", {"class":"row"})
    products = products_container.find_all("div", {"class":"col-md-6"})
    for product in products:
        title = product.find("a", {"class":"small-news__title"}).text
        url =base_url + product.find("a", {"class":"small-news__title"}).get('href')
        photo = product.select_one("a", {"class":"small-news__img"}).find('img')['src']
        result_uzb.append({
            "title" : title,
            "photo" : photo,
            "url" : url
        })
        
    with open("data/uzb.json", "w", encoding="utf-8") as file:
        json.dump(result_uzb, file, indent=4, ensure_ascii=False)

#   EURO NEWS
def get_euro():
    url = "https://kun.uz/news/category/jahon"
    base_url = "https://kun.uz"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    container = soup.select_one(".top-news")
    
    products_container = container.find("div", {"class":"top-news__small-items"}).find("div", {"class":"row"})
    products = products_container.find_all("div", {"class":"col-md-6"})
    for product in products:
        title = product.find("a", {"class":"small-news__title"}).text
        url =base_url + product.find("a", {"class":"small-news__title"}).get('href')
        photo = product.select_one("a", {"class":"small-news__img"}).find('img')['src']
        result_uzb.append({
            "title" : title,
            "photo" : photo,
            "url" : url
        })
        
    with open("data/euro.json", "w", encoding="utf-8") as file:
        json.dump(result_uzb, file, indent=4, ensure_ascii=False)

get_euro()