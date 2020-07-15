Python downloaden und installieren: https://www.python.org/downloads/

Im Installer die Option "Add Python to PATH" aktivieren!


Wenn installiert ❖ (windows key) + r -> cmd (enter) -> pip (enter)

Wenn hier eine Auflistung von Parametern erscheint war alles richtig. Falls nicht im Installer gucken.
Ansonsten google -> Add Python to PATH


Jetzt die Befehle in windows CMD eingeben:

```pip install cryptography```

```pip install pynput```


Jetzt kannst du den Passwort Manager öffnen.


Tutorial:
─────────────────────────────────────────────────────────────────────────
"Passwort Manager.py" öffnen

2 Möglichkeiten: Demo oder Echte Datenbank.

Echte Datenbank:
start -> 1 (Passwort eingeben) -> 3 (Eine neue Datenbank anlegen)

1 (Passwort auslesen):
Ein Passwort auslesen

2 (Passwort aktualisieren):
Ein Passwort aktualisieren
Falls mehrere Passwörter mit dem gleichen Namen: Auswählen

3 (Passwort hinzufügen):
Ein Passwort hinzufügen
Falls mehrere Passwörter mit dem gleichen Namen: Entweder:
	1 - Einen neuen Eintrag unter dem gleichen Namen anlegen
	2 - Einen Eintrag aktualisieren
	3 - Alle löschen und neuer Eintrag

4 (Passwort löschen):
Ein Passwort löschen mit Bestätigung: `"j", "ja", "y"` etc. Kann angepasst werden.

5 (Letztes Passwort eingeben):
Das letzte Passwort mit einem bestimmten Hotkey (veränderbar)
eingeben lassen. Ist besser, da das Passwort nicht in die Zwischenablage kopiert wird.

6 (Verschlüsselte Datei aus aktuellem Passwort erstellen):
Verschlüsselte Datei erstellen. Aktuelles Passwort heißt alle Passwörter, 
die während der Ausführung geladen und verändert wurden

7 (Textdatei aus aktuellem Passwort erstellen):
Textdatei aus aktuellen Passwörtern erstellen (siehe 6)

8 (Verschlüsselte Datei aus {clean_datei} erstellen):
Verschlüsselte Datei aus der Entschlüsselten Datei erstellen


Bei einer Veränderung immer dran denken 6 auszuführen um eine neue verschlüsselte Datei
zu erstellen -> Die Änderungen werden sonst nicht übernommen


Unterfunktionen:

Wenn ein Passwort eingegeben wird gibt es:
Nach typen filtern (modell von typ: partial, overlapping) mit
```filter typ```

Suchattribut von Name auf ein beliebiges Attribut - z.B. auf "email" 
(groß-kleinschreibung wird nicht beachtet) -> sehen wo die gleiche email verwendet wurde

Das Suchattribut approximieren -> Best-fit

Wenn sich das Symbol @ in dem Suchstring befindet und select nicht gesetzt wurde werden
alle Passwörter mit "email" als typ gefiltert und select wird auf "email" gesetzt.

mit der Kombination "show all" kann man alle verfügbaren Passwörter anzeigen lassen


Geheim:
Alle Passwörter haben ein Attribut names "geheim". Dieses Attribut ist dafür da
die Passwörter unsichtbar zu machen. Sie werden aber nicht extra gesichert, bietet
also keine extra Sicherheit.
Alle geheimen Passwörter können wieder angezeigt werden, wenn man im Hauptmenü
die Kombination "1234" eingibt (veränderbar). 


Bei der Eingabe eines Passwortes gibt es die Möglichkeit eins generieren zu lassen:
r     muss als erstes
64    Anzahl der stellen (falls gesetzt sonst standard)
optional typen:
lower
upper
digits, number, numbers
sonder
Falls keine typen gesetzt sind, wird die Standardeinstellung genommen (veränderbar). 
Alle zeichen sind gleichverteilt.

─────────────────────────────────────────────────────────────────────────

Veränderbares:
─────────────────────────────────────────────────────────────────────────
Hier ein kleiner Abschnitt zu veränderbaren Einstellungen. Diese müssen in der
"Passwort Manager.py" Datei verändert werden und nicht hier.
DIESE EINSTELLUNGEN HIER ZU VERÄNDERN BRINGT NICHTS!!!

Die Konstanten sind ganz oben in der .py Datei drin. Die .py Datei kannst du mit einem
beliebigen Texteditor öffnen.

Dateinamen:
```
clean_file = "Pass.clean"
encrypted_file = "Pass.encrypted"
demo_file = "Pass.demo"
legacy_file = "pass.legacy"
```

Standardeinstellung für das zufällige Passwort. Falls manche Buchstaben nicht funktionieren.
`string.printable[:94]` sind aber alle Zeichen -> eigentlich am Besten
```
random_password = string.printable[:94]  # Standardeinstellung

random_passwort = ["a", "b", "c", "D", "E", 1, 2, 3, "&", "@", "'"]  # Eigenes Passwort als Liste 
                                                              -> weitere Einträgt mit "," seperieren

random_passwort = "abcDE123&@'"  # Eigenes Passwort als String
```

Dazu:
Die standardmäßige zufällige Länge eines Passworts
```
random_length = 32
```


Geheimes Passwort:

Hier kannst du dein geheimes Passwort festlegen. Dies muss du im Hauptmenü eingeben
um zugriff auf alle geheim Passwörter zu erhalten.
```
secret_password = "1234"
```


Alle verfügbaren Passwörter anzeigen:
Nützlich wenn man nach typen filtert und sich alle von einem bestimmten Typ anzeigen
lassen will (auch über select möglich, aber dann nicht daraus auswählen)
```
show = ["show", "show all"]
```


Minimale Toleranz:
Minimale % beim Approximieren -> Bei = 0 wird der erst beste Eintrag genommen
```
toleranz_sequence = 0.1
```

Passworthinweis:
Ein Passworthinweis, der nach x Anzahl von falschen Eingaben angezeigt wird.
Für keinen einfach `= ""` oder `= None` benutzen.
```
passwort_hinweis = "Bitte benutze deine Arme!"
```

Dazu:
Nach wie vielen falschen Versuchen der Hinweis angezeigt werden soll:
```
passwort_hinweis_num = 2
```


Passwort eingeben lassen:
Taste die gedrückt wird um Passwort eingeben zu lassen, zweite um den Modus zu verlassen
```
enter_pw_key = keyboard.Key.delete
esc_pw_key = keyboard.Key.esc
```
Die `Key.*` können herausgefunden werden, indem du im Hauptmenü 5 eingibst.
Dort werden nämlich (bei Sonderzeichen) Key. wie die Taste Heißt angezeigt.
Die musst du dann ersetzen.


Verschlüsselungs-Algorithmus:
Wenn du einen dieser Werte veränderst funktioniert die aktuell verschlüsselte Datei
nicht mehr. Achte also darauf, dass du vorher ein Backup machst.
```
salt = b"""\xf3\x9fp\x0b\xf6"""
```
Dies ist ein sehr langer string. Diesen solltest du ändern um maximale Sicherheit zu
erzielen. Diesen kannst du selber generieren lassen indem du folgendes machst:
❖ (windows key) + r -> py
```
import os
os.urandom(128)
```
Den String der herauskommt musst du in b"""{}""" einfügen. Falls du das nicht machst
ist es nicht so sicher wie es sein kann beim verschicken der Daten.


Anzahl der Iterationen:
Dies ist die Anzahl der Interationen für den Algorithmus. Je niedriger der Wert desto schneller geht das
Ver- und Entschlüsseln. Je schneller es geht, desto mehr Angriffe kann ein potenzieller Angreifer pro Sekunde
Ausführen. Es bietet sich also an den Wert bei ~1s zu halten, sodass ein Angreifer sehr lange braucht
Und es für dich nicht allzu lange ist. (Skaliert linear)
```
iterations = 10**6
```


Algorithmus zum verschlüsseln:
```
algorithm = hashes.SHA3_512()
```
