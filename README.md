
### FUNKTIONIERT NUR UNTER PYTHON 2.7 VOLLSTÄNDIG
Link zum Download: https://www.python.org/downloads/release/python-2718/

## Funktion
Das vorliegende Programm wird zu einer teilweisen Benutzung des Clouddienstes Evernote benutzt.
Hierbei ist zu beachten, dass sich die Benutzung rein auf die Kommandozeile beschränkt.


Mittels des Programms können Evernote-Nutzer ihre erstellten Notes herunterladen und auf Wunsch zippen und/oder verschlüsseln.
Auch können direkt neue Benutzer angelegt werden, oder Einstellungen wie z.B. das Passwort von einem bestehenden Account abgeändert werden.
Direkt Notes schreiben ist nicht möglich, da das Programm eine Art Backup von bereits vorhandenen Daten macht.

## Installation
Vor der Installation muss sichergestellt werden, dass Python und das Paketverwaltungsprogramm PIP installiert ist. 
Im Anschluss werden die benötigten Bibliotheken mittels des Kommandos ``python -m pip install -r requirements.txt`` installiert.
Um das Programm schlussendlich auszuführen, navigiert man in den Dateipfad der "python.exe" und gibt den Befehl 
``evernote_cli.py``
ein.

## Benutzung
Um nun die Daten eines bereits bestehenden Kontos herunterzuladen, wird folgender Befehl benutzt: 

``python.exe evernote_cli.py -u <Username> -p <Passwort> -d``

Ist kein Konto vorhanden, ändert sich der Befehl wie folgt:

``python.exe evernote_cli.py -u <Username> -n <Passwort> ``

