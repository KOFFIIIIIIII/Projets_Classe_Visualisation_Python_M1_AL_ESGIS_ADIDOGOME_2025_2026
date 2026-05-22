# app_dash.py - dashboard Dash equivalent du Streamlit
# Lancement : python dash_app/app_dash.py
# URL : http://127.0.0.1:8050
#
# Pourquoi Dash en plus de Streamlit ?
# Le prof a demande les deux. Streamlit re-execute tout le script a chaque
# interaction, Dash a des callbacks granulaires plus proches du web classique.

from pathlib import Path

import dash
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html, dash_table
from scipy import stats

CSV = Path(__file__).resolve().parent.parent / "data" / "bank-full.csv"

# Palette - meme que Streamlit et PPT
BG = "#06091F"
GLASS = "#1C224A"
INK = "#F5F7FA"
MUTED = "#8B92B3"
GOLD = "#FFC64D"
MINT = "#00E5B0"
CORAL = "#FF5C7A"
BLUE = "#6E95FF"

df = pd.read_csv(CSV, sep=";")
df["y_bin"] = (df["y"] == "yes").astype(int)

JOBS = sorted(df["job"].unique())
MARITALS = sorted(df["marital"].unique())
EDUCATION = sorted(df["education"].unique())


def theme(fig):
    # On force le fond sombre sur toutes les figures
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(color=INK, family="Inter, system-ui, sans-serif"),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor="#333D66", zerolinecolor="#333D66")
    fig.update_yaxes(gridcolor="#333D66", zerolinecolor="#333D66")
    return fig


app = Dash(__name__, title="Bank Marketing - Dash")

CARD = {
    "background": GLASS,
    "border": "1px solid #333D66",
    "borderRadius": "12px",
    "padding": "16px",
}
KPI = {**CARD, "textAlign": "center"}


app.layout = html.Div(
    style={
        "background": BG,
        "minHeight": "100vh",
        "padding": "24px",
        "fontFamily": "Inter, system-ui, sans-serif",
        "color": INK,
    },
    children=[
        # --- header -----------------------------------------------------
        html.Div([
            html.Div("M1 ESGIS - DASH",
                     style={"color": GOLD, "fontWeight": 700,
                             "letterSpacing": "2px", "fontSize": "12px"}),
            html.H1("Bank Marketing - Dashboard interactif",
                     style={"margin": "8px 0 4px", "fontSize": "32px"}),
            html.Div("Dataset UCI - 45 211 clients - 17 variables",
                     style={"color": MUTED, "fontSize": "14px"}),
        ], style={"marginBottom": "24px"}),

        # --- layout 2 colonnes ------------------------------------------
        html.Div(
            style={"display": "grid",
                   "gridTemplateColumns": "260px 1fr", "gap": "24px"},
            children=[
                # sidebar
                html.Div(style=CARD, children=[
                    html.Div("FILTRES",
                             style={"color": GOLD, "fontWeight": 700,
                                     "letterSpacing": "2px",
                                     "fontSize": "11px",
                                     "marginBottom": "12px"}),
                    html.Label("Metier",
                                style={"fontSize": "12px", "color": MUTED}),
                    dcc.Dropdown(JOBS, multi=True, id="f-job",
                                  placeholder="Tous",
                                  style={"color": "#000",
                                          "marginBottom": "12px"}),
                    html.Label("Statut marital",
                                style={"fontSize": "12px", "color": MUTED}),
                    dcc.Dropdown(MARITALS, multi=True, id="f-marital",
                                  placeholder="Tous",
                                  style={"color": "#000",
                                          "marginBottom": "12px"}),
                    html.Label("Education",
                                style={"fontSize": "12px", "color": MUTED}),
                    dcc.Dropdown(EDUCATION, multi=True, id="f-edu",
                                  placeholder="Toutes",
                                  style={"color": "#000",
                                          "marginBottom": "12px"}),
                    html.Label("Pret immobilier",
                                style={"fontSize": "12px", "color": MUTED}),
                    dcc.RadioItems(
                        options=[{"label": " Tous", "value": "all"},
                                  {"label": " Oui", "value": "yes"},
                                  {"label": " Non", "value": "no"}],
                        value="all", id="f-housing",
                        style={"marginBottom": "12px"},
                        labelStyle={"display": "block", "fontSize": "13px"}),
                    html.Label("Age",
                                style={"fontSize": "12px", "color": MUTED}),
                    dcc.RangeSlider(
                        int(df["age"].min()), int(df["age"].max()),
                        value=[int(df["age"].min()), int(df["age"].max())],
                        marks={i: str(i) for i in range(20, 95, 15)},
                        id="f-age",
                        tooltip={"placement": "bottom"}),
                ]),

                # contenu
                html.Div([
                    html.Div(id="kpis",
                             style={"display": "grid",
                                     "gridTemplateColumns": "repeat(5, 1fr)",
                                     "gap": "16px", "marginBottom": "20px"}),
                    dcc.Tabs(id="tabs", value="t1",
                              colors={"border": "#333D66",
                                       "primary": GOLD,
                                       "background": GLASS},
                              children=[
                                  dcc.Tab(label="Profil (Q1)", value="t1",
                                           style={"background": BG,
                                                   "color": INK,
                                                   "border": "1px solid "
                                                             "#333D66"},
                                           selected_style={
                                               "background": GLASS,
                                               "color": GOLD,
                                               "fontWeight": 700,
                                               "border": "1px solid #333D66",
                                               "borderBottom": "2px solid "
                                                                + GOLD}),
                                  dcc.Tab(label="Solde - t-test (Q2)",
                                           value="t2",
                                           style={"background": BG,
                                                   "color": INK,
                                                   "border": "1px solid "
                                                             "#333D66"},
                                           selected_style={
                                               "background": GLASS,
                                               "color": GOLD,
                                               "fontWeight": 700,
                                               "border": "1px solid #333D66",
                                               "borderBottom": "2px solid "
                                                                + GOLD}),
                                  dcc.Tab(label="Categoriel - Chi2 (Q3)",
                                           value="t3",
                                           style={"background": BG,
                                                   "color": INK,
                                                   "border": "1px solid "
                                                             "#333D66"},
                                           selected_style={
                                               "background": GLASS,
                                               "color": GOLD,
                                               "fontWeight": 700,
                                               "border": "1px solid #333D66",
                                               "borderBottom": "2px solid "
                                                                + GOLD}),
                                  dcc.Tab(label="Appel - Pearson (Q4)",
                                           value="t4",
                                           style={"background": BG,
                                                   "color": INK,
                                                   "border": "1px solid "
                                                             "#333D66"},
                                           selected_style={
                                               "background": GLASS,
                                               "color": GOLD,
                                               "fontWeight": 700,
                                               "border": "1px solid #333D66",
                                               "borderBottom": "2px solid "
                                                                + GOLD}),
                              ]),
                    html.Div(id="tab-content",
                              style={"marginTop": "20px"}),
                ]),
            ],
        ),
    ],
)


def filtrer(jobs, marital, edu, housing, age_range):
    d = df[df["age"].between(age_range[0], age_range[1])]
    if jobs:
        d = d[d["job"].isin(jobs)]
    if marital:
        d = d[d["marital"].isin(marital)]
    if edu:
        d = d[d["education"].isin(edu)]
    if housing != "all":
        d = d[d["housing"] == housing]
    return d


def kpi(label, val, color=MINT):
    return html.Div(style=KPI, children=[
        html.Div(label.upper(),
                  style={"color": MUTED, "fontSize": "10px",
                          "fontWeight": 700, "letterSpacing": "1.5px"}),
        html.Div(val, style={"color": color, "fontSize": "28px",
                                "fontWeight": 700, "marginTop": "6px"}),
    ])


@callback(
    Output("kpis", "children"),
    Input("f-job", "value"),
    Input("f-marital", "value"),
    Input("f-edu", "value"),
    Input("f-housing", "value"),
    Input("f-age", "value"),
)
def update_kpis(jobs, marital, edu, housing, age_range):
    d = filtrer(jobs, marital, edu, housing, age_range)
    if len(d) == 0:
        return [html.Div("Aucun client", style=KPI)]

    taux = (d["y"] == "yes").mean() * 100
    ref = (df["y"] == "yes").mean() * 100
    diff = taux - ref
    diff_color = MINT if diff >= 0 else CORAL

    return [
        kpi("Clients", f"{len(d):,}".replace(",", " "), INK),
        kpi("Age moyen", f"{d['age'].mean():.1f}", BLUE),
        kpi("Solde median", f"{d['balance'].median():.0f} EUR", GOLD),
        kpi("Duree mediane", f"{d['duration'].median():.0f} s", BLUE),
        html.Div(style=KPI, children=[
            html.Div("TAUX SOUSCRIPTION",
                     style={"color": MUTED, "fontSize": "10px",
                             "fontWeight": 700, "letterSpacing": "1.5px"}),
            html.Div(f"{taux:.1f} %",
                     style={"color": MINT, "fontSize": "28px",
                             "fontWeight": 700, "marginTop": "6px"}),
            html.Div(f"{diff:+.1f} pts vs global",
                     style={"color": diff_color, "fontSize": "11px",
                             "marginTop": "4px"}),
        ]),
    ]


@callback(
    Output("tab-content", "children"),
    Input("tabs", "value"),
    Input("f-job", "value"),
    Input("f-marital", "value"),
    Input("f-edu", "value"),
    Input("f-housing", "value"),
    Input("f-age", "value"),
)
def render(tab, jobs, marital, edu, housing, age_range):
    d = filtrer(jobs, marital, edu, housing, age_range)
    if len(d) == 0:
        return html.Div("Aucun client ne correspond aux filtres.",
                         style={**CARD, "color": CORAL})

    if tab == "t1":
        tab1 = (d.groupby("job")["y_bin"]
                  .mean().mul(100).reset_index(name="taux"))
        f1 = px.bar(tab1.sort_values("taux"), x="taux", y="job",
                     orientation="h", color="taux",
                     color_continuous_scale=[CORAL, GOLD, MINT],
                     labels={"taux": "% souscription", "job": ""})
        f1.update_layout(coloraxis_showscale=False, height=420,
                          title="Taux de souscription par metier")
        theme(f1)

        f2 = px.histogram(d, x="age", color="y", nbins=40,
                           barmode="overlay", opacity=0.7,
                           color_discrete_map={"no": CORAL, "yes": MINT},
                           title="Distribution de l'age selon souscription")
        f2.update_layout(height=420)
        theme(f2)

        agg = d.groupby(["job", "marital", "y"]).size().reset_index(name="n")
        f3 = px.treemap(agg, path=["job", "marital", "y"], values="n",
                         color="y",
                         color_discrete_map={"(?)": "lightgray",
                                              "no": CORAL, "yes": MINT},
                         title="Treemap : job -> marital -> souscription")
        f3.update_layout(height=480)
        theme(f3)

        return html.Div([
            html.Div(style={"display": "grid",
                            "gridTemplateColumns": "1fr 1fr", "gap": "16px"},
                      children=[
                          html.Div(dcc.Graph(figure=f1), style=CARD),
                          html.Div(dcc.Graph(figure=f2), style=CARD),
                      ]),
            html.Div(dcc.Graph(figure=f3),
                      style={**CARD, "marginTop": "16px"}),
        ])

    if tab == "t2":
        b_y = d[d["y"] == "yes"]["balance"]
        b_n = d[d["y"] == "no"]["balance"]
        f = px.box(d, x="y", y="balance", color="y", points=False,
                    color_discrete_map={"no": CORAL, "yes": MINT},
                    labels={"y": "Souscrit", "balance": "Solde (EUR)"},
                    title="Solde bancaire selon la souscription")
        f.update_layout(height=460, showlegend=False)
        theme(f)

        if len(b_y) > 1 and len(b_n) > 1:
            t, p = stats.ttest_ind(b_y, b_n, equal_var=False)
            verdict = ("p < 0.05 -> on rejette H0. Difference significative."
                        if p < 0.05
                        else "p >= 0.05 -> on ne peut pas rejeter H0.")
            verdict_color = MINT if p < 0.05 else GOLD
            panel = html.Div(style=CARD, children=[
                html.Div("TEST DE STUDENT",
                          style={"color": MINT, "fontWeight": 700,
                                  "letterSpacing": "2px",
                                  "fontSize": "11px"}),
                html.Div(f"{b_n.mean():.0f} EUR  ->  {b_y.mean():.0f} EUR",
                          style={"fontSize": "28px", "fontWeight": 700,
                                  "margin": "12px 0"}),
                html.Div("Solde moyen Refus -> Souscription",
                          style={"color": MUTED, "fontSize": "12px"}),
                html.Hr(style={"borderColor": "#333D66",
                                "margin": "20px 0"}),
                html.Div(f"t = {t:.3f}",
                          style={"fontSize": "20px", "fontWeight": 700}),
                html.Div(f"p = {p:.2e}",
                          style={"fontSize": "20px", "fontWeight": 700,
                                  "color": GOLD, "marginTop": "8px"}),
                html.Div(verdict,
                          style={"color": verdict_color,
                                  "marginTop": "16px", "fontSize": "13px"}),
            ])
        else:
            panel = html.Div("Echantillon trop petit.", style=CARD)

        return html.Div(
            style={"display": "grid",
                   "gridTemplateColumns": "2fr 1fr", "gap": "16px"},
            children=[html.Div(dcc.Graph(figure=f), style=CARD), panel])

    if tab == "t3":
        rows = []
        for col in ["job", "marital", "education", "housing",
                    "loan", "default", "contact"]:
            tbl = pd.crosstab(d[col], d["y"])
            if tbl.shape[0] < 2 or tbl.shape[1] < 2:
                continue
            chi2, p, dof, _ = stats.chi2_contingency(tbl)
            rows.append({"Variable": col, "Chi2": round(chi2, 2),
                          "ddl": dof, "p-value": f"{p:.2e}",
                          "Significatif": "OUI" if p < 0.05 else "non"})
        res = pd.DataFrame(rows).sort_values("Chi2", ascending=False)

        header_style = {"backgroundColor": GLASS, "color": GOLD,
                         "fontWeight": 700, "fontSize": "11px",
                         "letterSpacing": "1.5px",
                         "border": "none", "padding": "12px"}
        cell_style = {"backgroundColor": BG, "color": INK,
                       "border": "1px solid #333D66",
                       "padding": "10px", "fontSize": "13px"}

        return html.Div([
            html.Div(style=CARD, children=[
                html.H3("Test du Chi-2 sur les variables categorielles",
                         style={"marginTop": 0, "color": INK}),
                dash_table.DataTable(
                    data=res.to_dict("records"),
                    columns=[{"name": c, "id": c} for c in res.columns],
                    style_header=header_style, style_cell=cell_style,
                    style_data_conditional=[
                        {"if": {"filter_query": '{Significatif} = "OUI"',
                                 "column_id": "Significatif"},
                         "color": MINT, "fontWeight": 700},
                    ],
                ),
            ]),
        ])

    if tab == "t4":
        f1 = px.box(d, x="y", y="duration", color="y", points=False,
                     color_discrete_map={"no": CORAL, "yes": MINT},
                     labels={"y": "Souscrit", "duration": "Duree (s)"},
                     title="Duree d'appel selon souscription")
        f1.update_layout(height=420, showlegend=False)
        theme(f1)

        sample = d.sample(min(3000, len(d)), random_state=42)
        f2 = px.scatter(sample, x="duration", y="balance", color="y",
                         opacity=0.5,
                         color_discrete_map={"no": CORAL, "yes": MINT},
                         labels={"duration": "Duree (s)",
                                  "balance": "Solde (EUR)"},
                         title="Solde x duree")
        f2.update_layout(height=420)
        theme(f2)

        corr = d[["age", "balance", "duration", "campaign",
                  "previous", "y_bin"]].corr()
        f3 = go.Figure(data=go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.columns,
            colorscale="RdBu", zmid=0,
            text=corr.round(2).values, texttemplate="%{text}",
            textfont={"size": 12, "color": INK}))
        f3.update_layout(height=420, title="Matrice de correlation")
        theme(f3)

        r_panel = ""
        if len(d) > 2:
            r, p = stats.pearsonr(d["duration"], d["y_bin"])
            r_panel = html.Div(style=CARD, children=[
                html.Div("CORRELATION PEARSON",
                          style={"color": BLUE, "fontWeight": 700,
                                  "letterSpacing": "2px",
                                  "fontSize": "11px"}),
                html.Div(f"r = {r:.3f}",
                          style={"fontSize": "32px", "fontWeight": 700,
                                  "margin": "12px 0"}),
                html.Div(f"p = {p:.2e}",
                          style={"color": GOLD, "fontWeight": 700}),
            ])

        return html.Div([
            html.Div(style={"display": "grid",
                            "gridTemplateColumns": "2fr 1fr", "gap": "16px"},
                      children=[html.Div(dcc.Graph(figure=f1), style=CARD),
                                 r_panel]),
            html.Div(style={"display": "grid",
                            "gridTemplateColumns": "1fr 1fr",
                            "gap": "16px", "marginTop": "16px"},
                      children=[html.Div(dcc.Graph(figure=f2), style=CARD),
                                 html.Div(dcc.Graph(figure=f3),
                                           style=CARD)]),
        ])


if __name__ == "__main__":
    app.run(debug=True)
