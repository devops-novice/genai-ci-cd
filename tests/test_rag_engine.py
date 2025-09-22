from app.rag_engine import RAGEngine


def test_basic_query_contract():
    """Engine should return a valid RAGResponse with required fields populated."""
    engine = RAGEngine()
    result = engine.query("What is SimpleDirectoryReader?")

    # Contract: answer is a string
    assert isinstance(result.answer, str)
    assert len(result.answer) > 0

    # Contract: sources is a list of strings
    assert isinstance(result.sources, list)
    if result.sources:
        assert all(isinstance(s, str) for s in result.sources)

    # Contract: chunks is a list of strings
    assert isinstance(result.chunks, list)
    if result.chunks:
        assert all(isinstance(c, str) for c in result.chunks)


def test_query_different_prompt_contract():
    """Another query should also satisfy the same response contract."""
    engine = RAGEngine()
    result = engine.query("Explain precision@k vs recall@k")

    assert isinstance(result.answer, str)
    assert len(result.answer) > 0

    assert isinstance(result.sources, list)
    if result.sources:
        assert all(isinstance(s, str) for s in result.sources)

    assert isinstance(result.chunks, list)
    if result.chunks:
        assert all(isinstance(c, str) for c in result.chunks)

