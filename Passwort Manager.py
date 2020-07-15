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

salt = b"""(N\x18\xdbkJ{\xc4\xfb\x1a\x9d\xf3\xff\xda\xe0N\x01\xc5;09\x1eH\xd3\x8e\xdd\x1c"m\x9c\x12\xa6\xc2R\xdd\xcf\x9b\xd2\xe6w7G\x84=\x81\xb3\xf3\x8d\xf1D\x12\x7f\xc9\xa6\xaa\xb8L\xf8\xd7\xeb}\xfb\xfe\x8b\xa0\x00X\x08\xb3H\xaa\x00\xc5\x91\xa9\x8aT\xecX\x80\xc9;\x94\xe9"\xae\xa8KK\xe1\x07\xdax[4\x03B\xd4G\xd0\xf3\x95\xc89\xfa\xac\x1c\x83\xe1\xee\x89\xc0tM\x01"Y\x00}\x12qY\x94>\xb6\x1f;\xc0\xdf\xb0\xd3\x83\x9fV\x9c\x93\x9d\xbd\x82\xf2\r\x94!s\x97\xc1\x1f4\xcd\xdc\xf1\x16\xb6\xc59\\\x1e:\x7ff\x9f\xe3\xf5\x8bX\xdbU\xfe{w\xa9\xfc\x03e\xbaK\x9a0j\x91\xf7@d.\xff\xe5\xef\xf7R\xe0`\xd9\x0cl\x84>p\xe8q\xa3X\x90\']8@\x16\x90V\xc3\xd2\xa7 CP\x93\x046\x11tk\x01\x1e\x1aC@\xf3bH"\xbe\x06:_A\xd8$\xb9\x89\xaeD\xd4\xb2\x83\xddS -8M\x1b\xeex\xca\x84\xf1"""


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
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

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

