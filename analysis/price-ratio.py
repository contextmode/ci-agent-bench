#!/usr/bin/env python3
"""Cache write to cache read price ratio from the provider price page, for the models the lab uses.

Usage: python3 -I analysis/price-ratio.py [PRICE_PAGE.md]
Default input: confirm-1101/prices/anthropic-pricing-2026-11-01.md, a saved copy of
https://platform.claude.com/docs/en/about-claude/pricing.md (read 2026-11-01). To use a fresh copy, save the page as markdown
and pass its path. Output: per model, the 5-minute and 1-hour write price over the read price, and the same in units of the
plain input price. No regex.
"""
import os, sys

LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = ("Claude Sonnet 5.5", "Claude Opus 5.5")


def dollars(cell):
    s = cell.strip().split("/")[0].strip()
    if not s.startswith("$"):
        return None
    s = s[1:].strip()
    return float(s.split("<")[0].strip())


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(LAB, "confirm-1101/prices/anthropic-pricing-2026-11-01.md")
    rows = {}
    for line in open(path):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 6 and cells[0] in MODELS:
            rows[cells[0]] = [dollars(c) for c in cells[1:6]]
    print("model | input | 5m write | 1h write | read | 5m write / read | 1h write / read | read in input units")
    for m in MODELS:
        i, w5, w1, rd, _ = rows[m]
        print(f"{m} | ${i:g} | ${w5:g} | ${w1:g} | ${rd:g} | {w5 / rd:.0f} to 1 | {w1 / rd:.0f} to 1 | {rd / i:.2f}")
        # Break-even for cutting n tokens inside a cached prefix of P tokens, with the cache broken at the cut:
        # extra write cost per token of P = write - read; saving per removed token per later turn = read.
        print(f"  break-even, 5m: n x later turns > {(w5 - rd) / rd:.0f} x P; 1h: n x later turns > {(w1 - rd) / rd:.0f} x P")


main()
