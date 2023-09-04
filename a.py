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
revistas_data = []

# Encuentra todos los elementos div con clases que contienen "post--link"
link_divs = soup.find_all('div', class_=re.compile(r'.*category-*'))

for link_div in link_divs:
    link = link_div.find('a', class_='post--link')['href']
    
    # Encuentra el elemento con la etiqueta 'img' si existe
    img_element = link_div.find('img')  # Agrega esto para buscar la etiqueta img
    
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
                    revistas_data.append({
                        'link': link,
                        'image': img_src,
                        'heading': heading
                    })
    elif bg_image_url is None:
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

# Imprime las revistas con imágenes
print("Revistas:")
for revista in revistas_data:
    print(f"Enlace: {revista['link']}")
    print(f"Imagen: {revista['image']}")
    print(f"Título: {revista['heading']}")
    print("")

