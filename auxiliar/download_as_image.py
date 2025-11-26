import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def df_to_image_bytes(df: pd.DataFrame, title: str = None) -> BytesIO:
    """Converte um DataFrame em PNG e retorna os bytes em um buffer,
    com formatação mais bonita (header colorido, listras, fonte maior).
    """
    n_rows, n_cols = df.shape

    # Tamanho da figura (fixo mais "quadradinho", bom para poucas colunas)
    fig_width = max(5, n_cols * 2.5)
    fig_height = max(2.5, 0.5 * n_rows + 2)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis("off")

    # Título (se existir)
    if title:
        ax.set_title(title, pad=18, fontsize=14, fontweight="bold")

    # Cria a tabela
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="center",
        loc="center",
    )

    # Estilo base
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.3, 1.6)  # aumenta um pouco largura/altura das células

    # Cores
    header_color = "#2F5597"
    header_text_color = "white"
    row_colors = ["#f2f2f2", "#ffffff"]  # listrado

    # Aplica estilos célula a célula
    for (row, col), cell in table.get_celld().items():
        # Header
        if row == 0:
            cell.set_facecolor(header_color)
            cell.set_text_props(color=header_text_color, weight="bold")
        else:
            # Linhas alternadas
            cell.set_facecolor(row_colors[(row - 1) % 2])

        # Borda mais suave
        cell.set_edgecolor("#d0d0d0")

    # Ajuste de layout
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(
        buf,
        format="png",
        dpi=200,
        bbox_inches="tight",
        pad_inches=0.1,
        facecolor="white",
    )
    plt.close(fig)
    buf.seek(0)
    return buf