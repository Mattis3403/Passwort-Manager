"""Manager für Passwörter: Veränderbare Einstellungen unten."""

import base64
import json
import os
import random
import string
import time
import sys
import subprocess

from difflib import SequenceMatcher
from getpass import getpass
from numbers import Number
from multiprocessing import Process, Event
from functools import partial

os.system('cls' if os.name == 'nt' else 'clear')


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    from cryptography.fernet import Fernet
    from cryptography.fernet import InvalidToken
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

except ImportError:
    print("Das Modul cryptography wurde nicht gefunden. Es wird installiert:")
    install("cryptography")
    print("\n")

    from cryptography.fernet import Fernet
    from cryptography.fernet import InvalidToken
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

try:
    from pynput import keyboard
except ImportError:
    print("Das Modul pynput wurde nicht gefunden. Es wird installiert:")
    install("pynput")
    print("\n")
    from pynput import keyboard

try:
    from func_timeout import func_timeout, FunctionTimedOut
except ImportError:
    print("Das Modul func_timeout wurde nicht gefunden. Es wird installiert:")
    install("func_timeout")
    print("\n")
    from func_timeout import func_timeout, FunctionTimedOut

"""
Ab Hier kann verändert werden
------------------------------------------------------------------
"""
# Ein "#" kommentiert eine Zeile aus.

# Veränderbare Einstellungen:


# Dateinamen mit Dateierweiterung:

clean_file = "Pass.clean"
encrypted_file = "Pass.encrypted"
demo_file = "Pass.demo"
legacy_file = "Pass.legacy"

# Dateinamen mit .txt

# clean_file = "Pass_clean.txt"
# encrypted_file = "Pass_encrypted.txt"
# demo_file = "Pass_demo.txt"
# legacy_file = "Pass_legacy.txt"


# Legacy Datei benutzen:
use_legacy = False

# Ob das Graphical User Interface genutzt werden soll - hat zurzeit kein Einfluss
use_gui = False

# Zufälliges Passwort:

# Normales Passwort mit allen Sonderzeichen:
random_password = string.printable[:94]  # Standardeinstellung

# Du kannst entweder alle Werte, die im zufälligen Passwort enthalten sein sollen in eine Liste schreiben:

# random_passwort = ["a", "b", "c", "D", "E", 1, 2, 3, "&", "@", "'"]  # Eigenes Passwort als Liste
# 																-> weitere Einträgt mit "," seperieren

# random_passwort = r"""abcDE123&@'"""  # Eigenes Passwort als String

# Wenn du sie in einen String schreibst ist es wichtig die r"""  """ zu setzen.
# Ansonsten werden bestimmte Charaktere anders interpretiert.


# Hier kann die standardmäßige Länge des zufälligen Passwortes angepasst werden.
random_length = 32

# Geheimes Passwort:
secret_password = "1234"

# Werte, die als Wahr ausgewertet werden sollen:
true_accept = ["j", "ja", "y", "yes", "ye", "t", "true"]

# Alle verfügbaren Passwörter anzeigen:
show = ["show", "show all"]

# Minimale Toleranz:
toleranz_sequence = 0.1

# Passworthinweis:
passwort_hinweis = "Bitte benutze deine Arme!"

# Falls kein Hinweis benutzt werden soll:
# passwort_hinweis = None oder ""


# Nach wie vielen falschen Versuchen der Hinweis angezeigt werden soll
passwort_hinweis_num = 2

# Zeit, die zwischen polling vergeht (in Sekunden)
sleep_time = 0.0001

# Wie viele Sekunden du für Input Zeit hast (in s)
timeout_time = 5 * 60

# Taste die gedrückt wird um Passwort eingeben zu lassen, zweite um den Modus zu verlassen

# Mapping auf "normale" keys, die nichts eingeben:
password_mapping = "normal"
esc_key = keyboard.Key.esc
website_key = keyboard.Key.end
username_key = keyboard.Key.home
email_key = keyboard.Key.page_down
password_key = keyboard.Key.delete

# # Mapping auf numpad, letzte Eingabe wird gelöscht - Funktioniert noch nicht
# password_mapping = "numpad"
# esc_key = keyboard.Key.esc
# website_key = 97  # Numpad 1
# username_key = 98  # Numpad 2
# email_key = 99  # Numpad 3
# password_key = keyboard.Key.delete


# WENN DU EINEN DIESER WERTE VERÄNDERST FUNKTIONIERT DIE ENCRYPTED DATEI NICHT MEHR!
# STELLE SICHER, DASS DU DEINE PASSWÖRTER GESICHERT HAST

# Dies solltest du ändern. Dafür gibst du in win + r "py" ein. Dann sollte eine Python CMD Konsole kommen.
# Von da aus gibst du folgende befehle ein:
"""
import os
os.urandom(128)
"""
# Die 128 kannst du auch ändern, je nachdem wie sicher du es haben willst. Mehr als 1024 bringt es nicht.

salt = b'\xcet8\x18F\x9f\x054K\x0f\x10Lv\xd7P\x97v=TQp\xa0\xac\x92\xdf\x0f!\xba?\x96V\x86\xe5\xed\xeb\x13\xa0\xfb:g\xdb%\xeeg\xa3\x12\xfb\xd1\xdb\xa7\xb8\xa7\xcd\xb9ctc\x8be\xaf\xc9\xb6\x11\x16\xab\xc8\xb6\x94\xcb\x19l\x87\x89\x04\xf6w%z4\xe3N\x8f\xf63C\x8dW\xbb\xd9\xf5\x88\xdc\xfd,6U,4\xc1}\x1a\x03\xa1\xee\xac\x97`B\x03\xfd\xfbRQ\xbb\x14\r\xf7/U\xa7\xba~\xd0D\xde&g,\xeeD\x1a$fQ=\xd9\xd4.\xa7\xcaB\xd0\xfaB\xdc~\xcd\x1cA\xf1\xc3\xeb,\x130\x8f\x91\x9ei\xbd\x94\x929O{\xc3\xe81\xe0\x01g\xc3Z\xd6K\x81R\x8b\xd7\xb5\xda\r\xf6G\n\xaa\xabW\xe0\x1c\x97\xcc0m\xfa\x8c\xdez=d\x0e|\xca\xba\xc8\xac\xe8\xf4\xc6\xaf\x8d\xf5\x06R\xd0\x1c_N\xb1\xe8\xa6\xd0\x1a\xde\xf7\xf1.\xe9\x9f(Nc\xf0Q\xc7\x14\xaft\x1c\xb7\n\x84\'\xe9>v\xd0I?\x8d\xa3oIr\xad{\xa1\xdbx\xa1v#&\xaa\xf0\xc4f0\xfe!\x89\xc2x\xcb7\x03\xb9I\xc7\t,\xa1\xa0\xc0w\xd7\x7f4p.r\x94#:\xd6\t#\x95\x8e\xd2\xc7\x04U\xaa\xdcLm\xbbJ\xf1f\xd8\x88/\xfa\xd9k\xfe\xe7\x11w\xba\xc1\x10\xa0\xdd\x16\x06wu\x12\x94W\xa3Umh\xa1@%r\r\x80\x83\xe7*\xa8Y=\x01\xcb|*\tT\xec\x87\x82\x07\xf0\x1e\xe5\xd7\xbd\x95\xe8v\xcb\x9ef\xb0\x7f\xb9MI\xfa\xedn\xf0gI\xae&\n\x92Q\x8a\xbc\xa9#U\xfe|\xff[\x003x\xfaz)5pt~\xd1"\x81\xb2\xb0l\x1e\xa2{\xbd\xbe\xe9\x99\xac\xec.N\xb22G\xc0\xfd~\xc7\'\xe4\xfbl\xb3@\xcfm\xcc\x82\x11\xd9\x90\x00uJ\xc6\xb1!u\xf2i\x95h\xfb\x0f\xf3\x04\x08\xf6I\xfeb\x15\xdb3\xfc\x8e\x89a\x98uZ\x98\x1d\x15Y\x9b\xf3\xb7A|(\xb7\xae\x1b6\xed\xf9\xbc\x96rLh\xdaM\xb8\xcc\xa8\xefUY\x1a*T:\x05\xfd\x83W\x9a\xd0\x1ek\xb0\x93\xc7\xa9\x05\xf5\xf8\x8b\xa8N\x02\xd0\xc6b\x13=Z\x11\x0b\xccl{?\x86\xael\xe8\xa1Mg\x11;+\x80\x13x{\xd2\x0cS\xce#\xa2JLZ\x11zEF\xd5B<Z\x1dn\x81\xdf\xc6\x1f\xa23J\xfbXU\x18\xa2\xc6\x83^\xd4\xe0\rry\x1d\xe7\xa3\x97%\x84\xecO\xf6\xce/J\x8e\x99DU|G%\x8f\xc9\x8d\xd8\xb6%\xf0^\xe2\x87\xef\x15I\xde\xebiI^\xdb\t\xdf\xf3sE\xd6\x9bTu\x95\x1a\xa89\xb4\xa9\xc9x\xdbQT\xe1}\x7f>h\x91^K\x7f\xdcb\xea`\x1f\x14\xfe\xc4\xd7d\x98\xbe\x81L\x92GP\xa56\x1c\x01\xe6\xf6\xf1\xee\x04\xe2\xba(u\xda!\x90\xc7]\xdd\x9d@~\xaa\xbb\x93T\xde\x12B\xc7\x18\t\xfaaU.\x9bIR\xe0\x89\x18e\xe3c\xc1\x9f\xde\x01\xe0J\xfa?D\xfa\xa1\xcb\xc1\x9b\x95\xb6\x05\x10\xf6\x06A\xd1\xdad\x99\xdcr\xef\xdfG\x7f\xf0\xa1\xc6\x04H\xac"\x15\x1f\xde\xc4\\\xa4\xfcn\x10\xce\x0e&\xd5\xe0\x9aA)\x824\xf8\xa0\x8b)_\x11l\xd6\xb2\xb4:\x9ae\xd5mA\xc4\xc8\x87\xbf\xbc\xeb\xb9\x92$\xa1\xa8\xb8sio\xdd\x05\xd9Q\xfd\x07\x8a\xe9LO\xa4\xfdQ0\x17\xae\x9a\xea\xf8!g?\xfa\xf4\xd8\xeb\x9e:Z@\xda\xe1\xa1\x0e\x98\x8af\x17a\xa1\xec\x95\x14\x02e\x98\xbf\xf4m\xf7c\xb2}\xae\x16\xe7\r\x96 *\xa2\xa8\xa9r\xf5\xaf\x02\xcbY+{J\xcch\xfc\xee\x07\xa9\xd6F\'\xfb\xdc~\xbf\xe4k\xf3\xa34O\xb1\xca\xd8\xec4t\xd1\xf1\xbb\xaa*u\t\xf5\x9eh\xf3W\xaf\xf0*\x03\xf4\xd7b"y\xca\x9f\xf3\xea\x01\x91\xf4\rM()\xadj\x1bH\xf0\x08\xe0J\x91\xe6H\x99\x0eV\t\xf2!\xddS"({sp\xbd\xb5\x18J5\x9d\xd5\x07X\x0bZ\x82?\x147wS\x87\x1f?\xee\xd3\x8fB\xdd\x9c\xca\x15p\x08S\xe1}\xd3l=\xdc\xa5I\xed\xe2rJ|\xa9\xfc\x80\x02\xfbWn<X\x87[\xce\xd8\xda\x9fA\xf0\x8b\xe7\x02\xba\x9dTN\xc4\x97C\xe2h\x17\x9f\xc3\x1d\x8f\x95\xb96H\\pe\xb4\x83\xe6M\xb7\xa4\xe1\x05\xbb\x0c\xa1\x98\xd4P@\xcb\xd3\x0c$\x80\x9c\x0b,\x1b\xcbK"\xb6O\x91\x81Qb\x8c\xb1\xf4W\xbb\xd0\xf1\xe3\x86`\t\']\x8ad$CVl\xd0T\x9a\xbc5\xf4\xf2j\x81\x9fSXi\xec\xf2k,0\xd4\xe9\xce\xb5\x87\x8e\x8c\xa2\x97E\x87$$D[\x9f\x1a\x88ci\xfc=\x7f2 \xca,\x0e\x12\'\xb9\xd5\x02\x90u\x03\x15\x85C\xcbrs\x11\x00\x07\xfcw\xeb\xa9\x9e\xa2\xca\xafg\xc1}\xa0%\xf2 m%+\xce\xe3\xdb\x028R\x87\xbe\x9aA\x805\xc75\x01\xa8\xc2\xfe\xeb\xa3\xd6\t*\x1d\xd2\xac\xed\xe3\x8f\xa3t\xd1<\xa8\x8d\x11\xa4\n\x92\x19IW\n\xe6H\xb5\xe0\xd8 r\x96\xa1\xd5\xe8\xe0\xf2\xf2\xac\x01<*\x07#\xd4\x95\x1d\x0e\xcb,\x04U<\x95\xb9\xc1b\x83m\xaf\xd71\x98?*\x01\xfaZ\xf84\x94\xa5\xa5\x83gk\xc9\x9c\x06\x8ft7\x99\xdf* n\xb2\x9c+\xf8@\xd7\xe3\x90\xc7\xa8z\xa3\x86F\xfed2\xd3\x17\xc8\xb2\xff\xd8P"j\x903\xa8/\x91\x16\r,I;\x80\xf3F\xa8\xa3%\x9c.\xf8uF=\xd4\x07\x93\xa1\xa4\x86\xe4\x90>\xe0\xaa/w\x0e\xae\xbet\xd7\xe5\xc2\xb1\x07>\x12\xde\xf5\xac\xb7\x0f\xf9af\x06\xaa\xc0\x7fE\xc4\xd0\x121\xa0\xbf\x8dA\x18\xe1\xf1\x9f\x8f[\xcb\xe0\xb27\xc3\xe8A`\x97\xf1\xc4\xb4T\x9e\xb7a\x97\x7f\x1f\x1b\xc8\xba\x8c\xc0:\x90\xf150\xd83\xaf\x04K\xf7\x84\x17\xaf\xf4\x15\x0f\xda\xcdE\xfe\xb1duU`\x94\xf6\x8b\x90TP\rQ}\xe0\x99<\xd1\xec\xfb\xad\x9f\x06\xaap\x1aft\x9b^\x14\x1c\x83\xff\x1c\xd5g\xd4\xcdl\xe0\xe4j\xba\xf0\xd2(\x07\xe1\xd0\xf9rZL\xebAKQ1\xa8%\xcd\xe9i\xcf\xe7\xcc\xaa\xac\x04\x8e)Hit\x08\xb9"(\x01\x95\x96\xb1(2\xe6\xb4\xde>\x89i\xf6\xc5\x94W\x06Q\xcbQ\xdc\xa1\x8d\x9a\x02\x00^\x86<\xbd\x8e\xd1\xd5\xc2\xbd\xbf\xe8\x93\xb4\x85\xd4l:\xd2\xca\x11 K?\x95+\xdaF>\x1e\x04pS3\x9d\xde\x81VD{\x85\xd7\x9a\t\x1a\ti\xdeR\xce\xb4\xd0\xec_\xd3\xdfW\'m\x1b2-5\xea\xab\x0f\x99\xf0\x96\x1b\xcf\x7fQn\xeeo\x84\x92\xba\xe8(\xa4h\xcbM\xb5\xe4C\x80`\x10\xfc\x9b"N.\x00\x93\xf1\x1e\xdfse\x88\x18\x0f\xdc\x9f\xef\x7f\x88UH\'6y\xab\x90\x01\xbd\x17[\xd6x\x7f\xf4\x1cXZ\xe2\xc699\xcc \x11\xe1O\x8dhdIM\xc9\x8aK\x82\xa2t_\xba\x18\xb2\n\xef\x96H\xa6\xc2\x08Cp\x1fO\xfe=8m\xdd7\x1ci\xfc\x1a\x11[#(\t\x11\xd8\xd3\xd0\xad\xc7K\x11\x91\xf8\xeb!:L\x01\x8c\xb1_\x82\x91\xcd4W\x841E\xa2\xa6j"\xbc\xeb\xd3\xc3\x94\x11\x9bZ\xd1\xbc\xc8Q\x05\xb0Z\x1eT\x92^\xbb\r&\xc7\xe3~\xa9\xa9g2\xa5\xf3\x02\xd2\x9c\x9fc\x87\xf6s\xb2\x9da\xa0W\xf9L\xa0\x86\x98v\xaf\x96\xba\x8d\xe4D\\\x87\xdc\xc5\t\xdf\x90z\x87\x9aH\xd4\xa2v\xb3\x17\x95\t\x86\x15W\xf5j{\xd9\xa3\xba\x1e\x97\x85\x85\xd1\xc0\xe85\x87\xf19?,\x1aS\xb7,\x80l\xbd\xa3\xff\x1a\x03\xe5\xaaQ*\xb9\x88\x8f\xa6\x11\x9e\xe2\x9a\xf9\xb8\x1b\xce\xe4\xfa\xbc\xa5\xe2Fe\x0by\xaa\x0e\xf4\xbd\x00h~m$7\r\xbd\xab\xafsm\xd1\xa2U\x1eZ\xd5rJ\xf0Q\x12\nI\xee\x07^\xd6U\xa3\tz$S\x82\xcb\x9d\xe6\x9f\xa3\x8c8S\xd6\x98]Hk^\x81\xd3\x1e\xcd\xee-C\x02\x99\x03<\xa6\x87\xf2r\xe5\x87?\xdf\xe0\xc7\x9bL\x7f$\x0f\xa5\xcck\xaf2\x08@D\x1a\x85/\x98\x1b\xf2\x89\xb4E\xc8T\x18lc\xa8Q\xcb\xd5p\xb2\xe4\x81"-\xd9\x10\x1c\\\xf6z\xf3\xa4\xaa\x88\xe9\x9e\n"\x13\x96!\x8f\xed\x1e\xa6\x9a=\x97\xab\xb8\x7f\x89cic\xf1\xc2\x0c>7Ny\xd4\n\x9e\x818O\xeb\x8f\xfd\xd3\x8d`HJ\xf2#\n\xc1\xdf\x8a\xc9;\xb6x\xd9\xfd/Jr\xbdL\xb6\xeaK\xb1\x84\xe2\xc6\xea\xf5]\x17\\;\x91N\xa1\xe3\xb0?\xa9\xc1N\x1c|\xd6\x14\xbdC\xa4\xc9\x84\x03|{Ko\x8d\\)*|\xda3x:0Jv\xc0\x93\xf6\xef.g\xb0Np\x1f\xfa~\xea\xee\xdeD\x19#\xc4O\x84\x81Z\x0c\n1\xa7\xe7K\x89(N\x9d\x9a\xad\xd9\x05\xbb\r\'\nOw[\xde\xfc\xbck7Da\rh\x9aX+\xbeq\xbf\xf8_\xa2\xef\xd2\xe2K\xcf\xc3!\xc5\x94\n\xad\xd9\x9d\x93\x16\xfb\xd2\xd2\x95\xec\xb3\xbdFa\xa6v\xcaZ\xed\x85@\x8e\xd1.DAw\xdd~\xaf\x80\xda\xe9\xc2\x81i\x80\n\xc4\x0e\xf6\xd6{\x17\xf6\xca?\x0cBhB\x97\x81o-\x0e\xbe&\xf0\xbc$$?9\x9e\xe6{dpZ}\x16)b\xfah\t\xce\xcb\x80\x8e\x85g\xd2\x89\xd1.,H\x03kh\xc1\xb9\xb7\xe0H\xf1\x1c;\x80o\x9a\xf9\xd5\x8e\xcb!^\x99f\xa5Dt9K0Q\xcbzP\x82F2P\x81i\x10\\LJLo\x0c\xda\xf2t\xf1@z\x8e\x00\xf6\x0e,\x0b\xe5s\x93^\xcaN\x10P\x08\xa2,f,\x8a\xe0Go-#@lg\x01\xbc\xecH[\xe5\xb2C\xd6p\xb3\x93\x9a\x93\xce\x93\xab\xcd)a~\xf9\xf4\x1e8\xc8\x00\xabc\xf8o0\xa2L\x8f[\x7f=\x00\xe1w1^\x89\xba\xb8IM\xc6]\r\x82\x83\xa1\xe3\xf7\x88G\'`\xd0\xf9Z+\xefd\x12\xee\xff\x1b0\xd2\x1a\xf3-\xdeO!\xfc\xe2u\xbd\xa7)\xea\xb5\x97xi\xd9`\x1e\xed\x932)\xd6\x02\x86\x83h@C\xf9ka$3-c\x83\x00\xfa\xa5d\xf9\xf0\xca,?\x00\xd7\x98O\xf7\xc2\xae\xc0\xb2\x0cO\t\x8d\x9c\x05\xd8\x96U\x95raq\xc2\xd5w|\xf5\xc4D\x13A\x95\x11\x93\xec\x13\xa28\x0cg\x1f\x14\t\xa0v\xf5@\xcb\x8bq`\xf2\xab\x1b>\x11\xbfr1\xb4\x15\x9af\x80\x97.\x00Q\xc9L\xa8\n\x8c\x114\x9dS\xc3\x9b7\xd4\x8e\x94!\xaa\xfbn\xad\xb6pi\xbfk$\xa6\xb3,\xcf\x15`\xdb\tz\n\x93\x89\xe0\xcf\xf7\xdc\xbb\xa9{\xbd\xc3}F\xd2\x93\xeb\xc5\x9d\xe8zgB\xc2\xeeU\xf7\xac\xd5\x10sV2\xa8\xb9\xe3\xd3\x8a\xa7\x8e\xd8\xa6#\xbc0?\x16\xcc\x9d{\xff\x16\x18#\xe1+\xb5\xde\xa1w\xe0\xa1\xdf\xfcU\x12\xae\x1c\x8c\xc4\xe1\x87p-Tjk\xd6\x9d\xe4\x0cK\x1c[*\x1eM\x81.c\x031{\x05\x82KW\xda\xf3\xaf6\'\xa2\xf1\xe9\xf6\x92"\xfe\xb21M=oKN6I\x8b\xd7\xaf\n&\xe3\xeau9d\x88X\xb70\xaen\xa8e\xb1\x0f\x1e\xe9\xaf\xcc1N&$V-\x86\xaf\x17\x10d\xc8!\x05.(l\xe1{\x88\x8f\xaeH\x82\xed\xcc\xa2s\xa0\x8b\x9e\x8f4\x88\xc0}\xc3\xbe\x1b\x00\xee_\xcf\x1a\xc6\x1a?\xae\xf7\xf3kQ\xd9Z-P\xb6\x01\xf7\x021&\x10\x84\xce\xaf4\xfd\xac\x9cQ\x03\xc3\x8fj4\xc4\xbf.\xf9\x89>\x05\x03 :\x00#2b\xdc\xc8e\xdbQe?\xbdd\xfd\xc6\xec\x97k_\x1c|\x16C\x9b\x1b\xe4\xaa\xc5c\xe93}i\xd0\xcc\xbe\x8c%^\x0f1\xe7\xb2\xb6\x8c\x90\xb1\x1b0q\t\xea>\xb1X\xa7w]6\x91\x13V\x91\xb1\xe8X\xc2\xdf\x9e7\xcc\xddD\xa1\xa2\xe7\xe8\xd0\x15\xc7E\xad\x88\xc3\x81\xbfWO\x83\x80X\x16\x123S\x93\x10a\xba-\t\x94\x08/\xd93\xa5\xb5\x11\xb8*9u\x86\x9d\xf6o\xbd_\x19\x17\x07{3\xd4\x08\x8b+\x91OQH\xb6\xc5\xfb\x06\xd3\xb4\xb8\xf0\x1cHI\xa1\x17\x16\xaf\xf4\xed\xed)\x9d\xaax\x8f\n#\xc0\x01\xb9\x83\xba\x8dQ\x13\x8d\x7f\x12\xf8\xe3\xf4C\xbc\x92\xce+,*\x90\x0bXR\xec\xed\x92\xe9n#\x84\xcc\xd7\xd7\x9e\x0ff)\x915\xc4\xd6\xdaF\xc6~\xb3d\x8d\xac\r\x98.\xa0\x8a\xe8g\xc6.U\x8c\x89\xe0B\xad?\xa4\x9f14R.\x85`\xf58\x97\xbd\xd4K=\xa3\xa1\xf53\x01\xc0=N8\x12\tdE\x0c\x9f\x12\x05G\x04\xd4\xc5\xf3&\xf0I\x00\t\xb15a\x8c8\xd7#\x89n\x91\x16o|\xbe\x87mX\xe2\x00\\M8\x06\xcag\xb5\x8c)L+\xd1\xd8\xfa\r\xb1M\x83\xe4N7\xb6\x1f\xeb\x08,\x0f\xdb\xc0\xc8\x96\xca\xf3\x85T\xaez\xb0[\xf9\x17|\xc7\xd7\xaf\x99\x8d\xd1^@\x89ta\x02\xa8C\x9e\xe2\xeb0\xdb\xf0l\x99\x1eyv\xc8\xbb\xbc\xe5\xc6\xa3\xbbH:\\/r>0\x8e\x0b\x82\xf6\xd3\xf0o\x92\xda\x00s7\xc6b\x82\xf1\x86\x94^\x87\x9e\xe0\xf8^=\x86\x02\xb0\x1bbJ\xa2\n1\xd0\xf2\xa9W\xb0E\xeb\xddq\xa3\xa0\x07\xa4\xf5\xeb\x94\x12\x9a\t\x07\xa1\x7f_{fc\xd1\xa0\xc3-\x8e\x92\xb6\xdf\xcdu\x0f\xed}\x13\xd9\x18\xef\xeb\x89\xfc9z+\x8e\xbaU\xad\x1e\xdc\x8a{\x81\xbb\xdc\x99N\x12&\xb5\x1c)\xdb\xe3\x0b\xe8\xfc\x87\xfemM\xd7\x7f\xfe\x04\x13\xb3\xa2BS\xd9QY\x85\xd64\xe7f\x1f\x8bb\xf6\xf0\xed\xabc\xbc-AJG\x9b\x02\xdd\xfc1a \xe0\xc0*\x0c\x1f\xb2\x8c\xee\x1f).X\xa1\x83/\xe2y\\\x84\xdd\xc4\xb5\xa51\xc4\x8b\x83\x9a,\x1f![\x15\nL\xe5\x02\xdf(\x87\x9d\xd0\xcdGm\x94\xb5\xd5\xb8\xd0\xd0\x15\xe0)\xda\xc8\xfb\xb4UAeJ\xa0\x9d\xc4\xf3E\xfb|H\xac\xe8A\x06\xf1\x13\xaeb\xd5/\x07\xc7{m\x0e\xeb\x13\x86\xf2vd)\x13\x80a\x13BWY\x1bXX\x96:\xe6\xba\xc5  \xa6\xb9\xeca\x8c\xc4\xc6\xd5\t\xc6R\x08[f\xfc*\xd4!gw!2\xa8\xbd\xdb\x7fW\xa5\x8dF\x0et\x17\x87\xb3<\xb5\x80\xd3\xe0\xa7i>\xe3U\xd59\x901\xf1\x89\x13\x9e\x06\xc7\x92\xb7\xf1\xfa\x98v\xb4\xad\x9d2\xf6\xb6q\xaep\x815)\xdb\x14=\xa4\xa36\xd9\xa7\x94_\xb7\xcf\xb3\xef\xd1Y\xe0\x06tQ\x1c\x18\x17Y\x1b\nv\xe0\xc8\xed\xa7C3G\x81#\x02vS\xcf\xa4\x90X\xabe\x1c\xf1\xc2q\xe8\x9f\x13\xe0\xd9\xba\x94l\x8c\xee>\xad\x90\\\x9d1^\x8aJ#\x12z\t\x90\xcc\xec|R\x82\n~\xd6\xef\xf1h4\xdb\xa2K\x05v\x05X\x02\x97\xa7\xbd\x19\xe1\xd5\xb9\x98\n-\xfb\x01/\xb1\x95\xf1\x88uI\xdc\xda#\xbd\xa2\x86\xe6\xefm\x99<\x88\x9aC`\xa7\xb5T\x16\x9b\x064\xd2\xb1\x17phF@mH\xf4\xf7H\xec\x81\x01Fa\t\xfe\xf4\xfdH\x16\xc4\xa9}\xed\x8b3\xe8\xe0&\x1a\xcef[\xf7\x95\xfb\x14;A{\xbcI\x8f\xad&\x97S\x00Qc,\xbe\xbd\xfc\xc1\xac\xa0\xaf@\xfb\x91\xcfo\xc0?O}\xf1\xddYM8\x91\x0eY\xd8$m\x88\xaf\xe2RM\xda\xfd\xda\xfa\xb6\xf6S\xca\xec\xa01\x01t\xee\xb8OB?\xa1e-\x1f\x7fS\t\xed\xe3(\x1b\xfb\x9f\n\xbf\xa8\x98\\\xb9KAAL5G\x96v*\xc9\xd9s\xea\xbcP\xa5\xdfA\xb3\xd0\xc8\x1a\xa0^\xc8M\xb3\xf7oW\x9d\x0b\xdb+\xca\xff\xbb\x94\xd3\xac<Z\x90U[5\xcb\xcbG\xc8\x17+FA\xb4Q\xd8\xbd\xeeb\xec\xf4;Z\x80d\xbb\xe6\xb8\x89\x19\\\xde\x8d\xe2\xfa0\x93\xcefX\xdb\xb9\xf4\xd2\xcc2\xa8\xa4"\xf6\xec\xf9\x9d\xd7k\x1d;\x1d\xcb\xfcJ \xee\xe0\xff\x8b\xc2I\xc1\x90gI\x95\xad\xc9\xcc\x16\xc1F\xaa\x85\xad\xb8rZ#\x8e\xaa\xf1.\x9f\x8bE\x95\xbd\x92`,[\xf44S\xb9\xb1\x18\x80\xd9\x82\xaaEA@\xdck\xbe\x1f\xdc\xf8\x0b|4mH\x9dP:\xf8\x16\xe4>R\xd3\xe5\x11\xe7\xec4\xec\x056p\xd1i\'pAdq\xa7\xaa!ta\xcc\xd0\xe0g`y\xabL9\xf9@\x14=\xc3T\xc6\x87\x94U\xa1\xe0jj\xb4\xbcW\xe1l\x81\xf2\xb0B\x98\xf2\\C\xe1\xf8\n\xac\xd3\xa1\x95\x83\xae\xd9K\xc6\xeb\xc0rx\x1b\x8bH\x9b\xd7\xcf\x9c\xbbI?\x99\x1eja\xbd\xf88\xdaE\xaa\xbe\xa1PA\x05\x8f\x92\xcb\xedI\x86\x1b(?\x89\x06\xac\x04IU|))\xe1\xa8\x8fw\x031\x97\xc0\xd2\xf1\x1ax\xaeN\xf8\xb90\xef.\xc3Q5R\xbbE\xde\xad\xbaH\x93#\xfba\xf6\xaex\xe1\xa4\xa0}R\x1fr\xecc\xd2\xa5\xce\xa9\\\xd1\xeb\xaa\xac\x03+\x94\x8c\xa3IoB\xd7'

# Anzahl der Interationen für den Algorithmus:
iterations = 10 ** 6

# Algorithmus zum verschlüsseln:
algorithm = hashes.SHA3_512()

"""
Bis hierhin
</------------------------------------------------------------------
"""

# NICHT VERÄNDERN!

if isinstance(random_password, (list, tuple)):
    random_password = "".join(random_password)

length = 32
backend = default_backend()

# Vorbereitungsfunktionen --------------------------------------------------------------------------------------------------------


# Copyright für colored - NICHT FÜR DIESEN MANAGER GÜLTIG!!!
# coding: utf-8
# Copyright (c) 2008-2011 Volvox Development Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Author: Konstantin Lepa <konstantin.lepa@gmail.com>

"""ANSII Color formatting for output in terminal."""

__ALL__ = ['colored', 'cprint']

VERSION = (1, 1, 0)

ATTRIBUTES = dict(list(zip(['bold', 'dark', '', 'underline', 'blink', '', 'reverse', 'concealed'], list(range(1, 9)))))
del ATTRIBUTES['']

HIGHLIGHTS = dict(list(zip(['on_grey', 'on_red', 'on_green', 'on_yellow', 'on_blue', 'on_magenta', 'on_cyan', 'on_white'], list(range(40, 48)))))

COLORS = dict(list(zip(['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'], list(range(30, 38)))))

RESET = '\033[0m'


def colored(text, color=None, on_color=None, attrs=None):
    """Colorize text.

    Available text colors:
        red, green, yellow, blue, magenta, cyan, white.

    Available text highlights:
        on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white.

    Available attributes:
        bold, dark, underline, blink, reverse, concealed.

    Example:
        colored('Hello, World!', 'red', 'on_grey', ['blue', 'blink'])
        colored('Hello, World!', 'green')
    """
    if os.getenv('ANSI_COLORS_DISABLED') is None:
        fmt_str = '\033[%dm%s'
        if color is not None:
            text = fmt_str % (COLORS[color], text)

        if on_color is not None:
            text = fmt_str % (HIGHLIGHTS[on_color], text)

        if attrs is not None:
            for attr in attrs:
                text = fmt_str % (ATTRIBUTES[attr], text)

        text += RESET
    return text


def cprint(text, color=None, on_color=None, attrs=None, **kwargs):
    """Print colorize text.

    It accepts arguments of print function.
    """
    print((colored(text, color, on_color, attrs)), **kwargs)


def cls():
    """Cleart den Screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


class Input:
    """Class für Input."""

    def __init__(self):
        self.error = True


def error(inp):
    """Gibt einen Fehler wieder, je nachdem, was durch user_input*() für einen Wert gibt."""
    err_far = "red"
    if inp[0]:
        print()
        if inp[1] == "none":
            cprint("Bitte überhaupt etwas eingeben!", err_far)

        elif inp[1] == "zahl":
            cprint("Bitte eine Zahl eingeben!", err_far)

        elif inp[1] == "null":
            cprint("Nicht durch 0 teilen!", err_far)

        elif inp[1] == "größer":
            cprint("Eine Zahl eingeben, die nicht größer ist als die maximale Anzahl!", err_far)

        elif inp[1] == "kleiner":
            cprint("Eine Zahl eingeben, die nicht kleiner ist als die minimale Anzahl!", err_far)

        elif inp[1] == "matrix kleiner":
            cprint("Eine Matrix kann keine kleinere Dimension als 1 haben!", err_far)

        elif inp[1] == "float":
            cprint("Keine Kommazahlen eingeben!", err_far)

        elif inp[1] == "j":
            cprint('Bitte nur "Ja" eingeben!', err_far)

        elif inp[1] == "n":
            cprint('Bitte nur "Nein" eingeben!', err_far)

        elif inp[1] == "jn":
            cprint('Bitte nur "Ja" oder "Nein" eingeben!', err_far)

        elif inp[1] == "eval":
            cprint("Keine anderen Datentypen / Ausdrücke angeben!", err_far)

        elif inp[1] == "ebene darst":
            cprint('Entweder eine Zahl von 1 bis 3 eingeben oder "Parameterform", "Normalenform" oder "Koordinatenform"')

        print()


def user_input(err, string=False, ja=False, nein=False, max_amount=False, min_amount=1, erlaubte_werte=None, random=False,
               farben=False, matrix_nxm=False, ebene_darst=False, exit_after_time=timeout_time):
    """
    Gibt dem User die Möglichkeit bestimmte Eingaben zu nutzen.
    exit_after_time in sekunden
    """
    err.error = True

    if not isinstance(erlaubte_werte, (list, tuple)):
        erlaubte_werte = [erlaubte_werte]

    elif erlaubte_werte is None:
        pass

    try:
        if exit_after_time is not False:
            try:
                inp = func_timeout(exit_after_time, input, ("\n",))
            except FunctionTimedOut:
                cprint("Zu lange keinen Input: Programm beendet", "red")
                sys.exit(0)
        else:
            inp = input("\n")
        out = inp.lower()
        cls()

        if inp == "":
            if "" not in erlaubte_werte:
                err.error = True
                out = [True, "none"]
                error(out)
                return out

        if random:
            if out in ["random", "r"]:
                err.error = False
                out = "r"

            elif out in ["rr"]:
                err.error = False
                out = "rr"

            elif out[0] == "r":
                err.error = False

        if err.error:
            if string:
                if ja or nein:
                    err.error = True
                    if ja:
                        if out in ["ja", "j"]:
                            out = True
                            err.error = False

                    if nein:
                        if out in ["nein", "n"]:
                            out = False
                            err.error = False

                    if err.error:
                        out = [True, ""]

                        if ja:
                            out[1] += "j"

                        if nein:
                            out[1] += "n"

                        error(out)

                elif farben:
                    err.error = True
                    colors = [["Rot", "Grün", "Gelb", "Blau", "Violett", "Cyan", "Weiß"],
                              ["red", "green", "yellow", "blue", "magenta"], list(range(8))]
                    try:
                        inp = int(inp)
                        if inp in colors[2]:
                            err.error = False
                            out = inp, "Zahl"

                    except ValueError:
                        if inp.lower().capitalize() in colors[0]:
                            err.error = False
                            out = inp.lower().capitalize(), "Deutsch"

                        elif inp.lower() in colors[1]:
                            err.error = False
                            out = inp.lower(), "Englisch"

                elif ebene_darst:
                    err.error = True
                    try:
                        inp = int(inp)
                        if inp == 1:
                            err.error = False
                            out = "para"
                        elif inp == 2:
                            err.error = False
                            out = "norm"
                        elif inp == 3:
                            err.error = False
                            out = "koor"
                        else:
                            error([True, "ebene darst"])

                    except ValueError:
                        if inp.lower() in ["parameterform", "para", "p"]:
                            err.error = False
                            out = "para"

                        elif inp.lower() in ["normalenform", "norm", "n"]:
                            err.error = False
                            out = "norm"

                        elif inp.lower() in ["koordinatenform", "koor", "k"]:
                            err.error = False
                            out = "koor"

                        else:
                            error([True, "ebene darst"])

                else:
                    err.error = False
                    out = inp

            else:
                if inp in erlaubte_werte:
                    err.error = False
                    return inp

                inp = inp.replace(",", ".")
                out = eval(inp)

                if max_amount is False and min_amount is False:
                    if isinstance(out, Number):
                        err.error = False
                        pass

                    else:
                        out = [True, "eval"]
                        err.error = True
                        error(out)

                else:
                    if isinstance(out, (int, float)):
                        if isinstance(out, float):
                            out = int(round(out, 0))

                        if erlaubte_werte is not None:
                            if out in erlaubte_werte:
                                err.error = False
                                pass

                        if err.error:
                            if min_amount is False:
                                if out <= max_amount:
                                    err.error = False

                                else:
                                    out = [True, "größer"]
                                    err.error = True
                                    error(out)

                            elif max_amount is False:
                                if min_amount <= out:
                                    err.error = False

                                else:
                                    if matrix_nxm:
                                        out = [True, "matrix Kleiner"]
                                    else:
                                        out = [True, "kleiner"]

                                    err.error = True
                                    error(out)

                            elif isinstance(min_amount, int) and isinstance(max_amount, int):
                                if min_amount <= out <= max_amount:
                                    err.error = False
                                    pass

                                elif out > max_amount:
                                    out = [True, "größer"]
                                    err.error = True
                                    error(out)

                                elif out < min_amount:
                                    if matrix_nxm:
                                        out = [True, "matrix Kleiner"]
                                    else:
                                        out = [True, "kleiner"]
                                    err.error = True
                                    error(out)

                    else:
                        out = [True, "eval"]
                        err.error = True
                        error(out)

    except ZeroDivisionError:
        if inp in erlaubte_werte:
            err.error = False
            return inp
        out = [True, "null"]
        err.error = True
        error(out)

    except Exception:
        if inp in erlaubte_werte:
            err.error = False
            return inp
        out = [True, "zahl"]
        err.error = True
        error(out)

    return out


def parser_maxlen(phlist, prec, mehrere, string=False, absval=False, klammer=False):
    """Parsed die maximale Länge der Werte von phlist."""
    if isinstance(phlist, Number):
        phlist = [phlist]

    elif isinstance(phlist, str):
        phlist = ["", phlist]

    max_len = 0
    for item in phlist:
        if type(item) == str:
            if string:
                if len(item) > max_len:
                    max_len = len(item)

        else:
            forma = f".{prec}f"
            if absval:
                b = f"{abs(item):{forma}}"

            else:
                if klammer and mehrere:
                    if item < 0:
                        b = f"({item:{forma}})"
                    else:
                        if all(item >= 0 if isinstance(item, Number) else 1 for item in phlist):
                            b = f"{item:{forma}}"
                        else:
                            b = f"{' ' * (3 - len(str(int(item))))}{item:{forma}} "

                else:
                    b = f"{item:{forma}}"

            if len(b) > max_len:
                max_len = len(b)

    return max_len


def get_ausrichtung(ausrichtung):
    """Gibt die Ausrichtung für "links", "rechts", und "mitte"."""
    if ausrichtung == "links":
        ar = "<"
    elif ausrichtung == "mitte":
        ar = "^"
    elif ausrichtung == "rechts":
        ar = ">"
    return ar


def format_prec(phlist, prec=2, mehrere=True, min_length=0, ausrichtung="rechts", string=False, klammer=False,
                klammertyp="rund", vorne=False, absval=False, gross_klam=False,
                string_ausrichtung=None, bruch=False, nur_pfeil=False, liste=False, dotted=False, dotted_len=False):
    """format_prec - Die Spacing Funktion. Diese Funktion gibt formattierten Input zurück."""
    check = False

    if isinstance(phlist, Number):
        phlist = [phlist]
        check = True

    elif isinstance(phlist, str):
        phlist = [phlist]
        check = True

    elif isinstance(phlist, dict):
        phlist = list(phlist.values())

    elif isinstance(phlist, list):
        pass

    elif isinstance(phlist[0], list):
        pass

    if absval:
        phlist = [abs(item) if isinstance(item, Number) else item for item in phlist]
    if liste:
        check = False

    max_len = parser_maxlen(phlist, prec, mehrere, string, absval, klammer)
    if dotted_len is not False and isinstance(dotted_len, Number):
        max_len += dotted_len

    ar = get_ausrichtung(ausrichtung)
    if string_ausrichtung is None:
        str_ar = ar
    else:
        str_ar = get_ausrichtung(string_ausrichtung)

    anf_klam, end_klam = [""], [""]

    check_2 = False
    if vorne and ausrichtung == "links":
        for item in phlist:
            if item < 0:
                check_2 = True

    if check_2:
        vorne_space = " "
    else:
        vorne_space = ""

    ph = []
    i = 0
    n = 0

    if bruch:
        check_3 = True
        if mehrere:
            if len(phlist) % 2 == 0:
                while i < len(phlist):
                    max_len = parser_maxlen(phlist[i:i + 2], prec, mehrere, string, absval, klammer)
                    print(max_len)
                    if dotted_len is not False and isinstance(dotted_len, Number):
                        max_len += dotted_len

                    if isinstance(phlist[i], str):
                        if string:
                            x_1 = f" {anf_klam[n]}{phlist[i]:{str_ar}{max_len}}{end_klam[n]} "

                        else:
                            x_1 = f" {anf_klam[n]}{phlist[i].strip():{str_ar}{max_len}}{end_klam[n]} "

                    else:
                        forma = f".{prec}f"
                        if round(phlist[i], 12) == 0:
                            phlist[i] = abs(phlist[i])

                        if phlist[i] < 0:
                            temp_space = ""
                        else:
                            temp_space = vorne_space

                        b = f"{phlist[i]:{forma}}"
                        x_1 = f" {anf_klam[n]}{temp_space}{b:{ar}{max_len}}{end_klam[n]} "

                    if isinstance(phlist[i + 1], str):
                        if string:
                            x_2 = f" {anf_klam[n]}{phlist[i + 1]:{str_ar}{max_len}}{end_klam[n]} "

                        else:
                            x_2 = f" {anf_klam[n]}{phlist[i + 1].strip():{str_ar}{max_len}}{end_klam[n]} "

                    else:
                        forma = f".{prec}f"
                        if round(phlist[i + 1], 12) == 0:
                            phlist[i] = abs(phlist[i + 1])

                        if phlist[i + 1] < 0:
                            temp_space = ""
                        else:
                            temp_space = vorne_space

                        b = f"{phlist[i + 1]:{forma}}"
                        x_2 = f" {anf_klam[n]}{temp_space}{b:{ar}{max_len}}{end_klam[n]} "

                    forma = f"─<{max(len(x_1) - 2, len(x_2) - 2)}"
                    x_3 = f"╶{'':{forma}}╴"

                    if nur_pfeil:
                        ph.append(x_3)

                    else:
                        ph.append(x_1)
                        ph.append(x_3)
                        ph.append(x_2)

                    i += 2

        else:
            mitte = int(len(phlist) / 2)

            while i < len(phlist):
                if i == mitte and check_3:
                    forma = f"─<{max_len}"
                    x = f"╶{'':{forma}}╴"
                    check_3 = False

                else:
                    if isinstance(phlist[i], str):
                        if string:
                            x = f" {anf_klam[n]}{phlist[i]:{str_ar}{max_len}}{end_klam[n]} "

                        else:
                            x = f" {anf_klam[n]}{phlist[i].strip():{str_ar}{max_len}}{end_klam[n]} "

                    else:
                        forma = f".{prec}f"
                        if phlist[i] < 0:
                            temp_space = ""
                        else:
                            temp_space = vorne_space

                        b = f"{phlist[i]:{forma}}"
                        x = f" {anf_klam[n]}{temp_space}{b:{ar}{max_len}}{end_klam[n]} "

                    i += 1

                ph.append(x)

        return ph

    while i < len(phlist):
        if not mehrere:
            max_len = parser_maxlen(phlist[i], prec, mehrere, string, absval, klammer)

        if type(phlist[i]) == str:
            if dotted:
                x = f"{anf_klam[n]}{phlist[i]:{str_ar}}{end_klam[n]}"
                j = len(x)
                if j % 2 == 0:
                    x += " "
                else:
                    x += "  "

                j = len(x)

                while j < max_len:
                    if j == max_len - 1:
                        x += " "
                    elif j % 2 == 0:
                        x += " "

                    else:
                        x += "."

                    j += 1

            elif string:
                x = f"{anf_klam[n]}{phlist[i]:{str_ar}{max_len}}{end_klam[n]}"

            else:
                x = f"{anf_klam[n]}{phlist[i].strip():{str_ar}{max_len}}{end_klam[n]}"

        else:
            if round(phlist[i], 12) == 0:
                phlist[i] = abs(phlist[i])

            forma = f".{prec}f"
            b = f"{phlist[i]:{forma}}"

            if klammer and not gross_klam:
                if phlist[i] < 0:
                    b = f"({phlist[i]:{forma}})"

                elif mehrere:
                    if all(item >= 0 if isinstance(item, Number) else 1 for item in phlist):
                        b = f"{phlist[i]:{forma}}"
                    else:
                        b = f"{' ' * (3 - len(str(int(phlist[i]))))}{phlist[i]:{forma}} "

                else:
                    b = f"{phlist[i]:{forma}}"

            if phlist[i] < 0:
                temp_space = ""

            else:
                temp_space = vorne_space
            x = f"{anf_klam[n]}{temp_space}{b:{ar}{max_len}}{end_klam[n]}"

        ph.append(x)
        i += 1
        if klammer and gross_klam:
            n += 1

    if check:
        return ph[0]

    return ph


# /Vorbereitungsfunktionen -------------------------------------------------------------------------------------------------------

state = None
true_accept = [item.lower() for item in true_accept]

enc_main = False


class Password:
    def __init__(self, name="", email="", password="", username="", website="", geheim=False, typ=None):
        if not isinstance(geheim, bool):
            if isinstance(geheim, str):
                if geheim.lower() in ["ja", "j", "true", "t"]:
                    geheim = True
                else:
                    geheim = False
            else:
                try:
                    geheim = bool(geheim)
                except Exception:
                    raise Exception(colored(f"geheim konnte nicht zu einem bool konvertiert werden: \n{geheim}\n", "red"))

        if typ is None:
            typ = []
        if isinstance(typ, str):
            typ = [typ]
        if not isinstance(typ, (tuple, list)):
            typ = list(typ)

        self.typ = typ
        self.name = str(name)

        self.email = str(email)
        self.password = str(password)
        self.username = str(username)
        self.website = str(website)
        self.geheim = geheim
        self.rb = None
        self.rb_inited = False

    def to_json(self, geheim=False):
        if geheim and self.geheim:
            return ""
        else:
            to_dump = {k: getattr(self, k) for k in vars(self) if k != "rb_inited" and k != "rb"}
            return json.dumps(to_dump, default=str, sort_keys=True, indent=4)

    def __str__(self):
        final_str = ""
        keys = list(vars(self).keys())
        values = list(vars(self).values())

        keys_darst = format_prec(keys, ausrichtung="links", string=True, dotted=True, dotted_len=5)

        for i, (key, value) in enumerate(zip(keys_darst, values), start=1):
            if keys[i - 1] != "rb" and keys[i - 1] != "rb_inited":
                final_str += f"{i}: {key.capitalize()}{value}\n"

        return final_str[:-1]

    def change(self, already_changed=False):
        err = Input()
        while err.error:
            print("Was möchtest du verändern?\n")
            print(self)
            print(f"{len(vars(self)) + 1 - 2}: {'Bestätigen' if already_changed else 'Abbrechen'}")
            if already_changed:
                print(f"{len(vars(self)) + 2 - 2}: Rückgängig machen")

            user_change = user_input(err, max_amount=len(vars(self)) + 2 - 2)
            if user_change == len(vars(self)) + 1 - 2:
                return True
            elif user_change == len(vars(self)) + 2 - 2:
                return "rollback"

            cls()

        err.error = True
        while err.error:
            print("Attribut zu verändern:")
            print(f"{list(vars(self).items())[user_change - 1][0].capitalize()} . . .   \"{list(vars(self).items())[user_change - 1][1]}\"")
            print("\n\nNeuer Wert:")
            to_change = user_input(err, string=True, erlaubte_werte="")

        if list(vars(self).items())[user_change - 1][0].lower() == "typ":
            to_change = to_change.strip()
            append = None
            if to_change[0] == "+":
                append = True
                to_change = to_change[1:].strip()
            if to_change[0] == "-":
                append = False
                to_change = to_change[1:].strip()

            if append is None:
                self.typ = []
                append = True

            to_change = to_change.split(",")
            for item in to_change:
                if append:
                    self.typ.append(item.strip())

                else:
                    if item in self.typ:
                        self.typ.remove(item.strip())
            return

        elif list(vars(self).items())[user_change - 1][0].lower() == "password":
            changes = to_change.lower().split()
            if changes[0] == "r":
                if len(changes) == 1:
                    changes += [random_length]
                try:
                    to_change = random_passwordgen(int(changes[1]), changes[2:])
                except ValueError:
                    pass

        elif list(vars(self).items())[user_change - 1][0].lower() == "geheim":
            if to_change.lower() in true_accept:
                to_change = True
            else:
                to_change = False

        setattr(self, list(vars(self).items())[user_change - 1][0], to_change)

    def __eq__(self, other):
        if isinstance(other, Password):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other

    def rb_init(self):
        self.rb = vars(self).copy()
        self.rb_inited = True

    def rollback(self):
        if not self.rb_inited:
            print("Rollback not Initiated!")
            return

        for key, value in self.rb.items():
            setattr(self, key, value)


def dump_pw(pw_list, to_file=False):
    if not isinstance(pw_list, (tuple, list)):
        pw_list = [pw_list]

    final_str = "[\n" + ",\n".join(item.to_json() for item in pw_list) + "\n]"

    if to_file:
        with open(clean_file, "w+") as cf:
            cf.write(final_str)

    return final_str


def inst_pw(pw_str):
    return [Password(**item) for item in json.loads(pw_str)]


def demo():
    """Erstellt die Demo Datei."""
    pw = (
        Password(name="Email", email="AxelLalemann@gmail.com", password="Ein_Apfel", website="https://mail.google.com/", typ=["email", "gmail"]),  # Tatsächliche Registrierung
        Password(name="Email", email="EricHerzog@gmail.com", password="das sicherste Passwort was keiner je erraten kann weil ich so kluk bin", website="https://mail.google.com/", typ=["email", "gmail"]),
        Password(name="Email", email="LukasKrueger@gmail.com", password="""T/4.8F~C1D7>E.9LP]7..$]6G_Z;35uU=,':K9qr/?ATdG"W!Kd[<~ag`Ol$qzSl""", website="https://mail.google.com/", typ=["email", "gmail"]),
        Password(name="Email", email="PhilippJunker@gmail.com", password="ach passwörter sind doch nicht wichtig !!", website="https://mail.google.com/", typ=["email", "gmail"]),

        Password(name="Youtube", email="AxelLalemann@gmail.com", password="Ein_Apfel", username="", website="https://www.youtube.com/", geheim=False, typ=["youtube", "video"]),  # Tatsächliche Registrierung
        Password(name="Youtube", email="EricHerzog@gmail.com", password="Kartoffels@lat78", username="", website="https://www.youtube.com/", geheim=False, typ=["youtube", "video"]),
        Password(name="Youtube", email="LukasKrueger@gmail.com", password=r"""8@;M!nS)\~@J`M}r??#:=aQK;Y]d+.[@_Aqh!|FgW|@:=M1dfJUgZ_@vxX4ar0tu""", username="", website="https://www.youtube.com/", geheim=False, typ=["youtube", "video"]),

        Password(name="Twitch", email="AxelLalemann@gmail.com", password="Eine_Banane", username="smurfplay69", website="https://www.twitch.tv/", geheim=False, typ=["twitch", "video"]),  # Tatsächliche Registrierung
        Password(name="Twitch", email="EricHerzog@gmail.com", password="S[MlEt/47F^zmc0+", username="KesselKind", website="https://www.twitch.tv/", geheim=False, typ=["twitch", "video"]),
        Password(name="Twitch", email="LukasKrueger@gmail.com", password="""a;&8`VLZvE9C:&{Y30V7f|g)G,;jO4W$$b37yHSnRh;zmOz+Sd0"!}=v][uhfTR5""", username="PlsPickMeXayah", website="https://www.twitch.tv/", geheim=False, typ=["twitch", "video"]),

        Password(name="Instagram", email="AxelLalemann@gmail.com", password="Eine_Orange", username="_axel.lal", website="https://www.instagram.com/", geheim=False, typ=["instagram", "social media"]),
        Password(name="Instagram", email="EricHerzog@gmail.com", password="Kein brute force Angriff wird je gewinnen HAHAHA!", username="eric", website="https://www.instagram.com/", geheim=False, typ=["instagram", "social media"]),
        Password(name="Instagram", email="LukasKrueger@gmail.com", password="""Z7}EK,'qb5D9-BR)8WBV$gFK+}E/EvPp'snF)L;J&jK<YEBR+@lxt`3HtHoZ5Q<u""", username="_._._", website="https://www.instagram.com/", geheim=False, typ=["instagram", "social media"]),

        Password(name="Snapchat", email="LukasKrueger@gmail.com", password="""mdH4BkC%'{_~mo:U=vWkU1*VKWyjp]1=Y*-XD!Y9oHI5k`E$g8vj~Basu(ja66<f""", username="😀", website="https://www.instagram.com/", geheim=False, typ=["instagram", "social media"]),
    )
    with open(demo_file, "w+") as f:
        f.write(dump_pw(pw))


def random_passwordgen(n, typ=None):
    pass_list = []
    if typ is None:
        typ = []
    if "lower" in typ:
        pass_list.append(string.ascii_lowercase)
    if "upper" in typ:
        pass_list.append(string.ascii_uppercase)
    if "digits" in typ or "number" in typ or "numbers" in typ:
        pass_list.append(string.digits)
    if "sonder" in typ:
        pass_list.append(string.printable[10 + 26 * 2:94])

    pass_list = "".join(pass_list)

    if not typ:
        pass_list = random_password

    return "".join(random.SystemRandom().choice(pass_list) for _ in range(n))


def key_generator(password):
    """Generiert den Key aus einem Passwort für Symmetrische Verschlüsselung."""
    password = password.encode()
    kdf = PBKDF2HMAC(algorithm=algorithm, length=length, salt=salt, iterations=iterations, backend=backend)

    key = base64.urlsafe_b64encode(kdf.derive(password))

    return key


def _encrypter(password, text):
    key = key_generator(password)

    f = Fernet(key)
    encrypted = f.encrypt(text.encode()).decode()

    return encrypted


def encrypter(file_name=clean_file, string=False):
    """Encrypted eine Datei mit einem Passwort - mit Abfrage."""
    while True:
        print("Mit welchem Passwort möchtest du verschlüsseln?\n")

        user_password = getpass()
        print()
        print("Passwort erneut eingeben")
        user_password_2 = getpass()
        cls()

        if user_password != user_password_2:
            cprint("Die Passwörter stimmen nicht überein!\n", "red")
            continue

        break

    if string:
        encrypted = _encrypter(user_password, file_name)
    else:
        with open(file_name, "r") as f:
            encrypted = _encrypter(user_password, f.read())

    with open(encrypted_file, "w+") as f:
        f.write(encrypted)

    return user_password


def _decrypter(password, text):
    password = password.encode()

    kdf = PBKDF2HMAC(algorithm=algorithm, length=length, salt=salt, iterations=iterations, backend=backend)

    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)

    decrypted = f.decrypt(text.encode()).decode()

    return decrypted


def decrypter(file_name=encrypted_file):
    """Entschlüsselt eine gegebene datei mit Passwortpromt. Geheimes Passwort wird unterstützt."""
    i = 0
    while True:
        print("Bitte Passwort eingeben:\n")
        user_password = getpass()
        cls()

        try:
            with open(file_name, "r") as f:

                decrypted = _decrypter(user_password, f.read())

                break

        except InvalidToken:
            cprint("\nDas Passwort ist Falsch!", "red")
            if i + 2 > passwort_hinweis_num and passwort_hinweis:
                cprint(f'Der Passworthinweis ist: "{passwort_hinweis}"\n', "yellow")
            else:
                print()
            i += 1

    return user_password, decrypted


def name_solver(passwords, user_key, select=None, typ=None):
    if select is None:
        select = "name"

    passwords = [item for item in passwords if typ is None or typ in getattr(item, "typ")]
    namen = [str(getattr(item, select)).lower() for item in passwords]

    if user_key.lower() in namen:
        return user_key.lower()

    maximum = -1
    for item, password in zip(namen, passwords):
        ratio = SequenceMatcher(a=user_key, b=item).ratio()
        if ratio > maximum and ratio >= toleranz_sequence:
            maximum = ratio
            real_key = item

    if maximum != -1:
        print((f'Der Schlüssel wurde nicht gefunden. Er konnte aber durch "{real_key.capitalize()}" mit {maximum * 100:.2f}% '
               'approximiert werden.\n'))
        return real_key

    else:
        cprint("\nDer Schlüssel konnte nicht approximiert werden.", "red")
        return


def resolve_name(passwords, user_key, select=None, typ=None, choose=True):
    if select is None:
        select = "name"

    passwords = [item for item in passwords if typ is None or typ in getattr(item, "typ")]
    namen = [str(getattr(item, select)).lower() for item in passwords]

    if user_key not in namen:
        real_key = name_solver(passwords, user_key, select, typ)
        if real_key is None:
            return
    else:
        real_key = user_key.lower()

    num = namen.count(real_key)

    if num == 1:
        return passwords[namen.index(real_key)]

    elif num > 1:
        err = Input()
        while err.error:
            print(f"Dieses Passwort besitzt mehr als 1 Eintrag ({num}){'. Welches möchtest du wählen?' if choose else ''}\n")
            pw_kandidaten = [item for item in passwords if str(getattr(item, select)).lower() == real_key]
            for i, item in enumerate(pw_kandidaten, start=1):
                print(f"{i}:\n")
                print(item)
                print()

            if choose is False:
                return pw_kandidaten

            auswahl = user_input(err, max_amount=num)

        return pw_kandidaten[auswahl - 1]


def get_pw_user(passwords, geheim_care=True, choose=False, delete=False):
    err = Input()
    # Geheime Passwörter filtern
    passwords = [item for item in passwords if geheim_care is False or item.geheim is False]

    select = "name"
    filt = None
    solve_name = True
    while err.error:
        if delete is False:
            print("Für was möchtest du das Passwort wissen?")
        else:
            print("Welches Passwort möchtest du löschen?")

        user_key = user_input(err, string=True, min_amount=False)

        if err.error is False and user_key.lower() in show:
            cls()
            if passwords:
                for item in passwords:
                    print(item)
                    print("\n")
            else:
                print("Es gibt keine Passwörter!")
            err.error = True
            continue

        if err.error is False and user_key.split()[0].lower() == "select":
            if user_key.split()[1].lower() not in passwords[0].__dict__.keys():
                cprint("Das auszuwählende Attribut ist nicht in den verfügbaren Attributen\n", "red")
                err.error = True
                continue
            select = user_key.split()[1].lower()

            print(f"Erfolgreich {select.capitalize()} als suchattribut gewählt")
            err.error = True

        if err.error is False and user_key.split()[0].lower() == "filter":
            filt = user_key.split()[1].lower()
            _ = []
            for item in passwords:
                if isinstance(item.typ, (list, tuple)):
                    if filt in item.typ:
                        _.append(item)
                else:
                    if filt == item.typ:
                        _.append(item)
            passwords = _

            if filt == "email":
                select = "email"
            print(f"Erfolgreich nach {filt.capitalize()} gefiltert\n")
            err.error = True

        if err.error is False and "@" in user_key:
            if select == "name":
                select = "email"
                passwords = [item for item in passwords if "email" in item.typ]

        if err.error is False and filt == "email":
            try:
                user_key = int(user_key)
                for item in passwords:
                    if item.email == f"freezepro{user_key}@gmail.com":
                        pw = item
                        solve_name = False
                        break
            except ValueError:
                pass

    if solve_name:
        pw = resolve_name(passwords, user_key, select, filt, choose=choose)

    return pw


def read_pass(passwords, geheim_care=True):
    """Liest das Passwort aus einer Liste von Passwörtern aus."""
    pw = get_pw_user(passwords, geheim_care)
    if pw is not None and not isinstance(pw, (list, tuple)):
        print(pw)
    return pw


def change_pass(passwords, geheim_care=True, direct=False):
    """Aktualisiert das Passwort in Listen form."""
    global state
    if direct is False:
        pw = get_pw_user(passwords, geheim_care, choose=True)
    else:
        pw = passwords

    if pw is None or not isinstance(pw, Password):
        return

    pw.rb_init()
    check = False
    while True:
        ret = pw.change(check)
        if ret == "rollback":
            pw.rollback()
            check = False
            pw.rb_init()
            continue
        if ret:
            if check:
                state = "updated"
            else:
                state = "aborted"
            return pw
        else:
            cprint("\nErfolgreich verändert\n", "green")
        check = True
    return pw


def add_pass(passwords, geheim_care=True):
    """Fügt ein Passwort der liste hinzu"""
    err = Input()
    while err.error:
        print("Wie soll der Name des neuen Passworts sein?\n")
        pass_name = user_input(err, string=True)
    namen = [item.name for item in passwords if geheim_care is False or item.geheim is False]

    append = True
    if pass_name in namen:
        err.error = True
        while err.error:
            print("Das eingegebene Passwort befindet sich bereits in der Datenbank mit folgenden Eigenschaften:")
            for item in [item for item in passwords if item.name.lower() == pass_name.lower()]:
                print()
                print(item)
            print("\n")
            print("Möchtest du")
            print("1: Einen neuen Eintrag unter dem gleichen Namen anlegen")
            _ = "Den", "Den", "Eintrag"
            if namen.count(pass_name) > 1:
                _ = "Einen", "Die", "Einträge"
            print(f"2: {_[0]} vorhandenen Eintrag aktualisieren")
            print(f"3: {_[1]} vorhandenen {_[2]} mit einem neuen Passwort überschreiben")
            action = user_input(err, max_amount=3)

        if action == 2:
            if namen.count(pass_name) > 1:
                err.error = True
                while err.error:
                    print("Welchen der Einträge möchtest du verändern?")
                    pw_kandidaten = [item for item in passwords if item.name == pass_name]
                    for i, item in enumerate(pw_kandidaten, start=1):
                        print(f"{i}:\n")
                        print(item)
                        print()
                    nr = user_input(err, max_amount=namen.count(pass_name))
                    pw = pw_kandidaten[nr - 1]

            return change_pass(pw, geheim_care, direct=pass_name)

        elif action == 3:
            append = False

    pw = Password(pass_name)

    check = False
    while True:
        if pw.change(check):
            if check:
                if not append:
                    try:
                        while True:
                            passwords.remove(pass_name)
                    except ValueError:
                        pass
                passwords.append(pw)
            state = "added"
            return pw

        check = True


def delete_pass(passwords, secret_care=True, direct=False):
    global state
    if direct is False:
        pw = get_pw_user(passwords, secret_care, choose=True, delete=True)

    if pw is None:
        return

    print("Das folgende Passwort wird gelöscht:\n")
    print(pw)
    cprint("\nDies kann nicht rückgängig gemacht werden. Bitte bestätigen um Fortzufahren", "red")
    accept = user_input(Input(), string=True)

    if accept.lower() not in true_accept:
        state = "aborted"
        return

    for i, item in enumerate(passwords):
        if pw is item:
            passwords.pop(i)
            state = "removed"
            break
    else:
        state = "bug"


def check_exists():
    """Überprüft, ob die jeweiligen datein existieren"""
    encrypted_exists = True
    clean_exists = True
    demo_exists = True
    legacy_exists = True
    try:
        open(encrypted_file)
    except FileNotFoundError:
        encrypted_exists = False

    try:
        open(clean_file)
    except FileNotFoundError:
        clean_exists = False

    try:
        open(demo_file)
    except FileNotFoundError:
        demo_exists = False

    try:
        open(legacy_file)
    except FileNotFoundError:
        legacy_exists = False

    if use_legacy:
        clean_exists = legacy_exists

    return encrypted_exists, clean_exists, demo_exists, legacy_exists


def convert_from_legacy(file=legacy_file):
    *_, legacy_exists = check_exists()
    if not legacy_exists:
        return

    with open(file) as f:
        password_string = f.read()

    if "__________________________________________________" in password_string:
        password_string = password_string.split("__________________________________________________")[1]
    else:
        print("Die Anzahl der Unterstriche, die das Format und die Passwörter trennen sind nicht wie erwartet.")
        print("Dies kann behoben werden indem du die Unterstiche durch diese ersetzt:\n")
        print("\"__________________________________________________\"")

    password_string = password_string.replace("\r", "")

    pw = password_string.split("\n-------------------------\n")[1::2]
    iter_list = ["email", "passwort", "username", "geheim"]

    password_list = []

    for i, item in enumerate(pw):
        item = item.split("\n")
        typ = None
        geheim = False
        if item[0].lower() == "email":
            typ = "email"
        else:
            geheim = item.pop()

        password_list.append(Password(*item, geheim=geheim, typ=typ))

    return password_list


def listen_keys(password, kill_event, website_event, username_event, email_event, password_event, sync_event):
    def on_press(kill_event, website_event, username_event, email_event, password_event, sync_event, key):
        if not sync_event.is_set():
            print(key)

        if sync_event.is_set():
            time.sleep(sleep_time)

        elif key == esc_key:
            kill_event.set()
            sys.exit(0)

        elif key == website_key or password_mapping == "numpad" and hasattr(key, "vk") and key.vk == website_key:
            website_event.set()
            sync_event.set()
            print("-> Typing Website")

        elif key == username_key or password_mapping == "numpad" and hasattr(key, "vk") and key.vk == username_key:
            username_event.set()
            sync_event.set()
            print("-> Typing Username")

        elif key == email_key or password_mapping == "numpad" and hasattr(key, "vk") and key.vk == email_key:
            email_event.set()
            sync_event.set()
            print("-> Typing Email")

        elif key == password_key or password_mapping == "numpad" and hasattr(key, "vk") and key.vk == password_key:
            password_event.set()
            sync_event.set()
            print("-> Typing Password")

    print("Das Passwort:")
    print(password)
    print("\n")

    print(f"Die möglichen Kombinationen für Eingaben sind:\n")
    print(f'Diesen Modus verlassen:    "{esc_key}"')
    print(f'Website eingeben lassen:   "{website_key}"')
    print(f'Usernamen eingeben lassen: "{username_key}"')
    print(f'Email eingeben lassen:     "{email_key}"')
    print(f'Passwort eingeben lassen:  "{password_key}"')
    print("\n")

    with keyboard.Listener(on_press=partial(on_press, kill_event, website_event, username_event, email_event, password_event, sync_event)) as listener:
        listener.join()


def press_keys(password, kill_event, website_event, username_event, email_event, password_event, sync_event):
    kb = keyboard.Controller()
    _type = False
    event = None
    while True:
        if kill_event.is_set():
            sys.exit(0)

        elif website_event.is_set():
            to_type = password.website
            event = website_event
            _type = True

        elif username_event.is_set():
            to_type = password.username
            event = username_event
            _type = True

        elif email_event.is_set():
            to_type = password.email
            event = email_event
            _type = True

        elif password_event.is_set():
            to_type = password.password
            event = password_event
            _type = True

        if _type:
            to_type = to_type.replace("^", "^ ")
            print(to_type)
            kb.type(to_type)

            sync_event.clear()
            if event is not None:
                event.clear()
            _type = False
            print("</ Typing\n")
        else:
            time.sleep(sleep_time)
            continue


def press_password(password):
    if isinstance(password, (list, tuple)):
        err = Input()
        while err.error:
            print(f"Dieses Passwort besitzt mehr als 1 Eintrag ({len(password)}). Welches möchtest du wählen?\n")
            for i, item in enumerate(password, start=1):
                print(f"{i}:\n")
                print(item)
                print()

            auswahl = user_input(err, max_amount=len(password))
        password = password[auswahl - 1]

    if not isinstance(password, Password):
        cprint(f"password ist kein Passwort: {password}: {type(password)}", "red")

    website_event, username_event, email_event, password_event, sync_event, kill_event = Event(), Event(), Event(), Event(), Event(), Event()
    write_thread = Process(target=press_keys, args=(password, kill_event, website_event, username_event, email_event, password_event, sync_event))
    listen_thread = Process(target=listen_keys, args=(password, kill_event, website_event, username_event, email_event, password_event, sync_event))

    write_thread.start()
    listen_thread.start()

    write_thread.join()
    listen_thread.join()

    if kill_event.is_set() and password_event.is_set():
        state = "enter_pw written"
    elif kill_event.is_set() and not password_event.is_set():
        state = "aborted"
    else:
        state = "bug"


def main_no_gui():
    """Haupt Funktion"""
    cls()
    global state
    err = Input()
    secret = True
    while True:
        encrypted_exists, clean_exists, demo_exists, legacy_exists = check_exists()
        while err.error:
            accepted_val = [1, 3]
            print("Was möchtest du tun?\n")
            print("1: Passwort eingeben")

            if clean_exists:
                print(f"2: Verschlüsselte Datei aus {clean_file} erstellen")
                accepted_val.append(2)
            else:
                print()

            if demo_exists:
                print(f"3: Verschlüsselte Datei aus {demo_file} erstellen")
            else:
                print("3: Demo Datei erstellen")

            if legacy_exists:
                print(f"4: {legacy_file} konvertieren und in {clean_file} schreiben")
                accepted_val.append(4)

            action = user_input(err, max_amount=False, erlaubte_werte=accepted_val, exit_after_time=False)
        err.error = True
        if action == 1:
            if encrypted_exists:

                user_password, decrypted = decrypter(encrypted_file)

            else:
                err.error = True
                while err.error:
                    accepted_val = []
                    print("Es wurde keine verschlüsselte Datei gefunden. Was möchtest du tun?\n")
                    if clean_exists:
                        print(f"1: Eine verschlüsselte Datei aus {clean_file} erstellen")
                        accepted_val.append(1)

                    if demo_exists:
                        print(f"2: Eine verschlüsselte Datei aus {demo_file} erstellen")
                        accepted_val.append(2)

                    print(f"3: Eine neue Datenbank anlegen")

                    action = user_input(err, min_amount=3, erlaubte_werte=accepted_val)

                if action in [1, 2]:
                    if action == 1:
                        file = clean_file
                    elif action == 2:
                        file = demo_file

                    encrypter(file)

                    cprint("\nVerschlüsselte Datei erfolgreich erstellt\n\n", "green")

                    with open(file) as f:
                        decrypted = f.read()

                    encrypted_exists = True

                elif action == 3:
                    passwords = []
            break

        elif action == 2:
            encrypter(clean_file)
            cprint("\nVerschlüsselte Datei erfolgreich erstellt\n\n", "green")

        elif action == 3:
            if demo_exists:
                encrypter(demo_file)

                cprint("\nVerschlüsselte Datei erfolgreich erstellt\n\n", "green")

            else:
                demo()

        elif action == 4:
            passwords = convert_from_legacy(legacy_file)
            dump_pw(passwords, to_file=True)
            cprint("\nErfolgreich überschrieben!\n\n", "green")

    if encrypted_exists:
        if use_legacy and legacy_exists:
            passwords = convert_from_legacy(legacy_file)
        else:
            passwords = inst_pw(decrypted)

    err = Input()
    enter_pw = None

    while True:
        while err.error:
            print("Was möchtest du tun?\n")
            print("1: Password auslesen")
            print("2: Passwort aktualisieren")
            print("3: Passwort hinzufügen")
            print("4: Passwort löschen")
            print("5: Letztes Passwort eingeben")
            print("6: Verschlüsselte Datei aus aktuellem Passwort erstellen")
            print("7: Textdatei aus aktuellem Passwort erstellen")
            if clean_exists:
                print(f"8: Verschlüsselte Datei aus {clean_file} erstellen")
            print("9: Beenden")
            action = user_input(err, max_amount=9, erlaubte_werte=["c"] + [secret_password])

        err.error = True

        if action == secret_password:
            secret = False

        if action == "terminate":
            pass

        elif action == 1:
            enter_pw = read_pass(passwords, secret)

        elif action == 2:
            enter_pw = change_pass(passwords, secret)

        elif action == 3:
            enter_pw = add_pass(passwords)

        elif action == 4:
            delete_pass(passwords, secret)

        elif action == 5:
            if enter_pw is None:
                cprint("\nEs gibt kein letztes Passwort!\n", "red")
                err.error = True
                continue

            press_password(enter_pw)

        elif action == 6:
            encrypter(dump_pw(passwords), string=True)
            state = "dumped to encrypted"

        elif action == 7:
            dump_pw(passwords, to_file=True)
            state = "dumped to text"

        elif action == 8:
            encrypter(clean_file)
            state = "encrypted from clean"

        elif action == 9:
            break

        print()

        if state == "added":
            cprint("Erfolgreich hinzugefügt", "green")

        elif state == "aborted":
            cprint("Erfolgreich abgebrochen", "green")

        elif state == "updated":
            cprint("Erfolgreich aktualisiert", "green")

        elif state == "removed":
            cprint("Erfolgreich gelöscht", "green")

        elif state == "dumped to text":
            cprint("Textdatei aus aktuellem Passwort erfolgreich erstellt!", "green")

        elif state == "dumped to encrypted":
            cprint("Verschlüsselte Datei aus aktuellem Passwort erfolgreich erstellt", "green")

        elif state == "encrypted from clean":
            cprint(f"Verschlüsselte Datei aus {clean_file} erfolgreich erstellt", "green")

        elif state == "bug":
            cprint(f"Es ist ein Bug aufgetreten! Dieser Zustand sollte nie erreicht werden... Super Arbeit Mattis!", "red")

        elif state == "enter_pw written":
            cprint(f"Erfolgreich eingegeben", "green")

        elif state == "terminate":
            cprint(f"Zu lange keinen Input - Passwort manager hat sich heruntergefahren!", "green")
            return

        if state is not None:
            print()

        state = None


# class LockedScreen(GridLayout):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.cols = 2
#         self.add_widget(Label(text="Passwort:"))
#         self.user_password = TextInput(multiline=False)
#         self.add_widget(self.user_password)

#         self.submit = Button(text="Entschlüsseln")
#         self.submit.bind(on_press=decrypt_pass)
#         self.add_widget(self.submit)

#     def decrypt_pass(self):
#         pass


# class TestApp(App):
#     def build(self):
#         return LockedScreen()

# def main_gui():
#     TestApp().run()

if __name__ == "__main__":
    if use_gui:
        main_gui()
    else:
        main_no_gui()
