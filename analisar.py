import os
import pandas as pd
import unicodedata
from utils.cleaner import parse_price, parse_datetime

CSV_IN = "prices.csv"
CSV_CLEAN = "prices_cleaned.csv"

def normalize_col(name: str) -> str:
    """Remove acentos, espaços e coloca em minúsculo."""
    name = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    return name.strip().lower()

def main():
    if not os.path.exists(CSV_IN):
        print(f"Arquivo {CSV_IN} não encontrado. Rode o scraper primeiro.")
        return
    
    df = pd.read_csv(CSV_IN, encoding="utf-8")

    # Normaliza nomes das colunas
    col_map = {col: normalize_col(col) for col in df.columns}
    df = df.rename(columns=col_map)

    print("Colunas encontradas:", df.columns.tolist())

    # Detecta colunas importantes
    price_col = next((c for c in df.columns if "preco" in c or "price" in c), None)
    date_col = next((c for c in df.columns if "data" in c or "date" in c), None)
    product_col = next((c for c in df.columns if "produto" in c or "product" in c or "name" in c), None)


    if not price_col or not date_col or not product_col:
        raise ValueError(f"Coluna de preço, data ou produto não encontrada no CSV. Colunas: {df.columns.tolist()}")

    # Cria colunas parseadas
    df["price_value"] = df[price_col].apply(parse_price)
    df["date_parsed"] = pd.to_datetime(df[date_col], errors="coerce")

    # Limpar linhas inválidas
    before = len(df)
    df = df.dropna(subset=["price_value"])  # remove onde não conseguiu price
    df = df.drop_duplicates(subset=[date_col, product_col, price_col])  # remove duplicatas exatas
    after = len(df)
    print(f"Linhas antes: {before} - depois (limpeza + dedupe): {after}")

    # Salva CSV limpo
    df.to_csv(CSV_CLEAN, index=False, encoding="utf-8")
    print(f"CSV limpo salvo em: {CSV_CLEAN}")

    # Estatísticas por produto
    summary = df.groupby(product_col).agg(
        observations=("price_value", "count"),
        mean_price=("price_value", "mean"),
        min_price=("price_value", "min"),
        max_price=("price_value", "max")
    ).reset_index()

    pd.options.display.float_format = "{:,.2f}".format
    print("\nResumo por produto:")
    print(summary.to_string(index=False))

    # Para cada produto: último preço e data do menor preço
    for product in df[product_col].unique():
        dprod = df[df[product_col] == product].sort_values("date_parsed")
        if dprod.empty:
            continue
        last = dprod.iloc[-1]
        min_row = dprod.loc[dprod["price_value"].idxmin()]
        print(f"\n{product}")
        print(f"    Último preço: R$ {last['price_value']:.2f} em {last['date_parsed']}")
        print(f"    Menor preço: R$ {min_row['price_value']:.2f} em {min_row['date_parsed']}")

    # Gerar gráficos
    try:
        import matplotlib.pyplot as plt
        for product in df[product_col].unique():
            dprod = df[df[product_col] == product].sort_values("date_parsed")
            if len(dprod) < 2:
                continue
            plt.figure()
            plt.plot(dprod["date_parsed"], dprod["price_value"])
            plt.title(product)
            plt.xlabel("Data")
            plt.ylabel("Preço (R$)")
            plt.tight_layout()
            filename = f"plot_{product[:20].replace(' ', '_')}.png"
            plt.savefig(filename)
            print(f"    Gráfico salvo: {filename}")
    except Exception as e:
        print("Não foi possível gerar gráficos:", e)

if __name__ == "__main__":
    main()
