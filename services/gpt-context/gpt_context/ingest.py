import os
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader, PDFMinerLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings

from gpt_context.adapters import WeaviateVectorStoreAdapter

load_dotenv()


def main():
    if os.environ.get("OPENAI_API_KEY") is None:
        print("OpenAI API key not set")
        return None

    weaviate_url = os.environ.get("WEAVIATE_URL") or "http://localhost:8080"

    loader = None

    for root, dirs, files in os.walk("source_documents"):
        if not files:
            print(f"The directory '{root}' is empty.")
            continue

        for file in files:
            ext = os.path.splitext(file)[-1].lower()

            match ext:
                case ".txt":
                    loader = TextLoader(os.path.join(root, file), encoding="utf8")
                case ".pdf":
                    loader = PDFMinerLoader(os.path.join(root, file))
                case ".csv":
                    loader = CSVLoader(os.path.join(root, file))

    if loader is None:
        print("No loader found")
        return None

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    embedding = OpenAIEmbeddings()

    vector_store = WeaviateVectorStoreAdapter(weaviate_url, embedding=embedding)
    vector_store.from_documents(texts, embedding)

    print("All files loaded")


if __name__ == "__main__":
    main()
