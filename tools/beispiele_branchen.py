"""Strom Deal 24 – Rechenbeispiele nach Branche: 5 Reels + 5 Karussells.
Klar gekennzeichnete Beispielrechnungen (keine echten Kundenfälle), Preise können variieren.
Preisvorgabe Mohammed (22.10.2026): neuer Tarif 30–31 ct/kWh netto, Produktion 28 ct.
Aufruf: python3 beispiele_branchen.py OUTDIR [--no-video] [NAME ...]"""
import asyncio, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import stromdeal24_render as R
from stromdeal24_render import kicker, huge, big, mid, sub, gold, s_cta, CTA_REEL

def note(t, size=30):
    return f'<div class="sub" style="font-size:{size}px;color:#9FC3E8;line-height:1.3">{t}</div>'

HINWEIS = "Beispielrechnung – keine echte Kundenrechnung.<br>Preise können variieren. Netto, ohne Grundpreis."

def eur(x):
    return f"{x:,.0f}".replace(",", ".") + " €"

def kwh_s(k):
    return f"{k:,}".replace(",", ".") + " kWh"

def zahlen(kwh, alt, neu):
    a, n = kwh * alt / 100, kwh * neu / 100
    return a, n, a - n, round((a - n) / a * 100)

# ---------- Reels ----------
def reel(bg, branche, kwh, alt, neu, wofuer):
    a, n, d, p = zahlen(kwh, alt, neu)
    N = note(HINWEIS)
    return (bg, [
        (2.8, [kicker("RECHENBEISPIEL"), big(f"{branche}<br>" + gold("Was bringt ein Wechsel?"))]),
        (3.0, [kicker("DER BETRIEB"), big(gold(kwh_s(kwh))), sub(f"im Jahr – {wofuer}"), N]),
        (3.0, [kicker("ALTER TARIF"), mid(f"{alt} ct/kWh"), big(gold(eur(a) + " / Jahr")), N]),
        (3.0, [kicker("NEUER TARIF"), mid(f"{neu} ct/kWh"), big(gold(eur(n) + " / Jahr")), N]),
        (3.6, [kicker("ERSPARNIS IM BEISPIEL"), huge(gold(eur(d))), sub(f"pro Jahr – rund {p} %"), N]),
        (3.8, CTA_REEL + [N])])

REELS = {
    "BB_Reel_Cafe":       reel("chip", "Café", 20000, 37, 30, "Kaffeemaschine, Kühlung, Licht"),
    "BB_Reel_Baeckerei":  reel("mast", "Bäckerei", 80000, 37, 30, "Backöfen, Kühlräume"),
    "BB_Reel_Restaurant": reel("chip", "Restaurant", 50000, 38, 31, "Küche, Lüftung, Kühlung"),
    "BB_Reel_Apotheke":   reel("mast", "Apotheke", 30000, 37, 30, "Medikamenten-Kühlung, Licht"),
    "BB_Reel_Produktion": reel("chip", "Produktion", 150000, 34, 28, "Maschinen, Druckluft"),
}

# ---------- Karussells ----------
def karussell(bg, branche, kwh, alt, neu, wofuer):
    a, n, d, p = zahlen(kwh, alt, neu)
    N = note(HINWEIS, 28)
    return (bg, [
        [kicker("RECHENBEISPIEL"), huge(branche).replace('huge"', 'huge" style="font-size:120px"'), big("Was bringt ein<br>" + gold("Anbieterwechsel?")), N],
        [kicker("DER BETRIEB"), big(gold(kwh_s(kwh))), sub(f"Verbrauch im Jahr –<br>{wofuer}"), N],
        [kicker("ALTER TARIF"), mid(f"{alt} ct/kWh"), big(gold(eur(a))), sub("pro Jahr"), N],
        [kicker("NEUER TARIF"), mid(f"{neu} ct/kWh"), big(gold(eur(n))), sub("pro Jahr"), N],
        [kicker("ERSPARNIS IM BEISPIEL"), huge(gold(eur(d))), sub(f"pro Jahr – rund {p} %"), N],
        s_cta("Wie viel ist es<br>" + gold("bei Ihnen?")) + [N]])

CAROUSELS = {
    "BB_Karussell_Friseur":   karussell("mast", "Friseursalon", 15000, 38, 31, "Föhne, Warmwasser, Licht"),
    "BB_Karussell_Werkstatt": karussell("chip", "Kfz-Werkstatt", 25000, 37, 30, "Hebebühnen, Kompressor, Licht"),
    "BB_Karussell_Spaeti":    karussell("mast", "Späti", 18000, 38, 31, "Kühlschränke rund um die Uhr"),
    "BB_Karussell_Praxis":    karussell("chip", "Arztpraxis", 20000, 37, 31, "Geräte, IT, Klima"),
    "BB_Karussell_Fitness":   karussell("mast", "Fitnessstudio", 60000, 37, 30, "Licht, Lüftung, Duschen"),
}

async def run(out, names, video):
    from playwright.async_api import async_playwright
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); page = await b.new_page()
        for k, (bg, sl) in CAROUSELS.items():
            if not names or k in names: await R.render_carousel(page, k, bg, sl, out)
        if video:
            for k, (bg, sc) in REELS.items():
                if not names or k in names: await R.render_reel(page, k, bg, sc, out)
        await b.close()

if __name__ == "__main__":
    args = sys.argv[2:]; video = "--no-video" not in args
    asyncio.run(run(sys.argv[1], [a for a in args if not a.startswith("--")], video))
