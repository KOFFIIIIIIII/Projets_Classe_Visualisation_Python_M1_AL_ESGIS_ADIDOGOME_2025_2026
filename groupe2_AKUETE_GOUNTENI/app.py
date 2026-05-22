import streamlit as st
import wbdata
import plotly.express as px
from datetime import datetime
import logging
import plotly.graph_objects as go
import pandas as pd

logging.getLogger("wbdata").setLevel(logging.ERROR)
# Configuration de la page Streamlit
st.set_page_config(page_title="Dashboard Santé BM - ESGIS", layout="wide")

# 1. Titre de l'application
st.title("📊 Dashboard Dynamique : Analyse Comparée de la Santé en Afrique")
st.write("Projet d'Analyse et Visualisation de Données — Données issues de la Banque Mondiale")

# 2. Utilisation de @st.cache_resource pour éviter l'erreur de sérialisation dbm.sqlite3
@st.cache_resource
def charger_donnees():
    countries = ["BEN", "BFA", "CMR", "CIV", "GHA", "KEN", "NGA", "SEN", "TGO"]
    indicators = {
        "SH.DYN.AIDS.ZS": "VIH_Prevalence",
        "SH.TBS.INCD": "Tuberculose_Incidence",
        "SH.MLR.INCD.P3": "Malaria_Incidence",
        "SH.DTH.NCOM.ZS": "Mortalite_Maladies_Chroniques",
        "SH.IMM.HEPB": "Vaccination_Hepatite_B",
        "SP.DYN.LE00.IN": "Esperance_Vie",
        "SH.XPD.CHEX.GD.ZS": "Depenses_Sante",
        "SP.POP.TOTL": "Population"
    }
    
    # Récupération dynamique de l'année en cours
    annee_actuelle = datetime.now().year
    
    # Appel API Banque Mondiale
    df_brut = wbdata.get_dataframe(indicators, date=(datetime(2000, 1, 1), datetime(2024, 1, 1)))
    df_clean = df_brut.reset_index()
    df_clean['date'] = df_clean['date'].astype(int)
    df_clean.rename(columns={'country': 'Pays', 'date': 'Annee'}, inplace=True)
    return df_clean

# Chargement du dataframe
df = charger_donnees()

# 3. Barre latérale (Sidebar) pour le choix dynamique du pays
liste_pays = sorted(df['Pays'].unique())
pays_choisi = st.sidebar.selectbox("🌍 Choisir un Pays :", liste_pays)

# Filtrage du dataframe selon le choix de l'utilisateur
df_pays = df[df['Pays'] == pays_choisi].sort_values(by="Annee")

st.subheader(f"📈 Analyse épidémiologique pour le pays : {pays_choisi}")
st.markdown("---")

# 4. Organisation de l'affichage en colonnes
col1, col2 = st.columns(2)

with col1:
    # VISUALISATION 1 : Espérance de vie
    fig1 = px.line(
        df_pays, x="Annee", y="Esperance_Vie", 
        title="Évolution de l'espérance de vie", 
        markers=True, template="plotly_white"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # VISUALISATION 2 : Focus isolé - Prévalence du VIH (Graphique en escalier)
    fig_vih = px.line(
        df_pays, x="Annee", y="VIH_Prevalence",
        title="Détail : Prévalence du VIH (% population 15-49 ans)",
        line_shape="hv", markers=True,
        color_discrete_sequence=["#E74C3C"], template="plotly_white"
    )
    st.plotly_chart(fig_vih, use_container_width=True)

    # VISUALISATION 3 : Couverture vaccinale Hépatite B (Graphique à points reliés)
    fig3 = px.scatter(
        df_pays, x="Annee", y="Vaccination_Hepatite_B",
        title="Couverture vaccinale Hépatite B (% enfants 12-23 mois)",
        labels={"Vaccination_Hepatite_B": "Taux (%)"},
        color_discrete_sequence=["#2ECC71"], template="plotly_white"
    )
    fig3.update_traces(mode='lines+markers')
    fig3.update_yaxes(range=[0, 100])
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # VISUALISATION 4 : Vue d'ensemble comparative (Courbes superposées)
    fig2 = px.line(
        df_pays, x="Annee", 
        y=["VIH_Prevalence", "Tuberculose_Incidence", "Malaria_Incidence"],
        title="Comparaison des tendances épidémiologiques (Échelle globale)",
        labels={"value": "Indice", "variable": "Pathologie"},
        markers=True
    )
    st.plotly_chart(fig2, use_container_width=True)

    # VISUALISATION 5 : Mortalité due aux maladies chroniques (Diagramme en bâtons)
    fig4 = px.bar(
        df_pays, x="Annee", y="Mortalite_Maladies_Chroniques",
        title="Mortalité liée aux maladies non transmissibles (% décès)",
        labels={"Mortalite_Maladies_Chroniques": "Part des décès (%)"},
        color_discrete_sequence=["#8E44AD"]
    )
    fig4.update_layout(xaxis_type='category')
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("📊 Focus Pathologies & Axes Indépendants")

# VISUALISATION 6 : Graphique à facettes (Prend toute la largeur de la page)
df_maladies = df_pays.melt(
    id_vars=["Annee"], 
    value_vars=["VIH_Prevalence", "Tuberculose_Incidence", "Malaria_Incidence"],
    var_name="Maladie", 
    value_name="Valeur"
)
fig_facettes = px.line(
    df_maladies, x="Annee", y="Valeur", 
    facet_col="Maladie", color="Maladie",
    title="Analyses individuelles des pathologies (Axes Y autonomes)",
    markers=True, template="plotly_white",
    height=450
)
fig_facettes.update_yaxes(matches=None, autorange=True)
st.plotly_chart(fig_facettes, use_container_width=True)

st.markdown("---")
st.subheader("🧬 Corrélations et Facteurs Économiques")

col3, col4 = st.columns([3, 2])

with col3:
    # VISUALISATION 7 : Matrice de corrélation complète (Heatmap)
    colonnes_corr = [
        "VIH_Prevalence", "Tuberculose_Incidence", "Malaria_Incidence", 
        "Mortalite_Maladies_Chroniques", "Vaccination_Hepatite_B", 
        "Esperance_Vie", "Depenses_Sante", "Population"
    ]
    colonnes_presentes = [c for c in colonnes_corr if c in df_pays.columns]
    matrice_corr = df_pays[colonnes_presentes].corr()
    
    fig6 = px.imshow(
        matrice_corr, text_auto=".2f", 
        color_continuous_scale='RdBu_r',
        title="Matrice de corrélation des indicateurs"
    )
    st.plotly_chart(fig6, use_container_width=True)

with col4:
    # VISUALISATION 8 : Dépenses de santé vs Espérance de vie (Nuage de points)
    fig5 = px.scatter(
        df_pays, x="Depenses_Sante", y="Esperance_Vie",
        size="Population", hover_data=["Annee"],
        title="Analyse Investissements Santé vs Longévité",
        labels={"Depenses_Sante": "Dépenses (% PIB)", "Esperance_Vie": "Espérance de vie (ans)"}
    )
    st.plotly_chart(fig5, use_container_width=True)
    
st.markdown("---")
st.subheader("🗺️ Carte Choroplèthe — Comparaison Géographique")

# Sélecteur d'indicateur et d'année
col_carte1, col_carte2 = st.columns(2)

with col_carte1:
    indicateur_carte = st.selectbox("📌 Indicateur à cartographier :", {
        "Esperance_Vie": "Espérance de vie",
        "VIH_Prevalence": "Prévalence VIH",
        "Tuberculose_Incidence": "Incidence Tuberculose",
        "Malaria_Incidence": "Incidence Malaria",
        "Depenses_Sante": "Dépenses de Santé (% PIB)",
        "Vaccination_Hepatite_B": "Vaccination Hépatite B"
    }.keys(), format_func=lambda x: {
        "Esperance_Vie": "Espérance de vie",
        "VIH_Prevalence": "Prévalence VIH",
        "Tuberculose_Incidence": "Incidence Tuberculose",
        "Malaria_Incidence": "Incidence Malaria",
        "Depenses_Sante": "Dépenses de Santé (% PIB)",
        "Vaccination_Hepatite_B": "Vaccination Hépatite B"
    }[x])

with col_carte2:
    annees_dispo = sorted(df['Annee'].unique())
    annee_carte = st.select_slider("📅 Année :", options=annees_dispo, value=2019)

# Codes ISO-3 pour px.choropleth (doit correspondre aux noms du df)
iso_map = {
    "Benin": "BEN", "Burkina Faso": "BFA", "Cameroon": "CMR",
    "Cote d'Ivoire": "CIV", "Ghana": "GHA", "Kenya": "KEN",
    "Nigeria": "NGA", "Senegal": "SEN", "Togo": "TGO"
}

df_carte = df[df['Annee'] == annee_carte].copy()
df_carte['ISO'] = df_carte['Pays'].map(iso_map)
df_carte = df_carte.dropna(subset=['ISO', indicateur_carte])

fig_carte = px.choropleth(
    df_carte,
    locations="ISO",
    color=indicateur_carte,
    hover_name="Pays",
    color_continuous_scale="YlOrRd",
    scope="africa",
    title=f"Carte : {indicateur_carte.replace('_', ' ')} en {annee_carte}",
    labels={indicateur_carte: indicateur_carte.replace('_', ' ')}
)
fig_carte.update_layout(
    geo=dict(showframe=False, showcoastlines=True, bgcolor='rgba(0,0,0,0)'),
    height=550
)
st.plotly_chart(fig_carte, use_container_width=True)

st.markdown("---")
st.subheader("🕸️ Radar Chart — Profil Sanitaire Multi-pays")



col_radar1, col_radar2 = st.columns(2)
with col_radar1:
    pays_radar = st.multiselect(
        "🌍 Choisir 2 à 5 pays à comparer :",
        options=sorted(df['Pays'].unique()),
        default=sorted(df['Pays'].unique())[:3]
    )
with col_radar2:
    annee_radar = st.select_slider(
        "📅 Année (Radar) :", 
        options=sorted(df['Annee'].unique()), 
        value=2019,
        key="slider_radar"
    )

# Axes du radar — on normalise chaque indicateur entre 0 et 1
axes_radar = {
    "Esperance_Vie": "Espérance Vie",
    "Vaccination_Hepatite_B": "Vaccination HepB",
    "Depenses_Sante": "Dépenses Santé",
}
# Pour VIH et Tuberculose : valeur inversée (plus c'est bas, mieux c'est)
axes_inverses = {
    "VIH_Prevalence": "VIH (inv.)",
    "Tuberculose_Incidence": "Tuberculose (inv.)",
    "Malaria_Incidence": "Malaria (inv.)",
}

df_radar_annee = df[df['Annee'] == annee_radar].copy()

# Normalisation min-max
for col in list(axes_radar.keys()) + list(axes_inverses.keys()):
    if col in df_radar_annee.columns:
        col_min = df_radar_annee[col].min()
        col_max = df_radar_annee[col].max()
        if col_max != col_min:
            if col in axes_inverses:
                # Inversion : haute prévalence = mauvais score → on inverse
                df_radar_annee[col + "_norm"] = 1 - (df_radar_annee[col] - col_min) / (col_max - col_min)
            else:
                df_radar_annee[col + "_norm"] = (df_radar_annee[col] - col_min) / (col_max - col_min)
        else:
            df_radar_annee[col + "_norm"] = 0.5

categories = list(axes_radar.values()) + list(axes_inverses.values())
cols_norm = [c + "_norm" for c in list(axes_radar.keys()) + list(axes_inverses.keys())]

fig_radar = go.Figure()
couleurs = ["#3498DB", "#E74C3C", "#2ECC71", "#F39C12", "#9B59B6"]

for i, pays in enumerate(pays_radar):
    row = df_radar_annee[df_radar_annee['Pays'] == pays]
    if row.empty:
        continue
    valeurs = [row[c].values[0] if c in row.columns else 0 for c in cols_norm]
    valeurs += valeurs[:1]  # fermer le polygone

    fig_radar.add_trace(go.Scatterpolar(
        r=valeurs,
        theta=categories + [categories[0]],
        fill='toself',
        name=pays,
        line_color=couleurs[i % len(couleurs)],
        fillcolor=couleurs[i % len(couleurs)].replace(")", ", 0.15)").replace("rgb", "rgba") if "rgb" in couleurs[i % len(couleurs)] else couleurs[i % len(couleurs)],
        opacity=0.85
    ))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    showlegend=True,
    title=f"Profil sanitaire comparé — {annee_radar}",
    height=500
)
st.plotly_chart(fig_radar, use_container_width=True)
st.caption("ℹ️ Les indicateurs VIH, Tuberculose et Malaria sont **inversés** : un score élevé = bonne performance (faible prévalence).")

st.markdown("---")
st.subheader("⚖️ Comparateur Direct — 2 Pays Face à Face")

col_comp1, col_comp2 = st.columns(2)
with col_comp1:
    pays_A = st.selectbox("🔵 Pays A :", sorted(df['Pays'].unique()), index=0, key="paysA")
with col_comp2:
    pays_B = st.selectbox("🔴 Pays B :", sorted(df['Pays'].unique()), index=1, key="paysB")

indicateurs_comp = {
    "Esperance_Vie": "Espérance de vie (ans)",
    "VIH_Prevalence": "Prévalence VIH (%)",
    "Tuberculose_Incidence": "Incidence Tuberculose",
    "Malaria_Incidence": "Incidence Malaria",
    "Depenses_Sante": "Dépenses Santé (% PIB)",
    "Vaccination_Hepatite_B": "Vaccination Hépatite B (%)"
}

df_A = df[df['Pays'] == pays_A].sort_values("Annee")
df_B = df[df['Pays'] == pays_B].sort_values("Annee")

# Affichage en grille 2x3
indicateurs_list = list(indicateurs_comp.items())
for i in range(0, len(indicateurs_list), 2):
    cols = st.columns(2)
    for j, (ind_key, ind_label) in enumerate(indicateurs_list[i:i+2]):
        with cols[j]:
            fig_cmp = px.line(
                title=ind_label,
                template="plotly_white"
            )
            # Pays A
            if ind_key in df_A.columns:
                fig_cmp.add_scatter(
                    x=df_A["Annee"], y=df_A[ind_key],
                    mode='lines+markers', name=pays_A,
                    line=dict(color="#3498DB", width=2.5),
                    marker=dict(size=5)
                )
            # Pays B
            if ind_key in df_B.columns:
                fig_cmp.add_scatter(
                    x=df_B["Annee"], y=df_B[ind_key],
                    mode='lines+markers', name=pays_B,
                    line=dict(color="#E74C3C", width=2.5, dash='dash'),
                    marker=dict(size=5)
                )
            fig_cmp.update_layout(height=280, margin=dict(t=40, b=20))
            st.plotly_chart(fig_cmp, use_container_width=True)

# KPIs comparatifs (dernière année disponible commune)
st.markdown("#### 📊 KPIs — Dernières valeurs disponibles")
derniere_annee = min(df_A['Annee'].max(), df_B['Annee'].max())
row_A = df_A[df_A['Annee'] == derniere_annee].iloc[0] if not df_A[df_A['Annee'] == derniere_annee].empty else None
row_B = df_B[df_B['Annee'] == derniere_annee].iloc[0] if not df_B[df_B['Annee'] == derniere_annee].empty else None

kpi_cols = st.columns(len(indicateurs_comp))
for idx, (ind_key, ind_label) in enumerate(indicateurs_comp.items()):
    with kpi_cols[idx]:
        val_A = round(row_A[ind_key], 2) if row_A is not None and ind_key in row_A and not pd.isna(row_A[ind_key]) else None
        val_B = round(row_B[ind_key], 2) if row_B is not None and ind_key in row_B and not pd.isna(row_B[ind_key]) else None
        delta = round(val_A - val_B, 2) if val_A and val_B else None
        st.metric(
            label=f"{ind_label[:20]}…" if len(ind_label) > 20 else ind_label,
            value=f"{val_A}" if val_A else "N/A",
            delta=f"{delta:+.2f} vs {pays_B}" if delta else None
        )