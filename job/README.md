[![Wiki scraping/embedding](https://github.com/0ptim/JellyChat/actions/workflows/wiki_scraping.yml/badge.svg)](https://github.com/0ptim/JellyChat/actions/workflows/wiki_scraping.yml)

# JellyChat - Job

Contains a script that is executed daily at 02:45 UTC via a GitHub action. However, it only runs if there have been changes to the [`/docs`](https://github.com/0ptim/DeFiChainWiki/tree/main/docs) directory within [0ptim/DeFiChainWiki](https://github.com/0ptim/DeFiChainWiki) in the past 24 hours. If changes are detected, the script scrapes the [DeFiChainWiki](defichainwiki.com) to generate new embeddings. These embeddings are then stored in Supabase in the table `embeddings`.

## Process

- Scrapes defichainwiki.com
- Splits the content into documents
- Creates embeddings for each document
- Saves embeddings to Supabase

## Technologies

- Python
- LangChain
- OpenAI API
- Supabase

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API Key.
  - Used to embed documents.
- `SUPABASE_URL` - Supabase API URL.
  - Used to store the documents and their embeddings.
  - Can be obtained here: [app.supabase.io](https://app.supabase.com/)
- `SUPABASE_KEY` - Supabase anon key.
  - Used to store the documents and their embeddings.
  - Can be obtained here: [app.supabase.io](https://app.supabase.com/)

## Python basic commands

### Create virtual environment

```
python -m venv venv
```

### Activate virtual environment

```
.\venv\Scripts\activate
```

### Deactivate virtual environment

```
Deactivate
```

### Install all project dependencies

```
pip install -r requirements.txt
```
