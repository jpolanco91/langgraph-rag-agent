from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from .config import (
	VECTOR_DB_URI,
	VECTOR_INDEX_PARAMS,
	VECTOR_CONSISTENCY_LEVEL
)
from dotenv import load_dotenv
import os
import sys

load_dotenv()

cwd = os.getcwd()
milvus_path = f"{cwd}/vectorstores"
sys.path.insert(1, milvus_path)

from vectorstores.MilvusVectorStore import MilvusVectorStore

# MilvusDB rest of the code.
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
pdf_file = "Stock_Market_Performance_2024.pdf"
pdf_path = f"{cwd}/{pdf_file}"
pdf_loader = PyPDFLoader(pdf_path) # This loads the PDF

# Checks if the PDF is there
pages = None
try:
	pages = pdf_loader.load()
	print(f"::PDF has been loaded and has {len(pages)} pages::")
except Exception as e:
	print(f"::Error loading PDF: {e}::")

text_splitter = RecursiveCharacterTextSplitter(
	chunk_size=1000,
	chunk_overlap=200
)
pages_split = text_splitter.split_documents(pages)

milvus_vectorstore = MilvusVectorStore(
	VECTOR_DB_URI,
	VECTOR_INDEX_PARAMS,
	pages_split,
	embeddings,
	VECTOR_CONSISTENCY_LEVEL,
	False
)

token = f"{os.getenv('MILVUS_DB_USER')}:{os.getenv('MILVUS_DB_PASS')}"

milvus_vectorstore.create_db("stock_market_performance_db")
milvus_vectorstore.create_vector_store_from_db(token, "stock_market_performance_db")

retriever = milvus_vectorstore.get_retriever()

@tool
def retriever_tool(query : str) -> str:
	"""
	This tool searches and returns the information from the Stock Market Performance 2024 Document
	"""
	docs = retriever.invoke(query)

	if not docs:
		return "I found no relevant information in the Stock Market Performance 2024 document"

	results = []

	for i, doc in enumerate(docs):
		results.append(f"Document {i+1}:\n{doc.page_content}")

	return "\n\n".join(results)
