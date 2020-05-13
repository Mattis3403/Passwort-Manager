Passwort Manager von Mattis Seebeck

Eine Kurze version ist am Ende.


Dieser Passwort Manager ist dafür gedacht, dass man seine Passwörter speichert und diese sicher auf
der Festplatte verschlüsselt speichern kann, sodass es Mathematisch unmöglich ist sie zu entschlüsseln.


Der Passwort Manager ist in Python geschrieben, benötigt also Python: https://www.python.org/downloads/
Einfach auf "Download Python 3.X" clicken und danach ganz runterscrollen zu Files. Dort findest du alle möglichen
Versionen, die du installieren kannst. Für Windows 64-Bit ist es Windows x86-64 executable installer.
Python ist Plattform Unabhängig, kann also auf Windows, MacOS und Linux (Je nach Python Version und installer)
ausgeführt werden. 

Für Windows muss im Installer muss die Option Add Python 3.X to PATH ausgewählt sein, so dass die Pakete sehr einfach installiert werden können.

Desweiteren werden einige Python Bibliotheken benötigt. Installieren kannst du diese über pip. Das ist der
Paketmanager von Python. 
Für Windows ist es sehr einfach: 
Windows cmd aufrufen - win + r - cmd - 
Danach im Konsolenfenster "pip" eingeben. Falls "Der Befehl pip ist entweder falsch geschrieben..." kommt
ist python nicht im PATH erkannt worden.

Falls der Befehl nicht erkannt wurde, google nach "Add pip to PATH" für Windows. Für andere Plattformen am
besten nach "Python install packages" googlen oder so.


Erforderliche Pakete:
cryptography
pandas

---------------
pip install cryptography
pip install pandas


Wenn du diese Pakete installiert hast, sollte es gehen. Falls allerdings ein "Missing Package Error" oder
ähnliches kommt, kannst du über "pip install ..." dieses Paket sehr einfach installieren.


Nun kannst du den Passwort Manager öffnen mit einem doppelclick. Der Passwort Manager kommt in einem Ordner, worin sich die
Readme Datei und der Manager selbst befindet. Es ist empfehlenswert, wenn du diesen Ordner dir irgendwo (am besten auf der Cloud) sicherst, sodass du immer zugriff auf die Passwörter hast.


Jetzt wo alles installiert ist zur Bedienung:

Wenn du den Passwort Manager das erste Mal benutzt und keine weiteren (später mehr) Datein im Ordner
vorhanden sind, sollte es 2 Optionen geben: Passwort eingeben und Demo Datei erstellen.

Erstellen wir also als erstes eine Demo Datei. Dem Ordner sollte jetzt eine neue Datei hinzugefügt worden
sein: "Pass.demo". Wenn du diese Datei mit einem Beliebigen Text-Editor (Windows Standard Editor auswählen) 
siehst du das abgespeicherte Format und ein paar Einträge, die als Beispiel dienen sollen.

Hier kann man ein paar Werte abspeichern: Name, Email, Passwort, Username und ob das Passwort geheim 
gehalten werden soll. Dazu auch später mehr. Entweder kannst du hier die Einträge hinzufügen oder 
über die Option "Passwort hinzufügen" im Manager. 

Für einen Email Eintrag Gibt es nur eine Relation: Email <-> Passwort. Ansonsten müssen die Einträge dieser
Form entsprechen, sonst können sie nicht Interpretiert werden.


Jetzt zurück zum Manager:
Die "Pass.demo" Datei ist erstellt und jetzt kann entweder über 3 - "Verschlüsselte Datei aus 
Pass.demo 
erstellen" die verschlüsselte Datei erstellt werden oder über 1 -> 2 - "Eine verschlüsselte Datei aus
Pass.demo
erstellen". Letzere Option gibt es, nachdem eine verschlüsselte Datei erstellt wurde, nicht mehr.

Hier muss jetzt zwei Mal ein Passwort zur Verschlüsselung angeben werden (unterstützt UTF-8, also 
alle Zeichen, die man überhaupt repräsentieren kann). Verschlüsseln wir das Passwort also mit dem 
besten Passwort, dass es gibt: "12345". Dann sollte die Meldung "Verschlüsselte Datei erfolgreich 
erstellt" kommen. Jetzt kann auch das Passwort mit 1 eingeben werden.

Hier siehst du nicht, was du eingibst, da der Input verborgen bleibt. Dies ist damit jemand anders, der über deine 
Schulter schaut nicht dein Passwort sehen kann.

Danach sollte es etwas dauern, bis das die Datei entschlüsselt wurde (Anzahl iterationen und Algorithmus 
ist veränderbar). Dies dauert bei meinem PC in etwa 0.5 Sekunden.


Wenn das richtige Passwort eingeben wurde gibt es mehr Optionen:

1: Passwort Auslesen
	Hier kann ein beliebiger Key von Pass.demo (oder deiner späteren Passwortdatenbank) eingeben werden. Es
	kann z.B. Passwort 1 etc. angegeben werden. Falls du den Eintrag nicht richtig geschrieben hast, wird
	der nächstbeste approximiert. Du siehst oben mit wie viel % es approximiert werden konnte.

	Falls du jetzt "c" eingibst, nachdem du ein Passwort ausgelesen hast, wird das Passwort in deine Zwischenablage gespeichert.
	Achtung hierbei: Manchmal setzt Python das Passwort "{Passwort}" in Anführungsstriche. Darauf musst du aufpassen oder
	ggf. manuell kopieren. In der windows Komandozeile kannst du sowohl mit strg + c kopieren als auch mit enter.


2: Passwort aktualisieren
	Hier muss als erstes ein bestimmtes Passwort angegeben werden. Auch hier wird approximiert. Nehmen wir
	als Beispiel Passwort 1:
	Man kann jeden Eintrag verändern, sowie auch das Passwort löschen. Hier musst du nur bedenken am Ende
	wieder eine verschlüsselte Datei zu erstellen, damit es auch gespeichert wird.

	Auch hier kann mit "c" das Passwort am Ende oder während des veränders kopiert werden.

	Bei dem Passwort Promt kannst du mit "r" ein zufälliges Passwort generieren lassen. Mit "r {len}", also "r 32" kannst du dir ein zufälliges Passwort der Länge 32 generieren lassen.

	Was das Passwort beinhalten kann, kannst du im Code mit dem Parameter "random_password" verändern.
	Standardmäßig sind alle darstellbaren ASCII charaktere ausgewählt, allerdings kannst du das auch 
	ändern. In der Zeile darunter ist eine List auskommentiert - einfach das "#" entfernen. Dann kannst du 
	jegliche Werte (auch Unicode, also Smileys etc.) hinzufügen. Wichtig: Jeden Wert in "" setzen, sonst 
	erkennt Python es nicht.

	Darunter kannst du auch die standardmäßige Länge anpassen


3: Passwort hinzufügen
	Auch hier muss als erstes ein Name angegeben werden. Falls sich dieser bereits in der Datenbank
	befindet, gibt es mehrere Optionen:
		1: Einen neuen Eintrag unter dem gleichen Namen anlegen
		2: Den vorhandenen Eintrag aktualisieren
		3: Den vorhandenen Eintrag mit einem neuen Passwort überschreiben

		Diese Optionen sind realtiv selbsterklärend. Beim erstes wird ein weiterer Eintrag erstellt, beim zweiten kann man den Eintrag aktualisieren und beim dritten überschreibt man das Passwort.

		Der Unterschied zwischen 2 und 3 ist, dass man bei 3 ein komplett neues Passwort bekommt 
		wohingegen bei 2 man den alten Eintrag hat. 

		Außerdem überschreibt 3 bei mehreren Passwörter Alle zu dem neuen, wohingegen man bei 2 auswählen
		kann, welches man überschreibt. In diesem Fall kann man nicht ein einzelnes Passwort mit einem neuen überschreiben.


4: Verschlüsselte Datei aus aktuellem Passwort erstellen
	Auch relativ selbsterklärend - Wichtig: Immer nachdem man eine änderung vorgenommen hat diese Option 
	verwenden, da sonst das Passwort nicht gespeichert wird.


5: Textdatei aus aktuellem Passwort erstellen
	Selbsterklärend



6: Verschlüsselte Datei aus Pass.clean erstellen
	Selbsterklärend




So viel zur groben Einführung.

Es gibt noch einige Parameter, die sich verändern lassen 
(Im Code - nicht hier in Z. 20++)

toleranz_sequence = 0.1

Dies ist minimale Toleranz zum approximieren der Passwörter. Wenn == 0, dann wird selbst bei "" der erste Eintrag erkannt.


clean_file = "Pass.clean"
encrypted_file = "Pass.encrypted"
demo_file = "Pass.demo"

Hier können die Datein spezifiziert werden. Falls du nur .txt möchtest kannst du die 
Dateinamenerweiterungen verändern.

salt = b'b'~{i\xd5\x9a\x97cY(\x80\x81W\x82\xf5\x89\x01\x1f~RK\xf1\xe7\xea\'\x17\xf6\xfc\xce5\xa0\xf9\xeaZ|&\x88\xf9?~\xe3\x02\xed\xba\xc4\xbet\x9d\xa8C+:\xfb\xbdgc\xe31r\x1e\xc9\xc7\xce\xdb\x84~\xf4\xb2\x0f\xe0]k\x0f\x1d\xcbC\xf4u[\xad/\xb70\xfa\x94\xd8\x93=r2\xac\x93\x9fB\x08\x9d/\xbf\xc2\x86\xd8\xf7\xace\xa2\xb9L\x1c\xbd,P\xf0\x94\xda\x9ea\t\x99\xca\xa5\x91\xdaZ\x8a\xb8\x04c\x10\x0e}\xc4\xa9(k\x1b\xaa8\xca\x94\x8b]yp\xb4s\x1boO\xa3\n\xa1\xa2\'\xf5\r\xe8C\xd9F]\xb6w\xf4?\x1b\x7f\xa6\xeedYu[\x00Zq\xa5\xbe\'i\x9cpjJ\xe1|\xa0-1\x0e\x88\x19X\xff3A}\xc2\x84\x00!\xf3\xadma\xc2}\xd7,\x16\xb6\xc8\x89\x82\xbd\xf9\xe1I\x8e\xd1\xd7\xdb\x89r7\x1f\x1fz\x99\x02[$\xe7\x7f|5\xf4\xef\x00-\xa5\xb5\x154o\x11\xc9\xc0\x10U\xde\x90\x95{\xf6\xa5\xb0|\x06\xf1P\xe2/CLNP\xef\x08\xeef\x00<\x86&r\x1c\x08\\m\xbf\xab,\x13\xd5\x1f\x93\x08\xbd\xfa1\x80\xab\xa3><\xe5e\x85ZF\xca*\xcdo\xa8\xd8\xdd\xb9\xc3\x8a\xf2\x89\x9a\x15\x88\x1c\xb5M@\x99\xd9\x8f\xcaw\xf1L\xc8\xae\x02I\xed\xb79V\xbd\x07\xf8q~\xd8t\xb7\xca\x8c\x99\xf0E{\xce\xad\xff\x11R\x87i\xa7\x1cP\xafj\x1f\n\xf8\xef\xdb\x86\xb1\x14\xff+-,\xa5I\x15\x08\x01\x94\x97s@^s+d\xfb\xda\x0eXo\xaf\xa5\t\xcf\x9eY",\x02\xb5\xc5\xd8\x03\xf4\xbf\xa0"\x97\xaal\x99O\xd7\xc0\x06\xb9\x17A%\xa2^J\xf0\x84\xe9@\x1eB\x96\xa7G\x0e\x01\xbcR\xb2\xfc\x02\xab|5VQ\xd7\xb0+C\x8b\xfa\x14\xc4\xaf\xeb/\x0cp\x1f\xb5\x8bu0i\x17\xfc%\n\xb9B\x0f\xf0B\x1b%v<\x05\xd1\xc3\xb3\xaa\\\xd6\x8a\x0cg\xb8\xc3\\\x0fR\xd3v\x00\xef\x0f\xbf\xa6\xe9\xaeG\xf72)\xb9A\xc3\xb9\xdb\xce\x1c\x07\xff\xe4\xb4\x0cC\\-\xdb^w\xe1L7A\x1d\xec\x14\x90>\xfe\xcf^ \xa9\xe4\xac\xadv\x9b2\xf64\xdc\xee\xf3\xfa\xd9\x14\x89\xdd\xdaK6\xe9\xdb6\xc6L\xd1\xa7\x12\xd5\x9e\x97j\x04\x88Z\xca\x93\xe7\x08t\x9c\xd9\xab\xd2\x00\xfd8B\x90\x86\x81\x80\x87KyeRJ4\xa8\xa4#\x1e\xf25\xe6\xd4^u\x07\x9ch\xeb\x9dh>\xe2\xac:\xb28\xa8&i\x14\x90\x8bfc\\\\\xceU2\re\xcaz4\xadW\xa5\x85\xae\xd0\xf8\xf2\x066\xa8\xc2\xd7\xfdp(\x93R\xc2\x1es\xba=)\xcf\xf0\x80\x04\x9e\xd4\xb8\x85!\xe9Pn\xac\xc2Uq\xcf\x1bK*\x81\xab1\x93\x90\x8f\x15\x17\xc9\x03\xac\xb85]-\x9dd1%\xd3\xaa4\x98\x7f:\xd5E\xf6\xda\xd15A\x99c\xf8\xd3\x07\x16\x0e"\xe2\xab\\N\xaa\x83\xc2K\xf1&\xde\xc5\x1e"\xbf\xd6\xfeF\xf9\x85\xb4V\xc9\xb1?A\xea\xf5\x1e\x88\x06\x9f\xa1\x1a\xd8im`\xb4\xb0\xf9\xa4\x18&\x04\x11\x98\x86]\xbf\xba\xc3\x97\x83\xbf\xe0\x1e\xafl\x145\xd6C,\xb6\xad\xb2\nRR\xae\xda\xb6P\xb7\rR\x96S\xfa7\x1aG\xa8\xb7\x8f6w\x01\x04\xcf\x8f\x8c\xf4\xd7Y\xe7\xac\xad2\x99$\x90\xe3p:\x04\xe7\xef\xf5\xd6\x97\x1a\x1d\x95\x85\x1b\xdb\xe5\xa2\xfd\xeb\x02\x8cE\xb5\x04I0a\xc4O\xae\x1b\x1ch7\x011\xc5\xdfJ\x0b\x93\xad\x86)&\xf8\x15\xf3\xcc \xd1\xa8;\xc8\xd1R\x18c\xf3\xa2\xdcc\xd1C\x05\x0c\xce\x01\xf6\xe0-\xc7\xb3\xbc\x07M\x9d\x0b~\x16-\n\xc6\x8c\xb5\xd9\x04\xe9\xaf\xcb\x14\xa47f\xa6&\xd2\xbe\xc1\xe29\xb6\xbay\xe9\x8e,\xd3<\x15$\xab\xaf\xb6\xec\xc2$\x98\xae\xf6\xce\x04\xe3K{\xc31\x9f\xc5G\\\xbe\xcf\xd5\xc3z\xb9\xd2\x98s\x9e\xc2G\xf2WK]\xffjet\xfa+\x9fk\x9cIo\xa8\x13\xf6G\x18c\xf7f\xb8\xd0\xb3f\xee_?:\xd5\xab%O\xc5D>\xc0\xd1\xa1\x88\x83)\x13TOp\x88;\xc5,\xfb\xe6U*\xf2\x85\xfb\x10\xecv'

Diesen Salt kannst du verändern. Diesen kannst du mit "os.urandom(len)" in Python erzeugen. Wichtig ist, 
dass er mindestens 64 lang ist, kann aber beliebig (auch 16384 etc.) lang sein, je nachdem wie sicher du 
es haben möchtest. 1024, wie hier reich allerdings völlig aus und ist eigentlich vollkommen overkill.
Für gewöhnlich wird etwas in die Richtung 64-128 Stellen verwendet.

Der ** Operator sehr für hoch, also 10^6


iterations = 10**6 ≈ 0.6s

Dieser Wert bestimmt wie lang der Verschlüsselungsalgorithmus dauert. Je größer desto höher. Der **
Operator bedeuted ^ = hoch


algorithm = hashes.SHA3_512()

Diese Werte kannst du verändern, sofern z.B. SHA3_1024() verfügbar wäre. 





Nun wie man geheime Passwörter hinzufügt:
Es gibt eine Variable: geheime_passwörter, wo alle geheimen Passwörter gespeichert sind. Hier kannst 
du nach belieben viele hinzufügen. 
Falls diese Liste leer ist, werden alle Passwörter angezeigt.
Die Passwörter sind nicht wirklich geheim oder speziell gesichert, sie werden nur verborgen.



Ein kleiner Exkurs zur sicherheit des Passwort Managers:

Die Funktion, die am längsten dauert bzw. die eigentliche Entschlüsselung vornimmt heißt kdf.derive(password). Diese kann,
meinen Informationen nach, nur auf einem Kern für ein Passwort ausgeführt werden.

Das heißt, wenn man nur ein Passwort prüfen möchte, dauert es eine gewisse Zeit. Diese wird von der Geschwindigkeit der CPU
beinflusst. Wenn deine CPU also 2 GHz z.B. hat, dann läuft es langsamer als bei 4 GHz.

Wenn allerdings mehrere Passwörter überprüft werden sollen, kann man von der parallelisierung gebrauch machen. Wenn man also
z.B. nur 2 Kerne @ 4 GHz hat, dann kann man damit genauso schnell ein Passwort überprüfen wie mit 4 Kerne @ 4GHz und sogar schneller als 16 Kerne @3 Ghz.
Falls man aber mehrere Passwörter gleichzeitig überprüfen möchte, wie es z.B. ein Angreifer machen würde, kann dieser mehere
Kerne verwenden um einen sogenannten "Brute-Force" Angriff zu starten. Das heißt im Endeffekt, dass alle Kombinationen 
durchprobiert werden, also "a", "b", "c", ..., "z", "A", "B", ..., "1", "2", ..., "aa", "ab", "ac", ...

Eine Grafikkarte ist letztendlich eine CPU mit sehr vielen, langsamen, Kernen. Es bietet sich also an einen Angriff darüber
zu starten. Das ist der Grund, warum, obwohl es 0.5s dauert, der Angreifer immernoch Tausende Kombinationen pro Sekunde probieren 
kann.


Angenommen der Angreifer schafft tatsächlich 10**9 Passwörter pro Sekunde, was eine absurd hohe Zahl ist. Diese Zahl lässt
sich durch die Anzahl der Iterationen sehr leicht nach unten bringen, allerdings muss man dann jedes Mal länger warten.

-> hash_per_second = 10**9

Nehmen wir dann an das Master Passwort besitzt 80 mögliche Charaktere: a-z, A-Z, 0-9, Sonderzeichen (18). 

-> anzahl_char = 80

Angenommen die Länge des Passwortes ist 16

-> len_password = 16

Dann folgt die Anzahl der Kombinationen:


anzahl_kombinationen = anzahl_char ** len_password = 2814749767106560000000000000000


Wenn wir nun wissen wollen, wie viele Sekunden es dauert um alle Passwörter durchzuprobieren müssen wir dies Zahl nur
durch hash_per_second teilen.

seconds_to_crack = anzahl_kombinationen / hash_per_second = 2.8 * 10**21 Sekunden

Das sind umgerechnet 89255129601299 Jahre = 89 Milliarden Jahre. Zum Vergleich: Das Universum ist 14 Milliarden Jahre alt = 
4.35 * 10 ** 17 Sekunden alt.


Damit das Passwort knackbar ist müsste entweder die hash_per_second = 10**22 -> sein.
Wenn die Länge des Passworts gleich 8 ist, dann ist das Passwort bereits in 466 Stunden geknackt.

Es ist also speziell gegen Brute Force angriffe wichtig ein Passwort zu haben, welchs lang genug (am besten 16 Stellen) und 
mindestens Groß und Kleinbuchstaben etc. enthält. Je mehr Charaktere desto besser.


Am Ende hängt alles von der Hash Rate ab, also wie viele Passwörter denn in einer Sekunde probiert werden können, allerdings ist
mit 10**6 iterationen bei einer CPU auf einem Kern -> 0.5s. Deswegen gehe ich selber nicht davon aus, dass hash_per_second größer
als 10000 werden kann. Selbstverständlich kann sich dies in ein paar Jahren ändern, allerdings kann man sehr einfach die 
Anzahl der Iterationen hochschrauben und ggf. auch einen anderen Algorithmus verwenden.



---------------------------------------------------------------------------------------------------------

Kurze Version:

Python downloaden und installieren: https://www.python.org/downloads/

Im Installer die Option "Add Python to PATH" aktivieren!


Wenn installiert ❖ (windows key) + r -> cmd (enter) -> pip (enter)

Wenn hier eine Auflistung von Parametern erscheint war alles richtig. Falls nicht im Installer gucken.
Ansonsten google -> Add Python to PATH

Jetzt die Befehle in windows CMD eingeben:

pip install cryptography
pip install pandas


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







