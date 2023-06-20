from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv, get_key
import re

from wiki_loader import DeFiChainWikiLoader
from sitemap_parser import get_urls

load_dotenv()

scrapeUrls = ["https://www.defichainwiki.com/sitemap.xml"]
chunk_size = 400
chunk_overlap = 0

urls = []

# Get all urls from sitemap
for url in scrapeUrls:
    urls.extend(get_urls(url))
print("🔎 Found %s pages in total" % len(urls))

# Remove duplicates
urls = list(dict.fromkeys(urls))
print("🔎 Found %s unique pages" % len(urls))

# Remove pages not in '/docs' because they have no content worth indexing
urls = [url for url in urls if "/docs" in url]
print("🔎 Found %s pages in /docs" % len(urls))

# Remove category pages because they have no content worth indexing
urls = [url for url in urls if "/category" not in url]
print("🔎 Found %s pages which are not a /category" % len(urls))

# Remove Updated_White_Paper because it contains very old data
urls = [url for url in urls if "/Updated_White_Paper" not in url]
print("🔎 Found %s pages which are not 'Updated_White_Paper'" % len(urls))


print("🔭 Scrape %s found pages.." % len(urls))
print("---")
docs = []
for url in urls:
    loader = DeFiChainWikiLoader(url)
    doc = loader.load()[0]
    docs.append(doc)
    print("🌐 Source:", doc.metadata["source"])
    print("🔖 Title:", doc.metadata["title"])
    print("📄 Content:", doc.page_content.replace("\n", " ")[:100])
    print("---")
print("✅ Scraped %s pages" % len(docs))


print("➖ Remove long strings..")
for document in docs:
    document.page_content = re.sub(
        r"(?<=\S)[^\s]{" + str(chunk_size) + ",}(?=\S)", "", document.page_content
    )
print("✅ Removed long strings")


print("🗨 Split into chunks..")
text_splitter = CharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator="\n"
)
docs = text_splitter.split_documents(docs)
print("✅ Split into %s chunks" % len(docs))


print("🔮 Embedding..")
embeddings = OpenAIEmbeddings()

qdrant = Qdrant.from_documents(
    docs,
    embeddings,
    url=get_key(".env", "QDRANT_HOST"),
    api_key=get_key(".env", "QDRANT_API_KEY"),
    prefer_grpc=True,
    collection_name="DeFiChainWiki",
)
print("✅ Embedded")
