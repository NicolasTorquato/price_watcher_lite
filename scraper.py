# biblioteca que faz a requisição
import requests 

# url do produto que eu vou puxar
url = "https://www.kabum.com.br/produto/439565/placa-de-video-rtx-4060"

# esse header é porque alguns sites bloqueiam scraping sem cabeçalho
headers = {
    "User-Agent": "Mozilla/5.0"
}

# comando que faz a requisição
response = requests.get(url, headers=headers)

# esse mostra o status da requisição, se for 200 é sucesso
print("Status:", response.status_code)

# isso mostra o começo do html
print(response.text[:500])