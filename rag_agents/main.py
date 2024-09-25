import os
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")
os.environ["HF_HOME"] = "/mnt/home/cached/"
os.environ["TORCH_HOME"] = "/mnt/home/cached/"
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.faiss import DistanceStrategy
from langchain.document_loaders import HuggingFaceDatasetLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document


def main():
    # Specify the document
    data = [
        Document(page_content="Why do we dream?"),
        Document(page_content="The universe is vast and mysterious."),
        Document(page_content="Quantum physics challenges our perception of reality."),
        Document(page_content="Artificial intelligence is transforming the world."),
        Document(page_content="Human emotions are complex and fascinating."),
        Document(page_content="Space exploration fuels our curiosity."),
        Document(page_content="Nature's beauty is unparalleled."),
        Document(page_content="Innovation drives human progress."),
        Document(
            page_content="AI is expected to automate routine tasks, potentially displacing some jobs while creating new ones in tech."
        ),
        Document(
            page_content="The future job market will likely require skills in AI management, data analysis, and cyber-physical systems."
        ),
    ]
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from transformers import pipeline
    tokenizer = AutoTokenizer.from_pretrained("SweatyCrayfish/llama-3-8b-quantized")

    model_4bit = AutoModelForCausalLM.from_pretrained("SweatyCrayfish/llama-3-8b-quantized", device_map="auto", load_in_4bit=True)

    

    generator = pipeline(task="text-generation", model=model_4bit, tokenizer=tokenizer)
    generator("Three Rings for the Elven-kings under the sky")

    print(f"Chunking a list of {len(data)} documents.")

    # It splits text into chunks of 1000 characters each with a 150-character overlap.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(data)

    print(docs[0])

    # Define the path to the pre-trained model you want to use
    modelPath = "sentence-transformers/all-MiniLM-l6-v2"

    # Initialize an instance of HuggingFaceEmbeddings with the specified parameters
    embeddings = HuggingFaceEmbeddings(
        model_name=modelPath,  # Provide the pre-trained model's path
        model_kwargs={"device": "cpu"},  # Pass the model configuration options
        encode_kwargs={"normalize_embeddings": True},  # Pass the encoding options
    )

    # Create an instance of the FAISS class with the documents and embeddings
    db = FAISS.from_documents(
        docs, embeddings, distance_strategy=DistanceStrategy.COSINE
    )

    question = "What is AI?"
    doc_list = db.similarity_search_with_relevance_scores(question)
    # Display results with similarity scores
    print(f"Query: {question}\n")
    for i, doc in enumerate(doc_list):
        print(f"Chunk {i+1}: {doc[0].page_content}\nScore: {doc[1]:.2f}\n")

    print("Good")


if __name__ == "__main__":
    main()
