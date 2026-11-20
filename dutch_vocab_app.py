import streamlit as st
import pandas as pd
import random
import re
from urllib.parse import quote

st.set_page_config(page_title="Dutch Vocab Flashcards - Nederlands naar Perfectie (B2–C1)", layout="centered")
st.title("🇳🇱 Dutch Vocabulary Flashcards - Nederlands naar Perfectie (B2–C1)")

# ---- YouGlish: hear the word in real conversations ----
def youglish_query(text) -> str:
    """Search phrase for YouGlish: the first alternative, without notes in brackets.
    'onder druk staan/zetten' -> 'onder druk staan', 'aanscherpen (sep.)' -> 'aanscherpen',
    'de afkeer (van)' -> 'afkeer'."""
    t = re.sub(r"^\s*ook:\s*", "", str(text))
    t = re.sub(r"(?<=\S )\((\w+)\)(?= \S)", r"\1", t)    # 'op (zichzelf) aangewezen zijn': keep the word
    t = re.sub(r"\([^)]*\)|\[[^\]]*\]", "", t)            # other notes in brackets
    t = re.split(r"\s+/\s*|\s*/\s+|\n|,|;", t)[0]        # first of several alternatives
    prev = None
    while prev != t:                                      # 'staan/zetten' -> 'staan'
        prev, t = t, re.sub(r"([\w'-]+)/\s*[\w'.…-]+", r"\1", t)
    t = re.sub(r"\.\.\.|…", " ", t)
    t = re.sub(r"\s+", " ", t).strip(" .")
    return re.sub(r"^(de|het) (?=\S+$)", "", t)           # 'de nuance' -> 'nuance'


def youglish_link(text):
    """Link to YouGlish with Dutch as spoken in the Netherlands (NL, not BE)."""
    q = youglish_query(text)
    st.markdown(f"[🎧 Hear it in real conversations (YouGlish, NL)](https://youglish.com/pronounce/{quote(q, safe='')}/dutch/nl)"
                + (" · results for phrases may be inaccurate" if " " in q else ""))


GOOGLE_TOPICS = "translation, break down word/phrase logic, etymology, synonyms, examples"


def google_link(text):
    """Google search for the word or phrase as written in the list, plus GOOGLE_TOPICS."""
    q = f"{' '.join(str(text).split())} {GOOGLE_TOPICS}"
    st.markdown(f"[🔎 Search on Google (translation, word logic, etymology, synonyms, examples)]"
                f"(https://www.google.com/search?q={quote(q, safe='')})")


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
# The English -> Dutch tab gets its own random selection from the same filters
sample_en = sub.sample(n=n, random_state=st.session_state.seed + 100_000).reset_index(drop=True)

tab_nl, tab_en = st.tabs(["🇳🇱 Dutch → English", "🇬🇧 English → Dutch"])

# ---- Cards: Dutch -> English ----
with tab_nl:
    st.caption(f"Showing {len(sample)} of {max_n} matching entries.")
    for i, row in sample.iterrows():
        with st.container(border=True):
            st.markdown(f"### {row['Dutch Word/Phrase']}")

            show = st.toggle("Show answer", key=f"toggle_{st.session_state.seed}_{i}")

            if show:
                st.markdown(f"**English:** {row['English Translation']}")
                st.markdown(f"**Voorbeeldzin:** {row['ranscribed Dutch Sentence']}")
                st.markdown(f"*{row['Literary English Translation (for back translation)']}*")
                youglish_link(row["Dutch Word/Phrase"])
                google_link(row["Dutch Word/Phrase"])

# ---- Cards: English -> Dutch ----
with tab_en:
    st.caption(f"Showing {len(sample_en)} of {max_n} matching entries · "
               "read the English meaning and think of the Dutch word or phrase.")
    for i, row in sample_en.iterrows():
        with st.container(border=True):
            st.markdown(f"### {row['English Translation']}")
            # The English example sentence gives context (the Dutch one would give the answer away)
            example_en = re.sub(r"^\s*-\s*", "", str(row["Literary English Translation (for back translation)"]))
            st.markdown(f"*e.g. {example_en}*")

            show = st.toggle("Show answer", key=f"toggle_en_{st.session_state.seed}_{i}")

            if show:
                st.markdown(f"**Dutch:** {row['Dutch Word/Phrase']}")
                st.markdown(f"**Voorbeeldzin:** {row['ranscribed Dutch Sentence']}")
                youglish_link(row["Dutch Word/Phrase"])
                google_link(row["Dutch Word/Phrase"])
