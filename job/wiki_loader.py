"""Loader that loads from DeFiChainWiki."""
from typing import List

from langchain.docstore.document import Document
from langchain.document_loaders.web_base import WebBaseLoader


class DeFiChainWikiLoader(WebBaseLoader):
    """Loader that loads from DeFiChainWiki."""

    def load(self) -> List[Document]:
        """Load webpage."""
        soup = self.scrape()

        title_tag = soup.find("h1")
        if title_tag:
            title = title_tag.get_text()
        else:
            title = ""

        last_updated_tag = soup.find("span", {"class": "theme-last-updated"})
        if last_updated_tag:
            last_updated = last_updated_tag.get_text()
        else:
            last_updated = ""

        article_tag = soup.find("article")
        if article_tag:
            content = article_tag.get_text(separator="\n")
        else:
            content = ""

        metadata = {
            "title": title,
            "last_updated": last_updated,
            "source": self.web_path,
        }

        return [Document(page_content=content, metadata=metadata)]


if __name__ == "__main__":
    loader = DeFiChainWikiLoader("https://www.defichainwiki.com/docs/auto/Introduction")
    docs = loader.load()
    doc = docs[0]
    print("Source:", doc.metadata["source"])
    print("Title:", doc.metadata["title"])
    print("Content:", doc.page_content)
