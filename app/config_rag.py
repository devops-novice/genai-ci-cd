from dataclasses import dataclass
from typing import Literal

@dataclass
class RAGConfig:
    index_mode: Literal["merged","per_doc"] = "per_doc"
    top_k: int = 6
    chunk_size: int = 800
    chunk_overlap: int = 120
    use_reranker: bool = True
    normalize_scores: bool = True
    fusion: Literal["rrf","weighted"] = "rrf"
