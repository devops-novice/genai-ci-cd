from app.embedding_utils import load_and_split_markdown_files, create_and_save_faiss_index

chunks = load_and_split_markdown_files(docs_dir="docs")
if chunks:
    create_and_save_faiss_index(chunks)
else:
    print("⚠️ No markdown chunks found.")
