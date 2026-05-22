import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Impact des Crises & Réfugiés", layout="wide")

st.markdown("---")
st.markdown("""
Bienvenue sur ce tableau de bord interactif d'analyse de données.  
Ce document vise à démontrer, preuves statistiques à l'appui, l'impact direct des conflits armés (guerres civiles, invasions) sur les mouvements de populations à travers le monde. Les données officielles sont issues de la **Banque Mondiale**.
""")
# 1. Chargement des données
chemin_dossier = r"C:\Users\Asus\Downloads\Compressed\API_SM.POP.REFG.OR_DS57_en_csv_v2_7413"
df = pd.read_csv(chemin_dossier + r"\APP.csv", skiprows=4)
dc = pd.read_csv(chemin_dossier + r"\Metadata_Country.csv")

# 2. Transformation de 'df' (Melt) : on rassemble toutes les colonnes d'années en une seule colonne 'Annee'
df_melted = df.melt(id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
                    var_name='Annee', 
                    value_name='Nombre_Refugies')

# On s'assure que la colonne année ne contient que des nombres et on la convertit en entier
df_melted = df_melted[df_melted['Annee'].str.isnumeric() == True]
df_melted['Annee'] = df_melted['Annee'].astype(int)

# 3. Fusion avec les métadonnées pays ('dc') pour ajouter la "Region"

df_final = pd.merge(df_melted, dc[['Country Code', 'Region', 'IncomeGroup']], 
                    on='Country Code', 
                    how='inner')

# 4. On retire les lignes sans données et on renomme proprement
df_final = df_final.dropna(subset=['Nombre_Refugies', 'Region'])
df_final = df_final.rename(columns={'Country Name': 'Pays', 'Country Code': 'Code_ISO'})

with st.expander(" un aperçu des données brutes de la Banque Mondiale"):
    st.dataframe(df_final.head(10))




# -0. Préparation : On se concentre sur la période récente (ex: depuis 1990) ---
df_recent = df_final[df_final['Annee'] >= 1990].copy()
annee_max = df_recent['Annee'].max()
df_map = df_recent[df_recent['Annee'] == annee_max].copy()


# 1. ÉVOLUTION GLOBALE PAR RÉGION (Area Chart) ---

df_region = df_recent.groupby(['Annee', 'Region'])['Nombre_Refugies'].sum().reset_index()
fig1 = px.area(
    df_region, x="Annee", y="Nombre_Refugies", color="Region", 
    title="Évolution du volume de réfugiés par région d'origine (1990-2023)"
)
fig1.update_layout(template="plotly_white")
st.plotly_chart(fig1)


# --- 2. CARTE CHOROPLÈTHE ANIMÉE ---
# Indispensable pour un Data Analyst : voir le flux migratoire se déplacer d'année en année.
# Astuce de pro : on borne la couleur max au 98ème centile pour éviter qu'un pays extrême écrase l'échelle de couleurs.
valeur_max = df_recent['Nombre_Refugies'].quantile(0.98)
fig2 = px.choropleth(
    df_recent.sort_values('Annee'), locations="Code_ISO", 
    color="Nombre_Refugies", hover_name="Pays", 
    animation_frame="Annee", color_continuous_scale="YlOrRd",
    title="Carte animée : Évolution mondiale des pays d'origine (1990-2023)",
    range_color=[0, valeur_max]
)
st.plotly_chart(fig2)


# --- 3. TREEMAP : RÉPARTITION HIÉRARCHIQUE ---
# Un visuel "Wahou" : il permet de voir en un coup d'œil la proportion exacte des réfugiés par continent PUIS par pays pour l'année la plus récente.
fig3 = px.treemap(
    df_map[df_map['Nombre_Refugies'] > 0], 
    path=[px.Constant("Monde"), 'Region', 'Pays'], 
    values='Nombre_Refugies', color='Nombre_Refugies', 
    color_continuous_scale='Reds',
    title=f"Répartition des réfugiés par Région et Pays d'origine (Année {annee_max})"
)
st.plotly_chart(fig3)


# --- 4. TOP 15 DES PAYS D'ORIGINE ---
# Statistique froide et efficace : le classement des pires zones d'émigration actuelles.
top_15 = df_map.nlargest(15, 'Nombre_Refugies')
fig4 = px.bar(
    top_15, x='Nombre_Refugies', y='Pays', orientation='h', color='Region',
    title=f"Top 15 des pays d'origine avec le plus de réfugiés (Année {annee_max})", 
    text_auto='.2s'
)
fig4.update_layout(yaxis={'categoryorder':'total ascending'}, template="plotly_white")
st.plotly_chart(fig4)



# --- Préparation des données ---
df_recent = df_final[df_final['Annee'] >= 1990].copy()
annee_actuelle = df_recent['Annee'].max()
annee_passe = annee_actuelle - 10 

df_actuel = df_recent[df_recent['Annee'] == annee_actuelle]
total_refugies_actuel = df_actuel['Nombre_Refugies'].sum()


# 1. LE GROS CHIFFRE (KPI) 

fig_kpi = go.Figure(go.Indicator(
    mode = "number",
    value = total_refugies_actuel,
    title = {"text": f"<span style='font-size:30px'>Nombre total de réfugiés dans le monde ({annee_actuelle})</span><br><span style='font-size:14px;color:gray'>Personnes ayant dû fuir leur pays</span>"},
    number = {'valueformat': ' ', 'font': {'size': 80, 'color': '#d32f2f'}}
))
st.plotly_chart(fig_kpi)



# 2. LA COURBE GLOBALE UNIQUE 

df_total = df_recent.groupby('Annee')['Nombre_Refugies'].sum().reset_index()
fig_courbe = px.line(
    df_total, x='Annee', y='Nombre_Refugies', 
    title="L'évolution globale de la crise des réfugiés (1990 - Aujourd'hui)"
)
# On met la courbe en rouge vif et on colorie le dessous pour que ça saute aux yeux
fig_courbe.update_traces(line_color='#d32f2f', line_width=4, fill='tozeroy', fillcolor='rgba(211, 47, 47, 0.2)')
fig_courbe.update_layout(template="plotly_white", yaxis_title="Nombre total de réfugiés", xaxis_title="Année")
st.plotly_chart(fig_courbe)



# 3. LE GRAPHIQUE EN ANNEAU (Donut Chart) : Les proportions par continent

fig_donut = px.pie(
    df_actuel, values='Nombre_Refugies', names='Region', hole=0.5,
    title=f"D'où viennent les réfugiés aujourd'hui ? (Répartition par continent en {annee_actuelle})"
)
# On force l'affichage du pourcentage et du nom directement sur le graphique
fig_donut.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
st.plotly_chart(fig_donut)


# 4. COMPARAISON AVANT/APRÈS : "Il y a 10 ans vs Aujourd'hui"
# Le cerveau humain adore les comparaisons directes (Barres groupées).

# On prend les 5 pays qui ont le plus de réfugiés aujourd'hui
top5_pays = df_actuel.nlargest(5, 'Nombre_Refugies')['Pays'].tolist()

# On filtre les données pour n'avoir que ces 5 pays, et seulement pour les 2 années (ex: 2013 et 2023)
df_compare = df_recent[(df_recent['Annee'].isin([annee_passe, annee_actuelle])) & (df_recent['Pays'].isin(top5_pays))].copy()
df_compare['Annee'] = df_compare['Annee'].astype(str) # Pour séparer proprement les couleurs

fig_avant_apres = px.bar(
    df_compare, x='Pays', y='Nombre_Refugies', color='Annee', barmode='group',
    title=f"L'explosion des crises : Comparaison {annee_passe} vs {annee_actuelle} (Top 5 actuel)",
    color_discrete_map={str(annee_passe): '#90caf9', str(annee_actuelle): '#1565c0'}, # Bleu clair (avant) / Bleu foncé (après)
    text_auto='.2s'
)
fig_avant_apres.update_layout(template="plotly_white", yaxis_title="Nombre de réfugiés")
st.plotly_chart(fig_avant_apres)





# 6. GRAPHIQUE LINÉAIRE MULTI-SÉRIES : Annotations Événementielles

st.write("---")
st.header("6. Impact direct des conflits armés sur les déplacements")
st.write("La preuve statistique irréfutable : la corrélation évidente entre une invasion ou une guerre et la flambée des réfugiés.")

# On utilise les données World Bank (df_recent)
pays_cibles = ["Syrian Arab Republic", "Ukraine", "Afghanistan", "Congo, Dem. Rep."]
df_lignes = df_recent[df_recent['Pays'].isin(pays_cibles)].copy()

fig_lignes = px.line(
    df_lignes, x='Annee', y='Nombre_Refugies', color='Pays',
    title="Évolution comparée des crises majeures",
    labels={"Annee": "Année", "Nombre_Refugies": "Nombre de Réfugiés"}
)

# Ajout des annotations événementielles pour donner du contexte
# Syrie 2011
val_syrie = df_lignes[(df_lignes['Pays']=="Syrian Arab Republic") & (df_lignes['Annee']==2011)]['Nombre_Refugies'].max() if not df_lignes[(df_lignes['Pays']=="Syrian Arab Republic") & (df_lignes['Annee']==2011)].empty else 0
fig_lignes.add_annotation(x=2011, y=val_syrie, text="Début de la guerre<br>en Syrie (2011)", showarrow=True, arrowhead=2, ax=-40, ay=-40)

# Ukraine 2022
val_ukraine = df_lignes[(df_lignes['Pays']=="Ukraine") & (df_lignes['Annee']==2022)]['Nombre_Refugies'].max() if not df_lignes[(df_lignes['Pays']=="Ukraine") & (df_lignes['Annee']==2022)].empty else 6000000
fig_lignes.add_annotation(x=2022, y=val_ukraine, text="Invasion de<br>l'Ukraine (2022)", showarrow=True, arrowhead=2, ax=-50, ay=30)

fig_lignes.update_layout(template="plotly_white")
st.plotly_chart(fig_lignes)


# 5. DIAGRAMME DE SANKEY : Répartition mondiale (Données du CSV)

st.write("---")
st.header("5. Diagramme de Sankey : Origine des flux")
st.write("Ce graphique utilise exclusivement tes données CSV pour illustrer la répartition hiérarchique des réfugiés (Monde ➔ Région ➔ Pays d'origine).")

# On utilise df_map qui contient les données de l'année la plus récente de ton CSV
df_sankey = df_map[df_map['Nombre_Refugies'] > 0].copy()

# Pour que le graphique reste lisible, on garde le Top 15 des pays, les autres vont dans "Autres pays"
top15_pays = df_sankey.nlargest(15, 'Nombre_Refugies')['Pays'].tolist()
df_sankey['Pays_Filtre'] = df_sankey['Pays'].apply(lambda x: x if x in top15_pays else "Autres pays de la région")

# 1er niveau de flux : Monde -> Region
flux_monde_region = df_sankey.groupby('Region')['Nombre_Refugies'].sum().reset_index()
flux_monde_region['Source'] = 'Monde'
flux_monde_region.rename(columns={'Region': 'Cible', 'Nombre_Refugies': 'Valeur'}, inplace=True)

# 2ème niveau de flux : Region -> Pays
flux_region_pays = df_sankey.groupby(['Region', 'Pays_Filtre'])['Nombre_Refugies'].sum().reset_index()
flux_region_pays.rename(columns={'Region': 'Source', 'Pays_Filtre': 'Cible', 'Nombre_Refugies': 'Valeur'}, inplace=True)

# Assemblage de tous les flux pour le Sankey
sankey_data = pd.concat([flux_monde_region, flux_region_pays], ignore_index=True)

# Création des index (Plotly a besoin de numéros pour relier les noeuds)
all_nodes = list(pd.concat([sankey_data['Source'], sankey_data['Cible']]).unique())
node_indices = {node: i for i, node in enumerate(all_nodes)}

# Couleurs dynamiques (Le Monde en noir, les Régions en bleu foncé, les pays en bleu clair)
node_colors = []
for node in all_nodes:
    if node == 'Monde':
        node_colors.append('#212121')
    elif node in flux_monde_region['Cible'].values:
        node_colors.append('#1976d2')
    else:
        node_colors.append('#64b5f6')

fig_sankey = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15, thickness=20, line=dict(color="black", width=0.5),
        label=all_nodes, color=node_colors
    ),
    link=dict(
        source=[node_indices[src] for src in sankey_data['Source']],
        target=[node_indices[tgt] for tgt in sankey_data['Cible']],
        value=sankey_data['Valeur'],
        color="rgba(100, 181, 246, 0.4)"
    )
)])

fig_sankey.update_layout(
    title_text=f"Diagramme de Sankey : Répartition Mondiale des Pays d'Origine (Année {annee_max})", 
    font_size=12, 
    height=700
)
st.plotly_chart(fig_sankey)
