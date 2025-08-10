from app.eval_metrics import precision_at_k, recall_at_k, mrr, exact_match, f1_tokens

def test_metrics_basic():
    retrieved = ["a","b","c","d","e"]; relevant = ["b","e"]
    assert precision_at_k(retrieved, relevant, 3) == 1/3
    assert round(recall_at_k(retrieved, relevant, 5),3) == 1.0
    assert round(mrr(retrieved, relevant),3) == 0.5
    assert exact_match("Hello", "hello") is True
    assert 0.0 <= f1_tokens("a b c", "b c d") <= 1.0
