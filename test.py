import time
from bs4 import BeautifulSoup
import requests
import re

# Reemplaza la URL con la dirección real de tu página web
url = "https://contraplano.cl/"  # Cambia esto

time.sleep(7)

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

news_data = []
news_without_images = []

# Encuentra todos los elementos div con clases que contienen "post--link"
link_divs = soup.find_all('div', class_=re.compile(r'.*category-*'))

for link_div in link_divs:
    link = link_div.find('a', class_='post--link')['href']
    
    # Encuentra el elemento con el atributo data-wixi-bg-src si existe
    bg_image_element = link_div.find('div', class_='post--bg-image')
    bg_image_url = bg_image_element.get('data-wixi-bg-src') if bg_image_element else None
    
    heading = link_div.find('h3', class_='post--heading').text.strip()
    
    if bg_image_url is None:
        news_without_images.append({
            'link': link,
            'heading': heading
        })
    else:
        news_data.append({
            'link': link,
            'image': bg_image_url,
            'heading': heading
        })

# Imprime los datos de las noticias con imágenes
for news in news_data:
    print(f"Enlace: {news['link']}")
    print(f"Imagen: {news['image']}")
    print(f"Título: {news['heading']}")
    print("")

# Imprime las noticias sin imágenes
print("Ediciones:")
for news in news_without_images:
    print(f"Enlace: {news['link']}")
    print(f"Título: {news['heading']}")
    print("")
