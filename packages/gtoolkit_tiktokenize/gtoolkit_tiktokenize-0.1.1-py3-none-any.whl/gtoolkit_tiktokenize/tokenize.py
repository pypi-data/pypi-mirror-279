import tiktoken

from dataclasses import dataclass
from gtoolkit_bridge import gtView


@dataclass
class Token:
    name: str
    num: int
    start: int
    end: int


class TokenizerResult:
    def __init__(self, tokens):
        self.tokens = tokens

    @gtView
    def gtViewTokens(self, view):
        clist = view.columnedList()
        clist.title("Tokens")
        clist.priority(2)
        clist.items(lambda: self.tokens)
        clist.column("Name", lambda each: each.name)
        clist.column("Byte", lambda each: each.num)
        clist.column("Start", lambda each: each.start)
        clist.column("End", lambda each: each.end)
        return clist


def tokenize(string, model):
    encoding = tiktoken.encoding_for_model(model)
    encoding = tiktoken.Encoding(
        name="gt_extended",
        pat_str=encoding._pat_str,
        mergeable_ranks=encoding._mergeable_ranks,
        special_tokens={
            **encoding._special_tokens,
            "<|im_start|>": 100264,
            "<|im_end|>": 100265,
            "<|im_sep|>": 100266,
        },
    )

    encoded = encoding.encode(string, allowed_special="all")
    start_range = 0
    tokens = []
    for b in encoded:
        decoded = str(encoding.decode_single_token_bytes(b), encoding="utf-8")
        end_range = start_range + len(decoded)
        tokens.append(Token(decoded, b, start_range + 1, end_range))
        start_range = end_range
    return TokenizerResult(tokens)
