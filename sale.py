import re
import meni

lista_sale = []


def dodaj_salu():
    """
    Metoda za rucno dodavanje sale.
    :return: 
    """
    try:
        sala = {}
        sala["sifra"] = unos_sifre()  # troslovna oznaka, npr AAA
        sala["naziv"] = input("Unesite naziv sale:\n>>").strip()  # nije obavezan
        sala["redovi"] = unos_redova()  # lista [1, 2, 3, ...]
        sala["sedista"] = unos_sedista()  # lista[A, B, C, ...]

        lista_sale.append(sala)
        sacuvaj_salu(sala2str(sala))
    except:
        print("Greska pri dodavanju sale!")
        return

    print("Sala uspesno dodata!")


# pomocne metode za rucno dodavanje sale

def sacuvaj_salu(sala):
    with open("podaci/sale.txt", "a") as f:
        f.write(sala)
        f.write("\n")



def unos_sifre():
    while True:
        print("Unesite sifru sale: ")
        sifra = input(">>").strip()
        if provera_sifre1(sifra) and provera_sifre2(sifra) and provera_sifre3(sifra):
            return sifra.upper()
        else:
            continue


def provera_sifre1(sifra):
    for s in lista_sale:
        if s["sifra"] == sifra:
            print("Sala sa tom sifrom vec postoji")
            return False
    return True


def provera_sifre2(sifra):
    pattern = re.compile("[A-Za-z]{3}")
    if not bool(pattern.match(sifra)):
        print("Sifra mora da bude troslovna oznaka.")
        return False
    return True


def provera_sifre3(sifra):
    if len(sifra) > 3:
        print("Sifra je predukacka, sifra sale mora tacno 3 karaktera da ima")
        return False
    elif len(sifra) < 3:
        print("Sifra je prekratka, sifra sale mora tacno 3 karaktera da ima")
        return False
    return True


def unos_redova():
    redovi = []
    print("Unesite ukupan broj redova: ")
    while True:
        broj = input(">>").strip()
        if not bool(re.match(r"[\d]+", broj)):
            print("Morate uneti broj")
            continue
        else:
            break
    br_redova = int(broj)
    for i in range(br_redova):
        redovi.append(i+1)
    return redovi


def unos_sedista():
    sedista = []
    print("Unesite broj sedista u redu")
    while True:
        broj = input(">>").strip()
        if not bool(re.match(r"[\d]+", broj)):
            print("Morate uneti broj")
            continue
        else:
            break
    br_sedista = int(broj)
    if br_sedista > 25:
        br_sedista = 25
    for i in range(br_sedista):
        sedista.append(chr(65 + i))
    return sedista


def vrati_salu_provera(sifra):
    if provera_sifre1(sifra) and provera_sifre2(sifra) and provera_sifre3(sifra):
        for s in lista_sale:
            if s["sifra"] == sifra:
                return s
    return None


def vrati_salu(sifra):
    # if provera_sifre2(sifra) and provera_sifre3(sifra):
    for s in lista_sale:
        if s["sifra"].lower() == sifra.lower():
            return s


def ucitavanje_sala(fajl="podaci/sale.txt"):
    global lista_sale
    with open(fajl, "r") as f:
        for linija in f:
            lista_sale.append(str2sala(linija))


def prikazi_salu(sala):
    redovi = sala["redovi"]
    sedista = sala["sedista"]

    for r in redovi:
        print(str(r) + "." + ' '.join(sedista))


# metode za konverziju sala

def str2sala(linija):
    sifra, naziv, redovi, sedista = linija.strip().split("|")
    sala = {}
    sala["sifra"] = sifra
    sala["naziv"] = naziv

    lst_redovi = []
    for i in range(int(redovi)):
        lst_redovi.append(i + 1)

    lst_sedista = []
    for i in range(int(sedista)):
        lst_sedista.append(chr(65 + i))

    sala["redovi"] = lst_redovi
    sala["sedista"] = lst_sedista
    return sala


def sala2str(sala):
    sifra = sala["sifra"].upper()
    naziv = sala["naziv"]
    br_redova = len(sala["redovi"])
    br_sedista = len(sala["sedista"])
    return sifra + "|" + naziv + "|" + str(br_redova) + "|" + str(br_sedista)


def print_sale(lst=lista_sale):
    print()
    zaglavlje = "{0:<20} {1:<20} {2:<20} {3:<20}".format(
        "SIFRA SALE",
        "NAZIV SALE",
        "BROJ REDOVA",
        "KOLONE"
    )
    zaglavlje_linija = "{0:-<20} {1:-<20} {2:-<20} {3:-<20}".format("-", "-", "-", "-")
    print(zaglavlje)
    print(zaglavlje_linija)

    for sala in lst:
        linija = "{0:<20} {1:<20} {2:<20} {3:<20}".format(
            sala["sifra"],
            sala["naziv"],
            str(len(sala["redovi"])),
            str(sala["sedista"])
        )
        print(linija)
    print()


# brisanje i izmena projekcije

def obrisi_salu(sifra):
    sala = vrati_salu_provera(sifra)
    lista_sale.remove(sala)
    sacuvaj_sve()
    meni.init()


def sacuvaj_sve(fajl="podaci/sale.txt"):
    with open(fajl, "w") as f:
        for sala in lista_sale:
            f.write(sala2str(sala))
            f.write("\n")


def izmeni_salu(sala):
    while True:
        print("Izmeni salu po:")
        print("0. Nazad")
        print("1. Sifra sale")
        print("2. Naziv sale")

        opcija = input(">>").strip()

        if opcija == "1":
            print("Unesite novu sifru sale")
            unos = unos_sifre()
            sala["sifra"] = unos
            meni.sacuvaj_ceo_sistem()
            print("Uspesno izmenjena sifra sale")
        elif opcija == "2":
            print("Unesite naziv sale")
            unos = input(">>").strip()
            sala["naziv"] = unos
            print("Uspesno izmenjen naziv sale")
        elif opcija == "0":
            break
        else:
            print("Nepoznata akcija! Probajte ponovo...")

    sacuvaj_sve()
    print("Sacuvane sve promene nad filmom u fajlovima!")


# todo makni
# def refresh_sale():
#     global lista_sale
#     lista_sale = []
#     ucitavanje_sala()
