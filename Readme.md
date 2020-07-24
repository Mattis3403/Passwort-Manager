Python downloaden und installieren: https://www.python.org/downloads/

Im Installer die Option "Add Python to PATH" aktivieren!

Nach der installation von Python kannst du den Passwort Manager öffnen. Die erforderlichen Pakete installieren sich von alleine.

Ich habe versucht alles an Information in dieses Readme zu schreiben. Falls du also irgendwo nicht weiter weißt, habe ich das irgendwo hier dokumentiert. Falls du alles durchgelesen hast und immernoch der Meinung bist nichts gefunden zu haben kannst du in github ein issue aufmachen und ich kann es mir dann ansehen.


Tutorial:
─────────────────────────────────────────────────────────────────────────
"Passwort Manager.py" öffnen

2 Möglichkeiten: Demo oder Echte Datenbank.

Echte Datenbank:
start -> 1 (Passwort eingeben) -> 3 (Eine neue Datenbank anlegen)

Demo:
start -> 3 (wenn keine demo Datei vorhanden:) Demo Datei erstellen (falls vorhanden:) Verschlüsselte Datei 
aus Demo Datei erstellen

Egal ob Demo oder echte, das Tutorial bleibt gleich:

Überall wo (veränderbar) steht kann etwas angepasst werden. Das sollte dann im Tab "Veränderbares" zu finden sein


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
	Ein Passwort löschen mit Bestätigung: "j", "ja", "y" etc. (veränderbar)

5 (Letztes Passwort eingeben):
	(fast) alle Attribute des letztes Passworts mit bestimmten Hotkeys (veränderbar) eingeben lassen

6 (Verschlüsselte Datei aus aktuellem Passwort erstellen):
	Verschlüsselte Datei erstellen. Aktuelles Passwort heißt alle Passwörter, die während der Ausführung geladen und / oder verändert wurden

7 (Textdatei aus aktuellem Passwort erstellen):
	Textdatei aus aktuellen Passwörtern erstellen (siehe 6)

8 (Verschlüsselte Datei aus {clean_datei} erstellen):
	Verschlüsselte Datei aus der Entschlüsselten Datei erstellen


Bei einer Veränderung immer dran denken 6 auszuführen um eine neue verschlüsselte Datei zu erstellen -> Die Änderungen werden sonst nicht übernommen


Unterfunktionen:

Wenn ein Passwort eingegeben wird gibt es:
	Nach typen filtern (modell von typ: partial, overlapping) mit
	```filter typ```

Suchattribut von Name auf ein beliebiges Attribut:
	z.B. auf "email"  (groß-kleinschreibung wird nicht beachtet) -> sehen wo die gleiche email verwendet wurde

Das Suchattribut approximieren -> Best-fit

Wenn sich das Symbol @ in dem Suchstring befindet und select nicht gesetzt wurde werden alle Passwörter mit "email" als typ gefiltert und select wird auf "email" gesetzt.

mit der Eingabe von "show all" kann man alle verfügbaren Passwörter anzeigen lassen

Geheim:
Alle Passwörter haben ein Attribut names "geheim". Dieses Attribut ist dafür da die Passwörter unsichtbar zu machen. Sie werden aber nicht extra gesichert, bietet also keine extra Sicherheit.
Alle geheimen Passwörter können wieder angezeigt werden, wenn man im Hauptmenü die Kombination "1234" eingibt (veränderbar). 


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
Hier ein kleiner Abschnitt zu veränderbaren Einstellungen. 

Diese müssen in der "Passwort Manager.py", also in der ausführbaren Datei verändert werden!
Dafür musst du die "Passwort Manager.py" Datei mit einem beliebigen Texteditor öffnen (rechtsclick -> öffnen mit -> weitere Apps -> editor). Dann ein wenig runterscrollen. Du solltest ein "Ab hier kann verändert werden ------" finden. Dort sind die Einstellungen, die du unten auch findest.


Ein wenig was zu python: Mit einem "#" kannst du eine Zeile auskommentieren, sie wird nicht gewertet. Deswegen kann man auch "# Dateinamen:" schreiben ohne, dass es zu einem Fehler führt. (Das wäre keine gültige Syntax ohne Kommentar)

Dateinamen:

Dies sind die Dateinamen für die jeweiligen Datein. `clean_file` ist eine unverschlüsselte Datei, `encrypted_file` die verschlüsselte, `demo_file` die Demo Datei und `legacy_file` die legacy Datei. Diese sind alle über die Dateiendung, also .clean etc. unterscheidbar. Falls du lieber alle als .txt speichern möchtest kannst du das auch tun (auskommentiert im Code). Diese kannst du einkommentieren indem du das "#" vorne (und das Leerzeichen) entfernst. Dann solltest du auch die oberen Definitionen auskommentieren.

```
clean_file = "Pass.clean"
encrypted_file = "Pass.encrypted"
demo_file = "Pass.demo"
legacy_file = "Pass.legacy"

# clean_file = "Pass_clean.txt"
# encrypted_file = "Pass_encrypted.txt"
# demo_file = "Pass_demo.txt"
# legacy_file = "Pass_legacy.txt"
```


# Legacy Datei benutzen:

Wenn dies auf `True` gesetzt ist, dann wird, sofern existent, die legacy_file umgewandelt und eingelesen. Ist nicht sonderlich nützlich wenn keine `legacy_file` vorhanden ist. Das ist noch ein überbleibsel aus meiner ersten Version dieses Managers, wo ich mein eigenen Dateitypen kreiert habe. Dies ist jetzt zu JSON geworden.

```
use_legacy = False
```


Standardeinstellung für das zufällige Passwort:

Falls manche Buchstaben für ein bestimmtes Passwort nicht funktionieren.
`string.printable[:94]` sind aber alle Zeichen. Ist also eigentlich am Besten

```
random_password = string.printable[:94]  # Standardeinstellung

random_passwort = ["a", "b", "c", "D", "E", 1, 2, 3, "&", "@", "'"]  # Eigenes Passwort als Liste 
-> weitere Einträgt mit "," seperieren und in "" setzen

random_passwort = "abcDE123&@'"  # Eigenes Passwort als String
```

Dazu die standardmäßige zufällige Länge eines Passworts:

```
random_length = 32
```


Geheimes Passwort:

Hier kannst du dein geheimes Passwort festlegen. Dies muss du im Hauptmenü eingeben um zugriff auf alle geheim Passwörter zu erhalten. Siehe Doku oben

```
secret_password = "1234"
```


Werte, die als Wahr ausgewertet werden sollen:

Werte, die bei allen Ja / Nein abfragen als `True` ausgewertet werden sollen. Die Eingaben werden `input.lower()` gemacht. Deswegen sind keine uppcase char in `true_accept`

```
true_accept = ["j", "ja", "y", "yes", "ye", "t", "true"]
```


Alle verfügbaren Passwörter anzeigen:

Nützlich wenn man nach typen filtert und sich alle von einem bestimmten Typ anzeigen lassen will (auch über select möglich, aber dann nicht daraus auswählen)
```
show = ["show", "show all"]
```

passwort_hinweis = "Bitte benutze deine Arme!"


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

Dazu Nach wie vielen falschen Versuchen der Hinweis angezeigt werden soll:
```
passwort_hinweis_num = 2
```

Zeit für Polling:

Wie viel Zeit zwischen einer neuen Suche von Input vergeht (in Sekunden). Je kleiner sie ist, desto interaktiver (responsive) fühlt sich das System an.

``` 
sleep_time = 0.0001
```


Passwort eingeben lassen:

Tasten die Attribute eingeben lassen. Das Keymapping, also welche Taste wie heißt, kannst du herausfinden indem du im Hauptmenü 5 eingibst. Dort wird dann deine Eingabe angezeigt. Das Mapping ist eine vorerst unbrauchbare Eigenschaft. Vielleicht kommt das noch in einer zukünfigen Version (Idee ist auch Numpad etc zu unterstützen). Ich würde dir empfehlen die Tasten so zu mappen, dass es Tasten ohne Eingabe wie z.B. `Key.delete` oder  `Key.page_down` sind. Wenn du z.B. ein `c` nimmst oder `numpad_1`, dann gibst du das `c` bzw. `1` vor dem Passwort ein, was zu einem Fehler führt.

```
password_mapping = "normal"
esc_key = keyboard.Key.esc
website_key = keyboard.Key.end
username_key = keyboard.Key.home
email_key = keyboard.Key.page_down
password_key = keyboard.Key.delete
```


Rund um Verschlüsselung:

Wenn du einen dieser Werte veränderst funktioniert die aktuell verschlüsselte Datei nicht mehr. BACKUP MACHEN!!!

Salt:

Eine Kombination von zeichen, die in dein Passwort zur Ver- bzw. Entschlüsselung integriert wird um einem Angreifer, der dieses Salt nicht besitzt die Arbeit quasi unmöglich zu machen. Ein kleines Salt hat aber kaum Vorteile. Ich würde ein Salt der Länge 1024 oder 2056 empfehlen, benutze aber selber 4096 um noch sicherer zu sein. Am Ende gibt es kein Limit (außer vielleicht Speicherkapazität) für dich.

Dieses Salt kannst du generieren indem du `❖ (windows key) + r -> py` eingibst und dann folgende zeilen:
```
import os
os.urandom(2056)
```
Den String, der dann herauskommt, musst du mit dem b'...' am Anfang komplett kopieren und in die folgende Zeile einfügen.

```
salt = b'\xcet8\x18F\x9f'
```


Anzahl der Iterationen:

Dies ist die Anzahl der Interationen für den Algorithmus. Je niedriger der Wert desto schneller geht das
Ver- und Entschlüsseln. Je schneller es geht, desto mehr Angriffe kann ein potenzieller Angreifer pro Sekunde
Ausführen. Es bietet sich also an den Wert bei ~0.1s zu halten, sodass ein Angreifer (auf viele Versuche) sehr lange braucht
Und es für dich nicht allzu lange ist. (Skaliert linear)

```
iterations = 10**6
```


Algorithmus zum verschlüsseln:

```
algorithm = hashes.SHA3_512()
```
