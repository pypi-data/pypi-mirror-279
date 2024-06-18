import os
import uuid
from typing import List

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone

from memory.memory_base import MemoryBase

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_INDEX = os.environ.get('PINECONE_INDEX')
pc = Pinecone(api_key=PINECONE_API_KEY)
memory_index = pc.Index(PINECONE_INDEX)


class SemanticMemory(MemoryBase):

    def _embed_memory(self, mem_key):
        client = OpenAIEmbeddings(model="text-embedding-3-large")
        semantic_value = client.embed_query(mem_key)

        return semantic_value

    def retrieve_memory_item(self, mem_key: str, kwargs=None):
        semantic_mem_val = self._embed_memory(mem_key)
        memory_item = memory_index.query(vector=semantic_mem_val,top_k=1,include_metadata=True)

        return memory_item


    def add_memory_item(self, mem_key: str, mem_val: str):
        semantic_mem_val = self._embed_memory(mem_key)
        memory_item = {"key":mem_key,"value":mem_val}

        id = str(uuid.uuid4())

        vector = [{"id":id, "values":semantic_mem_val,"metadata":memory_item}]

        self._insert_to_mem_store(vector)

        return semantic_mem_val,memory_item

    def _insert_to_mem_store(self,vector:List):
        memory_index.upsert(vector)

    def clean_up_memory_item(self):
        pass
