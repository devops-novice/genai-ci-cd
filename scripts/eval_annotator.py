import json
import os
import glob

LOG_FOLDER = "logs"

def load_jsonl(file_path):
    with open(file_path, "r") as f:
        return [json.loads(line) for line in f]

def save_jsonl(file_path, logs):
    with open(file_path, "w") as f:
        for entry in logs:
            f.write(json.dumps(entry) + "\n")

def annotate_logs(logs):
    updated = 0
    for entry in logs:
        if "was_correct" in entry and "hallucinated" in entry:
            continue  # already annotated

        print("\n" + "="*80)
        print(f"🧠 Query: {entry.get('query')}")
        print(f"\n💬 Answer:\n{entry.get('answer')}")
        print("\n📄 Sources:")
        for src in entry.get("sources", []):
            print(f"  - {src}")

        was_correct = input("✅ Was the answer correct? (y/n): ").strip().lower() == "y"
        hallucinated = input("❌ Did it hallucinate? (y/n): ").strip().lower() == "y"
        comment = input("📝 Any comments? (optional): ").strip()

        entry["was_correct"] = was_correct
        entry["hallucinated"] = hallucinated
        entry["comment"] = comment
        updated += 1

    print(f"\n✅ Annotated {updated} new entries.")
    return logs

def main():
    jsonl_files = glob.glob(os.path.join(LOG_FOLDER, "*.jsonl"))
    if not jsonl_files:
        print("⚠️  No JSONL log files found in the logs/ folder.")
        return

    for file_path in jsonl_files:
        print(f"\n📂 Processing file: {file_path}")
        logs = load_jsonl(file_path)
        updated_logs = annotate_logs(logs)
        save_jsonl(file_path, updated_logs)

    print("\n🏁 All log files processed.")

if __name__ == "__main__":
    main()
