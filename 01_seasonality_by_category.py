import os
import pandas as pd
import matplotlib.pyplot as plt
from sales_clean import run_etl

os.makedirs("outputs/plots", exist_ok=True)

def main():
    df = run_etl()
    df["year_month"] = df["date"].dt.to_period("M")

    # Agrupa por mês e categoria
    pivot = (
        df.groupby(["year_month", "category"])["total_value"]
        .sum()
        .unstack(fill_value=0)
    )

    pivot.to_csv("outputs/seasonality_by_category_monthly.csv")

    # Reconstrói um novo DataFrame com apenas as top 2 categorias por mês
    filtered_rows = []
    for month in pivot.index:
        top2 = pivot.loc[month].sort_values(ascending=False).head(2)
        filtered_rows.append(top2)

    # Cria DataFrame final com as top 2 categorias por mês
    final_df = pd.DataFrame(filtered_rows, index=pivot.index)
    final_df = final_df.fillna(0)

    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = 1.4  # Largura total para as duas barras juntas
    months = final_df.index
    x = range(len(months))

    # Cores sóbrias
    colors = ["#4C78A8", "#66C2A5"]

    # Espaçamento entre meses
    for i, month in enumerate(months):
        # Garante que só as top 2 categorias sejam usadas
        category_values = final_df.loc[month].sort_values(ascending=False).head(2)
        x_positions = [i * 2 + j * (bar_width / 2) for j in range(2)]  # Posiciona sem espaço interno
        for j, (category, value) in enumerate(category_values.items()):
            ax.bar(
                x_positions[j],
                value,
                width=bar_width / 2,  # Cada barra usa metade da largura total
                color=colors[j],
                edgecolor="black"
            )
            if pd.notna(value) and value > 0:
                # Posiciona o rótulo dentro da coluna, no centro vertical
                ax.text(
                    x_positions[j], value / 2, category,
                    rotation=90, ha="center", va="center",
                    fontsize=8, color="black"
                )

    ax.set_xticks([i * 2 + 0.5 for i in range(len(months))])  # Centro entre as barras
    ax.set_xticklabels([month.strftime("%b") for month in months], rotation=45, ha="right")
    ax.set_title("Vendas Mensais — Top 2 Categorias por Mês")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Vendas Totais (€)")
    plt.tight_layout()
    plt.savefig("outputs/plots/top2_categories_per_month_grouped.png", bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    main()