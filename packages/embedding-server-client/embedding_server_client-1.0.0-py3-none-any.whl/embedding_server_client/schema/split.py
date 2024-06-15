from dataclasses import dataclass
from typing import Optional, List

from embedding_server_client.schema.base import Base


@dataclass
class Split(Base):
    """
    Dataclass representing a Split response.
    """
    split_id: int
    sequence_id: int
    doc_id: int
    text_content: str
    token_len: int
    tokens: Optional[List[int]]
