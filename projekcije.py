import re

import filmovi
import sale
from datetime import datetime
import meni
import termini

lista_projekcija = []


def dodaj_projekciju():
    """
    Metoda za rucno dodavanje projekcije.
    :return: 
    """
    try:
        global lista_projekcija

        projekcija = {}
        projekcija["sifra"] = dodaj_sifru()
        projekcija["sala"] = dodaj_salu()
        projekcija["pocetak"] = dodaj_vreme("pocetak")
        projekcija["kraj"] = dodaj_vreme("kraj")
        projekcija["dani"] = dodaj_dane()
        projekcija["film"] = dodaj_film()
        projekcija["cena"] = dodaj_cenu()

        lista_projekcija.append(projekcija)
        print_projekcije([projekcija])
        sacuvaj_projekciju(projekcija2str(projekcija))
    except:
        print("Greska pri dodavanju projekcije.")
        return

    print("Projekcija uspesno dodata!")


# pomocne funkcije za rucno dodavanje projekcija

def dodaj_sifru():
    while True:
        print("Unesite sifru projekcije")
        sifra = input(">>").strip()
        if provera_sifre1(sifra) and provera_sifre2(sifra) and provera_sifre3(sifra):
            return sifra
        else:
            continue


def provera_sifre1(sifra):
    for p in lista_projekcija:
        if p["sifra"] == sifra:
            print("Dodeljena sifra vec postoji")
            return False
    return True


def provera_sifre2(sifra):
    pattern = re.compile(r"[\d]{4}")
    if not bool(pattern.match(sifra)):
        print("Sifra mora da ima 4 cifre")
        return False
    return True


def provera_sifre3(sifra):
    if len(sifra) > 4:
        print("Sifra je predukacka, sifra projekcije mora da ima 4 cifre.")
        return False
    elif len(sifra) < 4:
        print("Sifra je prekratka, sifra projekcije mora da ima 4 cifre.")
        return False
    return True


def dodaj_salu():
    sale.print_sale()
    while True:
        print("Unesite sifru sale za ovu projekciju:")
        sifra_sale = input(">>").strip().upper()
        sala = sale.vrati_salu(sifra_sale)
        if sala is None:
            print("Pogresan unos sifre sale.")
            continue
        return sala


def dodaj_vreme(poc_kra):
    while True:
        print("Unesite " + poc_kra + " u formatu hh:mm")
        str_vreme = input(">>").strip()
        try:
            vreme = datetime.strptime(str_vreme, "%H:%M")
        except:
            print("Pogresno unesen format vremena, probajte ponovo")
            continue
        return vreme


def dodaj_dane():
    lst_dani = []
    print("Dodajte kojim danima ce se pustati film:")
    print("0. Zavrsen unos")
    print("1. Ponedeljak")
    print("2. Utorak")
    print("3. Sreda")
    print("4. Cetvrtak")
    print("5. Petak")
    print("6. Subota")
    print("7. Nedelja")
    while True:

        opcija = input(">>").strip()

        if opcija == "1":
            lst_dani.append("monday")
        elif opcija == "2":
            lst_dani.append("tuesday")
        elif opcija == "3":
            lst_dani.append("wednesday")
        elif opcija == "4":
            lst_dani.append("thursday")
        elif opcija == "5":
            lst_dani.append("friday")
        elif opcija == "6":
            lst_dani.append("saturday")
        elif opcija == "7":
            lst_dani.append("sunday")
        elif opcija == "0":
            if len(lst_dani) == 0:
                print("Morate uneti bar jedan dan")
                continue
            return lst_dani
        else:
            print("Nepoznata operacija")


        # print("Unesite dane na engleskom! (monday, tuesday...):")
        # inp_dani = input(">>").strip()
        # try:
        #     dani = inp_dani.strip().split(",")
        # except:
        #     print("Greska pri unosu dana")
        #     continue
        # return dani


def dodaj_film():
    filmovi.print_filmove()
    while True:
        print("Unesite naziv filma za projekciju")
        naziv = input(">>").strip()
        film = filmovi.vrati_film(naziv)
        if film is None:
            print("Pogresno unet naziv filma")
            continue
        return film


def dodaj_cenu():
    while True:
        print("Unesite cenu projekcije.")
        cena = input(">>").strip()
        try:
            float(cena)
        except ValueError:
            print("Cena mora da bude ceo broj")
            continue
        return cena


# funkcije za rad sa fajlovima

def sacuvaj_projekciju(projekcija, fajl="podaci/projekcije.txt"):
    with open(fajl, "a") as f:
        f.write(projekcija)
        f.write("\n")


def ucitavanje_projekcija(fajl="podaci/projekcije.txt"):
    global lista_projekcija
    with open(fajl, "r") as f:
        for linija in f:
            projekcija = str2projekcija(linija)
            if projekcija is None:
                continue
            lista_projekcija.append(projekcija)


def print_projekcije(lst=lista_projekcija):
    print()
    zaglavlje = "{0:<20} {1:<20} {2:<20} {3:<20} {4:<20}".format("SIFRA", "FILM", "SALA", "POCETAK", "KRAJ")
    zaglavlje_linija = "{0:-<20} {1:-<20} {2:-<20} {3:-<20} {4:-<20}".format("-", "-", "-", "-", "-")
    print(zaglavlje)
    print(zaglavlje_linija)
    for projekcija in lst:
        linija = "{0:<20} {1:<20} {2:<20} {3:<20} {4:<20}".format(projekcija["sifra"],
                                                                  projekcija["film"]["naziv_filma"],
                                                                  projekcija["sala"]["sifra"],
                                                                  datetime.strftime(projekcija["pocetak"], "%H:%M"),
                                                                  datetime.strftime(projekcija["kraj"], "%H:%M"))
        print(linija)
    print()


# pretrage projekcija

def pretraga_po_filmu(upit):
    lst = []
    for projekcija in lista_projekcija:
        if upit in projekcija["film"]["naziv_filma"].lower():
            lst.append(projekcija)
    return lst


def pretraga_po_sali(upit):
    lst = []
    for projekcija in lista_projekcija:
        if upit == projekcija["sala"]["sifra"].lower():
            lst.append(projekcija)
    return lst


def pretraga_po_pocetku(upit):
    lst = []
    upit = datetime.strptime(upit, "%H:%M")
    for projekcija in lista_projekcija:
        if upit == projekcija["pocetak"]:
            lst.append(projekcija)
    return lst


def pretraga_po_kraju(upit):
    lst = []
    upit = datetime.strptime(upit, "%H:%M")
    for projekcija in lista_projekcija:
        if upit == projekcija["kraj"]:
            lst.append(projekcija)
    return lst


# funkcija za vracanje projekcije na osnovu sifre

def vrati_projekciju(sifra):
    for p in lista_projekcija:
        if p["sifra"] == sifra:
            return p


# konverzije projekcija

def projekcija2str(projekcija):
    sifra = projekcija["sifra"]
    sala = projekcija["sala"]["sifra"]
    pocetak = datetime.strftime(projekcija["pocetak"], "%H:%M")
    kraj = datetime.strftime(projekcija["kraj"], "%H:%M")
    dani = ",".join(str(d) for d in projekcija["dani"])
    film = projekcija["film"]["naziv_filma"]
    cena = projekcija["cena"]

    return sifra + "|" + sala + "|" + pocetak + "|" + kraj + "|" + dani + "|" + film + "|" + cena


def str2projekcija(linija):
    sifra, s_sale, pocetak_s, kraj_s, dani, film_s, cena = linija.strip().split("|")
    pocetak = datetime.strptime(pocetak_s, "%H:%M")
    kraj = datetime.strptime(kraj_s, "%H:%M")
    film = filmovi.vrati_film(film_s)
    sala = sale.vrati_salu(s_sale)
    if film is None:
        return
    if sala is None:
        return
    return {"sifra": sifra, "sala": sala, "pocetak": pocetak, "kraj": kraj,
            "dani": dani.split(","), "film": film, "cena": cena}


# brisanje i izmena projekcije

def obrisi_projekciju(projekcija):

    lista_projekcija.remove(projekcija)
    termini.obavesti_obrisana_projekcija(projekcija)
    sacuvaj_sve()


def obavesti_obrisan_film(film):
    for projekcija in lista_projekcija:
        if film is projekcija["film"]:

            lista_projekcija.remove(projekcija)
            termini.obavesti_obrisana_projekcija(projekcija)
    sacuvaj_sve()


def obavesti_obrisana_sala(sala):
    for projekcija in lista_projekcija:
        if sala is projekcija["sala"]:

            lista_projekcija.remove(projekcija)
            termini.obavesti_obrisana_projekcija(projekcija)
    sacuvaj_sve()


def sacuvaj_sve(fajl="podaci/projekcije.txt"):
    with open(fajl, "w") as f:
        for projekcija in lista_projekcija:
            f.write(projekcija2str(projekcija))
            f.write("\n")


def izmeni_projekciju(projekcija):
    while True:
        print("Izmeni projekciju po:")
        print("0. Zavrsi i sacuvaj sve promene")
        print("1. Sala")
        print("2. Pocetak")
        print("3. Kraj")
        print("4. Dani")
        print("5. Film")
        print("6. Cena")

        opcija = input(">>").strip()

        if opcija == "1":
            unos = dodaj_salu()
            projekcija["sala"] = unos
            print("Uspesno sacuvana sala za projekciju")

        elif opcija == "2":
            unos = dodaj_vreme("pocetak")
            projekcija["pocetak"] = unos
            print("Uspesno sacuvan pocetak projekcije")

        elif opcija == "3":
            unos = dodaj_vreme("kraj")
            projekcija["kraj"] = unos
            print("Uspesno sacuvan kraj projekcije")

        elif opcija == "4":
            unos = dodaj_dane()
            projekcija["dani"] = unos
            print("Uspesno sacuvani dani projekcije")

        elif opcija == "5":
            unos = dodaj_film()
            projekcija["film"] = unos
            print("Uspesno sacuvan film projekcije")

        elif opcija == "6":
            unos = dodaj_cenu()
            projekcija["cena"] = unos
            termini.update_termin_cena(projekcija)  # obavestavamo termin da se promenila cena
            meni.sacuvaj_ceo_sistem()
            print("Uspesno sacuvana cena projekcije")

        elif opcija == "0":
            break

        else:
            print("Nepoznata opcija! Probajte ponovo...")

    sacuvaj_sve()
    print("Sacuvane sve promene nad projekcijom u fajlovima!")

