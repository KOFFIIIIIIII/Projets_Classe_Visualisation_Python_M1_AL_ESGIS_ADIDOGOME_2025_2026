# 🌍 Analyse des maladies et indicateurs de santé en Afrique

Ce projet analyse la situation sanitaire des pays africains à partir de données officielles de la **Banque Mondiale** via la bibliothèque API `wbdata` et déploie une application interactive via **Streamlit**.  
L'objectif est de comprendre comment les maladies infectieuses, les maladies chroniques, la prévention vaccinale et les conditions économiques influencent la santé des populations (espérance de vie, structures de mortalité, etc.).

---

# 🎯 Objectif du projet

Ce projet cherche à répondre à des questions clés :
- Quels pays d'Afrique de l'Ouest et de l'Est sont les plus touchés par les grandes endémies ?
- Observe-t-on une transition épidémiologique vers les maladies chroniques ?
- L'augmentation des dépenses publiques de santé et de la vaccination améliore-t-elle directement l'espérance de vie ?
- Comment les profils sanitaires diffèrent-ils dynamiquement d'un pays à l'autre ?

---

# 📊 Données utilisées

Les données proviennent de la base mondiale de la **World Bank (DataBank)**, qui centralise des statistiques validées par l'OMS, les ministères de la santé nationaux et diverses organisations internationales.

---

# 🦠 Explication des indicateurs

Voici les variables exploitées dans le projet après phase de nettoyage :

---

## 🧬 VIH — SH.DYN.AIDS.ZS
👉 **Prévalence du VIH (% de la population adulte âgée de 15 à 49 ans)**
- Indique la proportion de personnes vivant avec le VIH.
- Mesure l'impact à long terme d'une maladie transmissible chronique.

---

## 🫁 Tuberculose — SH.TBS.INCD
👉 **Incidence de la tuberculose (pour 100 000 habitants)**
- Nombre de nouveaux cas détectés chaque année.
- Révèle la vitesse de propagation de la maladie et l'efficacité des systèmes de détection.

---

## 🦟 Paludisme — SH.MLR.INCD
👉 **Incidence du paludisme (pour 1 000 personnes à risque)**
- Très important pour les pays tropicaux africains.
- Dépend fortement des facteurs environnementaux, du climat et des infrastructures d'assainissement.

---

## 💉 Hépatite B — SH.IMM.HEPB
👉 **Couverture vaccinale contre l'Hépatite B (% des enfants de 12 à 23 mois)**
- Mesure le taux d'enfants ayant reçu la troisième dose du vaccin (HepB3).
- Représente un indicateur clé de l'effort de prévention des maladies transmissibles par les gouvernements.

---

## 🩺 Maladies Chroniques — SH.DTH.NCOM.ZS
👉 **Mortalité due aux maladies non transmissibles (% du total des décès)**
- Regroupe les décès liés au cancer, aux maladies cardiovasculaires, au diabète et aux maladies respiratoires chroniques.
- Permet d'analyser l'émergence des maladies de structures face aux maladies infectieuses.

---

## 👶 Espérance de vie — SP.DYN.LE00.IN
👉 **Espérance de vie à la naissance (en années)**
- Indicateur global synthétisant la qualité de vie, l'accès aux soins, la nutrition et la sécurité sanitaire globale d'un pays.

---

## 💰 Dépenses de santé — SH.XPD.CHEX.GD.ZS
👉 **Dépenses de santé courantes (% du PIB)**
- Reflète le niveau de priorité financière accordé par un pays à son système de santé par rapport à sa richesse nationale.

---

## 👥 Population — SP.POP.TOTL
👉 **Population totale**
- Utilisée pour contextualiser la taille démographique des pays étudiés et pondérer l'importance des analyses graphiques (ex: graphiques à bulles).

💡 *Note sur le nettoyage : L'indicateur initial `SH.DTH.COMM.ZS` (Mortalité maladies transmissibles) présentait un taux de valeurs manquantes trop élevé (79 %) et a été volontairement supprimé pour maintenir la rigueur scientifique de l'étude.*

---

# 🌍 Zone d'étude

Le projet se concentre sur un échantillon ciblé de 9 pays d'Afrique subsaharienne :

- Togo 🇹🇬
- Bénin 🇧🇯
- Burkina Faso 🇧🇫
- Cameroun 🇨🇲
- Côte d'Ivoire 🇨🇮
- Ghana 🇬🇭
- Kenya 🇰🇪
- Nigeria 🇳🇬
- Sénégal 🇸🇳

---

# 📈 Visualisations du Dashboard

Le dashboard est organisé en **4 grandes sections** couvrant 11 visualisations interactives.

---

## Section 1 — Analyse épidémiologique par pays

> Un pays est sélectionné dynamiquement via la barre latérale. Toutes les visualisations de cette section se mettent à jour automatiquement.

---

### 📉 Visualisation 1 : Évolution de l'espérance de vie *(Courbe temporelle)*

**Type :** Graphique en lignes avec marqueurs  
**Données :** `Esperance_Vie` sur la période 2000–2024

**Pourquoi cette représentation ?**  
La courbe temporelle est idéale pour observer une tendance continue sur le long terme. Elle permet de détecter des ruptures nettes (guerres, épidémies, crises économiques) ou une progression régulière due à des politiques de santé efficaces. L'espérance de vie étant un indicateur synthétique, cette courbe résume à elle seule l'état général du système de santé d'un pays.

---

### 📉 Visualisation 2 : Prévalence du VIH *(Graphique en escalier)*

**Type :** Courbe en escalier (`line_shape="hv"`)  
**Données :** `VIH_Prevalence`

**Pourquoi cette représentation ?**  
Contrairement à une courbe lissée, le graphique en escalier représente fidèlement la nature discrète des données épidémiologiques annuelles : la prévalence ne change pas de manière continue mais par paliers lors des enquêtes périodiques. Cette forme met en évidence les années de stabilisation ou de recul grâce aux antirétroviraux.

---

### 📉 Visualisation 3 : Couverture vaccinale Hépatite B *(Points reliés)*

**Type :** Nuage de points connectés  
**Données :** `Vaccination_Hepatite_B` — axe Y fixé entre 0 et 100 %

**Pourquoi cette représentation ?**  
L'axe Y volontairement borné à [0–100 %] ancre la lecture dans son contexte réel : un taux de couverture vaccinale. Chaque point représente une mesure annuelle distincte. La connexion entre les points permet de visualiser la progression (ou les reculs) des campagnes nationales de vaccination dans le temps.

---

### 📉 Visualisation 4 : Comparaison des tendances épidémiologiques *(Courbes superposées)*

**Type :** Graphique multi-séries  
**Données :** `VIH_Prevalence`, `Tuberculose_Incidence`, `Malaria_Incidence`

**Pourquoi cette représentation ?**  
Superposer les trois grandes pathologies infectieuses sur un même graphique permet d'observer leur évolution relative et d'identifier d'éventuelles corrélations ou décalages temporels. C'est la visualisation la plus synthétique pour saisir d'un coup d'œil le profil infectieux d'un pays sur 20 ans.

---

### 📊 Visualisation 5 : Mortalité due aux maladies non transmissibles *(Diagramme en bâtons)*

**Type :** Graphique à barres  
**Données :** `Mortalite_Maladies_Chroniques`

**Pourquoi cette représentation ?**  
Les barres verticales par année permettent de comparer des valeurs ponctuelles indépendantes. L'absence de connexion entre les barres est intentionnelle : chaque année est une mesure autonome. Cette représentation est particulièrement adaptée pour observer si la part des décès chroniques augmente progressivement — signe d'une transition épidémiologique.

---

## Section 2 — Focus Pathologies & Axes Indépendants

---

### 📊 Visualisation 6 : Analyses individuelles par pathologie *(Graphique à facettes)*

**Type :** Facettes (`facet_col`) avec axes Y indépendants  
**Données :** `VIH_Prevalence`, `Tuberculose_Incidence`, `Malaria_Incidence`

**Pourquoi cette représentation ?**  
Les trois pathologies ont des unités et des ordres de grandeur très différents (% vs pour 100 000 vs pour 1 000). Les superposer sur un même axe Y écraserait les petites valeurs. Le graphique à facettes offre à chaque maladie son propre axe Y autonome (`matches=None`), ce qui révèle des tendances internes invisibles dans la visualisation globale. C'est une représentation rigoureuse sur le plan statistique.

---

## Section 3 — Corrélations et Facteurs Économiques

---

### 🔥 Visualisation 7 : Matrice de corrélation *(Heatmap)*

**Type :** Carte de chaleur (`px.imshow`)  
**Données :** Tous les indicateurs numériques

**Pourquoi cette représentation ?**  
La heatmap est le standard pour explorer les relations entre plusieurs variables quantitatives simultanément. Chaque cellule contient le coefficient de corrélation de Pearson (entre -1 et +1). La palette `RdBu_r` (rouge = corrélation négative forte, bleu = positive forte) permet une lecture immédiate. C'est un outil exploratoire puissant pour formuler des hypothèses (ex : *les dépenses de santé sont-elles corrélées à l'espérance de vie ?*).

---

### 🔵 Visualisation 8 : Dépenses de santé vs Espérance de vie *(Nuage de points à bulles)*

**Type :** Scatter plot avec taille variable (`size="Population"`)  
**Données :** `Depenses_Sante` (x), `Esperance_Vie` (y), `Population` (taille)

**Pourquoi cette représentation ?**  
Ce graphique à trois dimensions visuelles (position x, position y, taille de la bulle) permet d'analyser simultanément la relation entre investissement en santé, longévité et poids démographique. Chaque point représente une année. Une tendance ascendante de gauche à droite confirmerait qu'investir davantage en santé est associé à une meilleure espérance de vie.

---

## Section 4 — Analyses Comparatives Multi-pays

---

### 🗺️ Visualisation 9 : Carte Choroplèthe *(Carte géographique interactive)*

**Type :** Carte choroplèthe (`px.choropleth`) — périmètre Afrique  
**Paramètres :** Indicateur sélectionnable + année ajustable via slider

**Pourquoi cette représentation ?**  
La carte choroplèthe est la seule visualisation qui ancre les données dans leur dimension **géographique et spatiale**. Elle permet d'observer d'un seul regard les disparités régionales entre les 9 pays étudiés pour un indicateur et une année donnés. L'intensité de couleur encode la valeur : plus la teinte est foncée (palette `YlOrRd`), plus la valeur est élevée. C'est particulièrement révélateur pour le paludisme (dont la prévalence suit des logiques climatiques et géographiques) ou pour les dépenses de santé (qui suivent des logiques économiques).

**Interaction :** L'utilisateur peut changer l'indicateur et faire glisser le slider temporel pour observer l'évolution géographique année par année.

---

### 🕸️ Visualisation 10 : Radar Chart — Profil sanitaire comparé *(Graphique en toile d'araignée)*

**Type :** Scatterpolar (`go.Scatterpolar`) — axes normalisés [0–1]  
**Paramètres :** Sélection de 2 à 5 pays + année

**Pourquoi cette représentation ?**  
Le radar chart (ou spider chart) est idéal pour comparer **plusieurs entités sur plusieurs dimensions simultanément**. Chaque axe représente un indicateur sanitaire normalisé, ce qui permet de comparer des variables d'unités différentes sur une échelle commune. La surface couverte par chaque polygone donne une idée immédiate du "niveau sanitaire global" d'un pays : plus la surface est grande, meilleur est le profil.

> ⚠️ **Note importante sur l'inversion :** Les indicateurs VIH, Tuberculose et Malaria sont **volontairement inversés** lors de la normalisation. Ainsi, un score élevé sur ces axes signifie une *faible* prévalence — donc une *bonne* performance sanitaire. Cela rend la lecture cohérente : un grand polygone = un bon profil, quel que soit l'axe.

**Interaction :** Le multiselect permet de superposer jusqu'à 5 pays et le slider temporel permet d'observer comment les profils évoluent au fil des années.

---

### ⚖️ Visualisation 11 : Comparateur Direct — 2 Pays Face à Face

**Type :** Grille 2×3 de courbes superposées + KPIs (`st.metric`)  
**Paramètres :** Pays A (bleu) vs Pays B (rouge pointillé)

**Pourquoi cette représentation ?**  
Cette section est conçue pour une **analyse comparative ciblée** entre deux pays. Chaque indicateur est affiché dans son propre graphique avec les deux pays superposés, ce qui permet d'identifier précisément sur quels aspects l'un dépasse l'autre et à partir de quelle année les trajectoires divergent.

Les **KPIs synthétiques** en bas de section affichent pour chaque indicateur :
- La valeur absolue du Pays A pour la dernière année disponible
- Le **delta** (écart) avec le Pays B, avec flèche verte (avantage) ou rouge (retard)

C'est la visualisation la plus opérationnelle du dashboard : elle permet de formuler des conclusions directes et chiffrées sur les écarts sanitaires entre deux pays.

---

# 🛠️ Stack Technique

| Composant | Technologie |
|---|---|
| Interface web | Streamlit |
| Données | wbdata (API Banque Mondiale) |
| Visualisations | Plotly Express + Plotly Graph Objects |
| Traitement des données | Pandas |
| Langage | Python 3.x |

---

# 🚀 Lancement du projet

```bash
pip install streamlit wbdata plotly pandas
streamlit run app.py
```

---

*Projet réalisé dans le cadre du cours d'Analyse et Visualisation de Données — ESGIS*