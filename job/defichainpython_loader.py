"""Loader that loads from DefichainPython."""
from typing import List

from langchain.docstore.document import Document
from langchain.document_loaders.web_base import WebBaseLoader


class DefichainPythonLoader(WebBaseLoader):
    """Loader that loads from DefichainPython."""

    @staticmethod
    def replace_enter(text: str) -> str:
        while text.find("\n\n") != -1:
            text = text.replace("\n\n", "\n")
        return text

    def load(self) -> List[Document]:
        """Load webpage."""
        soup = self.scrape()

        title_tags = soup.find_all("h1")
        if title_tags:
            title = ", ".join([tag.get_text() for tag in title_tags])
        else:
            print(self.web_path)
            raise ValueError("Title tag not found.")

        documents = []

        method_tags = soup.find_all("dl", class_="method")
        for method_tag in method_tags:
            area = self.web_path.split("/")[5]
            tech = self.web_path.split("/")[6]
            method_signature = method_tag.find("dt").get_text()
            method_description = method_tag.find("dd").get_text()

            metadata_methods = {
                "title": title,
                "source": self.web_path,
                "area": area,
                "tech": tech,
                "class": title,
                "method": method_signature.split("(")[0].replace("\n", ""),
            }

            content = method_signature + "\n" + method_description

            document = Document(page_content=content, metadata=metadata_methods)
            documents.append(document)

        """Embeddings for classes"""
        class_tags = soup.find_all("dl", class_="class")
        for class_tag in class_tags:
            area = self.web_path.split("/")[5]
            tech = self.web_path.split("/")[6]

            class_full_tag = class_tag.find("dd")
            all_tags = class_full_tag.find_all("dl")

            method_tags = [tag for tag in all_tags if "method" in tag["class"]]

            for method_tag in method_tags:
                method_tag.decompose()

            class_signature = class_tag.find("dt").get_text()
            class_description = " ".join([all_tag.get_text() for all_tag in all_tags])

            content = class_signature + "\n" + class_description

            metadata_class = {
                "title": title,
                "source": self.web_path,
                "area": area,
                "tech": tech,
                "class": title,
            }

            document = Document(page_content=content, metadata=metadata_class)
            documents.append(document)

        """Embeddings for normal text"""
        article_tag = soup.find("article")
        all_tags = article_tag.find_all("dl")

        class_tags = [tag for tag in all_tags if "class" in tag["class"]]

        for class_tag in class_tags:
            class_tag.decompose()

        content = DefichainPythonLoader.replace_enter(article_tag.get_text())

        metadata_class = {
            "title": title,
            "source": self.web_path,
        }

        document = Document(page_content=content, metadata=metadata_class)
        documents.append(document)
        return documents


if __name__ == "__main__":
    loader = DefichainPythonLoader(
        "https://docs.defichain-python.de/build/html/guides/example/chainedTransactions.html"
    )
    docs = loader.load()
    for doc in docs:
        print("Source:", doc.metadata["source"])
        print("Title:", doc.metadata["title"])
        print("Content:", doc.page_content)
