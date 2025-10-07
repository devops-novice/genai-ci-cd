class NoOpReranker:
    def rerank(self, query: str, candidates, k: int):
        return candidates[:k]
