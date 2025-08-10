from app.retrieval import retrieve_topk

q = "What is the grace period for late EMI?"
rs = retrieve_topk(q, k=5, cfg={"index_path":"faiss_index"})
print("\nTOP-K retrieved:")
for i, r in enumerate(rs, 1):
    print(f"{i:>2}. id={r['id']}  source={r.get('source','?')}\n    {r['text'][:120]}...\n")
