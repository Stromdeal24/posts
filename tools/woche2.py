"""Strom Deal 24 – Woche 2 (Mo 26.10. – Fr 30.10.2026). Design: stromdeal24_render.py"""
import asyncio, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import stromdeal24_render as R
from stromdeal24_render import kicker, huge, big, mid, sub, num, gold, checklist, s_title, s_num, s_qa, s_cta, CTA_REEL

def mythos(i, q, a, text):
    s = s_qa(i, q, a, text)
    s[0] = kicker(f"MYTHOS {i}")
    return s

R.REELS = {
    "W2_Mo_Reel_Grundversorgung": ("mast", [
        (2.8, [kicker("KURZE FRAGE"), big("Noch in der<br>" + gold("Grundversorgung?"))]),
        (3.0, [mid("Dann zahlen Sie<br>wahrscheinlich"), big(gold("zu viel."))]),
        (3.2, [mid("Sonderverträge sind<br>in der Regel"), big(gold("günstiger."))]),
        (3.2, [kicker("GUTE NACHRICHT"), big("Raus kommen Sie<br>" + gold("in 2 Wochen."))]),
        (3.6, CTA_REEL)]),
    "W2_Di_Reel_Preiserhoehung": ("chip", [
        (2.8, [kicker("POST VOM VERSORGER?"), big("Preiserhöhung<br>" + gold("angekündigt?"))]),
        (3.0, [mid("Dann haben Sie<br>in der Regel ein"), big(gold("Sonder-<br>kündigungsrecht."))]),
        (3.2, [mid("Aber Achtung:"), big("Kündigen bis zum<br>" + gold("Stichtag."))]),
        (3.2, [kicker("UNSER TIPP"), big("Brief nicht liegen<br>lassen – " + gold("prüfen."))]),
        (3.6, CTA_REEL)]),
    "W2_Mi_Reel_Verlaengert": ("chip", [
        (2.8, [kicker("SCHON PASSIERT?"), big("Vertrag einfach<br>" + gold("weitergelaufen?"))]),
        (3.0, [mid("Frist verpasst?<br>Dann oft"), big(gold("automatisch verlängert."))]),
        (3.2, [mid("Und oft zu Preisen,<br>die längst"), big(gold("nicht mehr passen."))]),
        (3.2, [checklist("Vertragsende notiert", "Frist im Kalender", "Rechtzeitig verglichen")]),
        (3.6, CTA_REEL)]),
    "W2_Do_Reel_Nachts": ("mast", [
        (2.8, [kicker("FEIERABEND?"), big("Ihr Zähler<br>" + gold("nicht."))]),
        (3.0, [mid("Kühlung, Rechner,<br>Licht, Standby …"), big(gold("laufen weiter."))]),
        (3.2, [big("Wissen Sie, was<br>" + gold("nachts läuft?"))]),
        (3.2, [kicker("UNSER TIPP"), big("Verbrauch senken<br>" + gold("und Tarif prüfen."))]),
        (3.6, CTA_REEL)]),
    "W2_Fr_Reel_Gewerbe": ("chip", [
        (2.8, [kicker("FÜR SELBSTSTÄNDIGE"), big("Gewerbe ist<br>" + gold("nicht privat."))]),
        (3.0, [mid("Anderer Verbrauch,<br>andere Zeiten,"), big(gold("andere Tarife."))]),
        (3.2, [mid("Viele Betriebe laufen<br>trotzdem im"), big(gold("falschen Tarif."))]),
        (3.2, [kicker("MIT UNS"), big("Ein Tarif, der<br>" + gold("zu Ihrem Betrieb passt."))]),
        (3.6, CTA_REEL)]),
}

R.CAROUSELS = {
    "W2_Mo_Karussell_Wechsel": ("chip", [
        s_title("ANBIETERWECHSEL", "4 Schritte,", "so einfach ist " + gold("der Wechsel.")),
        s_num(1, "Foto schicken", "Ihre letzte Strom- oder<br>Gasrechnung per DM."),
        s_num(2, "Wir vergleichen", "Passende Tarife für Ihren<br>Verbrauch und Betrieb."),
        s_num(3, "Sie entscheiden", "Erst wenn das Angebot passt,<br>geht es weiter."),
        s_num(4, "Wir erledigen den Rest", "Kündigung und Anmeldung –<br>ohne Unterbrechung."),
        s_cta("Bereit für den Wechsel?<br>" + gold("Wir prüfen das."))]),
    "W2_Di_Karussell_Rechnung": ("mast", [
        s_title("RECHNUNG VERSTEHEN", "4 Angaben,", "auf die es " + gold("wirklich ankommt.")),
        s_num(1, "Verbrauch in kWh", "So viel Energie hat Ihr<br>Betrieb im Jahr gebraucht."),
        s_num(2, "Arbeitspreis", "Was Sie pro Kilowattstunde<br>bezahlen."),
        s_num(3, "Grundpreis", "Der feste Betrag –<br>egal wie viel Sie verbrauchen."),
        s_num(4, "Vertragsende & Frist", "Wann Sie spätestens<br>kündigen müssen."),
        s_cta("Rechnung zur Hand?<br>" + gold("Wir lesen mit."))]),
    "W2_Mi_Karussell_Mythen": ("chip", [
        s_title("ANBIETERWECHSEL", "3 Mythen,", "die Sie " + gold("Geld kosten.")),
        mythos(1, "Beim Grundversorger bin ich sicherer.", "Falsch.", "Auch bei Problemen des<br>Anbieters fließt der Strom weiter."),
        mythos(2, "Ich brauche einen neuen Zähler.", "Nein.", "Ihr Zähler bleibt,<br>wie er ist."),
        mythos(3, "Lohnt sich nur bei viel Verbrauch.", "Falsch.", "Auch kleine Betriebe<br>zahlen oft zu viel."),
        s_cta("Klingt gut?<br>" + gold("Wir prüfen das."))]),
    "W2_Do_Karussell_Stromfresser": ("mast", [
        s_title("ENERGIE SPAREN", "4 Bereiche,", "in denen " + gold("Strom versickert.")),
        s_num(1, "Kühlung", "Läuft rund um die Uhr –<br>alte Geräte besonders viel."),
        s_num(2, "Beleuchtung", "Alte Leuchtmittel brauchen<br>deutlich mehr Strom als LED."),
        s_num(3, "Standby", "Geräte, die nachts<br>nie ganz ausgehen."),
        s_num(4, "Alte Maschinen", "Neue Geräte sind sparsamer –<br>oft sogar mit Förderung."),
        s_cta("Tarif und Förderung?<br>" + gold("Wir prüfen beides."))]),
    "W2_Fr_Karussell_Umzug": ("chip", [
        s_title("NEUER STANDORT?", "Umzug,", "aber " + gold("an Energie gedacht?")),
        s_num(1, "Zählerstand notieren", "Am alten und am neuen<br>Standort – mit Foto."),
        s_num(2, "Vertrag rechtzeitig klären", "Sonst landen Sie oft in der<br>teuren Grundversorgung."),
        s_num(3, "Verbrauch neu einschätzen", "Neue Fläche, neue Geräte –<br>neuer Bedarf."),
        s_cta("Umzug geplant?<br>" + gold("Wir kümmern uns."))]),
}

if __name__ == "__main__":
    asyncio.run(R.main())
