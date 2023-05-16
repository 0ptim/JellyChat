# JellyChat - Job

Contains scripts that are executed periodically. Currently, it contains a script that scrapes defichainwiki.com and creates embeddings for each document. The embeddings are saved to Qdrant.

## Process

- Scrapes defichainwiki.com
- Splits the content into documents
- Creates embeddings for each document
- Saves embeddings to Qdrant

## Technologies

- Python
- LangChain
- OpenAI API
- Qdrant

# Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API Key.
- `QDRANT_HOST` - Qdrant host URL of cluster.
- `QDRANT_API_KEY` - Qdrant API Key.

# Python basic commands

## Create virtual environment

```
python -m venv venv
```

## Activate virtual environment

```
.\venv\Scripts\activate
```

## Deactivate virtual environment

```
Deactivate
```

## Install all project dependencies

```
pip install -r requirements.txt
```

## Freeze requirements

```
pip freeze > requirements.txt
```
