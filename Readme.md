Python downloaden und installieren: https://www.python.org/downloads/

Im Installer die Option "Add Python to PATH" aktivieren!


Wenn installiert ❖ (windows key) + r -> cmd (enter) -> pip (enter)

Wenn hier eine Auflistung von Parametern erscheint war alles richtig. Falls nicht im Installer gucken.
Ansonsten google -> Add Python to PATH

Jetzt die Befehle in windows CMD eingeben:

```pip install cryptography```
```pip install pandas```


Jetzt kannst du den Passwort Manager öffnen.


Um Optionen auszuwählen muss du die Zahl eingeben und dann enter.


Bei der Option 1 versucht der Manager als erstes von einer encrypted Datei zu lesen. Falls diese nicht
existent ist, kannst du entweder eine neue Datenbank anlegen oder, sofern existent, die clean bzw. demo Datei
verschlüsseln.

Die Demo Datei kannst du mit Option 3 anlegen. Danach kannst du sie entweder über Option 1 oder 3 verschlüsseln.
Hier musst du ein Master Passwort eingeben. Dies ist das Passwort womit alle Passwörter entschlüsselt werden können.
Pass also auf, dass du dieses Passwort nirgends anders benutzt, da es sonst die Möglichkeit gibt, dass alle deine
Passwörter abrufbar sind (sofern der Hacker den Manager, die encrypted Datei und dein Passwort besitzt).

Nachdem dies geschen ist kannst du die abgebildeten Optionen durchführen.

Wenn du ein Passwort festlegst kannst du mit "r" ein zufälliges mit der Standardlänge festlegen. Mit "r 64" kannst 
du ein 64 Stellen langes Passwort erstellen.

Mit "c" kannst du (in den meisten Fällen) das angezeigte Passwort kopieren.
-> Achtung: Ab und zu werden die Passwörter mit "{Passwort}" in die Zwischenablage kopiert.

Wenn du etwas verändert hast musst du wieder eine verschlüsselte Datei erstellen um die Änderungen zu übernehmen.


Geheime Passwörter kannst du abrufen indem du das geheime Passwort entweder beim Eingeben des Passwortes eingibst
-> gelbes Passwort wurde nicht erkannt statt rot
oder während des Hauptloops, also Pass auslesen, Pass aktualisieren, ...

Veränderbare Einstellungen:

Die Optionen sind ganz oben im Passwort Manager. Sie hier zu ändern bringt nichts.


Hier kannst du die Dateinamen festlegen:

clean_file = "Pass.clean"
encrypted_file = "Pass.encrypted"
demo_file = "Pass.demo"


Hier kannst du einstellen welche Charaktere in dem zufälligen Passwort erlaubt sind
-> # kommentiert etwas
-> Entweder als Liste oder als String von "abc"

random_password = string.printable[:94]

# random_password = ["a", "b", "c"]


Hier kannst du die Standardlänge eines zufälligen Passworts anpassen

random_length = 16


Die Passwörter um auf geheime Passwörter zugreifen zu können

geheime_passwörter = ["1234"]


Hier kannst du das Salt zur Hashung verändern. Ist zu empfehlen aber nicht notwendig. Siehe Doc in .py

salt = b"""{...}"""


Anzahl Iterationen für das Hashen. Hier empfiehlt sich ~0.5s (mit Stoppuhr messen)

iterations = 10**6