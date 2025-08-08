import re
from datetime import datetime
import pandas as pd

def parse_price(price_str):
    # Recebe strings e devolve float, e retorna None se não conseguir parsear
    if price_str is None:
        return None
    s = str(price_str)
    s = s.replace('\xa0', '').strip() # Remove NBSP se tiver, 
    s = re.sub(r'[^\d\.,\-]', '', s) # remove tudo exceto dígito, ponto, vírgula e sinal negativo
    if s == '':
        return None
    
    # Caso tenha '.' e ',' assume formato brasileiro: . = milhares e , = decimal
    if '.' in s and ',' in s:
        s = s.replace('.', '').replace(',', '.')
    else:
        # se só tiver vírgula, troca por ponto
        if ',' in s and '.' not in s:
            s = s.replace(',', '.')
        # se só tiver ponto provavelmente já tá certo
    try:
        return float(s)
    except Exception:
        return None

def parse_datetime(dt):
    # tenta converter vários formatos pra datetime caso ainda não estejam certos
    if dt is None:
        return None
    if isinstance(dt, datetime):
        return dt
    s = str(dt)
    for fmt in ("&Y-%m-%d %H-%M-%S", "%Y-%m-%d", "%d-%m-%Y %H-%M-%S", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            pass
    # fallback para pandas
    try:
        return pd.to_datetime(s, dayfirst=True, errors='coerce')
    except Exception:
        return None