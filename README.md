# Dutch Vocabulary Practice — Nederlands naar Perfectie (B2–C1)

An interactive flashcard app for practicing Dutch vocabulary from the textbook
*Nederlands naar Perfectie* (levels B2 to C1).

This repository is linked to two versions of the app, with the same words and features:

- **Web app (works on phones and desktop):** [Dutch Vocabulary Flashcards (GitHub Pages)](https://antonis-koutsoumpis.github.io/dutch_vocabulary_practice_nederlands_naar_perfectie_b2_c1/). It can be installed on a phone's home screen (iPhone: *Share → Add to Home Screen*; Android: menu ⋮ → *Install app*) and works offline after the first visit.
- **Streamlit app:** [Dutch Vocabulary Flashcards](https://dutch-vocab-practice.streamlit.app/).

## What it does

- Presents Dutch words and phrases as individual flashcards (tab **Dutch → English**)
- Also practices the other way round (tab **English → Dutch**): the card shows the English meaning with an English example sentence for context, and you think of the Dutch word or phrase
- Lets you filter by **Hoofdstuk** (chapter) and **Tekst** (text)
- Lets you choose how many words to practice: 5, 10, 20, or all
- Reveals the English translation and an example Dutch sentence on demand
- Links every word or phrase to [YouGlish](https://youglish.com/dutch) (Dutch as spoken in the Netherlands, *NL*), to hear it in real conversations. Notes in brackets and alternatives are left out of the search (*onder druk staan/zetten* searches *onder druk staan*); results for longer phrases may be less accurate
- Shuffles a fresh random selection with the **New set** button

## Who it's for

Dutch learners working through *Nederlands naar Perfectie* who want a quick,
randomized way to drill vocabulary — on laptop or phone.

## How to use it

1. Open the app link
2. In the sidebar, pick a chapter and text (or leave both on "All")
3. Choose how many words you want (5 / 10 / 20 / All)
4. Choose a tab: **Dutch → English** or **English → Dutch**
5. Click **Show answer** on each card to reveal the translation and example sentence
6. Click **🔀 New set** anytime for a fresh random selection

## Web app (GitHub Pages)

The web app lives in `docs/` (plain HTML, CSS and JavaScript). Its word list, `docs/data/words.json`, is made from the Excel file by `scripts/export_web.py`. The GitHub Action `.github/workflows/web-data.yml` runs that script whenever the Excel file changes, so both apps always show the same words.

To publish it: in the repository on GitHub go to **Settings → Pages**, choose **Deploy from a branch**, branch **main**, folder **/docs**, and save.

## Built with

- [Streamlit](https://streamlit.io) — app framework
- [pandas](https://pandas.pydata.org) — data handling
- Plain HTML, CSS and JavaScript — web app
- Vocabulary source: *Nederlands naar Perfectie* (B2–C1)
