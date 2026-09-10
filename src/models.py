from pydantic import BaseModel, Field
from typing import List


class TableData(BaseModel):
    page_number: int
    content: str


class ImageData(BaseModel):
    page_number: int
    image_base64: str
    image_format: str
    description: str = ""


class PageData(BaseModel):
    page_number: int
    text: str
    tables: List[TableData] = Field(default_factory=list)
    images: List[ImageData] = Field(default_factory=list)


class DocumentData(BaseModel):
    source_file: str
    file_type: str
    pages: List[PageData] = Field(default_factory=list)
    

class ChunkData(BaseModel):
    chunk_id: str
    source_file: str
    file_type: str
    page_number: int
    content_type: str
    content: str