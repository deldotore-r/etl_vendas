import pandas as pd
from sales_clean import run_etl
import matplotlib.pyplot as plt

def analyze_sales():
    # Executa o ETL
    transformed_data = run_etl()

    # Exibe as primeiras linhas
    print("Prévia dos dados transformados:")
    print(transformed_data.head())

    # -------------------------------
    # Gráfico 1: Vendas por mês (barras verticais) + média/mediana
    # -------------------------------
    transformed_data["year_month"] = transformed_data["date"].dt.to_period("M")
    sales_over_time = transformed_data.groupby("year_month")["total_value"].sum()

    mean_month = sales_over_time.mean()
    median_month = sales_over_time.median()

    plt.figure(figsize=(9, 6))  # 50% do tamanho anterior
    sales_over_time.plot(kind="bar", color="green", edgecolor="black")
    plt.axhline(mean_month, color="blue", linestyle="--", linewidth=1.5, label=f"Média ({mean_month:.2f})")
    plt.axhline(median_month, color="red", linestyle=":", linewidth=1.5, label=f"Mediana ({median_month:.2f})")
    plt.title("Vendas por Mês")
    plt.xlabel("Mês")
    plt.ylabel("Vendas Totais (€)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))  # legenda fora do gráfico
    plt.tight_layout()
    plt.savefig("sales_by_month.png", bbox_inches="tight")
    plt.show()

    # -------------------------------
    # Gráfico 2: Top 10 produtos mais vendidos + média/mediana
    # -------------------------------
    top_products = (
        transformed_data.groupby("product")["total_value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    mean_product = top_products.mean()
    median_product = top_products.median()

    plt.figure(figsize=(9, 6))  # 50% do tamanho anterior
    top_products.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.axhline(mean_product, color="blue", linestyle="--", linewidth=1.5, label=f"Média ({mean_product:.2f})")
    plt.axhline(median_product, color="red", linestyle=":", linewidth=1.5, label=f"Mediana ({median_product:.2f})")
    plt.title("Top 10 Produtos Mais Vendidos")
    plt.xlabel("Produto")
    plt.ylabel("Vendas Totais")
    plt.xticks(rotation=45, ha="right")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig("top_products.png", bbox_inches="tight")
    plt.show()

    # -------------------------------
    # Gráfico 3: Vendas por região (barras horizontais) + média/mediana
    # -------------------------------
    sales_by_region = transformed_data.groupby("store_location")["total_value"].sum().sort_values()

    mean_region = sales_by_region.mean()
    median_region = sales_by_region.median()

    plt.figure(figsize=(9, 5))  # 50% do tamanho anterior
    sales_by_region.plot(kind="barh", color="coral", edgecolor="black")
    plt.axvline(mean_region, color="blue", linestyle="--", linewidth=1.5, label=f"Média ({mean_region:.2f})")
    plt.axvline(median_region, color="red", linestyle=":", linewidth=1.5, label=f"Mediana ({median_region:.2f})")
    plt.title("Vendas por Região")
    plt.xlabel("Vendas Totais (€)")
    plt.ylabel("Região")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig("sales_by_region.png", bbox_inches="tight")
    plt.show()

    # -------------------------------
    # Exibição no console
    # -------------------------------
    print("\nResumo das vendas por região:")
    print(sales_by_region)
    print("\nResumo Top 10 produtos:")
    print(top_products)
    print("\nVendas por mês:")
    print(sales_over_time)

if __name__ == "__main__":
    analyze_sales()
