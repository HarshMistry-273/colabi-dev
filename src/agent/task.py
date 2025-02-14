from src.celery import celery_app
from src.utils.logger import logger_set
from src.utils.pinecone import PineConeConfig


@celery_app.task()
def embedding_docs(api_key: str, index_name:str, namespace:str, url: str, url_file_type:str):
    """
    Embeds documents into a Pinecone index.

    Args:
        api_key (str): The API key for accessing the Pinecone service.
        index_name (str): The name of the Pinecone index where documents will be embedded.
        namespace (str): The namespace for organizing the embedded documents.
        file_path (str): The path to the file containing the documents to embed.
        file_type (str): The type of the file (e.g., 'txt', 'pdf').

    Returns:
        str: A confirmation message indicating successful embedding.

    Notes:
        This function uses the PineConeConfig to configure the embedding process
        and is designed to be run as a Celery task for asynchronous processing.
    """
    try:
        pc = PineConeConfig(
            api_key=api_key,
            index_name=index_name,
            namespace=namespace,
            url="/app/external_upload/"+url.rsplit("/")[-1],
            url_file_type=url_file_type,
        )
        pc.add_documents()
        logger_set.info(
            f"Document embedded successfully. Namespace (vector_id): {namespace}"
        )
        return f"Document embedded successfully. Namespace: {namespace}"
    except Exception as e:
        logger_set.info(
            f"Document embedding failed. Namespace (vector_id): {namespace}"
        )
        return f"Document embedding failed. Namespace: {namespace}"
