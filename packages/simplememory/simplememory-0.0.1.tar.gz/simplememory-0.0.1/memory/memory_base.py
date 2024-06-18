from abc import abstractmethod

from pydantic.v1 import BaseModel


class MemoryBase(BaseModel):

    @abstractmethod
    def retrieve_memory_item(self,mem_key:str,kwargs=None):
        pass

    @abstractmethod
    def add_memory_item(self,mem_key:str,mem_val:str):
        pass

    def clean_up_memory(self):
        pass

