# biblioteca que faz a requisição
import requests 
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import csv


products = [
    {
        "name": "Ryzen 7 7800X3D",
        "url": "https://www.kabum.com.br/produto/426262/processador-amd-ryzen-7-7800x3d-5-0ghz-max-turbo-cache-104mb-am5-8-nucleos-video-integrado-100-100000910wof",
        "price_class": "text-4xl text-secondary-500 font-bold transition-all duration-500"
    },
    {
        "name": "Intel Core i9-12900KS", 
        "url": "https://www.kabum.com.br/produto/315286/processador-intel-core-i9-12900ks-3-4ghz-5-5ghz-max-turbo-cache-30mb-lga-1700-video-integrado-bx8071512900ks",
        "price_class": "text-4xl text-secondary-500 font-bold transition-all duration-500"
    }
]


# esse header é porque alguns sites bloqueiam scraping sem cabeçalho
def fetch_product_info(product):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # comando que faz a requisição
    response = requests.get(product["url"], headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontrar nome e preço no site
    title = soup.find("h1").text.strip()
    price = soup.find("h4", class_=product["price_class"]).text.strip()

    return title, price

# Arquivo de saída
csv_file = "prices.csv"

# Criar cabeçalho se ainda não existir
try:
    with open(csv_file, "x", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Data", "Produto", "Preço"])
except FileExistsError:
    pass

# Salvar os dados com data e hora
with open(csv_file, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for product in products:
        try:
            title, price = fetch_product_info(product)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([now, title, price])
            print(f"Salvo: {title} - {price}")
        except Exception as e:
            print(f"Erro as processar {product['name']}: {e}")