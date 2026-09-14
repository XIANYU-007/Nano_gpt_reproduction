from pathlib import Path
import json

from datasets import load_dataset

output_dir = Path("data/tinystories")
output_dir.mkdir(parents=True, exist_ok=True)

for split, limit in [("train", 10000), ("validation", 1000)]:
    dataset = load_dataset(
        "roneneldan/TinyStories",
        split=split,
        streaming=True,
    )

    output_path = output_dir / f"{split}.jsonl"

    with output_path.open("w", encoding="utf-8") as file:
        for example in dataset.take(limit):
            record = {"text": example["text"]}
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Saved {output_path}")