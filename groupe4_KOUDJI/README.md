# Bank Marketing - Analyse et Visualisation

Projet de fin de cours en visualisation de données.

- **Etudiant** : KOUDJI Junior Samuel
- **Niveau** : M1 Architecture Logiciels - ESGIS Adidogome
- **Annee** : 2025 / 2026
- **Groupe** : 4 (solo)
- **Theme impose** : Finance
- **Dataset** : UCI Bank Marketing (45 211 lignes, 17 colonnes)

## Question de recherche

> Quels profils de clients ont le plus de chances de souscrire un depot a
> terme lors d'une campagne d'appels telephoniques d'une banque ?

Quatre sous-questions :

1. Qui souscrit ? (age, metier, statut marital, education...)
2. Le solde bancaire influence-t-il la decision ?
3. Quelles variables categorielles sont liees a la souscription ?
4. La duree de l'appel est-elle correlee a la souscription ?

## Contenu du dossier

```
.
├── data/                  bank-full.csv (45 211 x 17)
├── notebook/              Analyse complete (Jupyter)
├── app/                   app.py - Dashboard Streamlit (storytelling 9 pages)
├── dash_app/              app_dash.py - Dashboard Dash equivalent
├── plotly_studio/         Figures exportees en JSON pour Plotly Studio
├── presentation.pptx      Slides de l'expose (22 slides)
├── speech.pdf             Notes orateur slide par slide
├── requirements.txt       Dependances Python
└── README.md
```

## Lancer le projet

J'ai utilise Python 3.13 sur Windows + un venv local.

```powershell
# Installer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Notebook (analyse complete)
jupyter notebook notebook/analyse.ipynb

# Streamlit (la "demo" principale de l'expose)
streamlit run app/app.py

# Dash (meme dataset, navigation par onglets)
python dash_app/app_dash.py
# -> http://127.0.0.1:8050

# Regenerer les exports Plotly Studio
python plotly_studio/export_figures.py
# Puis charger un .json sur https://plotly.com/studio/
```

## Les 6 outils demandes dans le bareme

| # | Etape                                | Outil utilise                                     |
|---|--------------------------------------|---------------------------------------------------|
| 1 | Chargement des donnees               | pandas                                            |
| 2 | Traitement / EDA                     | pandas + numpy + scipy.stats                      |
| 3 | Visualisations Plotly                | plotly.express, plotly.graph_objects              |
| 4 | Dashboard Streamlit                  | `app/app.py` (9 pages)                            |
| 5 | Dashboard Dash                       | `dash_app/app_dash.py` (callbacks + onglets)      |
| 6 | Plotly Studio                        | 5 figures JSON dans `plotly_studio/`              |

## Methode

1. Lecture du CSV avec `sep=";"` (separateur portugais).
2. Aucun NaN dans le dataset mais des `"unknown"` deguises -> documentes.
3. Trois tests statistiques pour appuyer les visualisations :
   - **t-test de Welch** sur le solde (Q2)
   - **Chi-2** sur 7 variables categorielles (Q3)
   - **Pearson** sur la duree d'appel (Q4)
4. Streamlit re-execute le test en live a chaque chargement de page : ce
   n'est pas une capture d'ecran, c'est calcule a partir du CSV au moment
   ou on regarde le dashboard.

## Resultats principaux

- **Solde** : t = 12.8, p ~ 4e-37. Les souscripteurs ont en moyenne ~440 EUR
  de plus sur leur compte.
- **Categoriel** : toutes les variables testees sortent significatives
  (p < 0.001), avec **education** et **housing** en tete.
- **Duree** : r = 0.39, p ~ 0. Plus l'appel est long, plus la souscription
  est probable. Attention au biais : un appel court signifie souvent un
  refus immediat.

## Stack technique

Python 3.13, pandas, numpy, scipy, plotly, streamlit, dash, jupyter,
matplotlib, seaborn (pour quelques figures du notebook).

Editeur : VS Code. Termina : PowerShell.

---

Pour toute question : KOUDJI Junior Samuel - M1 ALSI 1 - ESGIS.
