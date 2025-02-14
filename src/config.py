import os
from dotenv import load_dotenv

# loading the env file
load_dotenv()


class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2") or "true"
    MODEL_NAME = os.getenv("MODEL_NAME")
    DATABSE_URL = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL")
    PINECONE_INDEX_NAME = "colabi"
    AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")
    # MONGODB_URL = os.getenv("MONGODB_URL")
    # MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")
    # MONGODB_COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME")
    MYSQL_HOST_NAME = os.getenv("MYSQL_HOST_NAME")
    MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
    ZAPIER_NLA_API_KEY = os.getenv("ZAPIER_NLA_API_KEY")
    EXPOSED_ACTION_URL = os.getenv("EXPOSED_ACTION_URL")
    CRYPTO_SALT = os.getenv("CRYPTO_SALT")
    CRYPTO_SECRET_KEY = os.getenv("CRYPTO_SECRET_KEY")
    SUPPORTED_FILE_TYPES = {"csv", "pdf", "txt", "json"}
    BASE_URL = os.getenv("BASE_URL")

    # Additional API Keys
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    LANGTRACE_API_KEY = os.getenv("LANGTRACE_API_KEY")
    EXA_API_KEY = os.getenv("EXA_API_KEY")
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
    OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
    REDIT_CLIENT_ID = os.getenv("REDIT_CLIENT_ID")
    REDIT_SECRET_KEY = os.getenv("REDIT_SECRET_KEY")

    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
    S3_REGION_NAME = os.getenv("S3_REGION_NAME")
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
