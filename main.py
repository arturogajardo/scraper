import time
from bs4 import BeautifulSoup
import requests
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Realizar el scraping una vez al iniciar la aplicación
scraped_data = None

def perform_scraping():
    global scraped_data
    url = "https://contraplano.cl/"

    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    news_data = []
    news_without_images = []

    link_divs = soup.find_all('div', class_=re.compile(r'.*category-*'))

    for link_div in link_divs:
        link = link_div.find('a', class_='post--link')['href']
        bg_image_element = link_div.find('div', class_='post--bg-image')
        bg_image_url = bg_image_element.get('data-wixi-bg-src') if bg_image_element else None
        heading = link_div.find('h3', class_='post--heading').text.strip()

        # Buscar el contenido de post--excerpt dentro de la etiqueta <p>
        excerpt_paragraph = link_div.find('p', class_='post--excerpt')
        excerpt = excerpt_paragraph.get_text(strip=True) if excerpt_paragraph else None

        if bg_image_url is None:
            news_without_images.append({
                'link': link,
                'heading': heading,
                'excerpt': excerpt
            })
        else:
            news_data.append({
                'link': link,
                'image': bg_image_url,
                'heading': heading,
                'excerpt': excerpt
            })

    scraped_data = {
        'news_with_images': news_data,
        'news_without_images': news_without_images
    }

# Ejecutar el scraping al iniciar la aplicación
perform_scraping()

@app.get("/scrape_news")
def scrape_news():
    global scraped_data
    return scraped_data











