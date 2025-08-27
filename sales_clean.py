import pandas as pd

# Caminho do arquivo bruto
INPUT_FILE = "data/sales_2024.csv"


def run_etl():
    # === EXTRACT ===
    df = pd.read_csv(INPUT_FILE)

    # === TRANSFORM ===

    # 1. Padronizar datas para formato YYYY-MM-DD
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

    # 2. Corrigir categorias (capitalização consistente)
    df["category"] = df["category"].str.capitalize().str.strip()

    # 3. Corrigir preços (trocando vírgula por ponto e convertendo para float)
    df["price"] = df["price"].astype(str).str.replace(",", ".", regex=False)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    # 4. Calcular valor total da transação
    df["total_value"] = df["quantity"] * df["price"]

    # 5. Criar coluna ano-mês (útil para agregações)
    df["year_month"] = df["date"].dt.to_period("M")

    # 6. Remover registros inválidos (sem data, preço ou cliente)
    df = df.dropna(subset=["date", "price", "customer_id"])

    # === LOAD (para este MVP: apenas devolver DataFrame) ===
    return df


if __name__ == "__main__":
    clean_df = run_etl()
    print(clean_df.head())
