# export_figures.py
# Genere 5 figures Plotly exportees en JSON pour Plotly Studio.
# Pour les utiliser : ouvrir https://plotly.com/studio/ -> New chart
# -> Import -> charger un .json de ce dossier.

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "bank-full.csv"
OUT = Path(__file__).resolve().parent

BG = "#06091F"
INK = "#F5F7FA"
MINT = "#00E5B0"
CORAL = "#FF5C7A"
GOLD = "#FFC64D"


def themed(fig, title):
    fig.update_layout(
        title=title, paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(color=INK, family="Inter"),
        margin=dict(l=40, r=20, t=60, b=40),
    )
    fig.update_xaxes(gridcolor="#333D66")
    fig.update_yaxes(gridcolor="#333D66")
    return fig


def main():
    df = pd.read_csv(DATA, sep=";")
    df["y_bin"] = (df["y"] == "yes").astype(int)

    figures = {}

    # 1. Taux par metier
    g = df.groupby("job")["y_bin"].mean().mul(100).reset_index(name="taux")
    figures["01_taux_par_metier"] = themed(
        px.bar(g.sort_values("taux"), x="taux", y="job", orientation="h",
                color="taux",
                color_continuous_scale=[CORAL, GOLD, MINT],
                labels={"taux": "% souscription", "job": ""}),
        "Taux de souscription par metier")

    # 2. Distribution age
    figures["02_distribution_age"] = themed(
        px.histogram(df, x="age", color="y", nbins=40, barmode="overlay",
                      opacity=0.7,
                      color_discrete_map={"no": CORAL, "yes": MINT}),
        "Distribution de l'age selon la souscription")

    # 3. Box solde
    figures["03_box_solde"] = themed(
        px.box(df, x="y", y="balance", color="y", points=False,
                color_discrete_map={"no": CORAL, "yes": MINT},
                labels={"y": "Souscrit", "balance": "Solde (EUR)"}),
        "Solde bancaire selon la souscription")

    # 4. Heatmap correlations
    corr = df[["age", "balance", "duration", "campaign",
                "previous", "y_bin"]].corr()
    figures["04_correlation_heatmap"] = themed(
        go.Figure(data=go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.columns,
            colorscale="RdBu", zmid=0,
            text=corr.round(2).values, texttemplate="%{text}",
            textfont={"size": 12, "color": INK})),
        "Matrice de correlation des variables numeriques")

    # 5. Scatter duree vs solde
    sample = df.sample(3000, random_state=42)
    figures["05_duration_vs_balance"] = themed(
        px.scatter(sample, x="duration", y="balance", color="y",
                    opacity=0.5,
                    color_discrete_map={"no": CORAL, "yes": MINT},
                    labels={"duration": "Duree (s)",
                            "balance": "Solde (EUR)"}),
        "Solde x duree d'appel (echantillon 3000)")

    for nom, fig in figures.items():
        path = OUT / f"{nom}.json"
        pio.write_json(fig, path)
        print(f"OK - {path.name}")

    print(f"\n{len(figures)} figures exportees dans {OUT}")
    print("Pour les utiliser : https://plotly.com/studio/ -> Import -> JSON")


if __name__ == "__main__":
    main()
