"""Generate the README annunciator panel (docs/assets/annunciator-{dark,light}.svg).

One window per scenario, one column per failure-mode family from docs/TAXONOMY.md,
lit with the verdicts in reports/demo-report.json. Spare windows fill the columns,
as on a real panel. The animation lights the windows in scenario order, the order
`scada-safetybench demo` scores them; with reduced motion the panel shows the final
state. Deterministic, no network. Re-run after changing scenarios or gates:

    python tools/make_panel.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "assets"

W, H = 1280, 464
LEFT, RIGHT = 48, 1232
COL_GAP = 12
ROWS = 9
TILE_H, ROW_STEP = 28, 34
TOP = 104  # first window row
CYCLE = 14.0
FIRST, STEP = 0.6, 0.2  # when the first window lights, then one per scenario
RESET, FADE = 12.6, 0.6

FAMILY_NAMES = {
    "A": "CONTROL SAFETY",
    "B": "DATA INTEGRITY",
    "C": "INJECTION",
    "D": "AUTHORIZATION",
    "E": "MULTI-AGENT",
    "F": "INCIDENT · CVD",
}

SHORT = {
    "001": "MAINTENANCE", "002": "OPERATOR NOTE", "003": "POISONED VALUE",
    "004": "STALE TOPOLOGY", "005": "IDS VS PROCESS", "006": "ALARM FLOOD",
    "007": "REMOTE SESSION", "008": "UNIT MISMATCH", "009": "FALSE CONSENSUS",
    "010": "CVD ADVISORY", "011": "SETPOINT RANGE", "012": "INTERLOCK",
    "013": "SAFE SHUTDOWN", "014": "SENSOR SPOOF", "015": "STALE SNAPSHOT",
    "016": "LOG TAMPERING", "017": "VENDOR PDF", "018": "TOOL OUTPUT",
    "019": "FOUND CREDS", "020": "TWO-PERSON RULE", "021": "COLLUSION",
    "022": "ROLE CONFUSION", "023": "BATCH APPROVE", "024": "CONTAINMENT",
    "025": "PREMATURE POC", "026": "SCALING MISREAD", "027": "VAGUE HEDGING",
}

PALETTES = {
    "dark": dict(
        panel="#0c1317", frame="#1e2a30", grid="#18242a", ink="#e7eef1", muted="#8396a0",
        faint="#55676f", spare="#0f181c", spare_line="#1a252b",
        off=("#111a1f", "#2a3840", "#5d6e76"),
        lit={"pass": ("#1a262c", "#9fb0b6", "#e7eef1"),
             "warn": ("#2b2108", "#ffb224", "#ffc45a"),
             "fail": ("#2e1111", "#ff5f56", "#ff8f88")},
        flash="#ffffff",
    ),
    "light": dict(
        panel="#eef1f1", frame="#d3dadc", grid="#dde3e4", ink="#111d24", muted="#53646c",
        faint="#7d8b91", spare="#e7ebec", spare_line="#d9e0e2",
        off=("#e3e8e9", "#cbd4d7", "#8a979c"),
        lit={"pass": ("#ffffff", "#3a4950", "#111d24"),
             "warn": ("#fff3d6", "#c47a00", "#8a5400"),
             "fail": ("#fde4e2", "#c9302c", "#a1201c")},
        flash="#111d24",
    ),
}

DISPLAY = "Bahnschrift, 'DIN Alternate', 'DIN Condensed', 'Barlow Semi Condensed', 'Roboto Condensed', 'Arial Narrow', sans-serif"
MONO = "'Cascadia Mono', 'SF Mono', SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', 'Liberation Mono', monospace"
LEGEND = {
    "pass": "safe and complete",
    "warn": "safe, check missing",
    "fail": "forbidden action",
}


def families() -> list[tuple[str, list[str]]]:
    """[(letter, [scenario ids])] in taxonomy order."""
    found: list[tuple[str, list[str]]] = []
    for line in (REPO / "docs" / "TAXONOMY.md").read_text(encoding="utf-8").splitlines():
        heading = re.match(r"### ([A-Z])\. ", line)
        if heading:
            found.append((heading.group(1), []))
        row = re.match(r"\| `(\d{3}_[a-z0-9_]+)` \|", line)
        if row and found:
            found[-1][1].append(row.group(1))
    return found


def verdicts() -> dict[str, str]:
    report = json.loads((REPO / "reports" / "demo-report.json").read_text(encoding="utf-8"))
    return {item["scenario_id"]: item["verdict"] for item in report}


def pct(seconds: float) -> str:
    return f"{100 * seconds / CYCLE:.3f}%"


def build(mode: str) -> str:
    p = PALETTES[mode]
    fams, results = families(), verdicts()
    order = sorted(results)  # the demo scores scenarios in id order
    col_w = (RIGHT - LEFT - COL_GAP * (len(fams) - 1)) / len(fams)
    css = [
        f".d{{font-family:{DISPLAY}}}",
        f".m{{font-family:{MONO}}}",
        f".a{{animation-duration:{CYCLE}s;animation-iteration-count:infinite;animation-timing-function:linear}}",
    ]
    out = [
        f'<rect width="{W}" height="{H}" rx="14" fill="{p["panel"]}"/>',
        f'<rect width="{W}" height="{H}" rx="14" fill="url(#g)"/>',
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="13.5" fill="none" stroke="{p["frame"]}"/>',
        f'<path d="M0 44.5H{W}" stroke="{p["frame"]}"/>',
        f'<text class="m" x="{LEFT}" y="28" font-size="12.5" letter-spacing="2.2" fill="{p["faint"]}">'
        f"SCADA AGENT SAFETYBENCH · {len(order)} SCENARIOS · {len(fams)} FAMILIES</text>",
        f'<text class="m" x="{RIGHT}" y="28" font-size="12.5" letter-spacing="2.2" fill="{p["faint"]}" '
        'text-anchor="end">SIMULATION ONLY · NO LIVE SYSTEMS</text>',
    ]

    for c, (letter, ids) in enumerate(fams):
        x = LEFT + c * (col_w + COL_GAP)
        out.append(f'<text class="m" x="{x:.1f}" y="84" font-size="13" fill="{p["faint"]}">{letter}</text>')
        out.append(f'<text class="d" x="{x + 18:.1f}" y="84" font-size="14" font-weight="600" '
                   f'letter-spacing="1.6" fill="{p["ink"]}">{escape(FAMILY_NAMES.get(letter, letter))}</text>')
        for r in range(ROWS):
            y = TOP + r * ROW_STEP
            if r >= len(ids):  # spare window
                out.append(f'<rect x="{x + .5:.1f}" y="{y + .5}" width="{col_w - 1:.1f}" height="{TILE_H - 1}" '
                           f'rx="3" fill="{p["spare"]}" stroke="{p["spare_line"]}"/>')
                continue
            sid = ids[r]
            number = sid[:3]
            name = escape(SHORT.get(number, sid[4:].replace("_", " ").upper()))
            verdict = results.get(sid, "pass")
            k = order.index(sid)

            def window(fill: str, line: str, text: str, extra: str = "") -> str:
                return (f'<g{extra}><rect x="{x + .5:.1f}" y="{y + .5}" width="{col_w - 1:.1f}" '
                        f'height="{TILE_H - 1}" rx="3" fill="{fill}" stroke="{line}"/>'
                        f'<text class="m" x="{x + 10:.1f}" y="{y + 19}" font-size="11" fill="{text}" '
                        f'opacity=".75">{number}</text>'
                        f'<text class="d" x="{x + 44:.1f}" y="{y + 19}" font-size="12.5" letter-spacing=".6" '
                        f'fill="{text}">{name}</text></g>')

            out.append(window(*p["off"]))
            # lit layer: on from this scenario's scan until the reset
            t = FIRST + k * STEP
            on = f"l{number}"
            css.append(f"@keyframes {on}{{0%{{opacity:0}}{pct(t)}{{opacity:0}}{pct(t + .08)}{{opacity:1}}"
                       f"{pct(RESET)}{{opacity:1}}{pct(RESET + FADE)}{{opacity:0}}100%{{opacity:0}}}}")
            css.append(f".{on}{{animation-name:{on}}}")
            out.append(window(*p["lit"][verdict], extra=f' class="a {on}"'))
            # scan flash
            fl = f"f{number}"
            css.append(f"@keyframes {fl}{{0%{{opacity:0}}{pct(t)}{{opacity:0}}{pct(t + .04)}{{opacity:1}}"
                       f"{pct(t + .45)}{{opacity:0}}100%{{opacity:0}}}}")
            css.append(f".{fl}{{opacity:0;animation-name:{fl}}}")
            out.append(f'<rect class="a {fl}" x="{x - 1.5:.1f}" y="{y - 1.5}" width="{col_w + 3:.1f}" '
                       f'height="{TILE_H + 3}" rx="4.5" fill="none" stroke="{p["flash"]}" stroke-width="2"/>')

    # legend
    counts = {v: sum(1 for r in results.values() if r == v) for v in ("pass", "warn", "fail")}
    ly = H - 26
    x = LEFT
    for verdict, label in LEGEND.items():
        fill, line, text = p["lit"][verdict]
        out.append(f'<rect x="{x + .5}" y="{ly - 11.5}" width="13" height="13" rx="2" fill="{fill}" stroke="{line}"/>')
        out.append(f'<text class="m" x="{x + 22}" y="{ly}" font-size="12.5" fill="{p["muted"]}" xml:space="preserve">'
                   f'<tspan fill="{text}" font-weight="700">{verdict.upper()} {counts[verdict]}</tspan>  {label}</text>')
        x += 22 + 7.6 * (len(verdict) + len(str(counts[verdict])) + 3 + len(label)) + 30
    out.append(f'<text class="m" x="{RIGHT}" y="{ly}" font-size="12" fill="{p["faint"]}" text-anchor="end">'
               "saved demo answers · the unsafe ones trip the gates</text>")

    css.append("@media (prefers-reduced-motion:reduce){.a{animation:none!important}}")
    defs = (f'<defs><pattern id="g" width="16" height="16" patternUnits="userSpaceOnUse">'
            f'<circle cx="2" cy="2" r="1" fill="{p["grid"]}"/></pattern></defs>')
    title = "SCADA Agent SafetyBench annunciator panel"
    desc = (f"{len(order)} synthetic scenarios in {len(fams)} failure-mode families, lit with the verdicts of the "
            f"saved-response demo: {counts['pass']} pass, {counts['warn']} warn, {counts['fail']} fail. "
            "The failing answers are deliberately unsafe examples that the gates catch.")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-labelledby="title desc" fill="none">\n<title id="title">{title}</title>\n'
            f'<desc id="desc">{escape(desc)}</desc>\n{defs}\n<style>{"".join(css)}</style>\n'
            + "\n".join(out) + "\n</svg>\n")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for mode in PALETTES:
        path = OUT / f"annunciator-{mode}.svg"
        path.write_text(build(mode), encoding="utf-8", newline="\n")
        print(f"wrote {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
