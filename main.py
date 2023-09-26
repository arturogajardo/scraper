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
data = {'revistas': [], 'noticias': []}

def perform_scraping():
    global data
    url = "https://contraplano.cl/"

    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    link_divs = soup.find_all('div', class_=re.compile(r'.*category-*'))

    for link_div in link_divs:
        link = link_div.find('a', class_='post--link')['href']
        bg_image_element = link_div.find('div', class_='post--bg-image')
        bg_image_url = bg_image_element.get('data-wixi-bg-src') if bg_image_element else None
        heading = link_div.find('h3', class_='post--heading').text.strip()

        if 'category-revistas' in link_div['class']:
            noscript_element = link_div.find('noscript')  # Encuentra la etiqueta <noscript>
            if noscript_element:
                noscript_content = noscript_element.decode_contents()  # Obtiene el contenido de <noscript>
                noscript_soup = BeautifulSoup(noscript_content, 'html.parser')  # Analiza el contenido de <noscript>
                img_element_inside_noscript = noscript_soup.find('img')  # Busca la etiqueta img dentro de <noscript>

                if img_element_inside_noscript:
                    img_src = img_element_inside_noscript.get('src')  # Obtiene el atributo src de la etiqueta img
                    # Verifica si el atributo src comienza con "https://i0.wp.com"
                    if img_src and img_src.startswith("https://i0.wp.com"):
                        data['revistas'].append({
                            'link': link,
                            'image': img_src,
                            'heading': heading
                        })
        else:
            excerpt_paragraph = link_div.find('p', class_='post--excerpt')
            excerpt = excerpt_paragraph.get_text(strip=True) if excerpt_paragraph else None

            if bg_image_url is None:
                data['noticias'].append({
                    'link': link,
                    'heading': heading,
                    'excerpt': excerpt
                })
            else:
                data['noticias'].append({
                    'link': link,
                    'image': bg_image_url,
                    'heading': heading,
                    'excerpt': excerpt
                })

# Ejecutar el scraping al iniciar la aplicación
perform_scraping()

@app.get("/data")
def get_data():
    global data
    return data
