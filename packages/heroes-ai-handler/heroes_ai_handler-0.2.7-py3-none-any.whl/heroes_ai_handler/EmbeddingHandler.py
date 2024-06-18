import json
import requests
import weaviate
import tiktoken
from langchain.text_splitter import TokenTextSplitter
import uuid

from .Logger import Logger
from .BlobConversionHandler import BlobConversionHandler
from .FileHandler import FileHandler
from .DatabaseHandler import DatabaseHandler
from .Utils import Utils


LOGGER = Logger(
    name='EmbeddingHandler',
    log_to_console=True,
)

UTILS = Utils()


class EmbeddingHandler:
    def __init__(
            self,
        ):
        self.AZURE_OPENAI_ENDPOINT = UTILS.get_env_variable('AZURE_OPENAI_ENDPOINT')
        self.AZURE_OPENAI_API_KEY = UTILS.get_env_variable('AZURE_OPENAI_API_KEY')
        self.AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME = UTILS.get_env_variable('AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME')
        self.AZURE_OPENAI_API_VERSION = UTILS.get_env_variable('AZURE_OPENAI_API_VERSION')

        self.WEVIATE_CLUSTER_ENDPOINT = UTILS.get_env_variable('WEVIATE_CLUSTER_ENDPOINT')
        self.WEVIATE_CLUSTER_API_KEY = UTILS.get_env_variable('WEVIATE_CLUSTER_API_KEY')

        self.connect_to_weaviate_client()


    def connect_to_weaviate_client(
            self,
        ):
        '''
        Make a conneciton to the Weaviate client.
        '''
        try:
            LOGGER.info('Connecting to Weaviate client')
            # Connect to a WCS instance
            self.client = weaviate.connect_to_wcs(
                cluster_url = self.WEVIATE_CLUSTER_ENDPOINT,
                auth_credentials = weaviate.auth.AuthApiKey(self.WEVIATE_CLUSTER_API_KEY)
            )

        except Exception as e:
            LOGGER.error(f'Failed: {e}')


    def generate_embedding(
            self, 
            text: str
        ):
        '''
        Generate embeddings for an input string using embeddings API
        '''
        try:
            LOGGER.info('Generating an embedding')
            url = f"{self.AZURE_OPENAI_ENDPOINT}/openai/deployments/{self.AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME}/embeddings?api-version={self.AZURE_OPENAI_API_VERSION}"

            headers = {
                "Content-Type": "application/json",
                "api-key": self.AZURE_OPENAI_API_KEY,
            }

            data = {"input": text}

            response = requests.post(url, headers=headers, data=json.dumps(data)).json()
            # return response

            embedding = response['data'][0]['embedding']
            return embedding

        except Exception as e:
            LOGGER.error(f'Failed: {e}')


    def count_tokens(
            self,
            text: str, 
            model_name: str  # ['text-embedding-ada-002', 'gpt-3.5-turbo']
        ) -> int:
        '''
        Computes the number of required tokens for an input text using tiktoken library.
        '''
        encoding = tiktoken.encoding_for_model(model_name)
        tokens = encoding.encode(text)
        return len(tokens)
    

    def count_words(
            self, 
            text: str,
        ) -> int:
        '''
        Counts the number of words in the input text.
        '''
        return len(text.split())
    

    def split_text_into_chunks(
            self,
            text: str,
            chunk_size: int = 500,
            chunk_overlap: int = 100
        ):
        '''
        Split a piece of text into chunks.
        '''
        text_splitter = TokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        text_splitted = text_splitter.split_text(text)
        return text_splitted


    def process_all_blobs_to_embeddings(
            self,
            table_name: str,
            collection_name: str,
            file_handler: FileHandler,
            database_handler: DatabaseHandler,
            blob_conversion_handler: BlobConversionHandler,
            truncate_database_table: bool = False,
        ):
        '''
        Convert all textfiles from a SQL table to embeddings (word vectors), and save the result
        in SQL database (text + location) + Weaviate database (vector)
        '''
        # Clear output table if desired
        if truncate_database_table:
            database_handler.truncate_table('Embeddings')

        query = f"SELECT * FROM {table_name}"
        data = database_handler.execute_query(query, fetch_results=True)
        data_filtered = [
            {
                'Id': item['Id'], 
                'LocationText': item['LocationText']
            } for item in data
        ]
        
        for blob_info in data_filtered:
            id = blob_info['Id']
            blob_name = blob_info['LocationText']

            arr_bytes = file_handler.get_blob_as_bytes(blob_name)
            text = blob_conversion_handler.get_text(blob_name, arr_bytes)
            chunks = self.split_text_into_chunks(text)

            for chunk_id, chunk_text in enumerate(chunks):
                embedding = self.generate_embedding(chunk_text)
                vector_id = uuid.uuid4()
                properties = {
                    'id_external': id,
                    'location_text': blob_name
                }

                # Upload embedding vector to weviate
                self.upload_to_weviate(
                    collection_name=collection_name,
                    properties=properties,
                    embedding=embedding,
                    vector_id=vector_id,
                )

                # Upload embedding text to sql databaee
                database_handler.upload_to_database_embeddings(
                    id=vector_id,
                    chunk_id=chunk_id,
                    chunk_text=chunk_text,
                    file_path_original_file=blob_name,
                )

    
    def upload_to_weviate(
            self,
            collection_name: str,
            properties: dict,
            embedding: list,
            vector_id: str = None,
        ):
        '''
        Upload a single object to a Weaviate collection.
        '''
        try:
            LOGGER.info('Uploading single entry to Weaviate collection')

            vector_id = uuid.uuid4() if not vector_id else vector_id

            collection_files = self.client.collections.get(collection_name)

            collection_files.data.insert(
                properties=properties,
                uuid=vector_id,
                vector=embedding,
            )

        except Exception as e:
            LOGGER.error(f'Failed: {e}')