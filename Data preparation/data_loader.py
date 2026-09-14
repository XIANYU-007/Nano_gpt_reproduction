import json
import tiktoken
import torch


tokenizer = tiktoken.get_encoding("gpt2")






def load_tokens(path, max_stories=3):
    tokens = []
    with open(path, encoding="UTF-8") as f:
        for i,story in enumerate (f):
            if i > max_stories - 1:
                break
            text_dic = json.loads(story)
            tokens.extend(tokenizer.encode_ordinary(text_dic["text"]))
            tokens.append(tokenizer.eot_token)
    return torch.tensor(tokens, dtype=torch.long)


def get_batch(tokens, B=3, T=5):
    if len(tokens) < T+1:
        raise ValueError("tokens are not enough!")
    #sample the start
    start = torch.randint(0,len(tokens)-T,(B,))
    #get sequences and stack them together
    x = torch.stack([tokens[s:s+T] for s in start])
    y = torch.stack([tokens[s+1:s+T+1] for s in start])
    return x,y

path = "/home/24041528r/Keep_moving_forward/coding playground/Data preparation/data/tinystories/train.jsonl"

tokens = load_tokens(path, max_stories=1000000)
x,y = get_batch(tokens, B=3, T=5)
print(x)
print(y)