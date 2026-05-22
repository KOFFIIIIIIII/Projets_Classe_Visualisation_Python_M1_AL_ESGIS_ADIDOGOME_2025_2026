import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ── Titre de l'application ──────────────────────────────
st.title("Analyse du Trafic Routier 🚦")
st.markdown("Analyse en fonction des paramètres météorologiques et horaires")

# ── Chargement des données ──────────────────────────────
@st.cache_data  # met les données en cache pour ne pas recharger à chaque fois
def load_data():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00492/Metro_Interstate_Traffic_Volume.csv.gz"
    df = pd.read_csv(url)
    df['date_time']    = pd.to_datetime(df['date_time'])
    df['hour']         = df['date_time'].dt.hour
    df['day_of_week']  = df['date_time'].dt.day_name()
    df['month']        = df['date_time'].dt.month
    df['is_weekend']   = df['date_time'].dt.dayofweek >= 5
    df.drop_duplicates(subset='date_time', inplace=True)
    return df

df = load_data()

# ── Aperçu des données ──────────────────────────────────
st.subheader("📋 Aperçu des données")
st.dataframe(df.head())
st.write(f"Dimensions : {df.shape[0]} lignes × {df.shape[1]} colonnes")

# ── Statistiques descriptives ───────────────────────────
st.subheader("📊 Statistiques descriptives")
st.dataframe(df[['traffic_volume','temp','rain_1h','snow_1h','clouds_all']].describe())

# ── Graphique 1 : Trafic par heure ─────────────────────
st.subheader("📈 Trafic moyen par heure de la journée")
hourly = df.groupby('hour')['traffic_volume'].mean()
fig1, ax1 = plt.subplots(figsize=(12, 5))
sns.lineplot(x=hourly.index, y=hourly.values, marker='o', color='steelblue', ax=ax1)
ax1.set_xlabel("Heure")
ax1.set_ylabel("Volume de trafic moyen")
st.pyplot(fig1)  # ← remplace plt.show() par st.pyplot()

# ── Graphique 2 : Heatmap jour × heure ─────────────────
st.subheader("🗓️ Heatmap Heure × Jour de la semaine")
pivot = df.pivot_table(values='traffic_volume', index='day_of_week', columns='hour', aggfunc='mean')
days_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
pivot = pivot.reindex(days_order)
pivot.index = ['Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi','Dimanche']
pivot.index.name = 'Jour'
pivot.columns.name = 'Heure'
fig2, ax2 = plt.subplots(figsize=(16, 6))
sns.heatmap(pivot, cmap='YlOrRd', linewidths=0.3, ax=ax2)
st.pyplot(fig2)

# ── Graphique 3 : Conditions météo ─────────────────────
st.subheader("⛅ Trafic moyen selon les conditions météo")
meteo_traduction = {
    'Clear':'Ciel dégagé','Clouds':'Nuageux','Rain':'Pluie',
    'Drizzle':'Bruine','Thunderstorm':'Orage','Snow':'Neige',
    'Mist':'Brume','Fog':'Brouillard','Haze':'Brume sèche'
}
weather_traffic = df.groupby('weather_main')['traffic_volume'].mean().sort_values()
weather_traffic.index = weather_traffic.index.map(lambda x: meteo_traduction.get(x, x))
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.barplot(x=weather_traffic.values, y=weather_traffic.index, palette='coolwarm', ax=ax3)
ax3.set_xlabel("Volume moyen de trafic")
ax3.set_ylabel("Condition météo")
st.pyplot(fig3)

# ── Graphique 4 : Matrice de corrélation ───────────────
st.subheader("🎯 Matrice de corrélation")
colonnes_traduction = {
    'traffic_volume':'Volume de trafic','temp':'Température',
    'rain_1h':'Pluie (1h)','snow_1h':'Neige (1h)',
    'clouds_all':'Couverture nuageuse','hour':'Heure','month':'Mois'
}
corr_cols = ['traffic_volume','temp','rain_1h','snow_1h','clouds_all','hour','month']
corr_matrix = df[corr_cols].corr().rename(index=colonnes_traduction, columns=colonnes_traduction)
fig4, ax4 = plt.subplots(figsize=(9, 7))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', square=True, ax=ax4)
st.pyplot(fig4)

# ── Graphique 5 : Plotly interactif ────────────────────
st.subheader("📊 Évolution interactive du trafic par heure et par jour")
hourly_day = df.groupby(['hour','day_of_week'])['traffic_volume'].mean().reset_index()
fig5 = px.line(hourly_day, x='hour', y='traffic_volume', color='day_of_week',
               labels={'traffic_volume':'Trafic moyen','hour':'Heure','day_of_week':'Jour'},
               template='plotly_dark')
st.plotly_chart(fig5)  # ← remplace fig.show() par st.plotly_chart()