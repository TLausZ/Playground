#!/usr/bin/env python3
"""Compute Collatz sequences for 1..N and write them as CSV.

Usage:
    python3 scripts/generate_data.py [N]     # N defaults to 1000

Writes data/collatz.csv and re-embeds that CSV into the standalone index.html
so the double-click (file://) page keeps working after you change the range.
The fetch-based page (index-csv.html) reads data/collatz.csv directly and
needs no embedding.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "collatz.csv"
STANDALONE = ROOT / "index.html"
BLOCK = re.compile(r'(<script id="csvdata" type="text/csv">).*?(</script>)', re.S)


def collatz(n: int) -> list[int]:
    seq = [n]
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        seq.append(n)
    return seq


def build_csv(N: int) -> str:
    rows = ["n,steps,max,sequence"]
    for n in range(1, N + 1):
        s = collatz(n)
        rows.append(f'{n},{len(s) - 1},{max(s)},"{",".join(map(str, s))}"')
    return "\n".join(rows) + "\n"


def embed(csv_text: str) -> None:
    html = STANDALONE.read_text()
    if not BLOCK.search(html):
        print(f"note: no csvdata block in {STANDALONE.name}, skipped embedding")
        return
    html = BLOCK.sub(lambda m: f"{m.group(1)}\n{csv_text.strip()}\n{m.group(2)}", html)
    STANDALONE.write_text(html)


def main() -> None:
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    if N < 1:
        sys.exit("N must be >= 1")
    csv_text = build_csv(N)
    CSV.write_text(csv_text)
    embed(csv_text)
    print(f"wrote {CSV.relative_to(ROOT)} (1..{N}) and re-embedded it into {STANDALONE.name}")


if __name__ == "__main__":
    assert collatz(6) == [6, 3, 10, 5, 16, 8, 4, 2, 1]
    assert collatz(1) == [1]
    main()
