"""Render animated SVG cards for the profile README.

Reads data/contributions.json (see fetch_contributions.py) and writes
cards/hero.svg, graph.svg, activity.svg, build.svg, accounts.svg, learn.svg.

Env:
  STATIC=1  show every card at its final frame (for screenshots)
  DEMO=1    use generated sample data instead of data/contributions.json
"""
import datetime as dt
import json
import math
import os
import random
from collections import OrderedDict

STATIC = os.environ.get("STATIC") == "1"
DEMO = os.environ.get("DEMO") == "1"

PAPER, INK, MUTED = "#f6f1e7", "#17150f", "#7a7466"
BLUE, RED, YELLOW = "#2457f5", "#e4472f", "#f2b705"
SERIF = "'Instrument Serif', Georgia, 'Times New Roman', serif"
SANS = "'Geist', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

NAME_FIRST, NAME_LAST = "Prashant", "Mishra"
TAGLINE = "Accountant & store in-charge. Self-taught builder in Python and the web."
LOCATION = "Gorakhpur, Uttar Pradesh"

CSS = f"""
text{{font-family:{SANS}}}
.serif{{font-family:{SERIF}}}
@keyframes rise{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:none}}}}
@keyframes pop{{0%{{opacity:0;transform:scale(.2)}}70%{{opacity:1;transform:scale(1.15)}}100%{{opacity:1;transform:scale(1)}}}}
@keyframes grow{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}
@keyframes swing{{0%{{opacity:0;transform:translateY(40px) rotate(-6deg)}}65%{{opacity:1;transform:translateY(-6px) rotate(1.5deg)}}100%{{opacity:1;transform:none}}}}
@keyframes ring{{0%{{opacity:.7;transform:scale(.3)}}100%{{opacity:0;transform:scale(2.2)}}}}
@keyframes nudge{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(5px)}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
.anim{{opacity:0;animation-fill-mode:both;animation-timing-function:cubic-bezier(.2,.8,.2,1)}}
.rise{{animation-name:rise;animation-duration:.7s}}
.pop{{animation-name:pop;animation-duration:.45s}}
.grow{{transform-origin:bottom;transform-box:fill-box;animation-name:grow;animation-duration:.8s;opacity:1}}
.swing{{animation-name:swing;animation-duration:.9s}}
.ring{{transform-origin:center;transform-box:fill-box;animation:ring 2.4s ease-out infinite}}
.nudge{{animation:nudge 1.8s ease-in-out infinite}}
.dot{{animation:pulse 1.6s ease-in-out infinite}}
@media (prefers-reduced-motion:reduce){{
  .anim,.grow,.ring,.nudge,.dot{{animation:none!important;opacity:1!important;transform:none!important}}
  .ring{{opacity:0!important}}
}}
"""
if STATIC:
    CSS += ".anim,.grow,.ring,.nudge,.dot{animation:none!important;opacity:1!important;transform:none!important}.ring{opacity:0!important}"


def svg(w, h, body, extra_defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        f"<defs><style>{CSS}</style>{extra_defs}</defs>"
        f'<rect width="{w}" height="{h}" rx="18" fill="{PAPER}"/>'
        f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="17.5" fill="none" stroke="{INK}" stroke-opacity=".15" stroke-width="1.5"/>'
        f"{body}</svg>"
    )


def d(delay):
    return f"animation-delay:{delay:.2f}s"


# ---------------------------------------------------------------- data
def load():
    if DEMO or not os.path.exists("data/contributions.json"):
        random.seed(7)
        end = dt.date.today()
        days = []
        for i in range(364, -1, -1):
            day = end - dt.timedelta(days=i)
            busy = 1.0 if day.weekday() < 5 else 0.5
            c = 0 if random.random() > 0.55 * busy + 0.1 else int(random.expovariate(1 / 4)) + 1
            days.append({"date": day.isoformat(), "count": c})
        return {"user": "demo", "total": sum(x["count"] for x in days), "days": days}
    with open("data/contributions.json") as f:
        return json.load(f)


def stats(days):
    total = sum(x["count"] for x in days)
    active = sum(1 for x in days if x["count"] > 0)
    best = max(days, key=lambda x: x["count"])
    longest = cur = 0
    for x in days:
        cur = cur + 1 if x["count"] > 0 else 0
        longest = max(longest, cur)
    # current streak counts back from today (or yesterday if today is empty)
    streak = 0
    for x in reversed(days):
        if x["count"] > 0:
            streak += 1
        elif x is days[-1]:
            continue
        else:
            break
    months = OrderedDict()
    for x in days:
        months[x["date"][:7]] = months.get(x["date"][:7], 0) + x["count"]
    return dict(total=total, active=active, best=best, longest=longest, streak=streak, months=months)


# ---------------------------------------------------------------- cards
def hero(s):
    w, h = 900, 300
    grad = (
        f'<linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="220" y2="0">'
        f'<stop offset="0" stop-color="{INK}"/><stop offset=".38" stop-color="{INK}"/>'
        f'<stop offset=".5" stop-color="{BLUE}"/><stop offset=".62" stop-color="{INK}"/>'
        f'<stop offset="1" stop-color="{INK}"/>'
        + (
            ""
            if STATIC
            else '<animateTransform attributeName="gradientTransform" type="translate" '
            'values="-260 0;520 0;520 0" keyTimes="0;.35;1" dur="6s" begin="1.6s" repeatCount="indefinite"/>'
        )
        + "</linearGradient>"
    )
    body = (
        f'<text x="48" y="58" font-size="14" letter-spacing="2.5" fill="{MUTED}" class="anim rise" style="{d(0)}">'
        f'<tspan fill="{BLUE}">BUILD</tspan>  /  <tspan fill="{RED}">ACCOUNTS</tspan>  /  <tspan fill="#b98a00">LEARN</tspan></text>'
        f'<text x="48" y="160" font-size="92" class="serif anim rise" style="{d(.15)}" fill="{INK}">{NAME_FIRST}</text>'
        f'<text x="48" y="248" font-size="92" class="serif anim rise" style="{d(.4)}" fill="url(#shine)">{NAME_LAST}</text>'
        f'<circle cx="540" cy="146" r="5" fill="{BLUE}" class="dot"/>'
        f'<text x="556" y="152" font-size="17" fill="{INK}" class="anim rise" style="{d(.8)}">{LOCATION}</text>'
        f'<text x="540" y="190" font-size="17" fill="{MUTED}" class="anim rise" style="{d(1.0)}">'
        f'<tspan x="540">Accountant &amp; store in-charge.</tspan>'
        f'<tspan x="540" dy="26">Self-taught builder in</tspan>'
        f'<tspan x="540" dy="26">Python and the web.</tspan></text>'
    )
    return svg(w, h, body, grad)


def graph(days):
    w, cell, gap = 900, 12, 3
    first = dt.date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7  # Sunday-first rows
    mx = max(1, max(x["count"] for x in days))
    left, top = 48, 64
    cells = []
    for i, x in enumerate(days):
        idx = i + offset
        col, row = divmod(idx, 7)
        level = 0 if x["count"] == 0 else min(4, 1 + int(3 * x["count"] / mx))
        fill = ["#e6e0d2", "#b9c8fb", "#7c9bf8", "#4a74f6", BLUE][level]
        cx, cy = left + col * (cell + gap), top + row * (cell + gap)
        delay = 0.3 + col * 0.03
        cells.append(
            f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" rx="3" fill="{fill}" '
            f'class="anim pop" style="{d(delay)};transform-origin:{cx+cell/2}px {cy+cell/2}px"/>'
        )
    cols = (len(days) + offset + 6) // 7
    h = top + 7 * (cell + gap) + 34
    body = (
        f'<text x="48" y="40" font-size="14" letter-spacing="2.5" fill="{MUTED}">CONTRIBUTIONS · LAST 12 MONTHS</text>'
        + "".join(cells)
        + f'<text x="{left}" y="{h-14}" font-size="12" fill="{MUTED}">Less</text>'
    )
    for i, c in enumerate(["#e6e0d2", "#b9c8fb", "#7c9bf8", "#4a74f6", BLUE]):
        body += f'<rect x="{left+34+i*17}" y="{h-25}" width="12" height="12" rx="3" fill="{c}"/>'
    body += f'<text x="{left+34+5*17+4}" y="{h-14}" font-size="12" fill="{MUTED}">More</text>'
    return svg(w, h, body)


def activity(s):
    w, h = 900, 350
    months = list(s["months"].items())[-12:]
    mx = max(1, max(v for _, v in months))
    best_key = max(months, key=lambda kv: kv[1])[0]
    base, top, bw, gap, left = 235, 100, 38, 24, 48
    body = f'<text x="48" y="40" font-size="14" letter-spacing="2.5" fill="{MUTED}">ACTIVITY BY MONTH</text>'
    for i, (k, v) in enumerate(months):
        bh = max(3, (base - top) * v / mx)
        x = left + i * (bw + gap)
        col = BLUE if k == best_key else INK
        op = 1 if k == best_key else 0.85
        body += (
            f'<rect x="{x}" y="{base-bh:.1f}" width="{bw}" height="{bh:.1f}" rx="5" fill="{col}" fill-opacity="{op}" '
            f'class="grow" style="{d(.2+i*.07)}"/>'
            f'<text x="{x+bw/2}" y="{base+20}" font-size="12" text-anchor="middle" fill="{MUTED}">'
            f'{dt.date.fromisoformat(k + "-01").strftime("%b")}</text>'
        )
        if k == best_key:
            body += (
                f'<text x="{x+bw/2}" y="{base-bh-8:.1f}" font-size="15" font-weight="600" text-anchor="middle" fill="{BLUE}" '
                f'class="anim pop" style="{d(1.2)};transform-origin:{x+bw/2}px {base-bh-14:.1f}px">{v}</text>'
            )
    b = s["best"]
    best_day = dt.date.fromisoformat(b["date"]).strftime("%d %b")
    items = [
        (str(s["total"]), "contributions"),
        (str(s["active"]), "active days"),
        (f'{s["streak"]}d', "current streak"),
        (f'{s["longest"]}d', "longest streak"),
        (f'{b["count"]}', f"busiest day · {best_day}"),
    ]
    for i, (big, small) in enumerate(items):
        x = 48 + i * 168
        body += (
            f'<g class="anim rise" style="{d(1.0+i*.1)}">'
            f'<text x="{x}" y="316" font-size="30" class="serif" fill="{INK}">{big}</text>'
            f'<text x="{x}" y="336" font-size="12" fill="{MUTED}">{small}</text></g>'
        )
    return svg(w, h, body)


def count_up(x, y, value, delay, color, size=64):
    if STATIC or value <= 0:
        return f'<text x="{x}" y="{y}" font-size="{size}" class="serif" fill="{color}">{value}</text>'
    n = 18
    out = []
    for i in range(n):
        v = round(value * (i / (n - 1)) ** 2) if i < n - 1 else value
        t0 = delay + i * 0.045
        last = i == n - 1
        out.append(
            f'<text x="{x}" y="{y}" font-size="{size}" class="serif" fill="{color}" visibility="hidden">{v}'
            f'<set attributeName="visibility" to="visible" begin="{t0:.3f}s" '
            + ('fill="freeze"' if last else f'dur="0.045s"')
            + "/></text>"
        )
    return "".join(out)


def tile(key, color, ink, title, blurb, delay, stat=None, stat_label=""):
    w, h = 290, 280
    body = (
        f'<g class="anim swing" style="{d(delay)};transform-origin:145px 130px">'
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{color}"/>'
        f'<circle cx="{w-40}" cy="44" r="22" fill="none" stroke="{ink}" stroke-width="2" class="ring" style="{d(delay+.9)}"/>'
        f'<text x="26" y="48" font-size="13" letter-spacing="2.5" fill="{ink}" fill-opacity=".75">{key}</text>'
        f'<text x="26" y="112" font-size="44" class="serif" fill="{ink}">{title}</text>'
        + "".join(
            f'<text x="26" y="{142+i*22}" font-size="14" fill="{ink}" fill-opacity=".85">{line}</text>'
            for i, line in enumerate(blurb)
        )
        + (
            count_up(26, 252, stat, delay + 0.9, ink, 52)
            + f'<text x="{26 + 30*len(str(stat))+8}" y="252" font-size="13" fill="{ink}" fill-opacity=".8">{stat_label}</text>'
            if stat is not None
            else ""
        )
        + f'<text x="{w-44}" y="252" font-size="26" fill="{ink}" class="nudge">→</text>'
        + "</g>"
    )
    return svg(w, h, body).replace(f'<rect width="{w}" height="{h}" rx="18" fill="{PAPER}"/>', "").replace(
        f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="17.5" fill="none" stroke="{INK}" stroke-opacity=".15" stroke-width="1.5"/>',
        "",
    )


def main():
    data = load()
    days = data["days"][-365:]
    s = stats(days)
    os.makedirs("cards", exist_ok=True)
    cards = {
        "hero.svg": hero(s),
        "graph.svg": graph(days),
        "activity.svg": activity(s),
        "build.svg": tile("BUILD", BLUE, "#ffffff", "Build",
                          ["Python, web tools and", "ERP prototypes for real", "construction sites."], 0.4,
                          s["total"], "contributions"),
        "accounts.svg": tile("ACCOUNTS", RED, "#ffffff", "Accounts",
                             ["Site accounting, GST and", "TDS, vendor payments,", "inventory on Tally."], 0.65),
        "learn.svg": tile("LEARN", YELLOW, INK, "Learn",
                          ["CA Foundation, data", "science and finance,", "one chapter at a time."], 0.9),
    }
    for name, content in cards.items():
        with open(f"cards/{name}", "w") as f:
            f.write(content)
    print("Rendered", ", ".join(cards), "| total", s["total"], "streak", s["streak"])


if __name__ == "__main__":
    main()
