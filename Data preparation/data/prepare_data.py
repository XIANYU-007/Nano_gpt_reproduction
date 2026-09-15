import json
from pathlib import Path

import numpy as np
import tiktoken


def load_tokens(path, max_stories, tokenizer):
    """Yield token IDs one story at a time, including each story's end token."""
    with open(path, "r", encoding="UTF-8") as f:
        for i, text in enumerate(f):
            if i >= max_stories:
                break
            yield from tokenizer.encode_ordinary(json.loads(text)["text"])
            yield tokenizer.eot_token


def save_tokens(tokens, output_path, single_round_capacity):
    """Write a token iterator as uint16, keeping at most one output buffer."""
    if single_round_capacity <= 0:
        raise ValueError("single_round_capacity must be positive")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    buffer = np.empty(single_round_capacity, dtype=np.uint16)
    used = 0
    total_tokens = 0
    with output_path.open("wb") as f:
        for token in tokens:
            buffer[used] = token
            used += 1
            total_tokens += 1
            if used == single_round_capacity:
                buffer.tofile(f)
                used = 0
        # The final buffer may contain fewer tokens than its capacity.
        if used:
            buffer[:used].tofile(f)
    return total_tokens


def main(max_stories=50000, single_round_capacity=10000):
    tokenizer = tiktoken.get_encoding("gpt2")
    parent_path = Path(__file__).resolve().parent
    for split in ["train", "validation"]:
        output_path = parent_path / "tinystories" / "processed" / f"{split}.bin"
        load_path = parent_path / "tinystories" / "raw" / f"{split}.jsonl"
        tokens = load_tokens(load_path, max_stories, tokenizer)
        total_tokens = save_tokens(tokens, output_path, single_round_capacity)
        print(f"{split}: saved {total_tokens} tokens to {output_path}")


if __name__ == "__main__":
    main()
