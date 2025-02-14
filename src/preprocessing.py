import nltk
from langchain_text_splitters import CharacterTextSplitter
from src.config import Config
from langchain_openai import OpenAIEmbeddings
from nltk.stem import PorterStemmer

nltk.download("punkt_tab")
nltk.download("stopwords")

# Langchain embeddings and splitter that will be use
embeddings = OpenAIEmbeddings(
    api_key=Config.OPENAI_API_KEY, model="text-embedding-3-small"
)

splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

porter_stem = PorterStemmer()
