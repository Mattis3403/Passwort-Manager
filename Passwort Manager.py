"""Manager für Passwörter: Veränderbare Einstellungen unten."""

import os
import copy
import base64
import random
import string
import time

from numbers import Number
from difflib import SequenceMatcher

from pandas import DataFrame
from getpass import getpass
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

# Ein "#" kommentiert eine Zeile aus.

# Veränderbare Einstellungen:

# Dies sind die Dateinamen. Diese kannst du nach belieben ändern

clean_file = "Pass.clean"
encrypted_file = "Pass.encrypted"
demo_file = "Pass.demo"


# Du kannst entweder alle Werte, die im zufälligen Passwort enthalten
# sein sollen in eine Liste schreiben:

# random_password = ["a", "b", "c", "1", "2", "3", "😀"]

# oder als String von Charakteren:
# random_password = "abc123😀"
# random_password = """abc123😀"""

# """
# Wenn du sie in einen String schreibst ist es wichtig die """  """ zu setzen. Ansonsten werden bestimmte Charaktere
# anders interpretiert.

random_password = string.printable[:94]

# random_password = ["a", "b", "c"]

if isinstance(random_password, (list, tuple)):
    random_password = "".join(random_password)


# Hier kann die standardmäßige Länge des zufälligen Passwortes angepasst werden.
# Es kann auch über r 64 ein 64 langes Passwort gesetzt werden (Kann beliebig groß werden, auch 10**12)
# Bei meinem PC dauert 1 000 000, also 10**6 8.6s

random_length = 16


# Hier kann die Minimale Toleranz zum approximieren des Passworts festgelegt werden
toleranz_sequence = 0.1


# Hier kannst du geheime Passwörter festlegen. Sobald du einen Wert in "Passwort eingeben" oder in der Hauptfunktion
# eingibst, hast du zugriff aus geheime Passwörter. Diese Passwörter sind nicht wirklich geheim, viel mehr sind sie nur
# nicht angezeigt. Falls diese Liste leer ist, wird der "geheim" Parameter ignoriert.

geheime_passwörter = ["1234"]

# WENN DU EINEN DIESER WERTE VERÄNDERST FUNKTIONIERT DIE ENCRYPTED DATEI NICHT MEHR!
# STELLE SICHER, DASS DU DEINE PASSWÖRTER GESICHERT HAST

# Dies solltest du ändern. Dafür gibst du in win + r "py" ein. Dann sollte eine Python CMD Konsole kommen.
# Von da aus gibst du folgende befehle ein:
"""
import os
os.urandom(128)
"""
# Die 128 kannst du auch ändern, je nachdem wie sicher du es haben willst. Mehr als 1024 bringt es nicht.

salt = b"""\xf3\x9fp\x0b\xf6\\[\xcc\xef\x8bXU\xea\x82\xa96zF\x01\x8eK\xfd\xfe\xf66k\xfaw\xd7)\xa6\xd8i\xf6\xff\x18|2\x9e\x9c\xc5\xcd\xa8\xb52\xac\xc2\xaa\x0c\x8b*{\x9d"\xe9\n\x08*4FV\x17\xae\xacJB\xec\xd1\xb8oc\xce4<\x16lh\xdd;q(\xc9o\xc4Q!\xbb+\x1a\\S\xa4V\xda\xce\xe0\x8b\xe9I\xbcK\x84\xf4j\xeb\xe6\x11\x0f\xbaW*\xb8\xc0<\x1f"9\xf66\xa4\x15\xd8<\xb3.>A*\xc3\x90\xf8\xe0\x1aW\x80\xe8\xb5\xf9$z\x1f\x9b0\x08\xd6\x01\x121\xf4;\xb0j\x06JG/\x85I,\xca\xc8\x83e\t\x94\x1a<~\x95\xd3\xe7O\x8aM\x00c\x91\x1c|\x03D\xc0k\xf9\tF\x9a(\xc5l\n\x93\xdc&]\xcb\xdc-0\xcf\xb4f\xbc\x82\x01v<nX\xf5`C$\xb4\xba\xb9\x92\x8bt.\xf5V\xa1\x1f\xab9\x01)\x89w.1\xe4\x8e\x89\x8d\xac1\xbf!\xcc\x14+X\xd9\xeaQ}\x8d\xf185Y$\x9d\xec\xfb;p\xa5\x9b\xb9,"\xf8\xf2\x1e>q0Qf\xc1\x19\x92\x80\xdb\xd4\xcc\xdc\x11\x03~\x95\x15\x81v\xa163h\xe0e\nE\xe6\x18\xb6R\x91\xe9\xa3\xc8\x08K\x945\x11\x96\x98\xba\x1f\x9d\xd7-\xbc^\xf3Y\x12\x074\x9a.\xff0iR\x96A3cZ~\xcf\r\xbc\xc9\x8f7I\xef\xdbRsA\xbf\x00S\xd6\x9a\xa1D\x15\xe2T\x86G\x80\xd1\x83\x83\x1a\xea\n\xec}=\xa1\xdf3L\r\x99\x9bV\xa7\xebS:y\x08\xf4)\xea\x1b\x9c\x1e\xea\xdb\x80\xf2*0\xa5V\x8b\x97\x8c\x18\xd8\xa2\x9e\xde\x9a\xdaDs\xf6y\xd7\xee\xaf\x01\xe46{n\xce=\xed\xdc\xe5\x87\xdcJk8\xc1\x80\xcf\xab\x99,\xdbT"\x13\xc2\xd3\x8e\xc2\xd5_\xf00\xb1\xb6\x15\xa2\x8e\x171\xbe\xb9\xfb\x17\xc8~\xcd\x1ci\x9c\xb3P/XgVp\xc9fo\xa8\xfe\x90\xcf\x8c\xe0B\xff\x9e\xee\x85 A\x98*+\x9f\x0eA*U\xab\xa2\xdc\xd6d57\xa1\xcba\xc8\xaf\xf4F\xd4\t\x96\xf3\xa6\xee\r^gO\x158\x9a\x0c\xd5\xbdHd\x1f\xb6\xf4\xf4\xe7\x91,e\xba\xad\xf0\xc9,\x8b\xddx\xac\xb1\x0f\xa5\x8bK\xc2 \n\x0b\xe7$1.B\xbft\xa7D\x8b\x9b\x05M\xc4\xe3\x87\x11\xb5\xdde0\xdf\x9c\x93is\xf7\xbaWc\xec2\xf3\xd1\'\x88`8\xd4\xd3\xa9-\x82}\xceLPYr+\x8a\x03\xf5\xda$3B\x91\x8e\xf9lpN\xc9>\xb5\x10\x07:+\xdaTIa*\xd7z\x949D\n\xee$|z \x86|\xaeS\'&\\h\x8c\xa5hc\x06$\xdf\x11\x8aj\xca\xba`\xc0\xe0\x87L1\x15\xf1\x94\x9b|\x9b\x9e\xd8\n\xf0\x03\x01zr\xb3\xb8\x8e\xe7!3\xde\xe1\xba\xde\xa9n&\xcbAz\xc5B\x99P+!\xd9v\xcb\xb1\xc3-\x97\xb6\xfc\xbb\xa8\x10\xf7h\xa6C&\x16;\xf2\xb3Py\xfd\x81\xb0\xc0\xb8\xb1\xfb\x1e\x85GG1\x80T\x0e\xa6GY"\xbbA]\xa1R\xee\x88\xa5{Q\x9dq\xda\xbc\\+\xc3\x9f\xd9(\x05\x97L\xff\x9e\x1a\xa8\x1b\xb0@f\xbaG0\xdb;\xad\x1e\xd8\xb4\xed>b\xb3<\xe8u\xb9\xc5\xba\x06\x17\xf54\x89\xff\xb2~\xaa,\xdc\x0er\xe8c\xe5\x93WE\xee\xb8\xc9\x11\xe20(\xb5\x04\x93/SF\x00\xda)\xc4P\xd2\xceRv\xb6\xb4~y\xe15\xd8\x05g\x1a-Y\xe6{\xba\xc1\xc7{\x18\xa6\xb7\xc0\xa5\xa9\x8d\xbc\x80L$1I\xe77\x85orJl\x90x\x828\n\xf3\x11:\xec\x00\x1b\xf2\xc8\xdf\xf0\x9f\xab\xbb\xa10\xe0\xae\xee\x17h\xb8.\x0b\xb8\x91\xbfJ^b\xeb\r\xe0B\x9d\xe1`t&\xf9kr\x9f\xd7\xa2~-U\xfeOt\xed\xab\xb6\x91\xad\xfe\t\xc8\xab\xd14\xa2\xe7\xd3\x12#@\xe4\xa6\xc3\xf1\x1f_O^\xee\x95"v\xd6\xd0\xc1\xb7\xff\x86@-\x90,\x14\x0eQ/0\xfc\x11m5\xb5\x01\x13\xef\xc3=\xbc\x89\xaa\xb4\\\x8c\x12\x9e\xa5\xba\x0fpfou\xab\xbc\x11\x9b:\xd9;GG\x9aF\xeb\xee\x15\xfcC\x14\xee\r\xf1\x94g\xfbN\\yYt\xad"""


# Dies ist die Anzahl der Interationen für den Algorithmus. Je niedriger der Wert desto schneller geht das
# Ver- und Entschlüsseln. Je schneller es geht, desto mehr Angriffe kann ein potenzieller Angreifer pro Sekunde
# Ausführen. Es bietet sich also an den Wert bei ~1s zu halten, sodass ein Angreifer sehr lange braucht
# Und es für dich nicht allzu lange ist. (Skaliert linear)
iterations = 10**6


# Der Algorithmus der zum verschlüsseln und erstellen des Keys aus deinem Passwort, der wiederum zum
# Verschlüsseln verwendet wird.
algorithm = hashes.SHA3_512()


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


class Input():
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
                            b = f"{' '*(3-len(str(int(item))))}{item:{forma}} "

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
                    max_len = parser_maxlen(phlist[i:i+2], prec, mehrere, string, absval, klammer)
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

                    if isinstance(phlist[i+1], str):
                        if string:
                            x_2 = f" {anf_klam[n]}{phlist[i+1]:{str_ar}{max_len}}{end_klam[n]} "

                        else:
                            x_2 = f" {anf_klam[n]}{phlist[i+1].strip():{str_ar}{max_len}}{end_klam[n]} "

                    else:
                        forma = f".{prec}f"
                        if round(phlist[i+1], 12) == 0:
                            phlist[i] = abs(phlist[i+1])

                        if phlist[i+1] < 0:
                            temp_space = ""
                        else:
                            temp_space = vorne_space

                        b = f"{phlist[i+1]:{forma}}"
                        x_2 = f" {anf_klam[n]}{temp_space}{b:{ar}{max_len}}{end_klam[n]} "

                    forma = f"─<{max(len(x_1)-2, len(x_2)-2)}"
                    x_3 = f"╶{'':{forma}}╴"

                    if nur_pfeil:
                        ph.append(x_3)

                    else:
                        ph.append(x_1)
                        ph.append(x_3)
                        ph.append(x_2)

                    i += 2

        else:
            mitte = int(len(phlist)/2)

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
                        ph[i+1] = pfeil
                    except IndexError:
                        ph.append(pfeil)
                    i += 1
                    continue

                else:
                    if i == 0:
                        ph.insert(0, pfeil)
                    else:
                        ph[i-1] = pfeil

            if dotted:
                x = f"{anf_klam[n]}{phlist[i]:{str_ar}}{end_klam[n]}"
                j = len(x)
                if j % 2 == 0:
                    x += " "
                else:
                    x += "  "

                j = len(x)

                while j < max_len:
                    if j == max_len-1:
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
                        b = f"{' '*(3-len(str(int(phlist[i]))))}{phlist[i]:{forma}} "

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





def pass_to_string(pass_dict):
    """Dumped das Passwort in String form."""
    strich = "-------------------------"
    strich_under = "__________________________________________________"
    final_string = (f"Passwörter:\n\nFormat:\n{strich}\nName (Für Email - Email)\nEmail\nPasswort\nUsername\nGeheim True / Ja - "
                    f"Sonst False\n{strich}\n{strich_under}")
    for key, value in pass_dict.items():
        if key == "email":
            for key_2, value_2 in pass_dict[key].items():
                final_string += f"\n\n{strich}\nEmail\n{key_2}\n{value_2}\n{strich}"

        else:
            if isinstance(value, dict):
                final_string += (f"\n\n{strich}\n{key}\n{value['email']}\n{value['passwort']}\n{value['username']}\n"
                                 f"{value['geheim']}\n{strich}")

            elif isinstance(value, list):
                for item in value:
                    final_string += (f"\n\n{strich}\n{key}\n{item['email']}\n{item['passwort']}\n{item['username']}\n"
                                     f"{item['geheim']}\n{strich}")

    return final_string


def pass_to_dict(password, prov_pass):
    """Gibt ein dict aus einem Password String wieder."""
    password = password.split("__________________________________________________")[1]
    password = password.replace("\r", "")
    pass_dict = {"email": {}}
    if geheime_passwörter:
        geheim_check = prov_pass in geheime_passwörter
    else:
        geheim_check = True
    if password[-2] + password[-1] != "\n":
        password += "\n"

    pw = password.split("\n-------------------------\n")[1::2]
    iter_list = ["email", "passwort", "username", "geheim"]

    for i, item in enumerate(pw):
        item = item.split("\n")
        # Email
        if item[0].lower() == "email":
            pass_dict["email"].update({item[1]: item[2]})

        else:
            dict_hilf = {}
            if len(item[1:]) != len(iter_list):
                cprint(f"Fehler in Passwort {item[0]} ({i}): Es sind nicht alle Zeilen gesetzt: {item[1:]}")
                input()
                raise Exception

            for key, value in zip(iter_list, item[1:]):
                if key == "geheim":
                    dict_hilf.update({key: value.lower() in ["true", "ja"]})
                else:
                    dict_hilf.update({key: value})

            if dict_hilf["geheim"] and geheim_check is False:
                continue

            for values in pass_dict:
                if item[0] in values:
                    if isinstance(pass_dict[item[0]], dict):
                        dict_hilf_old = []
                        dict_hilf_old = pass_dict[item[0]]
                        dict_hilf = [dict_hilf_old, dict_hilf]

                    elif isinstance(pass_dict[item[0]], list):
                        pass_dict[item[0]].append(dict_hilf)
                        break

            else:
                dict_hilf = {item[0]: dict_hilf}
                pass_dict.update(dict_hilf)

    return pass_dict


def pass_auslesen(pass_dict):
    """Liest das Passwort aus einem dictionary aus."""
    err = Input()

    while err.error:
        print("Für was möchtest du das Passwort wissen?")
        user_key = user_input(err, string=True, min_amount=False)

    if user_key in pass_dict:
        real_key = user_key

    else:
        keys = list(pass_dict.keys())
        maximum = 0.0
        real_key = ""

    if real_key == "":
        for item in keys:
            ratio = SequenceMatcher(a=user_key, b=item).ratio()
            if ratio > maximum and ratio > toleranz_sequence:
                maximum = ratio
                real_key = item

        if maximum > toleranz_sequence:
            print((f'Der Schlüssel wurde nicht gefunden. Er konnte aber durch "{real_key}" mit {maximum * 100:.2f}% '
                   'approximiert werden.\n'))

        else:
            print("Der Schlüssel konnte nicht approximiert werden.")
            return

    if real_key == "email":
        print("Für welche E-Mail möchtest du das Passwort wissen?")
        user_key = user_input(err, string=True, min_amount=False)

        try:
            user_key = int(user_key)
            email = f"freezepro{user_key}@gmail.com"

            if email not in pass_dict["email"]:
                print("Der Eintrag wurde nicht gefunden.")

            print(f"E-Mail:")
            print(f"{email} . . {pass_dict['email'][email]}")
            return

        except ValueError:
            if user_key in pass_dict["email"]:
                real_key = user_key
                email = user_key

            else:
                keys = list(pass_dict["email"].keys())
                maximum = 0.0
                email = ""

                for item in keys:
                    ratio = SequenceMatcher(a=user_key, b=item).ratio()
                    if ratio > maximum and ratio > toleranz_sequence:
                        maximum = ratio
                        email = item

                if maximum > toleranz_sequence:
                    print((f'Der Schlüssel wurde nicht gefunden. Er konnte aber durch "{email}" mit {maximum * 100:.2f}% '
                           'approximiert werden.\n'))

                else:
                    cprint("Der Schlüssel konnte nicht approximiert werden.", "red")

            print(f"E-Mail:")
            print(f"{email} . . {pass_dict['email'][email]}")

    else:
        print_password(pass_dict, real_key)

        if not isinstance(pass_dict[real_key], (list, tuple)):
            return pass_dict[real_key]["passwort"]


def pass_aktualisieren(pass_dict, direct=None, pass_dict_geheim=None):
    """Aktualisiert das passwort in dictionary form. Kann pass_dict_geheim nur aktualisieren, falls gegeben."""
    err = Input()
    if direct is None:
        print("Welches Passwort möchtest du aktualisieren")
        user_key = user_input(err, string=True)

        if user_key in pass_dict:
            real_key = user_key

        else:
            keys = list(pass_dict.keys())
            maximum = 0.0
            real_key = ""

            for item in keys:
                ratio = SequenceMatcher(a=user_key, b=item).ratio()
                if ratio > maximum and ratio > toleranz_sequence:
                    maximum = ratio
                    real_key = item

            if maximum > toleranz_sequence:
                print((f'Der Schlüssel wurde nicht gefunden. Er konnte aber durch "{real_key}" mit {maximum * 100:.2f}% '
                       'approximiert werden.\n'))

            else:
                cprint("Der Schlüssel konnte nicht approximiert werden.", "red")
                return

    else:
        real_key = direct

    n = 0

    while True:
        err.error = True

        while err.error:
            print("Was möchtest du verändern?")
            try:
                multi_key
            except NameError:
                multi_key = None

            if isinstance(pass_dict[real_key], list) and multi_key is None:
                err_2 = Input()
                while err_2.error:
                    i = print_password(pass_dict, real_key)
                    print("Welches der Passwörter möchtest du verändern?")
                    multi_key = user_input(err_2, max_amount=i+1)

                multi_key -= 1

            keys, values, i = print_password(pass_dict, real_key, multi_key)
            print(f"{i+1}: Löschen")

            if n == 0:
                print(f"{i+2}: Abbrechen")
            else:
                print(f"{i+2}: Beenden")

            user_change = user_input(err, max_amount=i+2, erlaubte_werte="c")

            if user_change == "c":
                DataFrame([pass_dict[real_key]["passwort"]]).to_clipboard(index=False, header=False)
                err.error = True

        if user_change == i+1:
            if isinstance(pass_dict[real_key], (list, tuple)):
                del pass_dict[real_key][multi_key]
                if pass_dict_geheim is not None:
                    del pass_dict_geheim[real_key][multi_key]

                if len(pass_dict[real_key]) == 1:
                    pass_dict.update({real_key: pass_dict[real_key][0]})

            else:
                del pass_dict[real_key]
                if pass_dict_geheim is not None:
                    del pass_dict_geheim[real_key]

            return "del"

        if user_change == i+2:
            if n == 0:
                return "abbr"
            else:
                return "aktu"

        user_change -= 1

        print(f"{keys[user_change].capitalize()}:")
        print(f'Aktueller Wert: "{values[user_change]}"')

        print("Neuer Wert:")
        new_pass = user_input(err, string=True, erlaubte_werte="", random=real_key == "passwort")

        if new_pass and new_pass[0] == "r":
            try:
                pass_len = int(new_pass[2:])
            except ValueError:
                pass_len = random_length

            new_pass = "".join(random.SystemRandom().choice(random_password + string.digits) for _ in range(pass_len))

        if user_change == 0:
            pass_hilf = pass_dict[real_key]

            del pass_dict[real_key]
            if pass_dict_geheim is not None:
                del pass_dict_geheim[real_key]

            pass_dict.update({new_pass: pass_hilf})

            real_key = new_pass

        else:
            if isinstance(pass_dict[real_key], (list, tuple)):
                pass_dict[real_key][multi_key][keys[user_change]] = new_pass
            else:
                pass_dict[real_key][keys[user_change]] = new_pass

        n += 1


def pass_hinzufügen(pass_dict):
    """Fügt ein Passwort zu pass_dict hinzu."""
    err = Input()
    while err.error:
        print("Wie soll der Name des neuen Passworts sein?\n")
        pass_name = user_input(err, string=True)

    if pass_name.lower() == "email":
        neues_passwort = {"email": {"email": "", "passwort": ""}}

    else:
        neues_passwort = {pass_name: {"email": "", "passwort": "", "username": "", "geheim": False}}

    append = False

    if pass_name in pass_dict:
        err.error = True
        while err.error:
            print("Das eingegebene Passwort befindet sich bereits in der Datenbank mit folgenden Eigenschaften:")
            print_password(pass_dict, pass_name)
            print("\n")
            print("Möchtest du")
            print("1: Einen neuen Eintrag unter dem gleichen Namen anlegen")
            _ = "Den"
            if isinstance(pass_dict[pass_name], (tuple, list)):
                _ = "Einen"
            print(f"2: {_} vorhandenen Eintrag aktualisieren")
            print(f"3: Den vorhandenen Eintrag mit einem neuen Passwort überschreiben")
            aktion = user_input(err, max_amount=3)

        if aktion == 1:
            append = True

        elif aktion == 2:
            pass_aktualisieren(pass_dict, pass_name)
            return "aktu"

    n = 0

    while True:
        err.error = True
        while err.error:
            keys, values, i = print_password(neues_passwort, pass_name)

            if n == 0:
                print(f"{i+1}: Abbrechen")
            else:
                print(f"{i+1}: Fertig")

            to_update = user_input(err, max_amount=i+1, erlaubte_werte="c")

            if to_update == "c":
                DataFrame([neues_passwort[pass_name]["passwort"]]).to_clipboard(index=False, header=False)
                continue

        if to_update == i + 1:
            if n == 0:
                return "abbr"

            else:
                if pass_name.lower() == "email":
                    pass_dict["email"].update({neues_passwort["email"]["email"]: neues_passwort["email"]["passwort"]})

                elif append:
                    if isinstance(pass_dict[pass_name], dict):
                        neues_passwort = [pass_dict[pass_name], neues_passwort[pass_name]]
                        pass_dict.update({pass_name: neues_passwort})

                    elif isinstance(pass_dict[pass_name], list):
                        pass_dict[pass_name].append(neues_passwort[pass_name])

                else:
                    pass_dict.update(neues_passwort)

                return "hinz"

        to_update -= 1

        print(f"{keys[to_update].capitalize()}:")
        print(f'Aktueller Wert: "{values[to_update]}"')

        print("Neuer Wert:")
        new_pass = user_input(err, string=True, erlaubte_werte="", random=to_update == "passwort")

        if new_pass and new_pass[0] == "r":
            try:
                pass_len = int(new_pass[2:])
            except ValueError:
                pass_len = random_length

            new_pass = "".join(random.SystemRandom().choice(random_password + string.digits) for _ in range(pass_len))

        if to_update == 0:
            neues_passwort = {new_pass: neues_passwort[pass_name]}
            pass_name = new_pass
        else:
            neues_passwort[pass_name][keys[to_update]] = new_pass

        n += 1


def demo():
    """Erstellt die Demo Datei."""
    with open(demo_file, "w+") as f:
        pass_dict = {"email": {"DianaEbersbacher@cuvox.de": """{YTxR"2!-qkN}j^;""", "SaraBayer@cuvox.de": """')/Nzu*3-j8A/p+r"""},
                     "Passwort 1": {"email": "NiklasAckerman@einrot.com", "passwort": """2y(MN`'qc(n,J.vr""",
                                    "username": "Niklas1234", "geheim": False},
                     "Passwort 2": {"email": "FrankBarth@einrot.com", "passwort": """6a3jT4m.p<,7xZw&""",
                                    "username": "Frank1234", "geheim": True},
                     "Passwort 3": [{"email": "MathiasFreeh@cuvox.de", "passwort": """&Vp3;,%(BST8CL}@""",
                                    "username": "Mathias1234", "geheim": False},
                                    {"email": "DirkBaer@cuvox.de", "passwort": """;Pvd{JK.7D5vH{+!""",
                                    "username": "Dirk1234", "geheim": False}]
                     }

        pass_str = pass_to_string(pass_dict)

        f.write(pass_str)


def print_password(pass_dict, key, list_num=None):
    """Gibt das Passwort mit einem bestimmten key aus."""
    if isinstance(pass_dict[key], (list, tuple)) and list_num is None:
        print("Dieses Passwort hat mehrere Einträge:\n")

        for i, item in enumerate(pass_dict[key]):
            print(f"{i+1}.")
            print_password({key: item}, key)

            if i != len(pass_dict[key]) - 1:
                print("\n")

        return i

    else:
        if isinstance(pass_dict[key], (list, tuple)):
            pass_dict = {key: pass_dict[key][list_num]}

        keys = ["Name"] + list(pass_dict[key].keys())
        values = [key] + list(pass_dict[key].values())

        keys_darst = format_prec(keys, ausrichtung="links", string=True, dotted=True, dotted_len=5)

        for i, (key, value) in enumerate(zip(keys_darst, values), start=1):
            print(f"{i}: {key.capitalize()}{value}")

        return keys, values, i


def check_exists():
    """Überprüft, ob die jeweiligen datein existieren"""
    encrypted_exists = True
    clean_exists = True
    demo_exists = True
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

    return encrypted_exists, clean_exists, demo_exists


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
            contents = f.read()
            encrypted = _encrypter(user_password, contents)

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
    while True:
        print("Bitte Passwort eingeben:\n")
        user_password = getpass()
        cls()

        if user_password in geheime_passwörter:
            geheim_pass = user_password
            cprint("Das Passwort ist Falsch!\n", "yellow")
            continue

        try:
            with open(encrypted_file, "r") as f:
                decrypted = _decrypter(user_password, f.read())

                break

        except InvalidToken:
            cprint("Das Passwort ist Falsch!\n", "red")

    return user_password, geheim_pass, decrypted


length = 32
backend = default_backend()


def main():
    """Haupt Funktion für den Manager."""
    err = Input()
    geheim = False
    while True:
        encrypted_exists, clean_exists, demo_exists = check_exists()
        while err.error:
            erlaubte_werte = [1, 3]

            print("Was möchtest du tun?\n")

            print("1: Passwort eingeben")

            if clean_exists:
                print(f"2: Verschlüsselte Datei aus {clean_file} erstellen")
                erlaubte_werte.append(2)
            else:
                print()

            if demo_exists:
                print(f"3: Verschlüsselte Datei aus {demo_file} erstellen")
            else:
                print("3: Demo Datei erstellen")

            aktion = user_input(err, max_amount=False, erlaubte_werte=erlaubte_werte + geheime_passwörter)

        err.error = True

        if aktion == 1:
            if encrypted_exists:
                user_password, geheim_pass, decrypted = decrypter(encrypted_file)

                if geheim_pass in geheime_passwörter:
                    geheim = True

            else:
                err.error = True
                while err.error:
                    erlaubte_werte = []
                    print("Es wurde keine verschlüsselte Datei gefunden. Was möchtest du tun?\n")
                    if clean_exists:
                        print(f"1: Eine verschlüsselte Datei aus {clean_file} erstellen")
                        erlaubte_werte.append(1)

                    if demo_exists:
                        print(f"2: Eine verschlüsselte Datei aus {demo_file} erstellen")
                        erlaubte_werte.append(2)

                    print(f"3: Eine neue Datenbank anlegen")

                    aktion = user_input(err, min_amount=3, max_amount=3, erlaubte_werte=erlaubte_werte)

                if aktion in [1, 2]:
                    if aktion == 1:
                        file = clean_file
                    elif aktion == 2:
                        file = demo_file

                    user_password = encrypter(file)

                    cprint("\nVerschlüsselte Datei erfolgreich erstellt\n\n", "green")

                    with open(file) as f:
                        decrypted = f.read()

                    encrypted_exists = True
                    geheim_pass = ""

                elif aktion == 3:
                    pass_dict = {"email": {}}
                    pass_dict_geheim = copy.deepcopy(pass_dict)

            break

        elif aktion == 2:
            encrypter(clean_file)
            cprint("\nVerschlüsselte Datei erfolgreich erstellt\n\n", "green")

        elif aktion == 3:
            if demo_exists:
                encrypter(demo_file)

                cprint("\nVerschlüsselte Datei erfolgreich erstellt\n\n", "green")

            else:
                demo()

    if encrypted_exists:
        pass_dict = pass_to_dict(decrypted, geheim_pass)
        pass_dict_geheim = pass_to_dict(decrypted, geheime_passwörter[0])

    err = Input()

    passw = None

    while True:
        ret = None
        while err.error:
            print("Was möchtest du tun?\n")
            print("1: Password auslesen")
            print("2: Passwort aktualisieren")
            print("3: Passwort hinzufügen")
            print("4: Verschlüsselte Datei aus aktuellem Passwort erstellen")
            print("5: Textdatei aus aktuellem Passwort erstellen")
            if clean_exists:
                print(f"6: Verschlüsselte Datei aus {clean_file} erstellen")
            print("7: Beenden")
            aktion = user_input(err, max_amount=7, erlaubte_werte=["c"] + geheime_passwörter)

        err.error = True

        if aktion in geheime_passwörter:
            pass_dict = pass_dict_geheim

        if aktion == "c":
            DataFrame([passw]).to_clipboard(index=False, header=False)
            err.error = True

        elif aktion == 1:
            passw = pass_auslesen(pass_dict)

        elif aktion == 2:
            ret = pass_aktualisieren(pass_dict, pass_dict_geheim=pass_dict_geheim)

        elif aktion == 3:
            ret = pass_hinzufügen(pass_dict)

        elif aktion == 4:
            encrypter(pass_to_string(pass_dict_geheim), string=True)
            ret = "encr_aktu"

        elif aktion == 5:
            pass_string = pass_to_string(pass_dict_geheim)

            with open(clean_file, "w+") as f:
                f.write(pass_string)

            ret = "text_aktu"

        elif aktion == 6:
            encrypter(clean_file)
            ret = "encr_pass"

        elif aktion == 7:
            break

        print()

        if ret == "hinz":
            cprint("Erfolgreich hinzugefügt", "green")

        elif ret == "abbr":
            cprint("Erfolgreich abgebrochen", "green")

        elif ret == "aktu":
            cprint("Erfolgreich aktualisiert", "green")

        elif ret == "del":
            cprint("Erfolgreich gelöscht", "green")

        elif ret == "text_aktu":
            cprint("Textdatei aus aktuellem Passwort erfolgreich erstellt!", "green")

        elif ret == "encr_aktu":
            cprint("Verschlüsselte Datei aus aktuellem Passwort erfolgreich erstellt", "green")

        elif ret == "encr_pass":
            cprint(f"Verschlüsselte Datei aus {clean_file} erfolgreich erstellt", "green")

        if ret is not None:
            print("\n")

        pass_dict_geheim.update(pass_dict)


if __name__ == "__main__":
    main()
































