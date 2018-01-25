import re

lista_korisnika = []


def registracija_korisnika():
    """
    Metoda za rucni unos korisnika
    :return: korisnik <- dict
    """
    global lista_korisnika
    korisnik = {}

    korisnik["ime"] = input("Unesite ime: ")
    korisnik["prezime"] = input("Unesite prezime: ")
    korisnik["korisnicko_ime"] = dodaj_korisnicko()
    korisnik["lozinka"] = dodaj_siru()
    korisnik["tip"] = "kupac"

    # dodaj korisnika na globalnu listu
    lista_korisnika.append(korisnik)

    # snimanje korisnika
    sacuvaj_korisnika(korisnik)
    return korisnik


def registracija_radnika():
    """
    Metoda za registraciju novih menadzera ili radnika
    :return: 
    """
    global lista_korisnika
    korisnik = {}

    korisnik["ime"] = input("Unesite ime: ")
    korisnik["prezime"] = input("Unesite prezime: ")
    korisnik["korisnicko_ime"] = dodaj_korisnicko()
    korisnik["lozinka"] = dodaj_siru()
    korisnik["tip"] = dodaj_tip()

    # dodaj korisnika na globalnu listu
    lista_korisnika.append(korisnik)

    # snimanje korisnika
    sacuvaj_korisnika(korisnik)
    return korisnik


# pomocne funkcije za unos korisnika

def dodaj_korisnicko():
    while True:
        unos = input("Unesite korisnicko ime:").strip()
        if provera_korisnickog_imena(unos):
            print("Korisnicko ime vec postoji, probajte ponovo!")
            continue
        return unos


def provera_korisnickog_imena(sifra):
    for korisnik in lista_korisnika:
        if korisnik["korisnicko_ime"] == sifra:
            print("Pogresan unos korisnickog imena")
            return True
    return False


def dodaj_siru():
    while True:
        unos = input("Unesite sifru:").strip()
        if provera_sifre(unos):
            print("Sifra mora da bude duza od 6 karaktera i da ima bar jedan broj!")
            continue
        return unos


def provera_sifre(sifra):
    if len(sifra) < 6:
        return True
    if not re.search(r"[\d]+", sifra):
        return True
    return False


def dodaj_tip():
    while True:
        print("\t Izaberite tip novog korisnika")
        print("\t 1. Prodavac")
        print("\t 2. Menadzer")
        opcija = input(">>").strip()
        if opcija == "1":
            return "prodavac"
        elif opcija == "2":
            return "menadzer"
        else:
            print("Nepoznat unos! Pokusajte ponovo")


def prijava():
    kor_ime = input("Unesite korisnicko ime: ")
    sifra = input("Unesite lozinku: ")

    for korisnik in lista_korisnika:
        if korisnik["korisnicko_ime"] == kor_ime and korisnik["lozinka"] == sifra:
            return korisnik
    return None


def vrati_korisnika(korisnicko_ime):
    for korisnik in lista_korisnika:
        if korisnik["korisnicko_ime"].lower() == korisnicko_ime.lower():
            return korisnik


def vrati_kupce():
    lst = []
    for korisnik in lista_korisnika:
        if korisnik["tip"].lower()=="kupac":
            lst.append(korisnik)
    return lst


def print_korisnike(lst=lista_korisnika):
    print()
    zaglavlje = "{0:<20} {1:<20} {2:<20} {3:<20}".format(
        "IME",
        "PREZIME",
        "KORISNICKO IME",
        "TIP")
    zaglavlje_linija = "{0:-<20} {1:-<20} {2:-<20} {3:-<20}".format(
        "-", "-", "-", "-")
    print(zaglavlje)
    print(zaglavlje_linija)
    for korisnik in lst:
        linija = "{0:<20} {1:<20} {2:<20} {3:<20}".format(
            korisnik["ime"].capitalize(),
            korisnik["prezime"].capitalize(),
            korisnik["korisnicko_ime"],
            korisnik["tip"]
        )
        print(linija)
    print()


# metode koje citaju iz fajlova

def sacuvaj_korisnika(korisnik, fajl="podaci/korisnici.txt"):
    with open(fajl, "a") as f:
        f.write(korisnik2str(korisnik))
        f.write("\n")


def ucitavanje_korisnika():
    global lista_korisnika
    lista_korisnika = []
    with open("podaci/korisnici.txt", "r") as f:
        for linija in f:
            lista_korisnika.append(str2korisnik(linija))


# metode za konverziju korinika

def str2korisnik(linija):
    try:
        ime, prezime, korisnicko_ime, lozinka, tip = linija.strip().split("|")
    except ValueError:
        print("Greska pri ucitavanju iz baze, korisnik nije ucitan.")
        return
    korisnik = {"ime": ime, "prezime": prezime, "korisnicko_ime": korisnicko_ime, "lozinka": lozinka, "tip": tip}
    return korisnik


def korisnik2str(korisnik):
    return "|".join(
        [korisnik["ime"], korisnik["prezime"], korisnik["korisnicko_ime"], korisnik["lozinka"], korisnik["tip"]])


def sacuvaj_sve(fajl="podaci/korisnici.txt"):
    with open(fajl, "w") as f:
        for korisnik in lista_korisnika:
            f.write(korisnik2str(korisnik))
            f.write("\n")
