"""Export real executed notebook outputs as compact HTML evidence.

Run with the lab Python; capture the HTML in a browser for submission PNGs.
No numbers are retyped or generated: each block comes from a saved output cell.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def export() -> None:
    dest = ROOT / "submission" / "screenshots"
    dest.mkdir(parents=True, exist_ok=True)
    for path in sorted((ROOT / "notebooks").glob("[0-9]*.ipynb")):
        notebook = json.loads(path.read_text())
        blocks = []
        for cell in notebook["cells"]:
            if cell["cell_type"] != "code":
                continue
            if cell.get("execution_count") is None:
                raise ValueError(f"Unexecuted cell in {path.name}")
            texts = []
            for out in cell.get("outputs", []):
                if out["output_type"] == "error":
                    raise ValueError(f"Notebook error in {path.name}")
                if out["output_type"] == "stream" and out.get("name") == "stdout":
                    texts.append("".join(out["text"]))
                elif out["output_type"] in ("execute_result", "display_data"):
                    texts.append("".join(out.get("data", {}).get("text/plain", [])))
            text = ANSI.sub("", "".join(texts)).strip()
            if text:
                blocks.append(f'<section><h2>Output [{cell["execution_count"]}]</h2>'
                              f'<pre>{html.escape(text)}</pre></section>')
        title = path.stem.replace("_", " ")
        document = f'''<!doctype html><html lang="vi"><meta charset="utf-8">
<title>{title}</title><style>
body{{margin:0;padding:32px;background:#fff;color:#17212b;font:16px sans-serif}}
h1{{font-size:24px}}h2{{font-size:14px;color:#526170;margin:0 0 12px}}
section{{border-top:1px solid #cbd2d9;padding:18px 0}}
pre{{font:14px/1.5 monospace;white-space:pre-wrap;overflow-wrap:anywhere;margin:0}}
.source{{color:#526170;font-size:13px;margin-bottom:28px}}
</style><h1>Lab 19 · {title}</h1>
<p class="source">Actual saved outputs: notebooks/{path.name}. Lite / CPU.<br>
Browser capture of exported notebook outputs; stderr warnings omitted.</p>
{''.join(blocks)}</html>'''
        output = dest / f"{path.stem}.html"
        output.write_text(document, encoding="utf-8")
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    export()
