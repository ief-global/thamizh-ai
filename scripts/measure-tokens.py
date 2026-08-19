#!/usr/bin/env python3
"""Measure how English-trained tokenizers fragment Tamil words.

Writes src/data/tokenization.json. Run it rather than editing that file by hand,
and update `measured_on` when you do.

    uv run --with tiktoken python scripts/measure-tokens.py

Every Tamil form below also appears in the design repo, verified against the live
build. Do not add a form that has not been checked there.
"""
import json
import pathlib

import tiktoken

WORDS = [
    # tamil, english gloss, morpheme count (None where our own docs do not state one)
    ("மரம்", "tree", 1),
    ("மரத்தில்", "in the tree", 3),
    ("வந்தான்", "he came", 3),
    ("வருகிறான்", "he is coming", 3),
    ("கொடுத்தான்", "he gave", 3),
    ("படித்துக்கொண்டிருந்தார்கள்", "they were reading", None),
]

def main() -> None:
    cl = tiktoken.get_encoding("cl100k_base")
    o2 = tiktoken.get_encoding("o200k_base")
    rows = [
        {
            "tamil": ta, "english": en, "morphemes": m, "chars": len(ta),
            "cl100k": len(cl.encode(ta)), "o200k": len(o2.encode(ta)),
            "en_o200k": len(o2.encode(en)),
        }
        for ta, en, m in WORDS
    ]
    out = pathlib.Path(__file__).parent.parent / "src" / "data" / "tokenization.json"
    doc = json.loads(out.read_text(encoding="utf-8"))
    doc["tool"] = f"tiktoken {tiktoken.__version__}"
    doc["rows"] = rows
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for r in rows:
        print(f"{r['tamil']:<28} cl100k {r['cl100k']:>3}   o200k {r['o200k']:>3}   en {r['en_o200k']:>3}")

if __name__ == "__main__":
    main()
