"""Minimal frontmatter read/write for brain notes (flat `key: value`, inline `[a, b]` lists).

ponytail: no PyYAML so the cloud routine needs no installs; switch to yaml if frontmatter ever nests.
"""
import re

FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def parse(text):
    m = FM.match(text)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "#")):
            continue
        k, v = line.split(":", 1)
        v = v.split(" #")[0].strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip().strip("\"'") for x in v[1:-1].split(",") if x.strip()]
        out[k.strip()] = v
    return out


def set_field(text, key, value):
    """Replace (or add) a scalar field inside the frontmatter only."""
    m = FM.match(text)
    if not m:
        return text
    block = m.group(1)
    line = f"{key}: {value}"
    if re.search(rf"^{key}:.*$", block, re.M):
        block = re.sub(rf"^{key}:.*$", line, block, count=1, flags=re.M)
    else:
        block += "\n" + line
    return f"---\n{block}\n---\n" + text[m.end():]
