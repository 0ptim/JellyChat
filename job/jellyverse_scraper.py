from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv, get_key
from sitemap_parser import get_urls
import re

from langchain.document_loaders import PyPDFLoader
import os
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import DocArrayInMemorySearch


load_dotenv()

chunk_size = 2000
chunk_overlap = 200


# loader = PyPDFLoader("jellyverse_notion/Jellyverse_PitchDeck.pdf")
# pages = loader.load()

# directory = './jellyverse_notion/'
# txt_files = [filename for filename in os.listdir(
#     directory) if filename.endswith('.txt')]

loader = DirectoryLoader('./jellyverse_notion', glob="**/*.txt")
docs = loader.load()

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
db = DocArrayInMemorySearch.from_documents(docs, embeddings)

qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
    chain_type="stuff",
    retriever=db.as_retriever()
)

if __name__ == '__main__':
    while True:
        question = input(
            'Ask something, that can be answered using information from Jellyverse\' Notion: ')
        result = qa({"query": question})
        print("✅ Answer:", result["result"])


# qdrant = Qdrant.from_documents(
#     docs, embeddings,
#     url=get_key('.env', 'QDRANT_HOST'),
#     api_key=get_key('.env', 'QDRANT_API_KEY'),
#     prefer_grpc=True,
#     collection_name='DeFiChainWiki')
# print('✅ Embedded')
