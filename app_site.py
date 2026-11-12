
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Space Observatory",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded"
)
EXCEL_FILE = (
    Path(__file__).resolve().parent
    / "supernovae_FINAL_v2_CORRIGE.xlsx"
)
# =========================================================
# TRADUCTIONS DE L'INTERFACE
# Les données scientifiques ne sont jamais traduites.
# =========================================================

TEXT = {
    "English": {
        "subtitle": "Explore the universe, one supernova at a time.",
        "dashboard": "Dashboard",
        "catalogue": "Supernova Catalogue",
        "analysis": "Scientific Analysis",
        "about": "About",
        "navigation": "NAVIGATION",
        "language": "Language",
        "overview": "Overview",
        "total": "Total supernovae",
        "types": "Supernova types",
        "redshifts": "Objects with redshift",
        "photometry": "Photometric observations",
        "search": "Search by name, host or type",
        "type_filter": "Filter by supernova type",
        "redshift_filter": "Maximum redshift",
        "all_types": "All types",
        "results": "Search results",
        "details": "Object details",
        "choose": "Choose a supernova",
        "no_results": "No objects found.",
        "all_fields": "All original fields",
        "export": "Download filtered catalogue (CSV)",
        "distribution": "Distribution of supernova types",
        "redshift_chart": "Redshift distribution",
        "year_chart": "Discoveries by year",
        "missing": "Missing values",
        "records": "Records",
        "field": "Field",
        "value": "Value",
        "about_text": (
            "Space Observatory is a scientific platform "
            "for exploring supernova catalogue data."
        ),
        "source": "Data source",
        "source_text": (
            "Original catalogue supplied for this project. "
            "The Excel workbook is used without modifying "
            "its scientific values."
        ),
        "loading": "Loading the supernova catalogue...",
        "error": "Unable to read the Excel file.",
        "select_language": "Interface language"
    },

    "Français": {
        "subtitle": "Explorez l'univers, une supernova à la fois.",
        "dashboard": "Tableau de bord",
        "catalogue": "Catalogue des supernovae",
        "analysis": "Analyse scientifique",
        "about": "À propos",
        "navigation": "NAVIGATION",
        "language": "Langue",
        "overview": "Vue générale",
        "total": "Nombre total de supernovae",
        "types": "Types de supernovae",
        "redshifts": "Objets avec redshift",
        "photometry": "Observations photométriques",
        "search": "Rechercher par nom, hôte ou type",
        "type_filter": "Filtrer par type de supernova",
        "redshift_filter": "Redshift maximal",
        "all_types": "Tous les types",
        "results": "Résultats de recherche",
        "details": "Détails de l'objet",
        "choose": "Choisir une supernova",
        "no_results": "Aucun objet trouvé.",
        "all_fields": "Tous les champs originaux",
        "export": "Télécharger le catalogue filtré (CSV)",
        "distribution": "Répartition des types de supernovae",
        "redshift_chart": "Distribution des redshifts",
        "year_chart": "Découvertes par année",
        "missing": "Valeurs manquantes",
        "records": "Enregistrements",
        "field": "Champ",
        "value": "Valeur",
        "about_text": (
            "Space Observatory est une plateforme scientifique "
            "permettant d'explorer un catalogue de supernovae."
        ),
        "source": "Source des données",
        "source_text": (
            "Catalogue original fourni pour ce projet. "
            "Le classeur Excel est utilisé sans modification "
            "des valeurs scientifiques."
        ),
        "loading": "Chargement du catalogue...",
        "error": "Impossible de lire le fichier Excel.",
        "select_language": "Langue de l'interface"
    },

    "Русский": {
        "subtitle": "Исследуйте Вселенную через сверхновые звёзды.",
        "dashboard": "Главная панель",
        "catalogue": "Каталог сверхновых",
        "analysis": "Научный анализ",
        "about": "О проекте",
        "navigation": "НАВИГАЦИЯ",
        "language": "Язык",
        "overview": "Общая информация",
        "total": "Всего сверхновых",
        "types": "Типы сверхновых",
        "redshifts": "Объекты с красным смещением",
        "photometry": "Фотометрические наблюдения",
        "search": "Поиск по имени, галактике или типу",
        "type_filter": "Фильтр по типу сверхновой",
        "redshift_filter": "Максимальное красное смещение",
        "all_types": "Все типы",
        "results": "Результаты поиска",
        "details": "Информация об объекте",
        "choose": "Выберите сверхновую",
        "no_results": "Объекты не найдены.",
        "all_fields": "Все исходные поля",
        "export": "Скачать отфильтрованный каталог (CSV)",
        "distribution": "Распределение типов сверхновых",
        "redshift_chart": "Распределение красных смещений",
        "year_chart": "Открытия по годам",
        "missing": "Отсутствующие значения",
        "records": "Записи",
        "field": "Поле",
        "value": "Значение",
        "about_text": (
            "Space Observatory — научная платформа "
            "для исследования каталога сверхновых."
        ),
        "source": "Источник данных",
        "source_text": (
            "Исходный каталог, предоставленный для проекта. "
            "Файл Excel используется без изменения "
            "научных значений."
        ),
        "loading": "Загрузка каталога сверхновых...",
        "error": "Не удалось прочитать файл Excel.",
        "select_language": "Язык интерфейса"
    }
}

# =========================================================
# DESIGN
# =========================================================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 80% 0%,
        #18294b 0%, #0b1428 35%, #070d19 75%);
    color: #f0f3fa;
}

[data-testid="stSidebar"] {
    background-color: #0a1222;
    border-right: 1px solid #263653;
}

h1, h2, h3 {
    color: #f3f5fb !important;
}

p, label, span {
    color: #d2d9e8;
}

.hero {
    padding: 28px;
    border: 1px solid #344666;
    border-radius: 16px;
    background: linear-gradient(120deg,
        #152747, #101a30, #18243c);
    margin-bottom: 25px;
}

.hero-title {
    color: #f0c674;
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #c5d0e3;
    font-size: 16px;
}

.metric-card {
    background: #121f36;
    border: 1px solid #30415e;
    padding: 18px;
    border-radius: 13px;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD EXCEL
# =========================================================

@st.cache_data(show_spinner=False)
def load_catalogue(file_path, modified_time):

    df = pd.read_excel(
        file_path,
        sheet_name="Supernovae",
        engine="openpyxl",
        dtype=object
    )

    # Conversion des colonnes numériques utiles
    numeric_columns = [
        "redshift",
        "maxappmag",
        "phot_count",
        "spectra_count"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column + "_numeric"] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# =========================================================
# CHECK FILE
# =========================================================

if not EXCEL_FILE.exists():

    st.error(f"Excel file not found: {EXCEL_FILE}")
    st.stop()

try:

    with st.spinner("Loading catalogue..."):

        df = load_catalogue(
            str(EXCEL_FILE),
            EXCEL_FILE.stat().st_mtime
        )

except Exception as error:

    st.error(TEXT["English"]["error"])
    st.exception(error)
    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 🔭 SPACE OBSERVATORY")
st.sidebar.caption("SUPERNOVA SCIENCE PLATFORM")

language = st.sidebar.selectbox(
    "Interface language",
    ["English", "Français", "Русский"],
    index=0
)

t = TEXT[language]

st.sidebar.markdown("---")
st.sidebar.markdown(f"### {t['navigation']}")

page = st.sidebar.radio(
    "Navigation",
    [
        t["dashboard"],
        t["catalogue"],
        t["analysis"],
        t["about"]
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.caption("SUPERNOVA CATALOGUE")
st.sidebar.caption("150K+ astronomical records")


# =========================================================
# COMMON HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">🔭 SPACE OBSERVATORY</div>
    <div class="hero-subtitle">
        Explore the universe, one supernova at a time.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# DATA PREPARATION
# =========================================================

total = len(df)

if "claimedtype" in df.columns:
    type_count = df["claimedtype"].nunique(dropna=True)
else:
    type_count = 0

if "redshift_numeric" in df.columns:
    redshift_count = df["redshift_numeric"].notna().sum()
else:
    redshift_count = 0

if "phot_count" in df.columns:
    photometry_count = pd.to_numeric(
        df["phot_count"], errors="coerce"
    ).fillna(0).sum()
else:
    photometry_count = 0


# =========================================================
# PAGE 1: DASHBOARD
# =========================================================

if page == t["dashboard"]:

    st.title(t["overview"])
    st.write(t["subtitle"])

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(t["total"], f"{total:,}")
    c2.metric(t["types"], f"{type_count}")
    c3.metric(t["redshifts"], f"{redshift_count:,}")
    c4.metric(t["photometry"], f"{photometry_count:,.0f}")

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        st.subheader(t["distribution"])

        if "claimedtype" in df.columns:

            types = (
                df["claimedtype"]
                .fillna("Unknown")
                .value_counts()
                .head(15)
                .reset_index()
            )

            types.columns = ["Type", "Count"]

            fig = px.bar(
                types,
                x="Type",
                y="Count",
                color="Count",
                template="plotly_dark"
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig, width="stretch")

    with right:

        st.subheader(t["redshift_chart"])

        if "redshift_numeric" in df.columns:

            z = df["redshift_numeric"].dropna()

            if not z.empty:

                fig = px.histogram(
                    x=z,
                    nbins=50,
                    labels={"x": "Redshift", "y": "Count"},
                    template="plotly_dark"
                )

                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)"
                )

                st.plotly_chart(fig, width="stretch")

    st.markdown("---")

    st.subheader(t["year_chart"])

    if "discoverdate" in df.columns:

        dates = pd.to_datetime(
            df["discoverdate"],
            errors="coerce"
        )

        years = dates.dt.year.value_counts().sort_index()

        if not years.empty:

            year_df = years.reset_index()
            year_df.columns = ["Year", "Discoveries"]

            fig = px.line(
                year_df,
                x="Year",
                y="Discoveries",
                markers=True,
                template="plotly_dark"
            )

            st.plotly_chart(fig, width="stretch")


# =========================================================
# PAGE 2: CATALOGUE
# =========================================================

elif page == t["catalogue"]:

    st.title(t["catalogue"])

    filtered = df.copy()

    col1, col2 = st.columns([2, 1])

    with col1:

        search = st.text_input(
            t["search"],
            placeholder="SN1990I..."
        )

    with col2:

        if "claimedtype" in df.columns:

            available_types = sorted(
                df["claimedtype"]
                .dropna()
                .astype(str)
                .unique()
            )

            selected_type = st.selectbox(
                t["type_filter"],
                [t["all_types"]] + available_types
            )

        else:
            selected_type = t["all_types"]

    if selected_type != t["all_types"]:

        filtered = filtered[
            filtered["claimedtype"].astype(str) == selected_type
        ]

    if search.strip():

        query = search.strip().lower()

        search_columns = [
            c for c in ["name", "alias", "host", "claimedtype"]
            if c in filtered.columns
        ]

        mask = pd.Series(False, index=filtered.index)

        for column in search_columns:

            mask |= (
                filtered[column]
                .astype("string")
                .str.lower()
                .str.contains(query, na=False, regex=False)
            )

        filtered = filtered[mask]

    st.markdown("---")

    st.subheader(t["results"])

    st.write(f"{len(filtered):,} {t['records'].lower()}")

    display_columns = [
        c for c in [
            "name",
            "claimedtype",
            "discoverdate",
            "host",
            "redshift",
            "maxappmag",
            "phot_count",
            "spectra_count"
        ]
        if c in filtered.columns
    ]

    st.dataframe(
        filtered[display_columns],
        width="stretch",
        height=430,
        hide_index=True
    )

    csv_data = filtered.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        label=t["export"],
        data=csv_data,
        file_name="supernovae_filtered.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.subheader(t["details"])

    if not filtered.empty:

        detail_data = filtered.copy()
        detail_data.insert(0, "_original_row", filtered.index)

        options = detail_data["_original_row"].tolist()

        selected_row = st.selectbox(
            t["choose"],
            options,
            format_func=lambda x: (
                str(df.loc[x, "name"])
                if "name" in df.columns
                else f"Record {x}"
            )
        )

        record = df.loc[selected_row]

        st.markdown("### " + str(record.get("name", "Unknown")))

        details = pd.DataFrame({
            t["field"]: df.columns,
            t["value"]: [
                "—" if pd.isna(value) else str(value)
                for value in record.tolist()
            ]
        })

        st.dataframe(
            details,
            width="stretch",
            height=600,
            hide_index=True
        )

    else:

        st.info(t["no_results"])


# =========================================================
# PAGE 3: SCIENTIFIC ANALYSIS
# =========================================================

elif page == t["analysis"]:

    st.title(t["analysis"])

    st.write(
        "Explore the statistical properties of the catalogue."
    )

    if "redshift_numeric" in df.columns:

        z = df["redshift_numeric"].dropna()

        if not z.empty:

            st.subheader("Redshift statistics")

            a, b, c, d = st.columns(4)

            a.metric("Mean redshift", f"{z.mean():.4f}")
            b.metric("Median redshift", f"{z.median():.4f}")
            c.metric("Minimum", f"{z.min():.4f}")
            d.metric("Maximum", f"{z.max():.4f}")

            fig = px.histogram(
                x=z,
                nbins=80,
                template="plotly_dark",
                labels={"x": "Redshift", "y": "Number of objects"}
            )

            st.plotly_chart(fig, width="stretch")

    st.markdown("---")

    st.subheader(t["missing"])

    missing = df.isna().sum()

    missing_df = pd.DataFrame({
        "Field": missing.index,
        "Missing values": missing.values,
        "Percentage": (
            missing.values / len(df) * 100
        ).round(2)
    })

    missing_df = missing_df.sort_values(
        "Missing values",
        ascending=False
    )

    st.dataframe(
        missing_df,
        width="stretch",
        height=500,
        hide_index=True
    )

    st.markdown("---")

    st.subheader("Catalogue structure")

    st.write("Number of records:", f"{len(df):,}")
    st.write("Number of original fields:", len([
        c for c in df.columns
        if not c.endswith("_numeric")
    ]))


# =========================================================
# PAGE 4: ABOUT
# =========================================================

elif page == t["about"]:

    st.title(t["about"])

    st.markdown(
        f"""
        ### 🔭 Space Observatory

        {t["about_text"]}

        ### {t["source"]}

        {t["source_text"]}

        ### Catalogue information

        - Records: **{total:,}**
        - Original fields: **110**
        - Format: **Excel**
        - Sheet: **Supernovae**

        ### Scientific data integrity

        Original scientific values, object names and references
        are preserved. Only interface labels are translated.

        ---
        **Space Observatory**

        Scientific catalogue exploration platform.
        """
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "SPACE OBSERVATORY | Supernova Catalogue | "
    "Scientific data exploration"
)
