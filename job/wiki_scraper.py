from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv, get_key
from sitemap_parser import *
import re

load_dotenv()

scrapeUrl = 'https://www.defichainwiki.com/'
indexFileTarget = './indices/index_wiki.json'
chunk_size = 2000
chunk_overlap = 200

urls = getUrlsToScrape(scrapeUrl)

for url in urls:
    if "Updated_White_Paper" in url:
        print("Remove", url)
        urls.remove(url)


print('🔭 Scrape %s found pages..' % len(urls))
loader = UnstructuredURLLoader(urls=urls)
docs = loader.load()
print('✅ Scraped %s pages' % len(docs))


print('➖ Remove long strings..')
for document in docs:
    document.page_content = re.sub(
        r'(?<=\S)[^\s]{' + str(chunk_size) + ',}(?=\S)', '', document.page_content)
print('✅ Removed long strings')


print('🗨 Split into chunks..')
text_splitter = CharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap)
docs = text_splitter.split_documents(docs)
print('✅ Split into %s chunks' % len(docs))

print('🔮 Embedding..')
embeddings = OpenAIEmbeddings()

qdrant = Qdrant.from_documents(
    docs, embeddings,
    url=get_key('.env', 'QDRANT_HOST'),
    api_key=get_key('.env', 'QDRANT_API_KEY'),
    prefer_grpc=True,
    collection_name='DeFiChainWiki')
print('✅ Embedded')
