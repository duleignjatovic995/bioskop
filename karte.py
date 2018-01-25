from datetime import datetime
import termini
import collections

lista_karata = []


def dodaj_kartu(korisnik, termin, red, kolona, tip="rezervisana", prodavac="---"):
    sedista = termin["sedista"]
    oznaka_sediste = str(red+1) + str(chr(kolona+97))
    sedista[red][kolona] = "x"
    karta = {}
    karta["ime"] = korisnik["ime"]
    karta["prezime"] = korisnik["prezime"]
    karta["korisnicko_ime"] = korisnik["korisnicko_ime"]
    karta["termin"] = termin
    karta["oznaka"] = oznaka_sediste
    if tip == "kupljena":
        karta["datum_prodaje"] = datetime.now()
        karta["prodavac"] = prodavac
    elif tip == "rezervisana":
        karta["datum_prodaje"] = datetime.max
        karta["prodavac"] = "---"
    karta["tip"] = tip

    sacuvaj_kartu(karta)
    lista_karata.append(karta)


def ucitavanje_karti(fajl="podaci/karte.txt"):
    global lista_karata
    with open(fajl, "r") as f:
        for linija in f:
            karta = str2karta(linija)
            if karta is None:
                continue
            lista_karata.append(karta)


def sacuvaj_kartu(karta, fajl="podaci/karte.txt"):
    with open(fajl, "a") as f:
        f.write(karta2str(karta))
        f.write("\n")


def karta2str(karta):
    ime = karta["ime"]
    prezime = karta["prezime"]
    korisnicko_ime = karta["korisnicko_ime"]
    termin = str(karta["termin"]["sifra"])
    oznaka = karta["oznaka"]
    datum = str(datetime.strftime(karta["datum_prodaje"], "%d-%m-%Y"))
    tip = karta["tip"]
    prodavac = karta["prodavac"]
    return str(ime + "|" + prezime + "|" + korisnicko_ime + "|" + termin + "|" + oznaka + "|" + datum + "|" + tip + "|" + prodavac)


def str2karta(linija):
    try:
        ime, prezime, korisnicko_ime, termin_s, oznaka, datum, tip, prodavac = linija.strip().split("|")
    except:
        print("Greska pri citanju iz baze, karta nije ucitana")
        return
    termin = termini.vrati_termin(termin_s)
    if termin is None:
        return
    karta = {}
    karta["ime"] = ime
    karta["prezime"] = prezime
    karta["korisnicko_ime"] = korisnicko_ime
    karta["termin"] = termin
    karta["oznaka"] = oznaka
    karta["datum_prodaje"] = datetime.strptime(datum, "%d-%m-%Y")
    karta["tip"] = tip
    karta["prodavac"] = prodavac
    return karta


# metode za pretragu karata

def pretrazi_karte(korisnik, tip="rezervisana"):
    lst = []
    for karta in lista_karata:
        if karta["korisnicko_ime"] == korisnik["korisnicko_ime"] and karta["tip"] == tip:
            lst.append(karta)
    return lst


def pretrazi_karte_svi_tipovi(korisnik):
    lst = []
    for karta in lista_karata:
        if karta["korisnicko_ime"] == korisnik["korisnicko_ime"]:
            lst.append(karta)
    return lst


def pretrazi_karte_po_korisniku(kriterijum, upit):
    lst = []
    for karta in lista_karata:
        if karta[kriterijum].lower() == upit:
            lst.append(karta)
    return lst


def pretrazi_karte_po_tipu(tip="rezervisana"):
    lst = []
    for karta in lista_karata:
        if karta["tip"] == tip:
            lst.append(karta)
    return lst


def pretrazi_karte_datum_termina(datum, lista=lista_karata):
    lst = []
    for karta in lista:
        if karta["termin"]["datum"] == datum:
            lst.append(karta)
    return lst


def pretrazi_vreme_projekcije(str_vreme, tip="pocetak"):
    lst = []
    try:
        vreme = datetime.strptime(str_vreme, "%H:%M")
    except:
        print("Lose unet datum")
        return lst

    for karta in lista_karata:
        if karta["termin"]["projekcija"][tip] == vreme:
            lst.append(karta)
    return lst


def pretrazi_sifra_projekcije(sifra_projekcije):
    lst = []
    for karta in lista_karata:
        if karta["termin"]["projekcija"]["sifra"].lower() == sifra_projekcije:
            lst.append(karta)
    return lst


def pretrazi_karte_po_sedistu(sediste, lista=lista_karata):
    lst = []
    for karta in lista:
        if karta["oznaka"].lower() == sediste:
            lst.append(karta)
    return lst


def pretrazi_karte_sifra_termina(sifra, lista=lista_karata):
    lst = []
    for karta in lista:
        if sifra.lower() == karta["termin"]["sifra"].lower():
            lst.append(karta)
    return lst


def pretrazi_karte_datum_prodaje(datum):
    lst = []
    for karta in lista_karata:
        if karta["datum_prodaje"] == datum and karta["tip"] == "kupljena":
            lst.append(karta)
    return lst


def pretrazi_karte_datum_prodaje_prodavac(datum, prodavac):
    lst = []
    for karta in lista_karata:
        if karta["datum_prodaje"] == datum and karta["tip"] == "kupljena" and karta["prodavac"] == prodavac:
            lst.append(karta)
    return lst


def pretrazi_prodate_karte_po_filmu(naziv_filma):
    lst = []
    naziv = naziv_filma.lower()
    for karta in lista_karata:
        if naziv == karta["termin"]["projekcija"]["film"]["naziv_filma"].lower() and karta["tip"] == "kupljena":
            lst.append(karta)
    return lst


def print_karte(lst=lista_karata):
    print()
    zaglavlje = "{0:<20} {1:<20} {2:<20} {3:<20} {4:<20} {5:<20} {6:<20} {7:<20} {8:<20} {9:<20}".format(
        "SIFRA TERMINA", "IME",
        "PREZIME", "KORISNICKO IME",
        "NAZIV FILMA",
        "POCETAK", "KRAJ", "SEDISTE",
        "TIP", "DATUM PRODAJE")
    zaglavlje_linija = "{0:-<20} {1:-<20} {2:-<20} {3:-<20} {4:-<20} {5:-<20} {6:-<20} {7:-<20} {8:-<20} {9:-<20}".format(
        "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-")

    print(zaglavlje)
    print(zaglavlje_linija)
    for karta in lst:

        if datetime.strftime(karta["datum_prodaje"], "%d-%m-%Y") == datetime.max.strftime("%d-%m-%Y"):
            datum_prodaje = "Nije prodata"
        else:
            datum_prodaje = datetime.strftime(karta["datum_prodaje"], "%d-%m-%Y")
        linija = "{0:<20} {1:<20} {2:<20} {3:<20} {4:<20} {5:<20} {6:<20} {7:<20} {8:<20} {9:<20}".format(
            karta["termin"]["sifra"],
            karta["ime"],
            karta["prezime"],
            karta["korisnicko_ime"],
            karta["termin"]["projekcija"]["film"]["naziv_filma"],
            datetime.strftime(karta["termin"]["projekcija"]["pocetak"], "%H:%M"),
            datetime.strftime(karta["termin"]["projekcija"]["kraj"], "%H:%M"),
            karta["oznaka"],
            karta["tip"],
            datum_prodaje

        )
        print(linija)
    print()


def obrisi_kartu(karta):
    global lista_karata
    if karta in lista_karata:
        termini.oslobodi_sediste(karta)
        lista_karata.remove(karta)
        print("Karta je uspesno obrisana")
        sacuvaj_sve()
    else:
        print("Neuspesno brisanje")


def sacuvaj_sve(fajl="podaci/karte.txt"):
    """
    U slucaju izmene overridujemo ceo fajl
    """
    with open(fajl, "w") as f:
        for karta in lista_karata:
            f.write(karta2str(karta))
            f.write("\n")


def obavesti_obrisan_termin(termin):
    for karta in lista_karata:
        if termin is karta["termin"]:
            lista_karata.remove(karta)
    sacuvaj_sve()

# todo makni
# def refresh_karte():
#     global lista_karata
#     lista_karata = []
#     ucitavanje_karti()


def sum_cena(lst=lista_karata):
    ukupna_cena = 0
    for karta in lst:
        ukupna_cena += float(karta["termin"]["cena"])
    return ukupna_cena


def cena_po_prodavcu(lst=lista_karata):
    prodavci = collections.defaultdict(list)
    for karta in lst:
        if karta["tip"] == "kupljena":
            if karta["prodavac"] in prodavci.keys():
                prodavci[karta["prodavac"]][0] += float(karta["termin"]["cena"])
                prodavci[karta["prodavac"]][1] += 1
            else:
                prodavci[karta["prodavac"]] = [0, 0]
                prodavci[karta["prodavac"]][0] += float(karta["termin"]["cena"])
                prodavci[karta["prodavac"]][1] += 1
    return prodavci


def tabela_broj_cena(broj, cena):
    print()
    print("{0:<20} {1:<20}".format("BROJ", "UKUPNA CENA"))
    print("{0:-<20} {1:-<20}".format("-", "-"))
    print("{0:<20} {1:<20}".format(str(broj), str(cena)))


def tabela_cena(cena):
    print()
    print("{0:<20}".format("UKUPNA CENA"))
    print("{0:-<20}".format("-"))
    print("{0:<20}".format(str(cena)))


def tabela_prodavci(prodavci):
    print()
    print("{0:<20} {1:<20} {1:<20}".format("PRODAVAC", "UKUPNA CENA", "BROJ"))
    print("{0:-<20} {1:-<20} {1:-<20}".format("-", "-", "-"))
    for prodavac, lista in prodavci.items():
        # lista[0] - ukupna cena
        # lista[1] - ukupan broj
        print("{0:<20} {1:<20} {1:<20}".format(prodavac, lista[0], lista[1]))