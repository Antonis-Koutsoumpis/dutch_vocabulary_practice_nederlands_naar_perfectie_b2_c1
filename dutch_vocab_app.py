import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Dutch Vocab Flashcards", layout="centered")
st.title("🇳🇱 Dutch Vocabulary Flashcards")

# ---- Load data ----
@st.cache_data
def load_data(path):
    df = pd.read_excel(path)
    df.columns = [c.strip() for c in df.columns]
    return df

# Your actual Excel filename
FILE = "Nederlands_naar_perfectie_B2_C1_woordenschat.xlsx"
df = load_data(FILE)

# ---- Sidebar filters ----
st.sidebar.header("Filters")

# Multi-select for Hoofdstuk
chapters = ["All"] + sorted(df["Hoofdstuk"].dropna().unique().tolist())
chapter_choice = st.sidebar.multiselect(
    "Hoofdstuk",
    options=chapters,
    default=["All"],
)

if "All" in chapter_choice or not chapter_choice:
    sub = df.copy()
else:
    sub = df[df["Hoofdstuk"].isin(chapter_choice)]

# Multi-select for Tekst
texts = ["All"] + sorted(sub["Tekst"].dropna().unique().tolist())
text_choice = st.sidebar.multiselect(
    "Tekst",
    options=texts,
    default=["All"],
)

if "All" not in text_choice and text_choice:
    sub = sub[sub["Tekst"].isin(text_choice)]

# ---- Number of words ----
max_n = len(sub)
options = ["5", "10", "20", "All"]
choice = st.sidebar.radio("Number of words", options)

n = max_n if choice == "All" else min(int(choice), max_n)

# ---- Session state ----
if "seed" not in st.session_state:
    st.session_state.seed = 0
if "revealed" not in st.session_state:
    st.session_state.revealed = set()

if st.sidebar.button("🔀 New set"):
    st.session_state.seed += 1
    st.session_state.revealed = set()

# Deterministic sample per seed so cards stay stable while reviewing
sample = sub.sample(n=n, random_state=st.session_state.seed).reset_index(drop=True)

st.caption(f"Showing {len(sample)} of {max_n} matching entries.")

# ---- Cards ----
for i, row in sample.iterrows():
    with st.container(border=True):
        st.markdown(f"### {row['Dutch Word/Phrase']}")

        show = st.toggle("Show answer", key=f"toggle_{st.session_state.seed}_{i}")

        if show:
            st.markdown(f"**English:** {row['English Translation']}")
            st.markdown(f"**Voorbeeldzin:** {row['ranscribed Dutch Sentence']}")
            st.markdown(f"*{row['Literary English Translation (for back translation)']}*")
