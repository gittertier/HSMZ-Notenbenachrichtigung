# HSMZ-Notenbenachrichtigung über Discord Webhooks


## Funktion
Das Programm beruht darauf, dass eine Leistung auf dem CIM im Reiter Leistungen gelistet ist.

Hierbei wird nicht geprüft, ob die Leistung schon fertig eingetragen ist oder die Eingabe noch läuft. Aus Erfahrung spielt das keine Rolle, über das PDF ist die Note immer bereits einsehbar. 

## Nutzung

### Installation
Repository klonen:
```bash
git clone https://github.com/gittertier/HSMZ-Notenbenachrichtigung
```
Erstellen des virtual environments:
```bash
python -m venv .venv
```
Virtual environment aktivieren:
```bash
source .venv/bin/activate
```
Nötige Packages installieren (innerhalb des virtual environment):
```bash
pip install -r requirements.txt

```

### Konfiguration
Nutzernamen, Paswort und Webhook URL im `config.json` eintragen.

### Ausführen
Das Programm lässt sich nun mit `python main.py` ausführen.

Wichtig: Sicherstellen dass das Programm die Rechte hat Dateien zu schreiben.

### Cronjob erstellen
Damit das Programm auch regelmäßig läuft kann ein Cronjob erstellt werden, idealerweise läuft das Programm so alle bspw. 5 Minuten auf einem Raspberry Pi oder einem Server.
Cronjob editor öffnen:
```bash
crontab -e
```
Hinzufügen folgender Zeile (für alle 5 Minuten, bei Bedarf Zahl anpassen):
```
*/5 * * * * cd /path/to/dir/ && /path/to/dir/.venv/bin/python /path/to/dir/main.py
```
