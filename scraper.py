# biblioteca que faz a requisição
import requests 
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# url do produto que eu vou puxar
url = "https://www.kabum.com.br/produto/426262/processador-amd-ryzen-7-7800x3d-5-0ghz-max-turbo-cache-104mb-am5-8-nucleos-video-integrado-100-100000910wof"

# esse header é porque alguns sites bloqueiam scraping sem cabeçalho
headers = {
    "User-Agent": "Mozilla/5.0"
}

# comando que faz a requisição
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Encontrar nome e preço no site
name = soup.find("h1", class_="text-sm").text.strip()
price = soup.find("h4", class_="text-4xl text-secondary-500 font-bold transition-all duration-500").text.strip()

print("Produto: ", name)
print("Preço: ", price)

# Salva no csv
data = {
    "name": [name],
    "price": [price],
    "url": [url],
    "date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
}

df = pd.DataFrame(data)
df.to_csv("prices.csv", index=False)

print("Salvo em prices.csv!")