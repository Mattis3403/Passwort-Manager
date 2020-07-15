"""Manager für Passwörter: Veränderbare Einstellungen unten."""

import base64
import json
import os
import random
import string
import time
import sys
from difflib import SequenceMatcher
from getpass import getpass
from numbers import Number

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pynput import keyboard
from multiprocessing import Process, Event
from functools import partial

# Ein "#" kommentiert eine Zeile aus.

# Veränderbare Einstellungen:


# Dateinamen:

clean_file = "Pass.clean"
encrypted_file = "Pass.encrypted"
demo_file = "Pass.demo"
legacy_file = "pass.legacy"


# Legacy Datei benutzen:
use_legacy = True


# Zufälliges Passwort:

# Du kannst entweder alle Werte, die im zufälligen Passwort enthalten
# sein sollen in eine Liste schreiben:

# random_password = ["a", "b", "c", "1", "2", "3", "😀"]

# oder als String von Charakteren:
# random_password = r"abc123😀"
# random_password = r"""abc123😀"""

# Wenn du sie in einen String schreibst ist es wichtig die r"""  """ zu setzen. Ansonsten werden bestimmte Charaktere
# anders interpretiert.

# Normales Passwort mit allen Sonderzeichen:
random_password = string.printable[:94]

# Hier kann die standardmäßige Länge des zufälligen Passwortes angepasst werden.
random_length = 32


# Geheimes Passwort:
secret_password = "1234"


# Werte, die für geheim als Wahr angenommen werden sollen:
true_accept = ["j", "ja", "y", "yes", "ye", "t", "true"]


# Alle verfügbaren Passwörter anzeigen:
show = ["show", "show all"]


# Minimale Toleranz:
toleranz_sequence = 0.1


# Passworthinweis:
passwort_hinweis = "Bitte benutze deine Arme!"
# Falls keiner:
# passwort_hinweis = None oder ""

# Nach wie vielen falschen Versuchen der Hinweis angezeigt werden soll
passwort_hinweis_num = 2


# Taste die gedrückt wird um Passwort eingeben zu lassen, zweite um den Modus zu verlassen
# 100 000 Stellen eingeben bei mir: 28 sek
enter_pw_key = keyboard.Key.delete
esc_pw_key = keyboard.Key.esc


# WENN DU EINEN DIESER WERTE VERÄNDERST FUNKTIONIERT DIE ENCRYPTED DATEI NICHT MEHR!
# STELLE SICHER, DASS DU DEINE PASSWÖRTER GESICHERT HAST

# Dies solltest du ändern. Dafür gibst du in win + r "py" ein. Dann sollte eine Python CMD Konsole kommen.
# Von da aus gibst du folgende befehle ein:
"""
import os
os.urandom(128)
"""
# Die 128 kannst du auch ändern, je nachdem wie sicher du es haben willst. Mehr als 1024 bringt es nicht.

salt = b"""\xd2\x16"\xd81\xb8\xba_\x12\xad\x04\xdd\xa0\xde\x81\x1eN\xc45\xf0\xf2\x12\xc6\xb4\xc2>\x97h\xb6\x0f-\xdb5\xf4\xe7\xfa-\x85\xcaV\x1eZ\xfd\xdf\x0e\xe8\x81\xa2\x92"\xec\xba.\x1e\xa7\xe4\xdf9{\x85\x94\xfa\xc2\xabZ\xfa\xa9I/o.s\x1b\x13|\x9f\x03\xc7\xd1\xa7\xca\x8d\x13\x88\xaf\xbbzg\xa6\x99\x1b\x0c\xec\xefw\x85d,F\xf3\xa0b\xa6\xd9\xe4\xf9{A\x14\xd6\x99RS\xe1q\x1aV\xe5\xe7}t&\xcd\xb9\xac\xa1\x95\xaa\xf4\xdc\xa6p\xad\t\xca\xb8x\xfbw\x0b\xd6\xdd\xad\x1b\xf6\x04\xab\xc2\xa4\x7fs\x9d\xdd^\r\xbf\x0f\xbc\xd4zi\x1b\xd4\xeaB\x9f/\xaf-\xb4\xc5\x04\xe8F\xc7\xa2\x1e8\xca\x8c\xb2\xe0\xce\xdc\x1d\x1e\x7f\xee\x8b^\n\x85\xf0O\xaf\x04\n\x00\xaf\xbb]P\x1e\xa5=\xcb\xdb\xe7.\x88\xcb\x14\xcb"\xe0c\xda\x11,!h6\x17S\xbf\x86\xee\xe0\x8d[:\xce(\xbf!\x00\xc97!AvEp\x8b\xa6\xba\t-~I\x8a\xe6<\xda\xb0\xb0\x12\xb7\x839Js_I\xeaG\xe5\xc0It\xfa\xd5\x05\xa8\x1df\xe64W)\x17F\xe6\x9c%\x1f/\xa4nN\xe0p\xf8m\xe4g\x15\xc9\x93\x8b\x024\x19\xe5\xab\xbc\x11=4\xf4\xc4\x98\x92x\xda8\x96]\x02\xe6\xecc\xbe`\xf5\xe1\x1c\xe6\x17\xaa\x8c\xe2F\x1eW\xd1\xbdN\xf22\xa0\xd0\xaf\xfa_\x06\x18<\xe6N\x92k\x1e\x96\xc7\xe3H3u\x19\xe1\xf2\x99\x96\x8f\xb2\x9e9\xab\x12\x19\xf2AP\x7f4\xfa\xe283pb\xab\xc5RK\x14\x94de\xef\xa5\xe6L\x13\x97{\x04M\\\xe7(\x11\xd7\xbe\xc6\xc0\x0f\xc5[:\xbb\x8e\xff^5\xcd\xa7\xa5\x80\xf8\'\xfe\x198\x9d\x9e\xdfbj\xefi4>\x8e\xd0\xc4uq]y{_t\x02FuO$e\xa73\x9b\xd5\x19\x16\xbe\xb6f\xd0_\x9f\x00\xcd\xa4\x0e=\xa2\xa96R\x0b\xd3\xc0i\x9ag\x0c\xc0s\xb8\xba\r\xb3Y\xc4\xd2Jl\x84>\x04gO\n\xad\x97\x96`n9\xbfg\x7f\xf2\xe3\x16\x94d\xa2#\xcc<\xf7\x19\xacG;#\xa1\xa1\x85\xe5\x10\x8a>TjV&\x97\xe4A\x1e\xc0\x0f\x9c\xb5O\x9c^"\x1c\xd3NYp\x19\xc8\x92\x0c\\\xf0\x7f\'\xbe\x15\x1b6\x12\xdc\xa7\x0c\x7fz\x12\x9e\x7f\xe6\x88\xad(^;\xaf"j\xc9G\xfb\xfdyT\x17\xf4=\x89k\x1e\x86\x83\xbaW\x07\x8c"\xe0\xdbs`7t\x12\xb7\x83\xb0\x86~\x16DH0\xc2\x16\xb3\xe3~K;\xbbY.Z\xe3\xadN\x16?\x98V\x04\x1f|\xber)O\xe6:O^\n\x1bM@5\xb2\xaa\n,\x1f>x\xe3\xeakr\xa4>\x920\xe9\xaa@\xe4/\x0f\x12U\xadb\x14/\xe59F\x96\xab\xf8\xd2?\xfb\xe4\xc1\xc9b\x99\x14M\xc8\xaf\xd2\xb5"\x02\xcd^\x12\xdd]\r\xd2?SI]U\x02b\x82\x7f79d\x86p\x95\xd8\x7ft\xd55\xfc\xc9\x80\x18]gL\xc3\xf0\xe7\xe8\xc1\x9d=\xc5\x1f.\x10|\xd5\xe6\x1a\x04\x99|w\xae\xa5cb\xe1Hb\xd0\xce\x117\xa20Z\xdd\xe7\x19\x19\r\xc2\xb9\xbb\xf6\x07\'T&>\x1c0\xaa\xfa\x88\x9d\xf9\xc4\xbe[\xad\x13F\xf3\xa2\xb1\xb5\xd1\xaf\xc5j(u\xaf\xb3\xea\xe8@Uc\xc0\xf1.\xf5\xde\x05\xdf\x12#\x1a\x02\x91\xcf9\xa2\x01\x15\xc8\xc3B\xe0\xeb*7g\xc4Q{\x01\xa5\xab\x0f\xb3\xf2g\xcdFux\x17\x02\xbe+\xa8d\x12R\xb3\x7fp\x7f\xd1l6\xd8j\x0b\xe0\xb5\x85\xde\xe8\xb8[\xac\x8f\'kZw\xdb\xab\xf0\xc4U\x95t2\xba\xd0\xb5l9\xce\xef{\xd5\xd52\xfa"\xc1\x95\x06\xb6\x0e\xa7\x07kI\x99\xaa\xd9\x8ft\x8a$Bl|\x00\x83\xd5j\x13\x87~,%\x92\xdd\rR\x07\xe4Q\xe4>b\xb0\xafN\xcb(\xa8\xf9\x13\xed\x9b\x96\x86u\x06\xcb\x19\x80-~\x02\x91K\xfb\xc2\x9e\xfc\x1d\x13\xf8];b\xe2\x86\x8b\x96\xad\xdf\xe0\x19\xcb\xf52\xae)x\x11\xf6\xa8Y\xa3\xfd\xfeP\x07cs#Y\xaa\xbaqP\xec\xf4\x87\x81\xd1R\xb4&\x91\x95\xf9\xf0\r\xed>\xb1!;\x13\xd9VW\xca\xd7\x08R}\xb0\x90\xfe\xb9*\xbe\x9f\xd0\xda&\'k\xbf\xbbp)q\xe6\xd6:\xe9\x99\xfb\xe8\'\r\x1f\x1a8\x0c+\x9c\xb3-\xe9`\x1c{l\xc0\x13\x08\xdf\x11\xf4\x18k\xba\xfcu\xda!\xe7\xe8\xe9o\xba\xbc\xe6m\x19\xac\xecM7\xe8%=\xcb\x17\x91\xb3O\t\xe0\n\x0e\x8d@:>\xaa{A\xd7\xbd\xe0\x10A\xa4F\xe1]\xf8\r\xf6im3\xaf&\xbe\xfa)\x87][\xbc\x83\x1fT\xcc\x0b\x03w\xc3k\xf9\x82\xdf\rb\x89\\\x8b\xccI\x98\xfd\xfe\\[\x92\xc3\x85\xbc\xa5\x8d\xde\xf1}\xd1R\xfb\x9c\xd1\xae\xc2\xad+\xd2\xa6,f\xd0\xc6*,\xaao\xceg\x97\x19\x94T-\x882\xf1\xa9\x06\xf2#\xa4-\x83J2\xfd\x82c\xce4{\x03\xa0Q\xcd\x88"\xeb\xb6 U\xd7\x99\xc0?\x13\xf8\x82ga\x00\x11\xf8\x10=\xc0?\x98\xcb\xceA.\r\xadG\x10DbA\xcb9\xd4bL\xa9\xcc\x12~\x83\x92\x11\x0f\x0f(\x82e\xdc5\xae\xac\xaa:\x01\xe5\x19q\x00u\xb1\x0f\xdb\n\xa3\xa7\xb0Gj\x95^\x893\x0cKO,h\xf5\xde%\xd7\x9f/\xa0h\xaf\xb1\xa8W\x81h\xbdq\x913\x03,G\x98\xcf\xaf\xeam\xa8\xd1&\xa4\x13\xb2\x8d\x9f5\x95w\xb3\xb0\x16\xb5\x8d\xb0\xf0\x11\xa7\x98\x81\xcd\x804\x04\xcd\xad\x8bY|&!\x81\x1c\xeem\x03\n(0\xf0"\xd9\xfc\x8ed_\ny\xc3\xed>cR\xad\xa3\x9a\x93l:\x80\xff\xd0r\xc8\xa1\xda\x97qlN\x10oS^\xd2\xf3\xfbo\x90f\xed\xab\x94u\x01\x1d\xdc\xb7\xdb~R,\xa8\xfe\xa6\xd4q\x8d/\xa2U\xa4\xfa4O\xdf\xb0~\'\xffK\'\xe0\x9fY\x139J&\xce/(\xca\x9f\x8c\x14\xa4\xee\xc6\xa6E\x90\x81!\x88\xf91\x1e\x0e.S\xde/\xc2i\xad\xf9\xc5\xb0\xb6$w"\xda\x8aD\xf1H\xac\xe9 ~W\x14M;\xcd\xe9\xf7\x9f\xa8\xc8\x06uE\xae\x02b\xa8\xec\xb0\xae\x7fh\x14\x9e\x08#\xe1!\xdcU\xc9\xd6\xe5\x03\xe2\x00@\x90@\x12b>IgBp\xbc\xbfG\xe7\x8b\x90\x08\xc0m\x18\x05=\xbf\xcb\xe0\xb3\xa9\x1btG \xb0\xba\xe5\xb7\xf9\xc3\xd7\x1c\xd2$\xad\xc9\xb3\xd5\x94o\xe7\xfc\x047\x0e\xe6\x13%Td\x8e\x83\x01\xf5\x18\xc8(\x93\xd0\xf9*He9]\x8b\xd4\xf8\t\x94\xec7\xbf\xe7\x11G\x1bm,}\x10\xdc\xeaL\xbe\xcb\xd8\x86u\xf9^\xa1\xe7\xbb\x06M_W\xfa#\x9d\x1b\xaa\xe7\xd8\xde\xff\xa6\x05\x0f^\xfd\xce\xb8\x10\xcf\xd3e\xb7\xa4}\xc8c\xbf\xcb\x9a\x9eW/\x8e\xd1\x00\xa4\xd3\x0c\xae1\xfa!"U\x90\x9dM\x12}h\x8b\x10Fs\xc3\xd9\xfc\x18\x7f\x96\xf1\xcf\xac\xa0\x84\xeb4\xfd\xa1\xb1a\x12\xae\x06\xb5\xdd\x17\xb7\x00\x1b\x14y\x1cF\x03\x92\xfe\x83vz\x9c\xd9;\xd4D\x83\xcb\x04\x1e\xdc\xd8\x14U\xb9qe\x13\x1c\xe3\xfd_\x07\xc1\x8f\xdb\xfdU\t _\x11\x08>9\xcc\xf1\xcbQ=\x1f;\x8d\xed\xb5\xd4\n\xa2\x99\x91\xd5\xed\xe6\x0e\xa3\x83\xd7\xfd0\xa5\x89\xfc&\xe8\xed\xc4\t\xd9H\xb4xgs\xa4S\x14\xd6\xb6\xe6\xdc\x8e=\x15\x84\x01\xfe\x8c\xf2|\xd7\xa6\xde\x15\xb3\xa8\xa85\xc5\xa1\x9c\xdeN\xff\xee\xe6\x01\xfb\x00aJ\x87\x8b\xa0\xa2\x95a\xdd\xa6\xa2o[\xe8E\x8d\xcc\xfa\x92\x86i|3\x9f\x1d\xec\x82\xf4M\xad\x17M\xc2\x17XE)\xd6\x97\xd9%\xc1mcj0*\xb1\xb5\x90\xdadi\x96\xa7\xcf\xe4\x1d\xe8\xa3!^2\x98\x9b \x13\xb8\x17\xc6\xa3\x0el\xc0\xe0\x1de\x93\'\xdb%\xdd\xb4\xb0\x0b@\xff\x1d\xfe\x83\xf1\x97\xe3\xf7z?\xa3{\xbc\x987\xdeR\xa6\x81\xa4Q\xd4\xb8\xd5[\x82?\xf1;\xe5R\xd4\ns\x0e\xab\xd0\xbe\xbc\x87\xee*\xe3\xd5\xd4\xa41\xf0&\x97v\x1anBU\xe7n\x19\x12\xff<#\x8ay\xc2\xae\xde\xc0x\x08=\x8f,\x88b\xa3\x07\xa2\x83\t\xae\xaf\x86\x13\xb0\xcc\xc8*\x843\xe6<3j?\x10\x1b\xbb\xffc\xe7\xc2p\xe9\xfc\x17{y\xa0\xda\xcfHV\xa4T"2\xaf\x02\x127\x1aO\x9b\xd3W\xe0\x9dv\xc5\x07U\xc3\x8c&\xa2G\xa2\xde\xb1\xa3T\x98\xa7\x97Ap\xea\xe6@\x87\xe6c\x08\xd8|\x03Z\x9f\xc06\xb1\x01\x85\xda\x8a\xac\xca\xd7X2\xc9.l\x831\xf8\xd3\xca\xe4\x1a\xca\xbb\xe6~D;Le\xff\xb57\x07\\\t<\xb0\xda<7B\xb8\x82f;\x93\xb6x\xed\tQ-\xe7\xb7\x8b\xf0\xab\xb1m\xb6\xc4\x97\xd7#\xcd\xc1\x1c6\xe5)\xaetE\x90\xe4O\x9bq\x062(\xe9J\xb8e\xf47\x99\xce\x81\x13y\xaa\x04\r\xe3G\x18\x9e\xe2\x1ct\x8b\x163de\x07J\xff\xba/h\xe3\xa3 @!\t\xb0\xfbw\xb9\xf7\x83\x8c\xef\xaa\xed\x81\xcd*\xb4uI\xa6:\x86\xed\xeezNJ\xda\x13\xdc\xaf\xfcq\xc4\x1fB\x08\xdeL\xf5\xb9;\x92\x8b\xaf(\xeb\xae\xa1\x05\xba\xab\x9aK\xc6`\xb1\xa8B\x828<R\x0e)J\xab_/p\xc1\xa4=\xe3\x17.\x880\nf0\xa4\xd2m\xc96)\x11\xbb\x9e\x85\xee$\xd2gi\x0b\xef\'Q\x1c(%\ri\xa7\xc3\x18H\x0fWJ\x0fG\xa6\\\xfb.:*\xba\xe5F\xe6\xe3\x96\xf2\xa0C\xe2\xf2y\xceT\x8c*3\x9a\x84\xe7\xa1q.3\x8f\xd8\xe2\xa9\x88|\x9a\xb9\xab\xc2!\xb4\x04\xe7\xe6\x7f\xe3\xdd\x95\x19\xab\x9b\xb1h\xe9\xf1\xdd\xf9\xfb\xdb\xd8\xfc)?\x11I\xe2\x0f,l\xc9\xc8\xc2C\x97\xdc\x1f\xdc\x1eb$\xc9X\xb2\x1e\xd2\xf4\xe7hd\x93\xf2\xbe$s\xc1\xaa\xe4\x9d\xdd\x1e\xf92\xa4\x93\xee\x8f\xa7\x9cR_\xa9 \x02\xfa\xe9\xc3*\x8a9Il\x17\x9f\x8d@\xa1W\xbci7\xbc\x19z\xd2\x11\xdd\xd9\xcf\xce)H\xc28lQ\xafc\xa6\x85\x9ch\x05P\x18\xaf\xf9\xd0\xe68\xec1@`\xb6m\xe9\x11Y\xc7\xd9\xef\xd1\x12<\x9f)\x19x=\xdb\x99b\xdf\xb7yLvs\x85\x03\x91\xd6\x07U\xdf\xa0\xdaV\x90\xcc\xc2RUzhl\xee\x99r\xe00\x00<\x10\x0f5\\\xe3\x95fre\xc9\xdb\xa9Z\xadn0\x95\xe5T\xc6\x90Lq\xc3\x11\x19\xd3\xf2\xf2\x11\xd8\x87Pl\xee\x8cD\xef\xd7\xe9&\xb5!~\x1c\xe8\xf5\x1d\xea\xb6\\\x15\x03r\xc5\xf8\xca\xf2\xa6J\x89\xb3}\x1b\x86%\x04\x03\xba\xba\x99\x8b"\xe2\xbb\xce\xe0\xad\xce\t\r\x8f\r\xae\x04i\x92\x87z\x80\xd0\xecP\x92\xe2\xc5:\x9e\xaa\xe6K\xeaK\x88o\xdc\x90r\xbf4\xd1\xdd\x08\x9f<\xcb\x85\x0e7\xc2\xd0\xe5\xd3\x0c\x85&\r5\x01\xc7{\xf1\xd9\xb7\xd8*`\xe1\xd0\xc5Jp\x93\xe9\xcdQ\xf0\xcfd?|Y\x98\x81sl\xc3x\x10\xcdU\x11\x84H\xe6\xceQ\x08\xfbOoG$X\xd0\x9d\xfc2\xc6\xe57\xb4\x94^&\xdbV8aH\x1b}\x01#\xb2\x17[-\x93me\x9d/\xd1\x89-\xe8\xbd\xef5:\xfc\xf3\x94\x11\xe5R\xfc\xd6\xa5\x16\x13\xf7\xb8\xe4\x93\xcd\xc7>\xcax]|&SU=\xddFF\x8ed\xd6\x02K\xf3\xbe\x9a\xc0\tnE\xcd+J(\x96G\x94B\xca\'Q\xdb`\xea\xf9\x88\xf3\\h\x0efG\x94T\x9e\xc3\x13\x0cS\x1e\x97\xc5\xbc\x86\xa1\xd6>.\xc5c#\x95G\x9a\n;E\r\x91\xab\xafN\x90\xbd\xbeR \xe5\xc9\xc2\xf8\xf5\x85\xdb\xa4vX\x04\xe0<\xa6\xbd\xb2\xf6=\xb4\x81\x8d\xe8N>\x83\xb7\x12|\xaa\x8b\xdfGg\x1d\xd0\x0eMv.[\xbd\xed\x98\xfa\xd9\x1dIn\xd7\x178\x9f\xf9\x0f\xe3\xea&\xc8\x9b3}\x1cT\x06-\xedl\xe5\x80[\xf9\x02\xaf\x1e\x9cw\xee8\x16\xbf\xdd\x1c\xd0\xd3\xe8\xf3J\xc7\x01\x9d<Y\xa5\xef1\x00Q\x17*a\x8di\xcfI!\x84su\x97\xff\xfdKc\x12F\x9a;\xed[\xf0\x1fjX\x94\xe3~\x19\xd8\'\x85\x8e\x84\x85b9M\xe5\x10\x96\x12\x11\xf2.\xe6\xec,\xb2\xb1g\xd8Pr\xb9\x9c^f\xacz\x13\xd2@s\x1f\xcf\xfeT\xa0\xba\xb1]\xabd\xaa9\xc4(f\xad\xfb\xf6h\xaf\xb7 $\xf74\x16\xc4\xbb\\B\xffQ\x8d&Zk\xcek\x07\'\xd3\xcf*c\xdc\xb1\xc6Ip\xed\x9f\x8bw\xf3\xac\x04\x19\xed\xf5j\x80\x16\xf1>RA\xd7x\xc8*@\xaa\x17\xe6\x8b}+\xc7Jy\xc2\xb8\xec\x90\'Aa\xc0\r\x84[E\x1cR\x96\x17\x14O\xa4T!~\x9c4\xd0Wfc\xd1\xf4\xf2\xa8T-\xab\xb4h\xd4\x07Zn\xc3C\xbf\xa5-(\xb0`j\x8d\x1cc~p\x12\xab\x85\xc6\xc1\x12\\\xd3\xa1\xa7gD&Ep\xf8\xb2\xe1\x17}\xfa\xef\xca\xc0\x08\x0b,\xde\xacmH\x00{\xc5k<;\xb0e\xe8B\x13\x9d\xe2\x8fK\x86\x0b\x08\x12\x1a\x7f\xd2\x07>(1\x06\xa1[bU\xa4\xb9%\x1e\xab8\xde\xed\x8c\xc8\x0cwce\xa1\x8e2\xd1|m\xf9DT\x99B2\x10\xcc\xdd\xf1\t\x82\xc1a\x0e\xadz\xf9\xfb\xab\xc2\xf8\xaf!\xc09\xd9w\xbd,A\xbd\xa6\xf1 \x0f\x165\x1f\x8fbs\x7fNu\x05%\xdf\xa6\xe4\x92\xabyh{\x02\x87\xc9\xee\xe0f\x93\xfb\x92\x9f.t\x7f|\xf7/w^\x9c\xed\xcc\x92q!oJp\xf3\xca\xae\xdfYaYH\xbcc\x02,5\x93\xba@\x88\xb3\xe9 \xfb\xe9\x19\xed>((X\x11\xab0\xe1d \t\x9dh\x0cE\xd2\xef\t:O\xcb\xb6\xea\xee\xe6f\x18\xe2\xac\xff\xbc\xa3\x9c*K\xcb\xf7\xedqP$\xe6n\x1c\xf2\xb0\xdfI\x15d:\x93\xe8\xe5 \x1b\x1b<\x89\x95\x1f\xf3&]\xd2\xec\x89\\%\xe6\xdf4\xbe\xb3\xf9\xfd_>@\xdb0\x87ly\x08\xf6\x99\t\xd0\x92\x9e\n\x84Q\\<\x91\xd9\xa6\x12\x1d&\x08\xca\xa4}\x82h\xbe\x85\xe8\xaa\xa7\x16\xc6\x83\x83f\xc8\x13\xddb5\xe5\x11\xd071\x04\x97\x95f05\xb7\x86\xb9\xb5c\xc1\x96\x05\x9ao\x9b\x0b8\x96\x16\xc6\x18\xc3&\xd9\xbe\xf4h\xd4}\x12\xc5+\x8bdq\xd7\xa2\xb5\xcc\xb3\x1c\xb9\x9b\xc3h=s\xfc\xdd\x97=O\x07\xf2\x17\xf1L\x0e%S\x83\x86A\xc6\x94Y=\x12\x88\xf3\xd7Z\x00L\x0c\xa6\xb1;b\x0e\x19n\x12S\xb3\x16\xef\xe7\xc7\x82\xbc\x1f\xda\xe2\x15Y\x02\xc3\x87_%\xeaTr\'\xe4\x83\x9e\xe6\x8f\xa8\xe9I\xe8\xaeO\xf5@ox#"\xbf\x8b\x9as:\xe4\xfb\x07\xd1\xf48\x7fSu\xa7\x14\x00\xc5m\x801E\x1a\xba\xb7\xc5G7\xe0\xcd\xbc{\xe6\x8d(\xaf\x91V\xfcu\xa1yx\xa0:\x12\x08\xe7\xa5\xf7\x08\x98;3s\x14D\x14\x92JG\xbb)2\xb2\xd9\xea\xe2\xb5\xa5\xbe\xe1\xeb\xa9\xca\x82\xf8\xef;x\xdaLI+o\xd67\xa5+$\xba\x0f\xadj\xdf?I\x7f\xa3S\x13\xd9\xa8\xd3z\xdaOi"(V)\xc2\xd0\xabS\xd3\x90\x03\x0e\xea\x0eS\xe8\xa9\x92\x04\x8b\xfe\x9ep\x9d\x10+N\x00\x17\x95c\xf8%90\x0b:[\x9dT\xc5\x87\x0cK\x1er!"r\xec\xcdn-\xd8Go\xd9]\x82\x84E4?s\xcf\x10\xf0\xfa\xefJ\x86\xf6\xc8s\xbc\xfa\xcf\r\xa3/\x91\xbfrG\xc9\x02\x92\x95\x8dh7\x99O\xe1\xb6M\xd1\x90\xff\x8e\x82\x89\xe8\xca\x1b0\x1b\xe1F@\x93\xdds\xfb\xbb\x83]\xe1t(\xc4\\w\x81\x02\xd8\x8aQ\x82ar\xf26D |\t\xc9\xb2\x82\xd0\x87:9\xd1\x03\xe78*\xb22\x01\xb2\xa4\x83B\xec\xa1u\x15\x971\xaf\xceB\xef\xd5b\xfd\r\x93\x1e\xf8khGW\xc9\xd2\x94\xefn-\x0b\x95\x04\xee\x9f+\xae\x08\x04\x86g\xa1\xaf\xae\x1b(\x94\xa9$FJ[\xf6\x8f\x99\x84h\x0c\x94\x85L\r]\xd9-u\xf8\\\x97E\x1b\x9a\\\xc6\xe1(\xa7\x0f\xf4\xfe\x96\xa6p]d\xf8\xd1\xc9f\xaa\n*\xc5w\xb5\x0c\xff\x01\xf1-M\xbc\x97P6Uv\x9cYd&R\x83_\xc3\x1f\xcbn\x0f4a?\xf8f\xe2KC\x86\x9f\x858\x163\x07u\xf7\xa0^Q*\xc6\x94\x98\xba\r\x8f2\x18\x83\x87\x98a\xdf6pC|b:\xdb\x84\xc60z\x88\x91\xdeK\xf1\xc6\x07(8\n\xcf\x8a\x95\x88\x07\xbf\xfc\xac\x062\x18\x8b\'\xc5o\xa8\xd9\xcc3\x0e>>\xa3+fL\x9d\xa0\x9d5_hk\x14]\x00\x95b\x99\xe0\xca\xff_\xb0\xc3g\xa1\x85\x91\xa4\x8c\xe8\xe0q\xc0\xd6`\x7fx\xabF[\xa3\x10-\x03\xfcU\x1b\xed\xa0\x17A\t2.\xc1,\xb7C\x0ct}wAi\xc5\x95\x00\x9c\x95\xe7\xb7\xa5(\xc7l\xf8\x87JPUP"""

# Anzahl der Interationen für den Algorithmus:
iterations = 10**6


# Algorithmus zum verschlüsseln:
algorithm = hashes.SHA3_512()


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

ATTRIBUTES = dict(
    list(zip([
        'bold',
        'dark',
        '',
        'underline',
        'blink',
        '',
        'reverse',
        'concealed'
    ],
        list(range(1, 9))
    ))
)
del ATTRIBUTES['']

HIGHLIGHTS = dict(
    list(zip([
        'on_grey',
        'on_red',
        'on_green',
        'on_yellow',
        'on_blue',
        'on_magenta',
        'on_cyan',
        'on_white'
    ],
        list(range(40, 48))
    ))
)

COLORS = dict(
    list(zip([
        'grey',
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
        'white',
    ],
        list(range(30, 38))
    ))
)

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
               farben=False, matrix_nxm=False, ebene_darst=False):
    """Gibt dem User die Möglichkeit bestimmte Eingaben zu nutzen."""
    err.error = True

    if not isinstance(erlaubte_werte, (list, tuple)):
        erlaubte_werte = [erlaubte_werte]

    elif erlaubte_werte is None:
        pass

    try:
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
                klammertyp="rund", pfeil=False, pfeil_under=False, vorne=False, absval=False, gross_klam=False,
                string_ausrichtung=None, bruch=False, nur_pfeil=False, liste=False, dotted=False, dotted_len=False):
    """format_prec - Die Spacing Funktion. Diese Funktion gibt formattierten Input zurück."""
    check = False

    if isinstance(phlist, Number):
        phlist = [phlist]
        check = True

    elif isinstance(phlist, str):
        if pfeil:
            phlist = ["", phlist]
        else:
            phlist = [phlist]
        check = True

    elif isinstance(phlist, dict):
        phlist = list(phlist.values())

    elif isinstance(phlist, list):
        pass

    elif isinstance(phlist[0], list):
        pass

    if check:
        if pfeil and not nur_pfeil:
            check = False

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
    if klammer:
        if gross_klam:
            anf_klam, end_klam = get_klam(len(phlist), klammertyp)

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

        if get_divers("komma"):
            for i in range(len(ph)):
                ph[i] = ph[i].replace(".", ",")

        return ph

    while i < len(phlist):
        if not mehrere:
            max_len = parser_maxlen(phlist[i], prec, mehrere, string, absval, klammer)

        if type(phlist[i]) == str:
            if pfeil and phlist[i].strip():
                pfeil = get_pfeil(max_len)

                if nur_pfeil:
                    if liste:
                        pfeil = [pfeil]
                    return pfeil

                elif pfeil_under:
                    try:
                        ph[i] = phlist[i]
                    except IndexError:
                        ph.append(phlist[i])
                    try:
                        ph[i + 1] = pfeil
                    except IndexError:
                        ph.append(pfeil)
                    i += 1
                    continue

                else:
                    if i == 0:
                        ph.insert(0, pfeil)
                    else:
                        ph[i - 1] = pfeil

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

        self.typ = typ
        self.name = str(name)

        self.email = str(email)
        self.password = str(password)
        self.username = str(username)
        self.website = str(website)
        self.geheim = geheim
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
            if keys[i-1] != "rb" and keys[i-1] != "rb_inited":
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
            to_change = user_input(err, string=True)

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
                        self.typ.append(item)

                    else:
                        if item in self.typ:
                            self.typ.remove(item)
                print(self.typ)
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
        Password("Email", email="DianaEbersbacher@cuvox.de", password="""{YTxR"2!-qkN}j^;""", typ="email"),
        Password("Email", email="SaraBayer@cuvox.de", password="""')/Nzu*3-j8A/p+r""", typ="email"),

        Password("Passwort 1", "NiklasAckerman@einrot.com", "2y(MN`'qc(n,J.vr", "Niklas1234", "Diese Website", False,
                 typ="party"),
        Password("Passwort 2", "FrankBarth@einrot.com", "6a3jT4m.p<,7xZw&", "Frank1234", "Die andere", True, typ="party"),
        Password("Passwort 3", "MathiasFreeh@cuvox.de", "&Vp3;,%(BST8CL}@", "Mathias1234", "Diese Website", False,
                 typ="party"),
        Password("Passwort 3", "DirkBaer@cuvox.de", ";Pvd{JK.7D5vH{+!", "Dirk1234", "", False),
    )
    with open(demo_file, "w+") as f:
        f.write(dump_pw(pw))


def random_passwordgen(n, typ=[]):
    pass_list = []
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


def decrypter(file_name=clean_file):
    """Entschlüsselt eine gegebene datei mit Passwortpromt. Geheimes Passwort wird unterstützt."""
    geheim_pass = ""
    i = 0
    while True:
        print("Bitte Passwort eingeben:\n")
        user_password = getpass()
        cls()

        try:
            with open(encrypted_file, "r") as f:


                decrypted = _decrypter(user_password, f.read())


                break

        except InvalidToken:
            cprint("\nDas Passwort ist Falsch!", "red")
            if i+2 > passwort_hinweis_num and passwort_hinweis:
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
            print("Erfolgreich verändert\n")
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
            aktion = user_input(err, max_amount=3)

        if aktion == 2:
            if namen.count(pass_name) > 1:
                err.error = True
                while err.error:
                    print("Welchen der Einträge möchtest du verändern?")
                    nr = user_input(err, max_amount=namen.count(pass_name))
                    pw = passwords

            return pass_aktualisieren(passwords, geheim_care, pass_name)


        elif aktion == 3:
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
            global state
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
    if accept not in true_accept:
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


def convert_from_legacy(legacy_file=legacy_file):
    *_, legacy_exists = check_exists()
    if not legacy_exists:
        return

    with open(legacy_file) as f:
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


def listen_keys(kill_event, start_event):
    def on_press(kill_event, start_writing, key):
        print(key)
        if key == esc_pw_key:
            kill_event.set()
            sys.exit(0)
        if key == enter_pw_key:
            kill_event.set()
            start_event.set()
            sys.exit(0)

    with keyboard.Listener(on_press=partial(on_press, kill_event, start_event)) as listener:
        listener.join()


def press_keys(to_press, kill_event, start_event):
    kb = keyboard.Controller()
    while True:
        if start_event.is_set():
            kb.type(to_press)
            sys.exit(0)
        elif kill_event.is_set():
            sys.exit(0)
        else:
            time.sleep(0.01)


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

    start = Event()
    kill = Event()
    write_thread = Process(target=press_keys, args=(password.password, kill, start))
    listen_thread = Process(target=listen_keys, args=(kill, start))

    print(f'Die Einzugebende Kombination ist: "{enter_pw_key}", um diesen Modus zu verlassen bitte "{esc_pw_key}" drücken')
    write_thread.start()
    listen_thread.start()

    write_thread.join()
    listen_thread.join()

    global state
    if kill.is_set() and start.is_set():
        state = "enter_pw written"
    elif kill.is_set() and not start.is_set():
        state = "aborted"
    else:
        state = "bug"


def main():
    """Haupt Funktion"""
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

            action = user_input(err, max_amount=False, erlaubte_werte=accepted_val)

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

                    action = user_input(err, min_amount=3, max_amount=3, erlaubte_werte=accepted_val)

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

        if action == 1:
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

        if state is not None:
            print()

        state = None


if __name__ == "__main__":
    main()

