import schedule
import time
import subprocess
import sys

def rodar_scraper():
    print("Executando scraper...")
    subprocess.run([sys.executable, "scraper.py"])

#Executa a cada 30 minutos (dá pra mudar pra `every().hour ou every().minutes`, etc)
schedule.every(10).seconds.do(rodar_scraper)

print("Agendador iniciado. Pressione Ctrl+C para parar.")
while True:
    schedule.run_pending()
    time.sleep(1)