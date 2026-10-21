"""Strom Deal 24 – Woche 2 (Mo 26.10. – Fr 30.10.2026). Design: stromdeal24_render.py
Themen gegen content-log.md geprüft (keine Wiederholung von Woche 1 und den Posts vom 6.–15.10.)."""
import asyncio, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import stromdeal24_render as R
from stromdeal24_render import kicker, huge, big, mid, sub, num, gold, checklist, s_title, s_num, s_qa, s_cta, CTA_REEL

def mythos(i, q, a, text):
    s = s_qa(i, q, a, text)
    s[0] = kicker(f"MYTHOS {i}")
    return s

R.REELS = {
    "W2_Mo_Reel_Bonus": ("mast", [
        (2.8, [kicker("VORSICHT"), big("Hoher<br>" + gold("Neukundenbonus?"))]),
        (3.0, [mid("Im ersten Jahr<br>sieht alles"), big(gold("günstig aus."))]),
        (3.2, [mid("Ab dem zweiten Jahr<br>zahlen Sie oft"), big(gold("drauf."))]),
        (3.2, [kicker("UNSER TIPP"), big("Auf die Kosten<br>" + gold("nach dem Bonus") + " achten.")]),
        (3.6, CTA_REEL)]),
    "W2_Di_Reel_Preiserhoehung": ("chip", [
        (2.8, [kicker("POST VOM VERSORGER?"), big("Preiserhöhung<br>" + gold("angekündigt?"))]),
        (3.0, [mid("Dann haben Sie<br>in der Regel ein"), big(gold("Sonder-<br>kündigungsrecht."))]),
        (3.2, [mid("Aber Achtung:"), big("Kündigen bis zum<br>" + gold("Stichtag."))]),
        (3.2, [kicker("UNSER TIPP"), big("Brief nicht liegen<br>lassen – " + gold("prüfen."))]),
        (3.6, CTA_REEL)]),
    "W2_Mi_Reel_Oekostrom": ("chip", [
        (2.8, [kicker("NACHHALTIG?"), big("Ökostrom für<br>" + gold("Ihren Betrieb?"))]),
        (3.0, [mid("Viele denken:"), big("„Das ist doch<br>" + gold("viel teurer.“"))]),
        (3.2, [mid("Oft ist der Unterschied"), big(gold("kleiner als gedacht."))]),
        (3.2, [kicker("UND IHRE KUNDEN"), big("achten immer<br>" + gold("mehr darauf."))]),
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
    "W2_Mo_Karussell_Preisgarantie": ("chip", [
        s_title("GUT ZU WISSEN", "Preisgarantie", "ist nicht gleich " + gold("Preisgarantie.")),
        s_num(1, "Volle Preisgarantie", "Der Preis bleibt fest –<br>bis auf ganz wenige Ausnahmen."),
        s_num(2, "Eingeschränkte Garantie", "Steuern und Abgaben<br>können trotzdem steigen."),
        s_num(3, "Keine Garantie", "Der Preis kann sich<br>jederzeit ändern."),
        s_cta("Was steht in Ihrem Vertrag?<br>" + gold("Wir prüfen das."))]),
    "W2_Di_Karussell_Vergleich": ("mast", [
        s_title("ANGEBOTE VERGLEICHEN", "4 Punkte,", "die " + gold("wirklich zählen.")),
        s_num(1, "Kosten ohne Bonus", "Was zahlen Sie,<br>wenn der Bonus weg ist?"),
        s_num(2, "Laufzeit", "Wie lange sind Sie<br>gebunden?"),
        s_num(3, "Kündigungsfrist", "Wie früh müssen Sie<br>Bescheid geben?"),
        s_num(4, "Abschlag", "Passt der monatliche Betrag<br>zu Ihrem Verbrauch?"),
        s_cta("Zu viele Angebote?<br>" + gold("Wir vergleichen für Sie."))]),
    "W2_Mi_Karussell_Mythen": ("chip", [
        s_title("ANBIETERWECHSEL", "3 Mythen,", "die Sie " + gold("Geld kosten.")),
        mythos(1, "Der billigste Tarif ist immer der beste.", "Nicht immer.", "Laufzeit, Preisgarantie und<br>Bedingungen zählen mit."),
        mythos(2, "Ich brauche einen neuen Zähler.", "Nein.", "Ihr Zähler bleibt,<br>wie er ist."),
        mythos(3, "Ein Wechsel dauert ewig.", "Falsch.", "Der Wechsel selbst<br>geht heute schnell."),
        s_cta("Klingt gut?<br>" + gold("Wir prüfen das."))]),
    "W2_Do_Karussell_Stromfresser": ("mast", [
        s_title("ENERGIE SPAREN", "4 Bereiche,", "in denen " + gold("Strom versickert.")),
        s_num(1, "Kühlung", "Läuft rund um die Uhr –<br>alte Geräte besonders viel."),
        s_num(2, "Beleuchtung", "Alte Leuchtmittel brauchen<br>deutlich mehr Strom als LED."),
        s_num(3, "Standby", "Geräte, die nachts<br>nie ganz ausgehen."),
        s_num(4, "Alte Maschinen", "Neue Geräte sind sparsamer –<br>oft sogar mit Förderung."),
        s_cta("Tarif und Förderung?<br>" + gold("Wir prüfen beides."))]),
    "W2_Fr_Karussell_Team": ("chip", [
        s_title("FÜRS TEAM", "4 Spartipps,", "die " + gold("jeder umsetzen kann.")),
        s_num(1, "Licht aus", "In Lager, Toilette und Büro,<br>wenn keiner drin ist."),
        s_num(2, "Ganz ausschalten", "Steckerleiste statt Standby –<br>vor allem am Wochenende."),
        s_num(3, "Richtig lüften", "Kurz und kräftig statt<br>Fenster stundenlang gekippt."),
        s_num(4, "Kühlung zu", "Türen von Kühlschrank und<br>Kühltheke nicht offen lassen."),
        s_cta("Sparen ist das eine.<br>" + gold("Der Tarif das andere."))]),
}

if __name__ == "__main__":
    asyncio.run(R.main())
