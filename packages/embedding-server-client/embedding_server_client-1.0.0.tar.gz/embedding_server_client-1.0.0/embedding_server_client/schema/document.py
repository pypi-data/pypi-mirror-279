from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Union, Dict, Any
from uuid import UUID

from embedding_server_client.schema import EmbeddingUsage, Embedding
from embedding_server_client.schema.base import Base
from embedding_server_client.schema.split import Split


class DocumentInsertionStatus(Enum):
    """
    Enum that represent the insertion status of the Document.
    """
    SUCCESS = 1
    ERROR = 2


@dataclass
class Document(Base):
    """
    Dataclass representing a Document response.
    """
    document_id: int
    document_url: str
    splits: List[Split]


@dataclass
class DocumentInsertionRequest(Base):
    """
    Dataclass representing a document insertion request.
    """
    input: Union[str, List[str]]
    model: str
    user: Optional[UUID] = field(default=None)
    doc_urls: Optional[List[str]] = field(default=None)
    verbose: Optional[bool] = field(default=False)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
        }


@dataclass
class DocumentInsertionResponse(Base):
    """
    Dataclass representing a document insertion response.
    """
    status: DocumentInsertionStatus
    documents: Optional[List[Document]] = field(default=None)
    embeddings: Optional[List[Embedding]] = field(default=None)
    usage: Optional[EmbeddingUsage] = field(default=None)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "status": DocumentInsertionStatus,
        }


@dataclass
class DocumentQueryRequest(Base):
    """
    Dataclass representing a document query request.
    """
    input: str
    model: str
    top_k: Optional[int] = field(default=5)
    encoding_format: Optional[str] = field(default="float")
    dimensions: Optional[int] = field(default=None)
    user: Optional[UUID] = field(default=None)

    @classmethod
    def decode_map(cls) -> Dict[str, Any]:
        return {
            "user": UUID,
        }


@dataclass
class DocumentQueryResponse(Base):
    """
    Dataclass representing a document query response.
    """
    object: str
    data: List[Split]
    model: Optional[str] = field(default=None)
    usage: Optional[EmbeddingUsage] = field(default=None)
