#!/usr/bin/env python3
"""Render app/index.template.html + config.json -> dist/index.html.

Only substitutes placeholders, escaping each value for HTML title or JS string use.
"""
import html
import json
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent
config_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / "config.example.json"
with config_path.open(encoding="utf-8") as config_file:
    cfg = json.load(config_file)
need = ("LEARNER", "ROLE", "GOAL", "LEVEL")
missing = [key for key in need if not isinstance(cfg.get(key), str) or not cfg[key].strip()]
if missing:
    sys.exit("config is missing or invalid: " + ", ".join(missing))

# All replacements except the <title> are inside double-quoted JS strings.
# json.dumps correctly escapes quotes, backslashes, newlines and control chars.
# Escaping <, >, & prevents input such as </script> from ending HTML script nodes.
def js_string_contents(value):
    encoded = json.dumps(value, ensure_ascii=True)[1:-1]
    return encoded.replace("<", r"\u003c").replace(">", r"\u003e").replace("&", r"\u0026")

page = (root / "app" / "index.template.html").read_text(encoding="utf-8")
page = re.sub(
    r"<title>(.*?)</title>",
    lambda match: "<title>" + match.group(1).replace("{{LEARNER}}", html.escape(cfg["LEARNER"])) + "</title>",
    page,
    count=1,
    flags=re.S,
)
for key in need:
    page = page.replace("{{" + key + "}}", js_string_contents(cfg[key]))
left = re.findall(r"\{\{[A-Z_]+\}\}", page)
if left:
    sys.exit("unreplaced placeholders: " + ", ".join(sorted(set(left))))
output = root / "dist"
output.mkdir(exist_ok=True)
(output / "index.html").write_text(page, encoding="utf-8")
print("wrote", output / "index.html", len(page), "chars")
