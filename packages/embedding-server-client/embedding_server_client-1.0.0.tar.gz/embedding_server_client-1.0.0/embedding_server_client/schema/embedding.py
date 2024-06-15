from typing import List
from dataclasses import dataclass


@dataclass
class Embedding:
    object: str
    index: int
    embedding: List[float]


@dataclass
class EmbeddingUsage:
    prompt_tokens: int
    total_tokens: int
