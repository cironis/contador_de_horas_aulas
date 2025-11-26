import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def df_to_image_bytes(df: pd.DataFrame) -> BytesIO:
    """Converte um DataFrame em PNG e retorna os bytes em um buffer."""
    # Ajusta tamanho da figura mais ou menos proporcional à tabela
    n_rows, n_cols = df.shape
    fig, ax = plt.subplots(
        figsize=(max(4, n_cols * 1.2), max(1.5, n_rows * 0.4 + 1))
    )
    ax.axis("off")

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc="center",
        loc="center",
    )

    # Ajustes de fonte / escala (opcional)
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.5)

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=200, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    buf.seek(0)
    return buf