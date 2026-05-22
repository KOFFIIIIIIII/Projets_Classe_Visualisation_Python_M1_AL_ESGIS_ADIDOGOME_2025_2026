# app.py
# Streamlit app de presentation - Bank Marketing
# Lancement : streamlit run app/app.py
#
# Note pour moi-meme : structure en pages via la sidebar, on suit le plan
# de l'expose. Chaque page = un chapitre.

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats

# ----- Config & chargement ----------------------------------------------

CSV = Path(__file__).resolve().parent.parent / "data" / "bank-full.csv"

st.set_page_config(
    page_title="Bank Marketing - Junior Samuel KOUDJI",
    page_icon=":bar_chart:",
    layout="wide",
)


@st.cache_data
def load():
    d = pd.read_csv(CSV, sep=";")
    d["y_bin"] = (d["y"] == "yes").astype(int)
    return d


df = load()

# Palette - on s'aligne sur le PPT pour que la demo soit coherente
COUL_OK = "#00E5B0"   # souscription
COUL_KO = "#FF5C7A"   # refus
COUL_OR = "#FFC64D"   # accent / highlights
COUL_BL = "#6E95FF"

# ----- Petits helpers ---------------------------------------------------

def section(titre, sous_titre=None):
    st.markdown(f"## {titre}")
    if sous_titre:
        st.caption(sous_titre)
    st.markdown("---")


def insight(texte):
    """Encart 'Ce que ca veut dire' a la fin de chaque chapitre."""
    st.info(f"**Lecture :** {texte}")


def kpi_row(items):
    cols = st.columns(len(items))
    for c, (label, val, hint) in zip(cols, items):
        with c:
            st.metric(label, val, hint)


# ----- Sidebar : navigation linéaire ------------------------------------

st.sidebar.markdown("### Bank Marketing")
st.sidebar.caption("M1 ESGIS - Visualisation Python")
st.sidebar.markdown("---")

PAGES = [
    "1. Accueil",
    "2. Le dataset",
    "3. Exploration",
    "4. Q1 - Qui souscrit ?",
    "5. Q2 - Le solde",
    "6. Q3 - Variables categorielles",
    "7. Q4 - Duree d'appel",
    "8. Conclusions",
    "9. Stack & demo",
]
page = st.sidebar.radio("Navigation", PAGES, label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Junior Samuel KOUDJI**  \n"
    "Groupe 4 - 2025/2026  \n"
    "[Notebook complet](../notebook/analyse.ipynb)"
)

# =======================================================================
# PAGE 1 - Accueil
# =======================================================================
if page == PAGES[0]:
    st.title("Bank Marketing - analyse d'une campagne bancaire")
    st.caption("Junior Samuel KOUDJI - Groupe 4 - M1 Architecture Logiciels - ESGIS Adidogome")

    st.markdown("""
    Cette application accompagne mon expose. Elle reprend exactement les memes
    chapitres que la presentation orale, mais en interactif. Pour chaque
    question, on a :
    le **graphe**, l'**explication** de ce qu'on voit, et le **test statistique**
    quand il y en a un.
    """)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### Le sujet")
        st.write(
            "Une banque portugaise a passe 45 211 appels entre 2008 et 2013 "
            "pour vendre un depot a terme. Question : qu'est-ce qui differencie "
            "un client qui dit oui d'un client qui dit non ?"
        )
    with c2:
        st.markdown("#### La methode")
        st.write(
            "Analyse descriptive en 4 questions, chacune appuyee par un test "
            "statistique (Student, Chi-2, Pearson). Le code complet est dans "
            "le notebook, le dashboard sert a verifier les chiffres en live."
        )
    with c3:
        st.markdown("#### Les outils")
        st.write(
            "pandas pour les donnees, scipy pour les tests, plotly pour les "
            "graphes, et Streamlit + Dash pour les dashboards. Plotly Studio "
            "pour l'edition no-code."
        )

    st.markdown("### Chiffres cles")
    kpi_row([
        ("Clients", f"{len(df):,}".replace(",", " "), "lignes du CSV"),
        ("Variables", "17", "dont la cible y"),
        ("Taux souscription", "11.7 %", "5 289 sur 45 211"),
        ("Valeurs manquantes", "0", "rien a imputer"),
    ])

    st.markdown(" ")
    st.success(
        "Astuce : utilise la **sidebar a gauche** pour passer d'un chapitre "
        "a l'autre. Tout suit l'ordre de l'expose."
    )

# =======================================================================
# PAGE 2 - Le dataset
# =======================================================================
elif page == PAGES[1]:
    section(
        "Le dataset",
        "UCI Bank Marketing - 45 211 observations, 17 variables, source : "
        "Moro et al. (2014)",
    )

    st.markdown("""
    Le dataset a ete telecharge sur **UCI Machine Learning Repository**.
    Il decrit une campagne de telephonage realisee par une banque portugaise.
    Chaque ligne = un client appele. La variable cible `y` vaut `yes` si le
    client a souscrit a un depot a terme, `no` sinon.
    """)

    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("#### Apercu (10 premieres lignes)")
        st.dataframe(df.head(10), use_container_width=True)

    with c2:
        st.markdown("#### Resume")
        st.write(f"- **{df.shape[0]:,}** lignes".replace(",", " "))
        st.write(f"- **{df.shape[1]}** colonnes")
        st.write(f"- **{df.isna().sum().sum()}** valeurs manquantes")
        st.write("- Cible : `y` (binaire yes/no)")
        st.write("- Separateur CSV : `;`")
        st.write("- Encodage : UTF-8")

    st.markdown("#### Les variables")
    var_groupes = pd.DataFrame([
        ["Client", "age, job, marital, education", "Profil socio"],
        ["Finance", "default, balance, housing, loan", "Situation bancaire"],
        ["Contact", "contact, day, month, duration", "Detail de l'appel"],
        ["Campagne", "campaign, pdays, previous, poutcome", "Historique marketing"],
        ["Cible", "y", "Souscription oui/non"],
    ], columns=["Groupe", "Variables", "Description"])
    st.dataframe(var_groupes, use_container_width=True, hide_index=True)

    insight(
        "Le dataset est propre, equilibre en colonnes mais tres desequilibre "
        "en cible (88 % de non, 12 % de oui). Ce desequilibre est un point "
        "central de toute la suite."
    )

# =======================================================================
# PAGE 3 - Exploration
# =======================================================================
elif page == PAGES[2]:
    section(
        "Exploration",
        "Premiere lecture - on regarde a quoi ressemble la cible et les variables",
    )

    st.markdown("#### La cible : une decision sur huit est un oui")

    g1, g2 = st.columns([1, 2])
    with g1:
        rep = df["y"].value_counts().reset_index()
        rep.columns = ["souscription", "n"]
        rep["pct"] = (rep["n"] / rep["n"].sum() * 100).round(1)
        st.dataframe(rep, hide_index=True, use_container_width=True)

    with g2:
        fig = px.bar(
            rep, x="souscription", y="n", color="souscription",
            color_discrete_map={"no": COUL_KO, "yes": COUL_OK},
            text="pct", title="Repartition de la cible",
        )
        fig.update_traces(texttemplate="%{text} %", textposition="outside")
        fig.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig, use_container_width=True)

    insight(
        "Avec seulement 11.7 % de souscriptions, predire toujours 'non' "
        "donnerait 88 % d'accuracy sans aucune valeur business. C'est pour "
        "ca qu'on reste sur de l'analyse descriptive, pas sur du predictif."
    )

    st.markdown("#### Distribution de l'age")
    fig_age = px.histogram(
        df, x="age", nbins=40, color="y",
        color_discrete_map={"no": COUL_KO, "yes": COUL_OK},
        opacity=0.75, barmode="overlay",
        title="Age selon la souscription",
    )
    fig_age.update_layout(height=400)
    st.plotly_chart(fig_age, use_container_width=True)

    insight(
        "Deux pics chez les souscripteurs : autour de 25-30 ans (etudiants) "
        "et au-dela de 60 ans (retraites). Entre les deux, la masse de la "
        "population active n'est pas tres reactive a la campagne."
    )

# =======================================================================
# PAGE 4 - Q1 Profil
# =======================================================================
elif page == PAGES[3]:
    section(
        "Question 1 - Qui souscrit vraiment ?",
        "On regarde le taux de souscription par metier, marital, education",
    )

    st.write(
        "Hypothese de depart : le profil socio (metier surtout) joue un role "
        "majeur. On compare directement les taux."
    )

    tx_job = df.groupby("job")["y_bin"].mean().mul(100).reset_index()
    tx_job = tx_job.sort_values("y_bin")
    fig = px.bar(
        tx_job, x="y_bin", y="job", orientation="h",
        color="y_bin", color_continuous_scale=[COUL_KO, COUL_OR, COUL_OK],
        labels={"y_bin": "% souscription", "job": ""},
        title="Taux de souscription par metier",
    )
    fig.update_layout(coloraxis_showscale=False, height=450)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    top = tx_job.iloc[-1]
    bot = tx_job.iloc[0]
    c1.metric("Top metier", top["job"], f"{top['y_bin']:.1f} %")
    c2.metric("Flop metier", bot["job"], f"{bot['y_bin']:.1f} %")
    c3.metric("Ecart", f"x{top['y_bin']/bot['y_bin']:.1f}",
              "fois plus probable")

    insight(
        f"Un {top['job']} est environ "
        f"{top['y_bin']/bot['y_bin']:.1f} fois plus susceptible de souscrire "
        f"qu'un {bot['job']}. C'est l'ecart le plus fort qu'on trouvera dans "
        "tout le dataset, intra-variable."
    )

    st.markdown("#### Marital & education - vue complementaire")
    c1, c2 = st.columns(2)

    with c1:
        tx_m = df.groupby("marital")["y_bin"].mean().mul(100).reset_index()
        fig_m = px.bar(tx_m, x="marital", y="y_bin", color="marital",
                        text=tx_m["y_bin"].round(1),
                        labels={"y_bin": "% souscription"},
                        title="Par statut marital")
        fig_m.update_traces(textposition="outside")
        fig_m.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_m, use_container_width=True)

    with c2:
        tx_e = df.groupby("education")["y_bin"].mean().mul(100).reset_index()
        fig_e = px.bar(tx_e, x="education", y="y_bin", color="education",
                        text=tx_e["y_bin"].round(1),
                        labels={"y_bin": "% souscription"},
                        title="Par niveau d'education")
        fig_e.update_traces(textposition="outside")
        fig_e.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_e, use_container_width=True)

    insight(
        "Les celibataires souscrivent plus que les maries/divorces, et le "
        "niveau d'education tertiary se detache. Le profil 'gagnant' commence "
        "a se dessiner : etudiant ou retraite, plutot celibataire, plutot "
        "diplome."
    )

# =======================================================================
# PAGE 5 - Q2 Solde
# =======================================================================
elif page == PAGES[4]:
    section(
        "Question 2 - Les souscripteurs sont-ils plus riches ?",
        "Comparaison des soldes bancaires - test de Student",
    )

    st.write(
        "Hypothese H0 : le solde moyen est le meme dans les deux groupes. "
        "On utilise un test de Student de Welch (variances inegales)."
    )

    c1, c2 = st.columns([2, 1])

    with c1:
        # On filtre les outliers extremes pour la lisibilite du boxplot,
        # mais le test stat se fait sur tout
        d_box = df[df["balance"].between(df["balance"].quantile(0.01),
                                            df["balance"].quantile(0.99))]
        fig = px.box(
            d_box, x="y", y="balance", color="y",
            color_discrete_map={"no": COUL_KO, "yes": COUL_OK},
            points=False,
            labels={"y": "Souscrit", "balance": "Solde (euros)"},
            title="Solde bancaire par groupe (1-99 percentile pour la lisibilite)",
        )
        fig.update_layout(showlegend=False, height=450)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        b_yes = df.loc[df["y"] == "yes", "balance"]
        b_no = df.loc[df["y"] == "no", "balance"]
        t_stat, p_val = stats.ttest_ind(b_yes, b_no, equal_var=False)

        st.markdown("#### Test de Welch")
        st.metric("Moyenne refus", f"{b_no.mean():,.0f} EUR".replace(",", " "))
        st.metric("Moyenne souscription",
                  f"{b_yes.mean():,.0f} EUR".replace(",", " "))
        st.metric("t", f"{t_stat:.2f}")
        st.metric("p-value", f"{p_val:.2e}")

        if p_val < 0.05:
            st.success("p < 0.05 - on rejette H0")
        else:
            st.warning("p >= 0.05 - on garde H0")

    insight(
        "Difference de l'ordre de 500 euros sur la moyenne. Avec n=45 000, "
        "meme une petite difference devient statistiquement significative, "
        "mais ici l'effet est aussi visible a l'oeil. Conclusion : les "
        "souscripteurs ont en moyenne un solde plus eleve."
    )

# =======================================================================
# PAGE 6 - Q3 Catégoriel (Chi-2)
# =======================================================================
elif page == PAGES[5]:
    section(
        "Question 3 - Quelles variables categorielles comptent ?",
        "On passe 7 variables au test du Chi-2",
    )

    st.write(
        "Le Chi-2 teste si une variable categorielle est independante de la "
        "cible. Plus le Chi-2 est grand (et p petit), plus la variable "
        "discrimine. On les classe par force."
    )

    rows = []
    for col in ["job", "marital", "education", "housing",
                "loan", "default", "contact"]:
        tbl = pd.crosstab(df[col], df["y"])
        chi2, p, dof, _ = stats.chi2_contingency(tbl)
        rows.append({
            "Variable": col,
            "Chi-2": round(chi2, 1),
            "ddl": dof,
            "p-value": f"{p:.2e}",
            "Significatif (p<0.05)": "OUI" if p < 0.05 else "non",
        })
    res = pd.DataFrame(rows).sort_values("Chi-2", ascending=False)
    st.dataframe(res, hide_index=True, use_container_width=True)

    fig = px.bar(
        res.sort_values("Chi-2"), x="Chi-2", y="Variable", orientation="h",
        color="Chi-2", color_continuous_scale=[COUL_KO, COUL_OR, COUL_OK],
        title="Force de l'association avec la souscription",
    )
    fig.update_layout(coloraxis_showscale=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

    insight(
        "Toutes les variables testees ressortent significatives (p < 0.001). "
        "Le metier domine, suivi par le type de contact (cellulaire vs fixe) "
        "et le pret immobilier. La variable `default` (defaut de paiement) "
        "est la plus faible - logiquement, peu de clients sont en defaut."
    )

# =======================================================================
# PAGE 7 - Q4 Durée d'appel
# =======================================================================
elif page == PAGES[6]:
    section(
        "Question 4 - Qu'est-ce qui fait qu'un appel marche ?",
        "Correlation de Pearson entre la duree d'appel et la souscription",
    )

    st.write(
        "On regarde si la duree de l'appel est correlee a la souscription. "
        "Attention : la duree n'est connue qu'apres l'appel, donc c'est un "
        "indicateur **descriptif**, pas predictif (fuite de donnees sinon)."
    )

    c1, c2 = st.columns([2, 1])

    with c1:
        d_box = df[df["duration"] < df["duration"].quantile(0.99)]
        fig = px.box(
            d_box, x="y", y="duration", color="y",
            color_discrete_map={"no": COUL_KO, "yes": COUL_OK},
            points=False,
            labels={"y": "Souscrit", "duration": "Duree (secondes)"},
            title="Duree d'appel par groupe",
        )
        fig.update_layout(showlegend=False, height=420)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        r, p = stats.pearsonr(df["duration"], df["y_bin"])
        med_no = df.loc[df["y"] == "no", "duration"].median()
        med_yes = df.loc[df["y"] == "yes", "duration"].median()

        st.markdown("#### Test de Pearson")
        st.metric("Mediane Non", f"{med_no:.0f} s")
        st.metric("Mediane Oui", f"{med_yes:.0f} s",
                   f"x{med_yes/med_no:.1f}")
        st.metric("r", f"{r:.3f}")
        st.metric("p-value", f"{p:.2e}")

    st.markdown("#### Matrice de correlation (toutes variables num.)")
    corr = df[["age", "balance", "duration", "campaign",
                "previous", "y_bin"]].corr()
    fig_c = go.Figure(data=go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.columns,
        colorscale="RdBu", zmid=0,
        text=corr.round(2).values, texttemplate="%{text}",
    ))
    fig_c.update_layout(height=420,
                         title="Correlations entre variables numeriques")
    st.plotly_chart(fig_c, use_container_width=True)

    insight(
        f"r = {r:.2f}, p quasi nul, mediane qui passe de {med_no:.0f}s a "
        f"{med_yes:.0f}s. Le message operationnel : un commercial qui tient "
        "la conversation a beaucoup plus de chances de conclure. Mais "
        "encore une fois, on **explique** apres coup, on ne **predit** pas."
    )

# =======================================================================
# PAGE 8 - Conclusions
# =======================================================================
elif page == PAGES[7]:
    section("Conclusions et recommandations",
            "Ce qu'on retient pour les prochaines campagnes")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### 4 leviers actionnables")
        st.markdown("""
        1. **Cibler en priorite** : etudiants, retraites, celibataires
           diplomes, clients sans pret immobilier avec solde > mediane.
        2. **Former les commerciaux** a tenir la conversation - la duree
           d'appel correle fortement (r = 0.40).
        3. **Privilegier le contact mobile** sur le telephone fixe (le
           Chi-2 le confirme).
        4. **Limiter les relances** : au-dela de 3 contacts dans la meme
           campagne, le taux de reussite chute.
        """)

    with c2:
        st.markdown("#### Limites a reconnaitre")
        st.markdown("""
        - **Desequilibre 88/12** : biaiserait toute modelisation naive.
          Il faudrait stratifier ou utiliser class_weight si on passait
          au predictif.
        - **Duration est connue a posteriori** : descriptif uniquement.
        - **Donnees 2008-2013** : contexte post-crise, pas forcement
          representatif d'aujourd'hui.
        - On a fait du descriptif. Une suite naturelle serait de faire
          tourner une regression logistique ou un random forest, en
          excluant `duration`, pour voir ce qu'on peut **predire**.
        """)

    st.markdown("---")
    st.markdown("#### Resume des tests")
    resume = pd.DataFrame([
        ["Q1", "Profil", "Comparaison de taux", "Etudiants 28.7% vs ouvriers 7.3%"],
        ["Q2", "Solde", "Student (Welch)", "t=9.93 ; p<1e-22"],
        ["Q3", "Categoriel", "Chi-2", "7/7 variables significatives"],
        ["Q4", "Duree", "Pearson", "r=0.395 ; p~0"],
    ], columns=["Q", "Theme", "Test", "Verdict"])
    st.dataframe(resume, hide_index=True, use_container_width=True)

# =======================================================================
# PAGE 9 - Stack & démo
# =======================================================================
else:
    section("Stack de visualisation & demo",
            "Les 6 outils utilises pour ce projet")

    outils = [
        ("pandas", "Chargement & traitement",
         "DataFrame, agregations, recodages. Base de toute l'analyse."),
        ("matplotlib / seaborn", "Graphes statiques",
         "Distributions et boxplots dans le rapport (PNG)."),
        ("plotly", "Graphes interactifs",
         "Hover, zoom, legendes cliquables. Base de Streamlit et Dash."),
        ("streamlit", "Cette app",
         "Pages narratives, KPI, tests recalcules."),
        ("dash", "Dashboard applicatif",
         "Callbacks Python, meme palette. Lancement : python dash_app/app_dash.py"),
        ("plotly studio", "Edition no-code",
         "Importer les .json de plotly_studio/ sur plotly.com/studio/"),
    ]
    cols = st.columns(3)
    for i, (nom, sous, desc) in enumerate(outils):
        with cols[i % 3]:
            st.markdown(f"##### {nom}")
            st.caption(sous)
            st.write(desc)
            st.markdown(" ")

    st.markdown("---")
    st.markdown("#### Commandes de demo")
    st.code(
        "# 1. Notebook\n"
        "jupyter notebook notebook/analyse.ipynb\n\n"
        "# 2. Streamlit (cette app)\n"
        "streamlit run app/app.py\n\n"
        "# 3. Dash\n"
        "python dash_app/app_dash.py\n\n"
        "# 4. Plotly Studio\n"
        "# Ouvrir https://plotly.com/studio/\n"
        "# Puis Import -> plotly_studio/01_taux_par_metier.json",
        language="bash",
    )

    st.markdown(" ")
    st.success("Merci pour votre attention. Place aux questions.")
