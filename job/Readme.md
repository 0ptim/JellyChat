# JellyChat - Job

Contains scripts that are executed periodically. Currently, it contains a script that scrapes defichainwiki.com and creates embeddings for each document. The embeddings are saved to Supabase using pgvector.

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

### Freeze requirements

```
pip freeze > requirements.txt
```
