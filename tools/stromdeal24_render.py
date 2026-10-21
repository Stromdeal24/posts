#!/usr/bin/env python3
"""
Strom Deal 24 – Render-Skript für Reels (MP4) und Karussells/Beiträge (PNG)
============================================================================

Erzeugt im Strom-Deal-24-Design (Dunkelblau/Gold, Wappen-Logo, Poppins):
  * Reels:      1080 x 1920, animiert, 30 fps, MP4 (ohne Ton)
  * Karussells: 1080 x 1440, eine PNG pro Seite (mit Seitenzahl „1/5“)
Hintergründe: "mast" (Strommasten) und "chip" (Schaltkreis/Platine).

Voraussetzungen
  pip install playwright        (danach einmalig:  playwright install chromium)
  ffmpeg                        (für die MP4-Videos, z. B. apt/brew install ffmpeg)
  Schrift „Poppins“             (lokal installiert ODER Internet: wird von Google Fonts geladen)

Aufruf
  python stromdeal24_render.py                 # alles rendern nach ./output
  python stromdeal24_render.py --out mein_ordner
  python stromdeal24_render.py --only Tag2_Reel_Winter   # nur ein Element
  python stromdeal24_render.py --no-video      # nur Karussells (schnell)

Eigene Inhalte: unten im Abschnitt „INHALTE“ REELS und CAROUSELS anpassen.
Tipp: Kein „Link in der Bio“ verwenden – CTA ist „CHECK“ per DM/WhatsApp.
"""
import argparse, asyncio, math, pathlib, random, shutil, subprocess, sys

# --------------------------------------------------------------------------
# Marke
# --------------------------------------------------------------------------
NAVY, DEEP, GOLD, GREEN = "#0B2545", "#06142A", "#FFC93C", "#2BB673"
CREST = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMjAgMjkwIiB3aWR0aD0iMjIwIiBoZWlnaHQ9IjI5MCI+PGRlZnM+CjxsaW5lYXJHcmFkaWVudCBpZD0iZ29sZCIgeDE9IjAiIHkxPSIwIiB4Mj0iMCIgeTI9IjEiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iI0ZGRTI4QSIvPjxzdG9wIG9mZnNldD0iLjUiIHN0b3AtY29sb3I9IiNGRkM5M0MiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiNGNUE2MjMiLz48L2xpbmVhckdyYWRpZW50Pgo8bGluZWFyR3JhZGllbnQgaWQ9ImdvbGRUIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgeDE9IjAiIHkxPSI2NDAiIHgyPSIwIiB5Mj0iNzYwIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNGRkU5QTgiLz48c3RvcCBvZmZzZXQ9Ii41NSIgc3RvcC1jb2xvcj0iI0ZGQzkzQyIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iI0Y1QTYyMyIvPjwvbGluZWFyR3JhZGllbnQ+CjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JlZW4iIHgxPSIwIiB5MT0iMCIgeDI9IjAiIHkyPSIxIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiM1QkUzOUEiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMxNDg1NUEiLz48L2xpbmVhckdyYWRpZW50Pgo8bGluZWFyR3JhZGllbnQgaWQ9ImJsdWUiIHgxPSIwIiB5MT0iMCIgeDI9IjAiIHkyPSIxIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiM4RkQzRkYiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMxQjZGRDEiLz48L2xpbmVhckdyYWRpZW50Pgo8cmFkaWFsR3JhZGllbnQgaWQ9ImRpc2MiIGN4PSIuNSIgY3k9Ii4zOCIgcj0iLjciPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzFENEU4OSIvPjxzdG9wIG9mZnNldD0iLjYiIHN0b3AtY29sb3I9IiMwQjI1NDUiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMwNjE0MkEiLz48L3JhZGlhbEdyYWRpZW50Pgo8bGluZWFyR3JhZGllbnQgaWQ9InNoaWVsZEciIHgxPSIwIiB5MT0iMCIgeDI9IjAiIHkyPSIxIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiMxNjQwNkYiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMwODFCMzYiLz48L2xpbmVhckdyYWRpZW50Pgo8bGluZWFyR3JhZGllbnQgaWQ9InJpbmciIHgxPSIwIiB5MT0iMCIgeDI9IjEiIHkyPSIxIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNGRkUyOEEiLz48c3RvcCBvZmZzZXQ9Ii41IiBzdG9wLWNvbG9yPSIjRjVBNjIzIi8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjRkZFMjhBIi8+PC9saW5lYXJHcmFkaWVudD4KPGZpbHRlciBpZD0iZ2xvdyIgeD0iLTUwJSIgeT0iLTUwJSIgd2lkdGg9IjIwMCUiIGhlaWdodD0iMjAwJSI+PGZlR2F1c3NpYW5CbHVyIHN0ZERldmlhdGlvbj0iMTQiIHJlc3VsdD0iYiIvPjxmZU1lcmdlPjxmZU1lcmdlTm9kZSBpbj0iYiIvPjxmZU1lcmdlTm9kZSBpbj0iU291cmNlR3JhcGhpYyIvPjwvZmVNZXJnZT48L2ZpbHRlcj4KPGZpbHRlciBpZD0ic29mdGdsb3ciIHg9Ii01MCUiIHk9Ii01MCUiIHdpZHRoPSIyMDAlIiBoZWlnaHQ9IjIwMCUiPjxmZUdhdXNzaWFuQmx1ciBzdGREZXZpYXRpb249IjQwIi8+PC9maWx0ZXI+CjxmaWx0ZXIgaWQ9InNoYWRvdyIgeD0iLTMwJSIgeT0iLTMwJSIgd2lkdGg9IjE2MCUiIGhlaWdodD0iMTYwJSI+PGZlRHJvcFNoYWRvdyBkeD0iMCIgZHk9IjEwIiBzdGREZXZpYXRpb249IjEyIiBmbG9vZC1jb2xvcj0iIzAwMCIgZmxvb2Qtb3BhY2l0eT0iLjQ1Ii8+PC9maWx0ZXI+CjxjbGlwUGF0aCBpZD0ic2MiPjxwYXRoIGQ9Ik0xMDAgMCBMMTkwIDMwIEwxOTAgMTIwIEMxOTAgMTkwIDE1MCAyMzUgMTAwIDI2MiBDNTAgMjM1IDEwIDE5MCAxMCAxMjAgTDEwIDMwIFoiLz48L2NsaXBQYXRoPjwvZGVmcz48ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMTAgMTQwKSBzY2FsZSgxLjApIHRyYW5zbGF0ZSgtMTAwIC0xMzEpIiBmaWx0ZXI9InVybCgjc2hhZG93KSI+CiA8ZyBjbGlwLXBhdGg9InVybCgjc2MpIj48cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEyNSIgZmlsbD0iIzEzNDU3QyIvPjxyZWN0IHg9IjEwMCIgeT0iMCIgd2lkdGg9IjEwMCIgaGVpZ2h0PSIxMjUiIGZpbGw9IiMwRTJGNTciLz4KICA8cmVjdCB4PSIwIiB5PSIxMjUiIHdpZHRoPSIxMDAiIGhlaWdodD0iMTQwIiBmaWxsPSIjMEUyRjU3Ii8+PHJlY3QgeD0iMTAwIiB5PSIxMjUiIHdpZHRoPSIxMDAiIGhlaWdodD0iMTQwIiBmaWxsPSIjMTM0NTdDIi8+CiAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNTUgNjUpIHNjYWxlKC40MikgdHJhbnNsYXRlKC0xMDMgLTE2NikiPjxwYXRoIGQ9Ik0xMTYgOTIgTDY2IDE3OCBMMTAwIDE3OCBMODQgMjQwIEwxNDAgMTQ4IEwxMDYgMTQ4IEwxMjQgOTIgWiIgZmlsbD0idXJsKCNnb2xkKSIvPjwvZz4KICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxNDUgNzApIHNjYWxlKC4zMykgdHJhbnNsYXRlKC0xMDAgLTEzMSkiPjxwYXRoIGQ9Ik0xMDAgMCBDMTIwIDUwIDE5MCA5MCAxOTAgMTY1IEMxOTAgMjIyIDE1MCAyNjIgMTAwIDI2MiBDNTAgMjYyIDEwIDIyMiAxMCAxNjUgQzEwIDEyMCAzOCA5NSA1NSA1OCBDNjYgOTIgNzggMTA0IDkwIDExMCBDODQgNzAgODggMzIgMTAwIDAgWiIgZmlsbD0idXJsKCNibHVlKSIvPjwvZz4KICA8ZyB0cmFuc2Zvcm09InRyYW5zbGF0ZSg1OCAxODApIHNjYWxlKC40MikiPjxwYXRoIGQ9Ik0wIC02MCBMNzAgMCBMNzAgNzAgTC03MCA3MCBMLTcwIDAgWiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjRkZGRkZGIiBzdHJva2Utd2lkdGg9IjEyIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PC9nPgogIDx0ZXh0IHg9IjE0NSIgeT0iMTk4IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iUG9wcGlucyIgZm9udC13ZWlnaHQ9IjcwMCIgZm9udC1zaXplPSI1MiIgZmlsbD0idXJsKCNncmVlbikiPuKCrDwvdGV4dD48L2c+CiA8cGF0aCBkPSJNMTAwIDAgTDEwMCAyNjIgTTEwIDEyNSBMMTkwIDEyNSIgc3Ryb2tlPSJ1cmwoI3JpbmcpIiBzdHJva2Utd2lkdGg9IjQiLz4KIDxwYXRoIGQ9Ik0xMDAgMCBMMTkwIDMwIEwxOTAgMTIwIEMxOTAgMTkwIDE1MCAyMzUgMTAwIDI2MiBDNTAgMjM1IDEwIDE5MCAxMCAxMjAgTDEwIDMwIFoiIGZpbGw9Im5vbmUiIHN0cm9rZT0idXJsKCNyaW5nKSIgc3Ryb2tlLXdpZHRoPSI3IiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PC9nPjwvc3ZnPg=="
FONT_LINK = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700;800&display=swap">'

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;font-family:Poppins,sans-serif;color:#fff;overflow:hidden;position:relative;background:#0B2545}
.bg{position:absolute;inset:0}
.brand{position:absolute;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:10px}
.brand img{width:96px}.brand span{font-weight:700;font-size:34px;letter-spacing:3px}
.y{color:#FFC93C}.g{color:#2BB673}
.gold{background:linear-gradient(180deg,#FFE9A8,#FFC93C 55%,#F5A623);-webkit-background-clip:text;background-clip:text;color:transparent}
.scene{position:absolute;left:70px;right:70px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:34px}
.kicker{font-weight:600;font-size:46px;letter-spacing:8px;color:#9FC3E8}
.huge{font-weight:800;font-size:170px;line-height:1}
.big{font-weight:700;font-size:92px;line-height:1.08}
.mid{font-weight:700;font-size:70px;line-height:1.12}
.sub{font-weight:500;font-size:46px;line-height:1.35;color:#D6E4F5}
.num{width:190px;height:190px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:120px;color:#0B2545;
 background:linear-gradient(180deg,#FFE28A,#FFC93C 50%,#F5A623);box-shadow:0 0 60px rgba(255,201,60,.45)}
.pill{padding:30px 60px;border-radius:999px;font-weight:700;font-size:50px;background:linear-gradient(180deg,#5BE39A,#14855A);box-shadow:0 14px 30px rgba(0,0,0,.4)}
.box{border:5px dashed #FFC93C;border-radius:40px;padding:36px 60px;background:#0A1F3D}
.card{background:#0F2E55;border:3px solid #1E5A9C;border-radius:40px;padding:44px 50px;width:100%}
.answer{background:rgba(14,58,58,.95);border-color:#2BB673}
.bar{position:absolute;left:0;bottom:0;height:12px;background:linear-gradient(90deg,#FFC93C,#2BB673)}
.page{position:absolute;right:60px;top:80px;font:600 28px Poppins,sans-serif;color:#BCD3EC;background:rgba(6,20,42,.6);padding:8px 18px;border-radius:999px}
.swipe{position:absolute;right:60px;bottom:60px;font:700 32px Poppins,sans-serif;color:#FFC93C}
@keyframes pop{from{opacity:0;transform:translateY(60px) scale(.96)}to{opacity:1;transform:none}}
@keyframes show{from{opacity:0}to{opacity:1}}
@keyframes out{from{opacity:1;transform:none}to{opacity:0;transform:translateY(-50px)}}
@keyframes grow{from{width:0}to{width:100%}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}
"""

# --------------------------------------------------------------------------
# Hintergründe (als SVG erzeugt, keine Bilddateien nötig)
# --------------------------------------------------------------------------
def bg_mast(H):
    def mast(x, s):
        return (f'<g transform="translate({x} {H}) scale({s})" stroke="{GOLD}" stroke-width="3" fill="none" opacity=".55">'
                '<path d="M-60 0 L-12 -520 L12 -520 L60 0 M-30 -260 L30 -260 M-45 -130 L45 -130 M-12 -520 L12 -440 '
                'M12 -520 L-12 -440 M-110 -440 L110 -440 M-80 -380 L80 -380 M-45 -130 L30 -260 M45 -130 L-30 -260"/></g>')
    base = H - 430
    wires = "".join(f'<path d="M0 {y} Q 270 {y+60} 540 {y+10} T 1080 {y+30}" stroke="{GOLD}" stroke-width="2" fill="none" opacity=".35"/>'
                    for y in (base, base + 60, base + 110))
    return (f'<svg class="bg" width="1080" height="{H}" viewBox="0 0 1080 {H}"><defs><linearGradient id="l" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{DEEP}"/><stop offset=".7" stop-color="#143E6E"/><stop offset="1" stop-color="#2D5E8F"/></linearGradient></defs>'
            f'<rect width="1080" height="{H}" fill="url(#l)"/>{mast(190, 1)}{mast(860, .75)}{wires}</svg>')

def bg_chip(H, seed=7):
    rnd = random.Random(seed); tr = ""
    for _ in range(int(34 * H / 1440)):
        x = rnd.choice(range(0, 1081, 40)); y = rnd.choice(range(0, H + 1, 40)); d = f"M{x} {y}"
        for _ in range(4):
            if rnd.random() < .5: x += rnd.choice([-1, 1]) * rnd.randint(2, 6) * 40
            else: y += rnd.choice([-1, 1]) * rnd.randint(2, 6) * 40
            d += f" L{x} {y}"
        tr += (f'<path d="{d}" stroke="#E8B53A" stroke-width="3" fill="none" opacity=".35"/>'
               f'<circle cx="{x}" cy="{y}" r="9" fill="none" stroke="#E8B53A" stroke-width="3" opacity=".5"/>')
    veil = ('<div class="bg" style="background:radial-gradient(ellipse at 50% 50%,rgba(6,20,42,.82) 0%,'
            'rgba(6,20,42,.55) 45%,rgba(6,20,42,0) 80%)"></div>')
    return f'<svg class="bg" width="1080" height="{H}" viewBox="0 0 1080 {H}"><rect width="1080" height="{H}" fill="#08223F"/>{tr}</svg>{veil}'

BACKGROUNDS = {"mast": bg_mast, "chip": bg_chip}

def page_html(H, bg, body, brand_top):
    return (f'<html><head><meta charset="utf-8">{FONT_LINK}<style>{CSS} body{{height:{H}px}}</style></head><body>'
            f'{BACKGROUNDS[bg](H)}'
            f'<div class="brand" style="top:{brand_top}px"><img src="{CREST}"><span>STROM DEAL <span class="y">24</span></span></div>'
            f'{body}</body></html>')

# --------------------------------------------------------------------------
# Bausteine (Text-Elemente)
# --------------------------------------------------------------------------
def kicker(t): return f'<div class="kicker">{t}</div>'
def huge(t):   return f'<div class="huge">{t}</div>'
def big(t):    return f'<div class="big">{t}</div>'
def mid(t):    return f'<div class="mid">{t}</div>'
def sub(t):    return f'<div class="sub">{t}</div>'
def num(n):    return f'<div class="num">{n}</div>'
def gold(t):   return f'<span class="gold">{t}</span>'
def checklist(*items):
    return '<div class="card"><div class="mid" style="font-size:58px;line-height:1.5;text-align:left">' + "<br>".join("✓ " + i for i in items) + '</div></div>'
def check_box(with_channel=True):
    return ('<div class="box"><div class="sub">Schreiben Sie uns</div><div class="big gold">„CHECK“</div>'
            + ('<div class="sub">per DM oder WhatsApp</div>' if with_channel else '') + '</div>')
CTA_REEL = [kicker("KOSTENLOS &amp; UNVERBINDLICH"), big("Energie-Check<br>" + gold("für Ihren Betrieb")), check_box()]

# --------------------------------------------------------------------------
# Reel-Renderer
# --------------------------------------------------------------------------
def reel_html(bg, scenes):
    t = 0; parts = []; total = sum(d for d, _ in scenes)
    for dur, items in scenes:
        start, end = t, t + dur; inner = ""
        for i, it in enumerate(items):
            d = start + 0.12 + i * 0.28
            extra = f",pulse 1.2s ease-in-out {d+0.6:.2f}s infinite" if 'class="num"' in it else ""
            inner += f'<div style="animation:pop .55s cubic-bezier(.2,.8,.2,1) {d:.2f}s both{extra}">{it}</div>'
        last = abs(end - total) < 0.01
        anim = f"show .01s {start:.2f}s both" + ("" if last else f",out .35s ease-in {end-0.35:.2f}s forwards")
        parts.append(f'<div class="scene" style="animation:{anim}">{inner}</div>'); t = end
    body = "".join(parts) + f'<div class="bar" style="animation:grow {total}s linear 0s both"></div>'
    return total, page_html(1920, bg, body, 150)

async def render_reel(page, name, bg, scenes, out, fps=30):
    total, html = reel_html(bg, scenes)
    await page.set_viewport_size({"width": 1080, "height": 1920})
    await page.set_content(html); await page.evaluate("document.fonts.ready"); await page.wait_for_timeout(300)
    frames = out / f"_frames_{name}"; frames.mkdir(parents=True, exist_ok=True)
    for i in range(int(total * fps)):
        await page.evaluate(f"document.getAnimations().forEach(a=>{{a.pause();a.currentTime={i*1000/fps}}})")
        await page.screenshot(path=str(frames / f"{i:04d}.jpg"), type="jpeg", quality=90)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(frames / "%04d.jpg"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", str(out / f"{name}.mp4")], check=True)
    shutil.rmtree(frames)
    print("Reel  ✓", out / f"{name}.mp4")

# --------------------------------------------------------------------------
# Karussell-Renderer
# --------------------------------------------------------------------------
def slide_html(bg, items, i, n):
    body = (f'<div class="scene" style="top:170px;bottom:{230 if bg=="mast" else 60}px;gap:30px">{"".join(items)}</div>'
            f'<div class="page">{i}/{n}</div>' + ('<div class="swipe">Weiter wischen →</div>' if i == 1 and n > 1 else ""))
    return page_html(1440, bg, body, 70).replace('.brand img{width:96px}', '.brand img{width:80px}')

async def render_carousel(page, name, bg, slides, out):
    await page.set_viewport_size({"width": 1080, "height": 1440}); n = len(slides)
    for i, items in enumerate(slides, 1):
        await page.set_content(slide_html(bg, items, i, n)); await page.evaluate("document.fonts.ready"); await page.wait_for_timeout(200)
        await page.screenshot(path=str(out / f"{name}_{i:02d}.png"))
    print(f"Karussell ✓ {name} ({n} Seiten)")

# Vorlagen für typische Karussell-Seiten
def s_title(k, line1, line2):         return [kicker(k), huge(line1).replace("huge\"", "huge\" style=\"font-size:130px\""), big(line2)]
def s_num(n, title, text):            return [num(n), big(title).replace("big\"", "big\" style=\"font-size:78px\""), sub(text).replace("sub\"", "sub\" style=\"font-size:44px\"")]
def s_qa(i, q, a, text):              return [kicker(f"FRAGE {i}"), big(f"„{q}“").replace("big\"", "big\" style=\"font-size:76px\""),
                                              f'<div class="card answer"><div class="big" style="color:#5BE39A">{a}</div><div class="sub" style="margin-top:10px">{text}</div></div>']
def s_cta(line):                      return [kicker("KOSTENLOS &amp; UNVERBINDLICH"), big(line), check_box()]

# ==========================================================================
# INHALTE  (Beispiel: Woche ab Mi 21.10.2026)
# ==========================================================================
REELS = {
    "Tag1_Reel_Zwei_Vertraege": ("chip", [
        (2.8, [kicker("STROM UND GAS?"), big("Zwei Verträge.<br>" + gold("Zwei Fristen."))]),
        (3.0, [mid("Zwei Rechnungen,<br>zwei Kündigungen,"), big(gold("doppelter Aufwand."))]),
        (3.2, [kicker("MIT UNS"), big("Ein Ansprechpartner<br>" + gold("für beides."))]),
        (3.2, [checklist("Strom geprüft", "Gas geprüft", "Fristen im Blick")]),
        (3.6, CTA_REEL)]),
    "Tag2_Reel_Winter": ("mast", [
        (2.8, [kicker("OKTOBER"), big("Der Winter<br>" + gold("kommt."))]),
        (3.0, [mid("Heizung an,<br>Licht länger an …"), big(gold("Verbrauch hoch."))]),
        (3.2, [big("Ist Ihr Vertrag<br>" + gold("bereit dafür?"))]),
        (3.2, [kicker("UNSER TIPP"), big("Jetzt prüfen,<br>" + gold("nicht im Januar."))]),
        (3.6, CTA_REEL)]),
    "Tag3_Reel_Nur_fuer_Grosse": ("chip", [
        (2.8, [kicker("WIR HÖREN OFT"), big("„Lohnt sich nur<br>" + gold("für große Firmen.“"))]),
        (2.6, [huge(gold("FALSCH."))]),
        (3.4, [mid("Auch Café, Bäckerei<br>oder Praxis zahlen oft"), big(gold("mehr als nötig."))]),
        (3.2, [mid("Und der Check<br>dauert nur"), big("ein Foto<br>" + gold("Ihrer Rechnung."))]),
        (3.6, CTA_REEL)]),
}

CAROUSELS = {
    "Tag1_Karussell_5_Anzeichen": ("mast", [
        s_title("SELBST-CHECK", "5 Anzeichen,", "dass Ihr Energievertrag<br>" + gold("nicht mehr passt.")),
        s_num(1, "Hohe Nachzahlung", "Die Jahresabrechnung war<br>eine böse Überraschung."),
        s_num(2, "Abschläge steigen", "Der monatliche Betrag<br>wurde mehrfach erhöht."),
        s_num(3, "Jahrelang nicht geprüft", "Der Vertrag läuft einfach<br>immer weiter."),
        s_num(4, "Vertragsende unbekannt", "Sie wissen nicht, wann<br>Sie wechseln könnten."),
        s_num(5, "Betrieb hat sich verändert", "Neue Geräte, mehr Personal,<br>längere Öffnungszeiten."),
        s_cta("Ein Punkt trifft zu?<br>" + gold("Wir prüfen das."))]),
    "Tag2_Karussell_Foerderung": ("chip", [
        [kicker("ANSCHAFFUNG GEPLANT?"), big("So holen Sie<br>" + gold("Förderung") + "<br>nicht zu spät.").replace("big\"", "big\" style=\"font-size:96px\"")],
        s_num(1, "Vorhaben klären", "Was soll angeschafft oder<br>modernisiert werden?"),
        s_num(2, "Förderung prüfen", "Welche Programme passen<br>zu Ihrem Vorhaben?"),
        s_num(3, "Erst Antrag, dann Auftrag", 'Sonst ist die Förderung<br>meist <span class="y">verloren</span>.'),
        s_cta("Wir prüfen das<br>" + gold("vorher für Sie."))]),
    "Tag3_Karussell_FAQ": ("mast", [
        s_title("FAQ", "4 Fragen,", "die wir " + gold("ständig") + " hören."),
        s_qa(1, "Kostet mich das etwas?", "Nein.", "Vergleich und Wechsel sind<br>für Sie kostenlos."),
        s_qa(2, "Fällt beim Wechsel der Strom aus?", "Nein.", "Ihre Versorgung läuft<br>ohne Unterbrechung weiter."),
        s_qa(3, "Muss ich selbst kündigen?", "Nein.", "Kündigung und Anmeldung<br>übernehmen wir."),
        s_qa(4, "Was brauchen Sie von mir?", "Ein Foto.", "Von Ihrer letzten<br>Strom- oder Gasrechnung."),
        s_cta("Noch Fragen?<br>" + gold("Schreiben Sie uns."))]),
}

# ==========================================================================
async def main():
    ap = argparse.ArgumentParser(description="Strom Deal 24 – Reels & Karussells rendern")
    ap.add_argument("--out", default="output"); ap.add_argument("--only"); ap.add_argument("--no-video", action="store_true")
    a = ap.parse_args(); out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    if not a.no_video and not shutil.which("ffmpeg"):
        sys.exit("ffmpeg nicht gefunden – bitte installieren oder mit --no-video starten.")
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(); page = await browser.new_page()
        for name, (bg, slides) in CAROUSELS.items():
            if not a.only or a.only == name: await render_carousel(page, name, bg, slides, out)
        if not a.no_video:
            for name, (bg, scenes) in REELS.items():
                if not a.only or a.only == name: await render_reel(page, name, bg, scenes, out)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
