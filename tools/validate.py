#!/usr/bin/env python3
"""Read-only consistency checks (same checks used in the 2026-11-13 audit). Never writes anything.
Usage: python tools/validate.py <folder with phrases.json usage.json state.json days/*.json>
       (names also accepted: bank-phrases.json, bank-usage.json, story-state.json)
Exit code 1 if any ERROR is found."""
import json, re, sys, glob, os, collections
d = sys.argv[1] if len(sys.argv) > 1 else "seed"
errs, warns = [], []
def load(*names):
    for n in names:
        p = os.path.join(d, n)
        if os.path.exists(p):
            x = json.load(open(p, encoding="utf8")); return x.get("data", x) if isinstance(x, dict) and "id" in x and "data" in x else x
def E(m): errs.append(m)
def W(m): warns.append(m)
DATE = re.compile(r"\d{4}-\d\d-\d\d")
ph = load("phrases.json", "bank-phrases.json"); us = load("usage.json", "bank-usage.json"); st = load("state.json", "story-state.json")
chunks = set()
if ph:
    rows, mast = ph.get("rows", []), ph.get("mastered", [])
    c = collections.Counter(r.get("chunk") for r in rows); chunks = set(c)
    for k, v in c.items():
        if v > 1: E(f"phrases: duplicate chunk {k!r}")
    for m in mast:
        if m.get("chunk") in c: E(f"phrases: {m['chunk']!r} is in both rows and mastered")
    for r in rows:
        miss = [k for k in ("date", "scene", "chunk", "zh", "ex", "level", "due") if k not in r]
        if miss: E(f"phrases: {r.get('chunk')!r} missing {miss}")
        if not DATE.fullmatch(str(r.get("due", ""))): E(f"phrases: bad due on {r.get('chunk')!r}")
        if not (isinstance(r.get("level"), int) and 0 <= r["level"] <= 4): E(f"phrases: bad level on {r.get('chunk')!r}")
    print(f"phrases: {len(rows)} rows, {len(mast)} mastered")
else: W("no phrases file found")
if us:
    for r in us.get("rows", []):
        if r.get("stage") not in ("1", "1 对比", "2", "3"): E(f"usage: bad stage on {r.get('group')!r}")
        if r.get("due") != "已掌握" and not DATE.fullmatch(str(r.get("due", ""))): E(f"usage: bad due on {r.get('group')!r}")
    print(f"usage: {len(us.get('rows', []))} rows")
norm = lambda s: re.sub(r"[?.…()✍️ ]+", " ", s.lower()).strip()
days = sorted(glob.glob(os.path.join(d, "days", "*.json")) + glob.glob(os.path.join(d, "*day*.json")))
for f in days:
    x = json.load(open(f, encoding="utf8")); x = x.get("data", x); tag = os.path.basename(f)
    cards = x.get("cards", []); keys = [c["key"] for c in cards]
    if len(keys) != len(set(keys)): E(f"{tag}: duplicate card keys")
    lv = [c["level"] for c in cards if c.get("kind") != "usage"]
    if lv != sorted(lv): E(f"{tag}: cards not ordered by level")
    for c in cards:
        if c.get("kind") == "usage": continue
        if chunks and c["chunk"] not in chunks: W(f"{tag}: card chunk {c['chunk']!r} not in phrase bank")
        if c.get("stage") == "gap" and "____" not in c["prompt"]: E(f"{tag}: gap card {c['key']} has no blank")
        if c.get("stage") == "use" and not c["prompt"].rstrip().endswith("→"): E(f"{tag}: use card {c['key']} prompt does not end with →")
    L = x.get("lesson", {})
    if [q["chunk"] for q in L.get("quick", [])] != [c["chunk"] for c in L.get("chunks", [])]: E(f"{tag}: lesson.quick order differs from lesson.chunks")
    allc = [norm(c["chunk"]) for c in L.get("chunks", [])] + [norm(c) for c in L.get("voice", {}).get("chunks", [])] + [norm(c["chunk"]) for c in cards if c.get("kind") != "usage"]
    for ln in L.get("dialogue", []):
        for b in re.findall(r"\*\*(.+?)\*\*", ln.get("line", "")):
            if not any(norm(b) in a or a in norm(b) for a in allc): E(f"{tag}: bold {b!r} matches no chunk")
    n = len(L.get("voice", {}).get("prompt", "").split())
    if n >= 220: E(f"{tag}: voice prompt has {n} words (limit < 220)")
    print(f"{tag}: {len(cards)} cards, voice prompt {n} words")
if st:
    t = json.dumps(st, ensure_ascii=False)
    left = re.findall(r"\{\{[^}]*\}\}", t)
    if left: W(f"state: {len(left)} unfilled placeholder(s), e.g. {left[0]}")
for w in warns: print("WARN ", w)
for e in errs: print("ERROR", e)
print("RESULT:", "FAIL" if errs else "OK", f"({len(errs)} errors, {len(warns)} warnings)")
sys.exit(1 if errs else 0)
