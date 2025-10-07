# scripts/embed_and_store.py
# Run from repo root:
#   python3 -m scripts.embed_and_store --manifest docs/manifest.json

from __future__ import annotations
import json
import shutil
from pathlib import Path
from collections import defaultdict
from typing import List, Dict

# If you sometimes run this directly (not with -m), uncomment below:
# import os, sys
# ROOT = Path(__file__).resolve().parent.parent
# if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

# LangChain Document (handle both new/old imports)
try:
    from langchain_core.documents import Document
except Exception:
    from langchain.docstore.document import Document  # older LC

from app.config_rag import RAGConfig
from app.embedding_utils import create_and_save_faiss_index

CFG = RAGConfig()

# ---------- chunking & conversion ----------

def split_text(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    parts, start, n = [], 0, len(text)
    while start < n:
        end = min(start + chunk_size, n)
        parts.append(text[start:end])
        if end == n:
            break
        start = max(0, end - chunk_overlap)
    return parts

def make_chunks(doc_id: str, text: str, title: str, source_path: str, cfg: RAGConfig) -> List[Dict]:
    chunks: List[Dict] = []
    for i, p in enumerate(split_text(text, cfg.chunk_size, cfg.chunk_overlap)):
        chunks.append({
            "doc_id": doc_id,
            "chunk_id": f"{doc_id}_{i:04d}",
            "text": p,
            "meta": {"title": title, "source_path": source_path},
        })
    return chunks

def to_documents(chunks: List[Dict]) -> List[Document]:
    docs: List[Document] = []
    for ch in chunks:
        meta = ch.get("meta", {})
        docs.append(
            Document(
                page_content=ch["text"],
                metadata={
                    "source": meta.get("source_path") or ch["doc_id"],
                    "doc_id": ch["doc_id"],
                    "chunk_id": ch["chunk_id"],
                    "title": meta.get("title") or ch["doc_id"],
                },
            )
        )
    return docs

# ---------- IO helpers ----------

def load_manifest(path: str) -> List[Dict]:
    """
    Manifest JSON format:
    [
      {"doc_id":"chaos","title":"Chaos Guide","source_path":"docs/chaos.md"},
      {"doc_id":"sre","title":"SRE Assessment","source_path":"docs/sre.md"},
      {"doc_id":"ospo","title":"OSPO Policy","source_path":"docs/ospo.md"}
    ]
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Manifest not found: {p}")
    return json.loads(p.read_text(encoding="utf-8"))

def ingest_manifest(manifest_path: str) -> List[Dict]:
    items = load_manifest(manifest_path)
    all_chunks: List[Dict] = []
    for it in items:
        doc_id = it["doc_id"]
        title = it.get("title", doc_id)
        src = it["source_path"]
        text = Path(src).read_text(encoding="utf-8")
        all_chunks.extend(make_chunks(doc_id, text, title, src, CFG))
    return all_chunks

# ---------- writers (uses rename-after-write pattern) ----------

def write_per_doc(chunks: List[Dict]) -> None:
    per_dir = Path("faiss_index/per_doc")
    per_dir.mkdir(parents=True, exist_ok=True)

    tmp_faiss = Path("faiss_index/index.faiss")
    tmp_meta  = Path("faiss_index/index.pkl")

    by_doc: Dict[str, List[Dict]] = defaultdict(list)
    for ch in chunks:
        by_doc[ch["doc_id"]].append(ch)

    for doc_id, doc_chunks in by_doc.items():
        # clear temp outputs if present
        if tmp_faiss.exists(): tmp_faiss.unlink()
        if tmp_meta.exists():  tmp_meta.unlink()

        # write via existing helper (outputs to faiss_index/index.*)
        create_and_save_faiss_index(to_documents(doc_chunks))

        # move to per_doc/<doc_id>.*
        dest_faiss = per_dir / f"{doc_id}.faiss"
        dest_meta  = per_dir / f"{doc_id}.pkl"
        if dest_faiss.exists(): dest_faiss.unlink()
        if dest_meta.exists():  dest_meta.unlink()

        shutil.move(str(tmp_faiss), str(dest_faiss))
        shutil.move(str(tmp_meta),  str(dest_meta))
        print(f"✅ per-doc index: {dest_faiss}  ({len(doc_chunks)} chunks)")

def write_merged(chunks: List[Dict]) -> None:
    create_and_save_faiss_index(to_documents(chunks))  # leaves faiss_index/index.*
    print(f"✅ merged index: faiss_index/index.faiss  ({len(chunks)} chunks)")

# ---------- CLI ----------

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, help="Path to JSON manifest (see function docstring)")
    args = ap.parse_args()

    chunks = ingest_manifest(args.manifest)
    if not chunks:
        print("⚠️  No chunks produced from manifest.")
        raise SystemExit(0)

    write_per_doc(chunks)
    write_merged(chunks)

    print("🎯 Done: per-doc and merged FAISS indexes are ready.")
