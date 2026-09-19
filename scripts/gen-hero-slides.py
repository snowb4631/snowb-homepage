#!/usr/bin/env python3
"""Hero 캐러셀 슬라이드(SVG) 생성기 — 메인 일러스트와 같은 시리즈(설산 · 아이스 블루 · 스노우볼).

슬라이드: dashboard(대시보드형) · search(데이터 탐색형) · chart(차트 분석형) · quant(퀀트형) · snownote(SnowNote 메모장)
출력: assets/hero-<name>.svg  (1400×1120 — 메인 일러스트 1402×1122 과 같은 비율)
사용법: python3 scripts/gen-hero-slides.py   (표준 라이브러리만 사용, 시드 고정이라 결과가 매번 같다)
"""
import math
import random
from pathlib import Path

W, H = 1400, 1120
OUT = Path(__file__).resolve().parent.parent / "assets"

FONT = "'Pretendard Variable','Pretendard','Apple SD Gothic Neo','Noto Sans KR','Malgun Gothic',sans-serif"
MONO = "'SF Mono','JetBrains Mono',Menlo,Consolas,monospace"
TX, TX2, DM, BD, SF2 = "#0F1B2D", "#3A4A60", "#6B7A90", "#E1E8F1", "#F3F7FC"
AC, AC2, CHIP = "#1F63B5", "#8CC2F5", "#E6F0FB"
UP, DOWN = "#E5484D", "#1F63B5"  # 국내 관례: 상승 빨강 · 하락 파랑

# 카드(앱 화면) 영역
CX, CY, CW, CH = 190, 130, 1020, 780
IX0, IX1 = CX + 44, CX + CW - 44  # 카드 안쪽 좌우 여백


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def text(x, y, s, size=18, color=TX, weight=500, anchor="start", family=FONT, extra=""):
    return (f'<text x="{f(x)}" y="{f(y)}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{extra}>{s}</text>')


def rect(x, y, w, h, fill, rx=0, extra=""):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}" fill="{fill}"{extra}/>'


def poly(points):
    return " ".join(f"{f(x)},{f(y)}" for x, y in points)


def walk(rng, n, start, drift, vol):
    v, out = start, []
    for _ in range(n):
        v += drift + rng.gauss(0, vol)
        out.append(v)
    return out


def scale(vals, y0, y1, lo=None, hi=None):
    lo = min(vals) if lo is None else lo
    hi = max(vals) if hi is None else hi
    return [y1 - (v - lo) / (hi - lo) * (y1 - y0) for v in vals]


def spark(x0, x1, ys):
    step = (x1 - x0) / (len(ys) - 1)
    return [(x0 + i * step, y) for i, y in enumerate(ys)]


# ─── 공통 배경: 설산 · 소나무 · 눈 비탈 ───────────────────────────────
def defs():
    return f"""<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2E6CC0"/><stop offset=".45" stop-color="#8FC0EE"/><stop offset="1" stop-color="#EAF3FC"/>
  </linearGradient>
  <linearGradient id="slope" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#DCE9F6"/>
  </linearGradient>
  <radialGradient id="ball" cx=".38" cy=".32" r=".75">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset=".6" stop-color="#EEF4FB"/><stop offset="1" stop-color="#B9D1EA"/>
  </radialGradient>
  <linearGradient id="area" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{AC}" stop-opacity=".28"/><stop offset="1" stop-color="{AC}" stop-opacity="0"/>
  </linearGradient>
  <filter id="shadow" x="-10%" y="-10%" width="120%" height="130%">
    <feDropShadow dx="0" dy="24" stdDeviation="26" flood-color="#0F1B2D" flood-opacity=".28"/>
  </filter>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#0F1B2D" flood-opacity=".22"/>
  </filter>
</defs>"""


def tree(x, y, s):
    """눈 덮인 소나무 (x,y = 밑동, s = 높이)."""
    w = s * 0.42
    parts = [rect(x - s * 0.03, y - s * 0.08, s * 0.06, s * 0.1, "#3B2A20")]
    for i, t in enumerate((0.0, 0.28, 0.52)):
        top, base = y - s + t * s * 0.9, y - s * 0.08 - (2 - i) * s * 0.22
        ww = w * (0.55 + i * 0.25)
        parts.append(f'<polygon points="{poly([(x, top), (x - ww, base), (x + ww, base)])}" fill="#23465A"/>')
        parts.append(f'<polygon points="{poly([(x, top), (x - ww * 0.55, top + (base - top) * 0.45), (x + ww * 0.35, top + (base - top) * 0.4)])}" fill="#F4F8FC"/>')
    return "".join(parts)


def background(seed):
    rng = random.Random(seed)
    g = [rect(0, 0, W, H, "url(#sky)")]
    # 뒤 산맥
    g.append(f'<polygon points="{poly([(0,560),(140,360),(260,450),(420,230),(560,420),(700,300),(860,470),(1010,250),(1160,420),(1290,330),(1400,430),(1400,700),(0,700)])}" fill="#C6DDF3"/>')
    # 앞 산맥 + 그늘면
    g.append(f'<polygon points="{poly([(0,640),(180,470),(330,590),(520,380),(700,600),(900,450),(1080,610),(1250,470),(1400,560),(1400,760),(0,760)])}" fill="#F2F7FC"/>')
    for pk, l, r in (((520, 380), (430, 500), (600, 700)), ((900, 450), (830, 540), (980, 700)), ((1250, 470), (1190, 540), (1330, 700))):
        g.append(f'<polygon points="{poly([pk, l, r])}" fill="#D3E3F3"/>')
    # 소나무 (좌우 가장자리)
    for x, y, s in ((40, 820, 260), (120, 790, 200), (1290, 800, 240), (1370, 830, 280), (1215, 780, 170)):
        g.append(tree(x, y, s))
    # 눈 비탈
    g.append('<path d="M0,860 C300,780 700,760 1000,800 C1180,820 1300,800 1400,780 L1400,1120 L0,1120 Z" fill="url(#slope)"/>')
    g.append('<path d="M0,960 C380,900 760,930 1400,880" fill="none" stroke="#CFE0F2" stroke-width="3" opacity=".7"/>')
    # 뒤쪽 눈송이
    for _ in range(46):
        g.append(f'<circle cx="{f(rng.uniform(0, W))}" cy="{f(rng.uniform(0, 760))}" r="{f(rng.uniform(1.5, 4.5))}" fill="#fff" opacity="{f(rng.uniform(.45, .9))}"/>')
    return "".join(g)


def snowball(cx=235, cy=965, r=150):
    """메인 일러스트의 'Snowball co.,ltd' 눈덩이 모티프 — 구르는 모션 라인 포함."""
    g = []
    for i, (dy, ln) in enumerate(((-70, 150), (-10, 210), (50, 170))):
        g.append(f'<path d="M{f(cx + r + 20)},{f(cy + dy)} h{ln}" stroke="#FFFFFF" stroke-width="{8 - i * 2}" stroke-linecap="round" opacity=".85"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#ball)" filter="url(#soft)"/>')
    rng = random.Random(7)
    for _ in range(14):
        a, d = rng.uniform(0, 2 * math.pi), rng.uniform(.3, .85) * r
        g.append(f'<circle cx="{f(cx + math.cos(a) * d)}" cy="{f(cy + math.sin(a) * d)}" r="{f(rng.uniform(4, 11))}" fill="#DCE8F5" opacity=".7"/>')
    g.append(f'<g transform="rotate(-12 {cx} {cy})">')
    g.append(text(cx, cy + 4, "Snowball", 46, AC, 800, "middle", extra=' font-style="italic" letter-spacing="-1"'))
    g.append(f'<path d="M{cx - 88},{cy + 20} q88,-14 176,-6" stroke="{AC}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    g.append(text(cx + 10, cy + 60, "co.,ltd", 26, AC, 700, "middle"))
    g.append("</g>")
    return "".join(g)


def foreground_flakes(seed):
    rng = random.Random(seed + 99)
    return "".join(
        f'<circle cx="{f(rng.uniform(0, W))}" cy="{f(rng.uniform(0, H))}" r="{f(rng.uniform(2, 6))}" fill="#fff" opacity="{f(rng.uniform(.55, .95))}"/>'
        for _ in range(26))


def card(title, subtitle, right=""):
    g = [rect(CX, CY, CW, CH, "#FFFFFF", 30, ' filter="url(#shadow)"')]
    # 상단 바
    g.append(f'<circle cx="{IX0 + 14}" cy="{CY + 50}" r="14" fill="{AC}"/>')
    g.append(f'<circle cx="{IX0 + 14}" cy="{CY + 50}" r="6" fill="#fff"/>')
    g.append(text(IX0 + 40, CY + 58, title, 26, TX, 800, extra=' letter-spacing="-.5"'))
    g.append(text(IX0 + 40 + sum(8 if c == ' ' else 13 if c.isascii() else 26 for c in title) + 20, CY + 57, subtitle, 17, DM, 600))
    g.append(right)
    g.append(f'<line x1="{CX}" y1="{CY + 92}" x2="{CX + CW}" y2="{CY + 92}" stroke="{BD}" stroke-width="2"/>')
    return "".join(g)


def pill(x, y, s, fill=CHIP, color=AC, size=15, pad=14, w=None):
    w = w or sum(size * (.62 if c.isascii() else 1.0) for c in s) + pad * 2
    h = size + 16
    return rect(x, y, w, h, fill, h / 2) + text(x + w / 2, y + h / 2 + size * .36, s, size, color, 700, "middle")


def wrap(name, seed, body):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">'
           f"{defs()}{background(seed)}{body}{snowball()}{foreground_flakes(seed)}</svg>\n")
    (OUT / f"hero-{name}.svg").write_text(svg, encoding="utf-8")
    print(f"assets/hero-{name}.svg  {len(svg) // 1024} KB")


# ─── 1. 대시보드형 ────────────────────────────────────────────────────
def dashboard():
    rng = random.Random(11)
    g = [card("ai-trakit", "대시보드", pill(IX1 - 210, CY + 34, "● LIVE", "#FDECEC", UP) + text(IX1, CY + 57, "2026.09.19", 16, DM, 600, "end"))]
    top = CY + 124
    # KPI 타일
    tiles = (("누적 수익률", "+18.4%", "▲ 2.1%p 이번 달", UP), ("이번 주 시그널", "3건", "매수 2 · 리밸런싱 1", AC), ("시그널 적중률", "72%", "최근 12주 기준", TX))
    tw = (IX1 - IX0 - 2 * 22) / 3
    for i, (lab, val, sub, c) in enumerate(tiles):
        x = IX0 + i * (tw + 22)
        g.append(rect(x, top, tw, 124, SF2, 18))
        g.append(text(x + 22, top + 36, lab, 16, DM, 600))
        g.append(text(x + 22, top + 84, val, 40, c, 800, extra=' letter-spacing="-1"'))
        g.append(text(x + 22, top + 110, sub, 14, DM, 500))
    # 누적 수익 곡선
    cx0, cx1, cy0, cy1 = IX0, IX0 + 580, top + 160, top + 450
    g.append(rect(cx0, cy0, cx1 - cx0, cy1 - cy0, "#fff", 18, f' stroke="{BD}" stroke-width="2"'))
    g.append(text(cx0 + 22, cy0 + 36, "누적 수익 추이", 17, TX, 700))
    g.append(pill(cx1 - 150, cy0 + 16, "6개월", SF2, TX2, 14) + pill(cx1 - 78, cy0 + 16, "1년", AC, "#fff", 14))
    for k in range(4):
        yy = cy0 + 80 + k * 55
        g.append(f'<line x1="{cx0 + 22}" y1="{yy}" x2="{cx1 - 22}" y2="{yy}" stroke="{BD}" stroke-dasharray="4 6"/>')
    vals = walk(rng, 40, 100, 0.5, 1.6)
    bench = walk(random.Random(3), 40, 100, 0.18, 1.3)
    lo, hi = min(vals + bench) - 2, max(vals + bench) + 2
    pts = spark(cx0 + 22, cx1 - 22, scale(vals, cy0 + 70, cy1 - 24, lo, hi))
    bpts = spark(cx0 + 22, cx1 - 22, scale(bench, cy0 + 70, cy1 - 24, lo, hi))
    g.append(f'<polygon points="{poly(pts + [(cx1 - 22, cy1 - 24), (cx0 + 22, cy1 - 24)])}" fill="url(#area)"/>')
    g.append(f'<polyline points="{poly(bpts)}" fill="none" stroke="#A9B7C9" stroke-width="3" stroke-dasharray="7 6"/>')
    g.append(f'<polyline points="{poly(pts)}" fill="none" stroke="{AC}" stroke-width="4.5" stroke-linejoin="round"/>')
    ex, ey = pts[-1]
    g.append(f'<circle cx="{f(ex)}" cy="{f(ey)}" r="9" fill="#fff" stroke="{AC}" stroke-width="4"/>')
    # 자산 배분 도넛
    dx0 = cx1 + 24
    g.append(rect(dx0, cy0, IX1 - dx0, cy1 - cy0, "#fff", 18, f' stroke="{BD}" stroke-width="2"'))
    g.append(text(dx0 + 22, cy0 + 36, "자산 배분", 17, TX, 700))
    ocx, ocy, r = dx0 + 110, cy0 + 170, 72
    circ, acc = 2 * math.pi * r, 0
    alloc = ((.45, AC, "KOSPI ETF"), (.35, AC2, "미국 ETF"), (.20, "#D6E3F1", "현금"))
    for frac, c, _ in alloc:
        g.append(f'<circle cx="{f(ocx)}" cy="{f(ocy)}" r="{r}" fill="none" stroke="{c}" stroke-width="30" '
                 f'stroke-dasharray="{f(circ * frac - 4)} {f(circ)}" stroke-dashoffset="{f(-circ * acc)}" transform="rotate(-90 {f(ocx)} {f(ocy)})"/>')
        acc += frac
    g.append(text(ocx, ocy + 10, "3종", 26, TX, 800, "middle"))
    for i, (frac, c, lab) in enumerate(alloc):
        ly = cy0 + 108 + i * 42
        g.append(rect(ocx + 110, ly - 14, 16, 16, c, 4))
        g.append(text(ocx + 136, ly, lab, 15, TX2, 600))
        g.append(text(ocx + 136, ly + 20, f"{int(frac * 100)}%", 15, DM, 600))
    # 최근 시그널
    ly0 = cy1 + 26
    g.append(text(IX0, ly0 + 22, "최근 시그널", 17, TX, 700))
    rows = (("KOSPI200 ETF", "매수", "목표 +6.5%", UP), ("S&amp;P500 ETF", "리밸런싱", "비중 35% → 40%", AC))
    rw = (IX1 - IX0 - 20) / 2
    for i, (n, kind, note, c) in enumerate(rows):
        x = IX0 + i * (rw + 20)
        g.append(rect(x, ly0 + 38, rw, 64, SF2, 16))
        g.append(pill(x + 16, ly0 + 54, kind, "#fff", c, 14, 12))
        g.append(text(x + 116, ly0 + 78, n, 17, TX, 700))
        g.append(text(x + rw - 18, ly0 + 78, note, 15, DM, 600, "end"))
    wrap("dashboard", 1, "".join(g))


# ─── 2. 데이터 탐색형 ─────────────────────────────────────────────────
def search():
    rng = random.Random(21)
    g = [card("ai-trakit", "데이터 탐색", pill(IX1 - 120, CY + 34, "지표 128개", SF2, TX2, 14))]
    top = CY + 122
    # 검색창
    g.append(rect(IX0, top, IX1 - IX0, 70, "#fff", 35, f' stroke="{AC}" stroke-width="3"'))
    g.append(f'<circle cx="{IX0 + 42}" cy="{top + 32}" r="12" fill="none" stroke="{AC}" stroke-width="4"/><path d="M{IX0 + 51},{top + 41} l10,10" stroke="{AC}" stroke-width="4" stroke-linecap="round"/>')
    g.append(text(IX0 + 76, top + 43, "KOSPI 야간선물 · 원/달러 환율 · VIX", 22, TX, 600))
    g.append(f'<rect x="{IX0 + 470}" y="{top + 20}" width="3" height="30" fill="{AC}"/>')
    g.append(rect(IX1 - 118, top + 11, 106, 48, AC, 24) + text(IX1 - 65, top + 43, "검색", 18, "#fff", 700, "middle"))
    # 필터 칩
    x = IX0
    for s, on in (("기간 · 1년", True), ("지표 · 매크로", True), ("정렬 · 상관도", False), ("+ 필터", False)):
        w = sum(15 * (.62 if c.isascii() else 1.0) for c in s) + 30
        g.append(pill(x, top + 92, s, AC if on else SF2, "#fff" if on else TX2, 15, w=w))
        x += w + 12
    # 결과 테이블
    ty = top + 158
    cols = (IX0 + 20, IX0 + 320, IX0 + 470, IX0 + 600, IX0 + 810)
    for c, h in zip(cols, ("지표", "최신값", "변동", "추이 (1년)", "상관도")):
        g.append(text(c, ty, h, 14, DM, 700))
    g.append(f'<line x1="{IX0}" y1="{ty + 16}" x2="{IX1}" y2="{ty + 16}" stroke="{BD}" stroke-width="2"/>')
    rows = (("KOSPI 야간선물", "352.40", "+0.84%", .92), ("원/달러 환율", "1,338.5", "−0.41%", .81),
            ("VIX 변동성지수", "15.72", "−3.10%", .74), ("미 10년물 금리", "4.12%", "+0.03", .58),
            ("WTI 원유", "71.36", "+1.22%", .43))
    rh = 74
    spk_pts = None
    for i, (n, v, chg, corr) in enumerate(rows):
        y = ty + 30 + i * rh
        if i == 0:
            g.append(rect(IX0, y, IX1 - IX0, rh - 8, CHIP, 14))
        up = not chg.startswith("−")
        g.append(text(cols[0], y + 42, n, 18, TX, 700))
        g.append(text(cols[1], y + 42, v, 18, TX2, 600, family=MONO))
        g.append(text(cols[2], y + 42, chg, 17, UP if up else DOWN, 700))
        sv = walk(rng, 24, 0, .12 if up else -.12, 1)
        sp = spark(cols[3], cols[3] + 190, scale(sv, y + 14, y + 54))
        if i == 0:
            spk_pts = sp
        g.append(f'<polyline points="{poly(sp)}" fill="none" stroke="{UP if up else DOWN}" stroke-width="3" stroke-linejoin="round"/>')
        g.append(rect(cols[4], y + 30, 72, 10, SF2, 5) + rect(cols[4], y + 30, 72 * corr, 10, AC, 5))
        g.append(text(IX1 - 6, y + 42, f"{corr:.2f}", 16, TX2, 700, "end"))
    # 돋보기 — 첫 행 추이를 확대해 보여준다
    lx, ly, lr = IX1 - 90, CY + CH - 40, 118
    g.append(f'<clipPath id="lens"><circle cx="{lx}" cy="{ly}" r="{lr}"/></clipPath>')
    g.append(f'<circle cx="{lx}" cy="{ly}" r="{lr}" fill="#fff" filter="url(#soft)"/>')
    zs = [(lx - lr + (px - cols[3]) / 190 * lr * 2, ly + (py - (ty + 64)) * 3.2) for px, py in spk_pts]
    g.append(f'<g clip-path="url(#lens)"><rect x="{lx - lr}" y="{ly - lr}" width="{lr * 2}" height="{lr * 2}" fill="#F6FAFE"/>'
             f'<polygon points="{poly(zs + [(lx + lr, ly + lr), (lx - lr, ly + lr)])}" fill="{UP}" opacity=".1"/>'
             f'<polyline points="{poly(zs)}" fill="none" stroke="{UP}" stroke-width="6" stroke-linejoin="round"/></g>')
    g.append(f'<circle cx="{lx}" cy="{ly}" r="{lr}" fill="none" stroke="{TX}" stroke-width="16"/>')
    g.append(f'<circle cx="{lx}" cy="{ly}" r="{lr - 12}" fill="none" stroke="#fff" stroke-width="3" opacity=".7"/>')
    hx, hy = lx + lr * .72, ly + lr * .72
    g.append(f'<path d="M{f(hx)},{f(hy)} l70,70" stroke="{TX}" stroke-width="30" stroke-linecap="round"/>')
    g.append(f'<path d="M{f(hx + 22)},{f(hy + 22)} l44,44" stroke="{AC}" stroke-width="30" stroke-linecap="round"/>')
    wrap("search", 2, "".join(g))


# ─── 3. 차트 분석형 ───────────────────────────────────────────────────
def chart():
    rng = random.Random(31)
    tabs = "".join(pill(IX1 - 250 + i * 64, CY + 34, s, AC if s == "1M" else SF2, "#fff" if s == "1M" else TX2, 14, w=54)
                   for i, s in enumerate(("1D", "1W", "1M", "1Y")))
    g = [card("KOSPI200 ETF", "", tabs)]
    top = CY + 118
    g.append(text(IX0, top + 44, "34,250", 44, TX, 800, extra=' letter-spacing="-1"'))
    g.append(text(IX0 + 170, top + 42, "▲ 612 (+1.82%)", 20, UP, 700))
    g.append(pill(IX0 + 350, top + 16, "AI 추세 · 상승", "#FDECEC", UP, 14))
    # 캔들
    n = 44
    px0, px1, py0, py1 = IX0, IX1 - 80, top + 76, top + 400
    o, bars = 100.0, []
    for i in range(n):
        drift = -0.35 if 10 <= i < 20 else 0.55
        c = o + drift + rng.gauss(0, 1.4)
        hi, lo = max(o, c) + abs(rng.gauss(0, .8)), min(o, c) - abs(rng.gauss(0, .8))
        bars.append((o, hi, lo, c))
        o = c + rng.gauss(0, .3)
    lo_all, hi_all = min(b[2] for b in bars) - 1, max(b[1] for b in bars) + 1
    Y = lambda v: py1 - (v - lo_all) / (hi_all - lo_all) * (py1 - py0)
    step = (px1 - px0) / n
    for k in range(5):
        yy = py0 + k * (py1 - py0) / 4
        g.append(f'<line x1="{px0}" y1="{f(yy)}" x2="{px1}" y2="{f(yy)}" stroke="{BD}" stroke-dasharray="4 6"/>')
        val = hi_all - k * (hi_all - lo_all) / 4
        g.append(text(IX1, yy + 5, f"{int(val * 330):,}", 14, DM, 600, "end", MONO))
    sup = min(b[2] for b in bars[10:22]) + .2
    g.append(f'<line x1="{px0}" y1="{f(Y(sup))}" x2="{px1}" y2="{f(Y(sup))}" stroke="{AC}" stroke-width="2.5" stroke-dasharray="10 7"/>')
    g.append(pill(px0 + 8, Y(sup) + 8, "지지선", "#fff", AC, 13, 10))
    for i, (o_, h_, l_, c_) in enumerate(bars):
        x = px0 + step * (i + .5)
        col = UP if c_ >= o_ else DOWN
        g.append(f'<line x1="{f(x)}" y1="{f(Y(h_))}" x2="{f(x)}" y2="{f(Y(l_))}" stroke="{col}" stroke-width="2"/>')
        g.append(rect(x - step * .32, Y(max(o_, c_)), step * .64, max(2, abs(Y(o_) - Y(c_))), col, 2))
    closes = [b[3] for b in bars]
    for win, col in ((5, "#F2A33A"), (15, "#7C5CD6")):
        ma = [sum(closes[max(0, i - win + 1):i + 1]) / len(closes[max(0, i - win + 1):i + 1]) for i in range(n)]
        g.append(f'<polyline points="{poly([(px0 + step * (i + .5), Y(v)) for i, v in enumerate(ma)])}" fill="none" stroke="{col}" stroke-width="3" opacity=".9"/>')
    g.append(text(px0 + 110, py0 - 2, "— MA5", 13, "#F2A33A", 700) + text(px0 + 180, py0 - 2, "— MA15", 13, "#7C5CD6", 700))
    # AI 매수 시그널 마커
    bi = 22
    bx, by = px0 + step * (bi + .5), Y(bars[bi][2]) + 22
    g.append(f'<polygon points="{poly([(bx, by - 12), (bx - 13, by + 10), (bx + 13, by + 10)])}" fill="{UP}"/>')
    g.append(f'<g filter="url(#soft)">{rect(bx - 88, by + 20, 176, 58, TX, 14)}</g>')
    g.append(text(bx, by + 46, "AI 매수 시그널", 16, "#fff", 700, "middle") + text(bx, by + 68, "적중 확률 71%", 13, AC2, 600, "middle"))
    # 거래량
    vy0, vy1 = py1 + 20, py1 + 90
    for i, (o_, h_, l_, c_) in enumerate(bars):
        v = rng.uniform(.25, 1) * (1.6 if i in (bi, bi + 1) else 1)
        hh = min(1, v / 1.6) * (vy1 - vy0)
        g.append(rect(px0 + step * (i + .18), vy1 - hh, step * .64, hh, UP if c_ >= o_ else DOWN, 2, ' opacity=".35"'))
    # RSI
    ry0, ry1 = vy1 + 26, CY + CH - 34
    g.append(rect(px0, ry0, px1 - px0, ry1 - ry0, SF2, 12))
    g.append(rect(px0, ry0 + (ry1 - ry0) * .3, px1 - px0, (ry1 - ry0) * .4, CHIP, 0))
    g.append(text(px0 + 12, ry0 + 22, "RSI 14", 13, DM, 700))
    rsi = [50 + 18 * math.sin(i / 4) + rng.gauss(0, 5) for i in range(n)]
    g.append(f'<polyline points="{poly([(px0 + step * (i + .5), ry1 - v / 100 * (ry1 - ry0)) for i, v in enumerate(rsi)])}" fill="none" stroke="{AC}" stroke-width="3"/>')
    g.append(text(IX1, ry0 + (ry1 - ry0) * .3 + 5, "70", 13, DM, 600, "end") + text(IX1, ry0 + (ry1 - ry0) * .7 + 5, "30", 13, DM, 600, "end"))
    wrap("chart", 3, "".join(g))


# ─── 4. 퀀트형 ────────────────────────────────────────────────────────
def quant():
    rng = random.Random(41)
    g = [card("Quant Lab", "멀티팩터 백테스트", pill(IX1 - 150, CY + 34, "2016 – 2026", SF2, TX2, 14))]
    top = CY + 120
    # 수식 바
    g.append(rect(IX0, top, IX1 - IX0, 60, TX, 16))
    g.append(text(IX0 + 24, top + 38, '<tspan fill="#8CC2F5">score</tspan> = <tspan fill="#F2A33A">0.4</tspan>·Momentum + <tspan fill="#F2A33A">0.3</tspan>·Value − <tspan fill="#F2A33A">0.3</tspan>·Volatility',
                  20, "#E8EEF6", 600, family=MONO))
    g.append(text(IX1 - 24, top + 38, "▶ run", 17, "#7EE2A8", 700, "end", MONO))
    # 백테스트 곡선
    ex0, ex1, ey0, ey1 = IX0, IX0 + 560, top + 84, top + 420
    g.append(rect(ex0, ey0, ex1 - ex0, ey1 - ey0, "#fff", 18, f' stroke="{BD}" stroke-width="2"'))
    g.append(text(ex0 + 22, ey0 + 36, "누적 성과", 17, TX, 700))
    g.append(rect(ex0 + 250, ey0 + 24, 22, 5, AC, 2) + text(ex0 + 280, ey0 + 33, "전략", 14, TX2, 600))
    g.append(rect(ex0 + 340, ey0 + 24, 22, 5, "#A9B7C9", 2) + text(ex0 + 370, ey0 + 33, "KOSPI200", 14, TX2, 600))
    strat = walk(rng, 60, 100, .9, 2.2)
    bench = walk(random.Random(5), 60, 100, .35, 2.4)
    lo, hi = min(strat + bench) - 3, max(strat + bench) + 3
    sp = spark(ex0 + 22, ex1 - 22, scale(strat, ey0 + 64, ey1 - 26, lo, hi))
    bp = spark(ex0 + 22, ex1 - 22, scale(bench, ey0 + 64, ey1 - 26, lo, hi))
    g.append(f'<polygon points="{poly(sp + [(ex1 - 22, ey1 - 26), (ex0 + 22, ey1 - 26)])}" fill="url(#area)"/>')
    g.append(f'<polyline points="{poly(bp)}" fill="none" stroke="#A9B7C9" stroke-width="3"/>')
    g.append(f'<polyline points="{poly(sp)}" fill="none" stroke="{AC}" stroke-width="4.5" stroke-linejoin="round"/>')
    # 팩터 상관 히트맵
    hx0 = ex1 + 24
    g.append(rect(hx0, ey0, IX1 - hx0, ey1 - ey0, "#fff", 18, f' stroke="{BD}" stroke-width="2"'))
    g.append(text(hx0 + 22, ey0 + 36, "팩터 상관관계", 17, TX, 700))
    labels = ("MOM", "VAL", "VOL", "QLT", "SIZE")
    k = len(labels)
    cell = min((IX1 - hx0 - 90) / k, (ey1 - ey0 - 90) / k)
    gx, gy = hx0 + 70, ey0 + 60
    for i in range(k):
        g.append(text(gx - 10, gy + cell * (i + .5) + 5, labels[i], 13, DM, 700, "end", MONO))
        g.append(text(gx + cell * (i + .5), gy + cell * k + 20, labels[i], 13, DM, 700, "middle", MONO))
        for j in range(k):
            v = 1.0 if i == j else round(rng.uniform(-.7, .8), 2)
            col = AC if v >= 0 else UP
            g.append(rect(gx + cell * j + 2, gy + cell * i + 2, cell - 4, cell - 4, col, 8, f' opacity="{f(.12 + abs(v) * .8)}"'))
            if i == j or abs(v) > .55:
                g.append(text(gx + cell * (j + .5), gy + cell * (i + .5) + 5, f"{v:.1f}", 13, "#fff" if abs(v) > .55 else TX, 700, "middle"))
    # 성과 지표 타일
    sy = ey1 + 24
    stats = (("CAGR", "14.2%", UP, "연평균 수익률"), ("MDD", "−9.8%", DOWN, "최대 낙폭"), ("Sharpe", "1.47", TX, "위험 대비 수익"), ("승률", "63%", TX, "월간 기준"))
    tw = (IX1 - IX0 - 3 * 18) / 4
    for i, (lab, val, c, sub) in enumerate(stats):
        x = IX0 + i * (tw + 18)
        g.append(rect(x, sy, tw, CY + CH - 34 - sy, SF2, 16))
        g.append(text(x + 20, sy + 34, lab, 15, DM, 700))
        g.append(text(x + 20, sy + 82, val, 36, c, 800, extra=' letter-spacing="-1"'))
        g.append(text(x + 20, sy + 112, sub, 14, DM, 500))
    wrap("quant", 4, "".join(g))


# ─── 5. SnowNote (AI 메모장 · 디스코드형 레이아웃) ─────────────────────
def snownote():
    g = [card("SnowNote", "AI 메모장", pill(IX1 - 150, CY + 34, "COMING SOON", "#EEF1F5", DM, 14))]
    by0, by1 = CY + 92, CY + CH
    g.append(f'<clipPath id="body"><rect x="{CX}" y="{by0}" width="{CW}" height="{CH - 92}" rx="30"/>'
             f'<rect x="{CX}" y="{by0}" width="{CW}" height="40"/></clipPath><g clip-path="url(#body)">')
    # 좌측 레일 (주제 서버)
    rx1 = CX + 76
    g.append(rect(CX, by0, 76, CH - 92, TX))
    g.append(f'<circle cx="{CX + 38}" cy="{by0 + 44}" r="24" fill="url(#ball)"/>')
    g.append(text(CX + 38, by0 + 50, "S", 20, AC, 800, "middle", extra=' font-style="italic"'))
    g.append(rect(CX + 22, by0 + 84, 32, 3, "#2A3A52", 2))
    for i, (s, c) in enumerate((("일", "#3B82D6"), ("주", UP), ("책", "#7C5CD6"), ("+", "#22324A"))):
        y = by0 + 104 + i * 62
        g.append(rect(CX + 14, y, 48, 48, c, 16 if i != 1 else 14))
        g.append(text(CX + 38, y + 32, s, 20, "#fff" if s != "+" else "#7EE2A8", 700, "middle"))
    g.append(rect(CX, by0 + 104 + 62 + 12, 5, 24, "#fff", 2))
    # 채널 목록
    chx1 = rx1 + 214
    g.append(rect(rx1, by0, chx1 - rx1, CH - 92, SF2))
    g.append(text(rx1 + 22, by0 + 42, "주식", 20, TX, 800))
    g.append(text(rx1 + 22, by0 + 84, "TOPICS", 12, DM, 700, extra=' letter-spacing="1"'))
    chans = (("시황 메모", False, 0), ("매매 일지", True, 0), ("아이디어", False, 3), ("공부", False, 0), ("읽을 거리", False, 0))
    for i, (n, on, badge) in enumerate(chans):
        y = by0 + 98 + i * 44
        if on:
            g.append(rect(rx1 + 10, y, chx1 - rx1 - 20, 38, CHIP, 10))
        g.append(text(rx1 + 24, y + 26, "#", 19, AC if on else DM, 700))
        g.append(text(rx1 + 46, y + 26, n, 17, TX if on else TX2, 700 if on else 500))
        if badge:
            g.append(f'<circle cx="{chx1 - 28}" cy="{y + 19}" r="11" fill="{UP}"/>' + text(chx1 - 28, y + 24, str(badge), 13, "#fff", 700, "middle"))
    ay = by0 + 340
    g.append(text(rx1 + 22, ay, "AI", 12, DM, 700, extra=' letter-spacing="1"'))
    g.append(text(rx1 + 24, ay + 34, "✦", 17, AC, 700) + text(rx1 + 46, ay + 34, "자동 분류함", 17, TX2, 500))
    g.append(text(rx1 + 24, ay + 76, "✦", 17, AC, 700) + text(rx1 + 46, ay + 76, "AI 메모리", 17, TX2, 500))
    # 메인 — 기록 흐름
    mx0, mx1 = chx1 + 32, CX + CW - 40
    g.append(text(mx0, by0 + 44, "# 매매 일지", 21, TX, 800))
    g.append(text(mx0 + 128, by0 + 43, "주제별로 쌓이는 나의 기록", 15, DM, 500))
    g.append(f'<circle cx="{mx1 - 12}" cy="{by0 + 36}" r="10" fill="none" stroke="{DM}" stroke-width="3"/><path d="M{mx1 - 5},{by0 + 43} l8,8" stroke="{DM}" stroke-width="3" stroke-linecap="round"/>')
    g.append(f'<line x1="{chx1}" y1="{by0 + 70}" x2="{CX + CW}" y2="{by0 + 70}" stroke="{BD}" stroke-width="2"/>')

    def msg(y, time):
        return (f'<circle cx="{mx0 + 22}" cy="{y + 22}" r="22" fill="{CHIP}"/>' + text(mx0 + 22, y + 29, "나", 17, AC, 800, "middle")
                + text(mx0 + 60, y + 18, "나", 17, TX, 800) + text(mx0 + 84, y + 18, time, 14, DM, 500))
    cx0 = mx0 + 60
    y = by0 + 96
    g.append(msg(y, "오늘 09:12"))
    g.append(text(cx0, y + 54, "이번 주 체크리스트", 21, TX, 800))
    for i, (s, done) in enumerate((("야간선물 흐름 확인", True), ("환율 1,340원 돌파 여부 보기", True), ("리밸런싱 시그널 나오면 비중 점검", False))):
        yy = y + 76 + i * 34
        g.append(rect(cx0, yy, 20, 20, AC if done else "#fff", 5, "" if done else f' stroke="{BD}" stroke-width="2"'))
        if done:
            g.append(f'<path d="M{cx0 + 5},{yy + 10} l4,4 l7,-8" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        g.append(text(cx0 + 32, yy + 16, s, 17, DM if done else TX2, 500, extra=' text-decoration="line-through"' if done else ""))
    y += 196
    g.append(msg(y, "오늘 11:40"))
    g.append(text(cx0, y + 50, "반도체 ETF 비중 고민 — 실적 발표 이후 다시 보기", 17, TX2, 500))
    g.append(rect(cx0, y + 66, 290, 32, "#F1ECFD", 16))
    g.append(text(cx0 + 16, y + 88, "✦ AI가 #아이디어 로도 분류했어요", 14, "#6B4FCF", 700))
    y += 118
    g.append(msg(y, "오늘 14:05"))
    g.append(rect(cx0, y + 34, 5, 44, AC2, 2))
    g.append(text(cx0 + 18, y + 54, "잘 뭉쳐지는 눈과 아주 긴 언덕을 찾을 것.", 17, TX2, 500, extra=' font-style="italic"'))
    g.append(text(cx0 + 18, y + 76, "— 오늘의 원칙", 14, DM, 600))
    # 입력창 (마크다운)
    iy = by1 - 84
    g.append(rect(mx0, iy, mx1 - mx0, 56, "#fff", 14, f' stroke="{BD}" stroke-width="2"'))
    for i, s in enumerate(("B", "I", "#", "&lt;/&gt;")):
        g.append(text(mx0 + 22 + i * 30, iy + 35, s, 16, DM, 800, extra=' font-style="italic"' if s == "I" else ""))
    g.append(f'<line x1="{mx0 + 140}" y1="{iy + 14}" x2="{mx0 + 140}" y2="{iy + 42}" stroke="{BD}" stroke-width="2"/>')
    g.append(text(mx0 + 158, iy + 35, "#매매 일지 에 기록하기 · 마크다운 지원", 16, "#A3AFBF", 500))
    g.append("</g>")
    # 떠 있는 AI 메모리 패널 — 카드 밖으로 살짝 걸친다
    px, py, pw, ph = CX + CW - 250, CY + CH - 250, 330, 176
    g.append(f'<g filter="url(#soft)">{rect(px, py, pw, ph, TX, 22)}</g>')
    g.append(text(px + 24, py + 40, "✦ AI 메모리", 19, "#fff", 800))
    g.append(text(px + 24, py + 68, "기록 1,284개 · 주제 5개", 14, "#9FB0C6", 500))
    g.append(rect(px + 24, py + 86, pw - 48, 8, "#22324A", 4) + rect(px + 24, py + 86, (pw - 48) * .68, 8, AC2, 4))
    g.append(rect(px + 24, py + 114, 132, 40, AC, 12) + text(px + 90, py + 140, "↑ 내보내기", 15, "#fff", 700, "middle"))
    g.append(rect(px + 168, py + 114, 138, 40, "#22324A", 12) + text(px + 237, py + 140, "↓ 가져오기", 15, "#E8EEF6", 700, "middle"))
    wrap("snownote", 5, "".join(g))


if __name__ == "__main__":
    dashboard()
    search()
    chart()
    quant()
    snownote()
