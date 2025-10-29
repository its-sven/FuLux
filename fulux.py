#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# ==== Konfiguration ====
url = "https://www.aral.de/de_lu/luxembourg/home/kraftstoffe-und-preise/aktuelle-kraftstoffpreise.html"
log_folder = "tmp/aral_logs"  # Ordner für Logs
os.makedirs(log_folder, exist_ok=True)

# ==== Farben und Emojis ====
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
UP = "🔺"
DOWN = "🔻"

# ==== HTML holen ====
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# ==== Datum der Preisgültigkeit extrahieren ====
footer_text = soup.find(string=lambda t: t and "Preise gültig ab" in t)
if footer_text:
    footer_text = footer_text.strip()
else:
    footer_text = "Datum der Preisgültigkeit nicht gefunden"

# ==== Tabelle extrahieren ====
rows = []
for tr in soup.select("table tr")[1:]:
    cols = [c.get_text(strip=True).replace('\xa0', ' ') for c in tr.find_all("td")]
    if len(cols) == 4:
        rows.append(cols)

headers = ["Kraftstoff", "mit MwSt.", "ohne MwSt.", "MwSt.-Satz"]

# ==== Breiten für Formatierung ====
col_widths = [max(len(row[i]) for row in rows + [headers]) for i in range(len(headers))]

# ==== Funktion für formatierte Zeile mit Farben ====
def fmt_row(row, prev_row=None):
    line = ""
    for i, val in enumerate(row):
        padded = val.ljust(col_widths[i])
        # Preisänderung anzeigen (nur für Preis mit MwSt.)
        if prev_row and i == 1:
            try:
                current = float(val.replace("€","").replace(",","").replace(".","").strip()) / 1000
                prev = float(prev_row[i].replace("€","").replace(",","").replace(".","").strip()) / 1000
                if current > prev:
                    padded = f"{RED}{padded} {UP}{RESET}"
                elif current < prev:
                    padded = f"{GREEN}{padded} {DOWN}{RESET}"
            except:
                pass
        line += padded
        if i < len(row)-1:
            line += " | "
    return line

# ==== Ausgabe in Konsole ====
print(f"{YELLOW}{footer_text}{RESET}")
print(fmt_row(headers))
print("-" * (sum(col_widths) + 3*(len(headers)-1)))
for r in rows:
    print(fmt_row(r))

# ==== Ausgabe auch als Logdatei ====
log_file = os.path.join(log_folder, f"aral_prices_{datetime.now():%Y-%m-%d}.log")
with open(log_file, "w", encoding="utf-8") as f:
    f.write(f"{footer_text}\n")
    f.write(fmt_row(headers) + "\n")
    f.write("-" * (sum(col_widths) + 3*(len(headers)-1)) + "\n")
    for r in rows:
        f.write(fmt_row(r) + "\n")

print(f"\nLog gespeichert in: {log_file}")
