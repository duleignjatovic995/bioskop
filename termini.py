import sale
import re
from datetime import datetime
import projekcije
import karte
import meni

lista_termina = []


def dodaj_termin(projekcija):
    """
    Metoda za rucno dodavanje termina
    :param projekcija:
    """
    try:
        termin = {}
        datum = dodaj_datum(projekcija)
        termin["datum"] = datum
        termin["projekcija"] = projekcija
        termin["sifra"] = dodaj_sifru(projekcija)
        termin["sala"] = projekcija["sala"]
        termin["sedista"] = kreiraj_sedista(projekcija)  # kreiranje matrice sedista
        termin["cena"] = dodaj_cenu(projekcija, datum)  # dodajemo cenu da bi pratili snizenja u odnosu na dane

        lista_termina.append(termin)  # dodajemo termin u listu
        sacuvaj_termin(termin2str(termin))  # snimamo termin u datoteku
    except:
        print("Greska pri cuvanju termina.")


# pomocne funkcije za rucno dodavanje termina

def dodaj_datum(projekcija):
    while True:
        print("Unesite datum u formatu dd-mm-yyyy")
        datums = input(">>").strip()
        try:
            datum = datetime.strptime(datums, '%d-%m-%Y')
            dan = datum.strftime("%A").lower()

            if dan not in projekcija["dani"]:
                print("Dani nisu u skladu! Moguci dani su: ")
                print(", ".join(projekcija["dani"]))
                print("Probajte ponovo.")
                continue

        except:
            print("Lose unet datum, probajte ponovo")
            continue
        return datum


def dodaj_sifru(projekcija):
    while True:
        print("Unesite 2 karaktera za sifru termina")
        karakteri = input(">>").strip().upper()
        if provera_sifre1(karakteri) and provera_sifre2(karakteri) and provera_sifre3(karakteri):
            return str(projekcija["sifra"]) + karakteri
        else:
            continue


def provera_sifre1(sifra):
    for t in lista_termina:
        if t["sifra"] == sifra:
            print("Sifra vec postoji.")
            return False
    return True


def provera_sifre2(sifra):
    pattern = re.compile("[A-Za-z]{2}")
    if not bool(pattern.match(sifra)):
        print("Morate uneti dva karaktera (slova).")
        return False
    return True


def provera_sifre3(sifra):
    if len(sifra) > 2:
        print("Uneli ste vise od 2 karaktera.")
        return False
    elif len(sifra) < 2:
        print("Uneli ste manje od 2 karaktera.")
        return False
    return True


def kreiraj_sedista(projekcija):
    """
    Funkcija kreira matricu redova i kolona koja predstavlja 
    jednu bioskopsku salu.
    :param projekcija: 
    :return: [['a', 'b', 'c'], ['a', 'b', 'c']]
    """
    sala = sale.vrati_salu(projekcija["sala"]["sifra"])
    redovi = sala["redovi"]
    kolone = sala["sedista"]
    sedista = []
    for _ in redovi:
        sedista.append(kolone)
    return sedista


def dodaj_cenu(projekcija, datum):
    """
    Metoda kojom dodajemo modifikovanu cenu na termin
    :param projekcija: 
    :param datum: 
    :return: modifikovana cena
    """
    cena = float(projekcija["cena"])
    dan = datetime.strftime(datum, "%A").lower()
    if dan == "tuesday":
        cena -= 50
    elif dan == "saturday" or dan == "sunday":
        cena += 50

    return str(cena)


def pretraga_termina(sifra_projekcije):
    """
    Funkcija vraca listu termina.
    Na osnovu sifre projekcije pronalazi sve termine.
    
    :param sifra_projekcije: Sifra bioskopske projekcije
    :return: lista termina projekcija
    """
    lst = []
    sifra = sifra_projekcije.lower()
    for termin in lista_termina:
        if sifra == termin["projekcija"]["sifra"].lower():
            lst.append(termin)
    return lst


def print_termine(lst=lista_termina):
    print()
    zaglavlje = "{0:<20} {1:<20} {2:<20}".format("SIFRA TERMINA", "NAZIV FILMA", "DATUM")
    zaglavlje_linija = "{0:-<20} {1:-<20} {2:-<20}".format("-", "-", "-")
    print(zaglavlje)
    print(zaglavlje_linija)
    for termin in lst:
        linija = "{0:<20} {1:<15} {2:<10}".format(termin["sifra"],
                                                  termin["projekcija"]["film"]["naziv_filma"],
                                                  datetime.strftime(termin["datum"], "%d-%m-%Y"))
        print(linija)
    print()


# metode za cuvanje i ucitavanje

def sacuvaj_termin(termin, fajl="podaci/termini.txt"):
    with open(fajl, "a") as f:
        f.write(termin)
        f.write("\n")


def ucitavanje_termina(fajl="podaci/termini.txt"):
    global lista_termina
    with open(fajl, "r") as f:
        for linija in f:
            lista_termina.append(str2termin(linija))


# metode za konverziju

def termin2str(termin):
    datum = datetime.strftime(termin["datum"], "%d-%m-%Y")
    projekcija = str(termin["projekcija"]["sifra"])
    sifra = str(termin["sifra"])
    sala = termin["sala"]["sifra"]
    sedista = sedista2str(termin["sedista"])
    cena = termin["cena"]
    return sifra + "|" + datum + "|" + projekcija + "|" + str(sala) + "|" + sedista + "|" + str(cena)


def str2termin(linija):
    sifra, datums, projekcijas, sala_s, sedista, cena = linija.strip().split("|")
    # if projekcijas is None or projekcijas == "": todo makni
    #     return None
    termin = {
        "sifra": sifra,
        "datum": datetime.strptime(datums, '%d-%m-%Y'),
        "projekcija": projekcije.vrati_projekciju(projekcijas),
        "sala": sale.vrati_salu(sala_s),
        "sedista": str2sedista(sedista),
        "cena": str2cena(projekcijas, datums)
    }
    return termin


def str2cena(projekcijas, datums):
    projekcija = projekcije.vrati_projekciju(projekcijas)
    datum = datetime.strptime(datums, '%d-%m-%Y')
    cena = float(projekcija["cena"])
    dan = datum.strftime("%A").lower()
    if dan == "tuesday":
        cena -= 50
    elif dan == "saturday" or dan == "sunday":
        cena += 50

    return str(cena)


def sedista2str(sedista):
    str_sala = ""
    for red in sedista:
        str_red = ",".join(red)
        str_sala += str_red + ";"
    return str_sala.rstrip(";")


def str2sedista(linija):
    redovi = linija.strip().split(";")
    sedista = []
    for r in redovi:
        red = r.strip().split(",")
        sedista.append(red)
    return sedista


# metoda za vracanje termina

def vrati_termin(sifra):
    # if provera_sifre3(sifra) and provera_sifre2(sifra):
    for t in lista_termina:
        if t["sifra"].lower() == sifra.lower():
            return t


# metode za rezervaciju sala

def print_sedista(termin):
    sala = termin["sedista"]
    for i in range(len(sala)):
        print(str(i + 1) + ". Red: " + " ".join(sala[i]).upper())


def proveri_sediste(termin, red, kolona):
    sedista = termin["sedista"]
    if "x" == sedista[red][kolona].lower():
        return False

    return True


def rezervisi_sediste(korisnik, termin, red, kolona):
    try:
        red = int(red)
    except:
        print("Niste uneli ceo broj!")
    if proveri_sediste(termin, red, kolona):
        karte.dodaj_kartu(korisnik, termin, red, kolona)
    else:
        print("Sediste nije slobodno!")
    print_sedista(termin)
    sacuvaj_sve()


def prodaj_sediste(korisnik, termin, red, kolona):
    try:
        red = int(red)
    except:
        print("Niste uneli ceo broj!")
    if proveri_sediste(termin, red, kolona):
        karte.dodaj_kartu(korisnik, termin, red, kolona, tip="kupljena")
    else:
        print("Sediste nije slobodno!")
    print_sedista(termin)
    sacuvaj_sve()


def prodaj_rezervisano_sediste(karta):
    karta["tip"] = "kupljena"
    karta["datum_prodaje"] = datetime.now()
    sacuvaj_sve()
    karte.sacuvaj_sve()


# metode za brisanje i izmenu

def sacuvaj_sve(fajl="podaci/termini.txt"):
    with open(fajl, "w") as f:
        for termin in lista_termina:
            f.write(termin2str(termin))
            f.write("\n")


def oslobodi_sediste(karta):
    oznaka = karta["oznaka"]
    raw_red, raw_kolona = oznaka[0], oznaka[1].lower()
    red = int(raw_red) - 1
    kolona = ord(raw_kolona) - 97
    termin = vrati_termin(karta["termin"]["sifra"])
    sedista = termin["sedista"]
    sedista[red][kolona] = raw_kolona
    sacuvaj_sve()


# todo makni
# def refresh_termine():
#     global lista_termina
#     lista_termina = []
#     ucitavanje_termina()
#     karte.refresh_karte()


def update_termin_cena(projekcija):
    for termin in lista_termina:
        if termin["projekcija"]["sifra"] == projekcija["sifra"]:
            termin["cena"] = dodaj_cenu(projekcija, termin["datum"])


def obrisi_termin(termin):
    karte.obavesti_obrisan_termin(termin)
    lista_termina.remove(termin)
    sacuvaj_sve()


def obavesti_obrisana_projekcija(projekcija):
    for termin in lista_termina:
        if projekcija is termin["projekcija"]:
            karte.obavesti_obrisan_termin(termin)
            lista_termina.remove(termin)
    sacuvaj_sve()


def izmeni_termin(termin):
    while True:
        print("Izmeni termin projekcije po:")
        print("0. Zavrsi i sacuvaj sve promene")
        print("1. Sifra")
        print("2. Datum")

        opcija = input(">>").strip()

        if opcija == "1":
            unos = dodaj_sifru(termin["projekcija"])
            termin["sifra"] = unos
            meni.sacuvaj_ceo_sistem()
            print("Uspesno promenjena sifra")

        elif opcija == "2":
            datum = dodaj_datum(termin["projekcija"])
            termin["datum"] = datum
            termin["cena"] = dodaj_cenu(termin["projekcija"], datum)
            print("Uspesno ste promenili datum")

        elif opcija == "0":
            break

        else:
            print("Nepoznata akcija! Probajte ponovo...")

    sacuvaj_sve()
    print("Sacuvane sve promene nad terminom u fajlovima!")
