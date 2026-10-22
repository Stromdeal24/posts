"""Strom Deal 24 – Rechenbeispiele nach Branche (Tarif + Förderung).
Werte = klar gekennzeichnete Beispielrechnungen, keine echten Kundenfälle.
Quellen (Stand Okt. 2026): Gewerbestrom Neukunden Ø ca. 24,6 ct/kWh netto (stromvermittlung.de, 01.10.2026),
Grundversorgung Ø 40,39 ct/kWh brutto ≈ 34 ct netto (stromauskunft.de, 22.10.2026),
Stromsteuer 2,05 → 0,05 ct/kWh für produzierendes Gewerbe, auf Antrag, Frist 31.12. Folgejahr (Vattenfall),
EBN 50 % bis 3.000 € (Energiekosten > 10.000 €/Jahr), EEW Modul 1 bis 25 % für kleine Unternehmen, min. 2.000 € Invest, Antrag vor Beginn.
Aufruf: python3 rechenbeispiele.py OUTDIR [NAME ...]"""
import asyncio, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import stromdeal24_render as R
from stromdeal24_render import kicker, huge, big, mid, sub, gold, CTA_REEL

def note(t):
    return f'<div class="sub" style="font-size:30px;color:#9FC3E8;line-height:1.3">{t}</div>'

NOTE = note("Beispielrechnung, keine echte Kundenrechnung.<br>Netto-Arbeitspreise, ohne Grundpreis.")
NOTE_F = note("Beispielrechnung. Förderung nur bei Erfüllung<br>der Voraussetzungen und auf Antrag.")

def eur(x):
    return f"{x:,.0f}".replace(",", ".") + " €"

def tarif(bg, branche, kwh, alt, neu):
    a, n = kwh * alt / 100, kwh * neu / 100
    pct = round((a - n) / a * 100)
    kw = f"{kwh:,}".replace(",", ".")
    return (bg, [
        (2.8, [kicker("RECHENBEISPIEL"), big(f"{branche} mit<br>" + gold(f"{kw} kWh") + " im Jahr")]),
        (3.0, [kicker("ALTER TARIF"), mid(f"{alt} ct/kWh"), big(gold(eur(a) + " / Jahr"))]),
        (3.0, [kicker("NEUER TARIF"), mid(f"{neu} ct/kWh"), big(gold(eur(n) + " / Jahr"))]),
        (3.6, [kicker("ERSPARNIS"), huge(gold(eur(a - n))), sub(f"pro Jahr – rund {pct} %"), NOTE]),
        (3.8, CTA_REEL + [NOTE])])

REELS = {
    "RB_Cafe":       tarif("chip", "Café", 20000, 34, 28),
    "RB_Baeckerei":  tarif("mast", "Bäckerei", 80000, 33, 27),
    "RB_Restaurant": tarif("chip", "Restaurant", 50000, 34, 28),
    "RB_Apotheke":   tarif("mast", "Apotheke", 30000, 33, 27),
    "RB_Friseur":    tarif("chip", "Friseursalon", 15000, 34, 28),
    "RB_Produktion": tarif("mast", "Produktion", 150000, 30, 25),

    "FB_Baeckerei_Stromsteuer": ("chip", [
        (2.8, [kicker("FÖRDER-RECHENBEISPIEL"), big("Bäckerei mit<br>" + gold("80.000 kWh"))]),
        (3.0, [mid("Bäckereien zählen zum"), big(gold("produzierenden Gewerbe."))]),
        (3.2, [mid("Stromsteuer: statt 2,05 ct<br>nur noch"), big(gold("0,05 ct/kWh."))]),
        (3.6, [kicker("ZURÜCK VOM STAAT"), huge(gold("1.600 €")), sub("pro Jahr – auf Antrag"), NOTE_F]),
        (3.4, [kicker("ACHTUNG"), big("Ohne Antrag<br>" + gold("gibt es nichts.")), sub("Für 2026: Antrag bis 31.12.2027")]),
        (3.8, CTA_REEL)]),
    "FB_Schreinerei_Stromsteuer": ("mast", [
        (2.8, [kicker("FÖRDER-RECHENBEISPIEL"), big("Schreinerei mit<br>" + gold("150.000 kWh"))]),
        (3.0, [mid("Produzierendes Handwerk<br>zahlt seit 2026"), big(gold("fast keine Stromsteuer."))]),
        (3.2, [mid("2 ct pro kWh"), big(gold("zurück vom Staat."))]),
        (3.6, [kicker("ERGEBNIS"), huge(gold("3.000 €")), sub("pro Jahr – auf Antrag"), NOTE_F]),
        (3.8, CTA_REEL)]),
    "FB_Restaurant_Energieberatung": ("chip", [
        (2.8, [kicker("FÖRDER-RECHENBEISPIEL"), big("Restaurant mit<br>" + gold("hohen Energiekosten?"))]),
        (3.0, [mid("Eine Energieberatung<br>zeigt, wo"), big(gold("Geld versickert."))]),
        (3.2, [mid("Kosten der Beratung:"), big("4.000 €")]),
        (3.6, [kicker("DER STAAT ZAHLT"), huge(gold("50 %")), sub("hier 2.000 € – bis zu 3.000 € möglich"), NOTE_F]),
        (3.8, CTA_REEL)]),
    "FB_Produktion_Anlage": ("mast", [
        (2.8, [kicker("FÖRDER-RECHENBEISPIEL"), big("Alte Anlage<br>" + gold("frisst Strom?"))]),
        (3.0, [mid("Neue, effiziente Anlage<br>Investition:"), big("20.000 €")]),
        (3.4, [kicker("ZUSCHUSS"), huge(gold("bis 25 %")), sub("für kleine Unternehmen – hier bis 5.000 €"), NOTE_F]),
        (3.2, [kicker("WICHTIG"), big("Erst Antrag,<br>" + gold("dann Auftrag."))]),
        (3.8, CTA_REEL)]),
}

async def run(out, names):
    from playwright.async_api import async_playwright
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); page = await b.new_page()
        for n in names:
            bg, scenes = REELS[n]
            await R.render_reel(page, n, bg, scenes, out)
        await b.close()

if __name__ == "__main__":
    asyncio.run(run(sys.argv[1], sys.argv[2:] or list(REELS)))
