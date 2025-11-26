import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def df_to_image_bytes(df: pd.DataFrame, title: Optional[str] = None) -> BytesIO:
    """Converte um DataFrame em PNG e retorna os bytes em um buffer.
    
    Parâmetros
    ----------
    df : pd.DataFrame
        DataFrame a ser convertido em imagem.
    title : str, opcional
        Título a ser exibido acima da tabela.
    """
    n_rows, n_cols = df.shape
    
    # Se tiver título, aumenta um pouco a altura da figura
    extra_height = 0.6 if title else 0
    fig, ax = plt.subplots(
        figsize=(max(4, n_cols * 1.2), max(1.5, n_rows * 0.4 + 1 + extra_height))
    )
    ax.axis("off")

    # Define o título (se foi passado)
    if title:
        ax.set_title(title, pad=12, fontsize=12, fontweight="bold")

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.5)

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=200, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    buf.seek(0)
    return buf