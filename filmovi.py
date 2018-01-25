import meni
import projekcije
lista_filmova = []


def dodaj_film():
    """
    Metoda za rucno dodavanje filmova
    :return: 
    """
    global lista_filmova
    try:
        film = {}
        film["naziv_filma"] = input("Unesite naziv filma: ").strip()
        film["zanr"] = input("Unesite zanr: ").strip()
        film["trajanje"] = dodaj_trajanje_filma()
        film["reziseri"] = input("Unesite rezisere: ").strip()
        film["uloge"] = input("Unesite uloge: ").strip()
        film["zemlja_porekla"] = input("Unesite zemlju porekla: ").strip()
        film["godina_proizvodnje"] = dodaj_godinu_proizvodnje()

        lista_filmova.append(film)
        sacuvaj_film(film2str(film))

    except:
        print("Greska pri dodavanju filma.")
        return

    print("Film uspesno dodat!")


# pomocne metode za dodavanje filma

def dodaj_trajanje_filma():
    """
    Metoda za unos trajanja filma u minutima.
    Uneta vrednost mora da bude broj
    :return: trajanje u minutima <- string
    """
    while True:
        trajanje = input("Unesite trajanje (u minutima): ").strip()
        try:
            float(trajanje)
        except ValueError:
            print("Trajanje u minutima mora da bude broj!")
            continue
        return trajanje


def dodaj_godinu_proizvodnje():
    """
        Metoda za unos godine proizvodnje filma u minutima.
        Uneta vrednost mora da bude broj
        :return: trajanje u minutima <- string
        """
    while True:
        godina = input("Unesite trajanje (u minutima): ").strip()
        try:
            int(godina)
        except ValueError:
            print("Trajanje u minutima mora da bude broj!")
            continue
        return godina


def sacuvaj_film(film, fajl="podaci/filmovi.txt"):
    try:
        with open(fajl, "a") as f:
            f.write(film)
            f.write("\n")
    except:
        print("Greska pri cuvanju filma u fajl")


def ucitavanje_filmova(fajl="podaci/filmovi.txt"):
    global lista_filmova
    with open(fajl, "r") as f:
        for linija in f:
            lista_filmova.append(str2film(linija))


def print_filmove(lst=lista_filmova):
    print()
    zaglavlje = "{0:<20} {1:<15} {2:<10} {3:<15} {4:<60} {5:<20} {6:<20} ".format("   NAZIV FILMA", "    ZANR",
                                                                                  " TRAJANJE", "   REZISERI",
                                                                                  "                        ULOGE",
                                                                                  "   ZEMLJA POREKLA",
                                                                                  "GODINA PROIZVODINJE")
    zaglavlje_linija = "{0:-<20} {1:-<15} {2:-<10} {3:-<15} {4:-<60} {5:-<20} {6:-<20}".format("-", "-", "-", "-", "-",
                                                                                               "-", "-", "-")
    print(zaglavlje)
    print(zaglavlje_linija)
    for film in lst:
        linija = "{0:<20} {1:<15} {2:<10} {3:<15} {4:<60} {5:<20} {6:<20}".format(film["naziv_filma"], film["zanr"],
                                                                                  film["trajanje"], film["reziseri"],
                                                                                  film["uloge"], film["zemlja_porekla"],
                                                                                  film["godina_proizvodnje"])
        print(linija)
    print()


def pretraga_filmova(kriterijum, pretraga):
    lst = []
    for film in lista_filmova:
        if pretraga in film[kriterijum].lower():
            lst.append(film)
    return lst


def vrati_film(naziv_filma):
    naziv = naziv_filma.lower().strip()
    for f in lista_filmova:
        if f["naziv_filma"].lower() == naziv:
            return f


# metode za konverziju filmova

def str2film(linija):
    delovi = linija.strip().split("|")
    film = {}
    film["naziv_filma"] = delovi[0]
    film["zanr"] = delovi[1]
    film["trajanje"] = delovi[2]
    film["reziseri"] = delovi[3]
    film["uloge"] = delovi[4]
    film["zemlja_porekla"] = delovi[5]
    film["godina_proizvodnje"] = delovi[6]
    return film


def film2str(film):
    return str(
        film["naziv_filma"] + "|" + film["zanr"] + "|" + str(film["trajanje"]) + "|" + film["reziseri"] + "|" +
        film["uloge"] + "|" + film["zemlja_porekla"] + "|" + str(film["godina_proizvodnje"])
    )


# metode za brisanje i izmenu filmova

def obrisi_film(film):
    lista_filmova.remove(film)
    projekcije.obavesti_obrisan_film(film)
    sacuvaj_sve()


def sacuvaj_sve(fajl="podaci/filmovi.txt"):
    with open(fajl, "w") as f:
        for film in lista_filmova:
            f.write(film2str(film))
            f.write("\n")


def izmeni_film(film):
    while True:
        print("Izmeni film po:")
        print("0. Zavrsi i sacuvaj sve promene")
        print("1. Naziv filma")
        print("2. Trajanje")
        print("3. Reziseri")
        print("4. Uloge")
        print("5. Zemlja porekla")
        print("6. Godina proizvodnje")
        print("7. Zanr")

        opcija = input(">>").strip()

        if opcija == "1":
            print("Unesite novi naziv filma")
            unos = input(">>").strip().upper()
            film["naziv_filma"] = unos
            meni.sacuvaj_ceo_sistem()
            print("Uspesno promenjen naziv filma")
        elif opcija == "2":
            print("Unesite novo trajanje filma")
            unos = dodaj_trajanje_filma()
            film["trajanje"] = unos
            print("Uspesno promenjeno trajanje")
        elif opcija == "3":
            print("Unesite nove rezisere filma")
            unos = input(">>").strip()
            film["reziseri"] = unos
            print("Uspesno promenjeni reziseri")
        elif opcija == "4":
            print("Unesite nove uloge filma")
            unos = input(">>").strip()
            film["uloge"] = unos
            print("Uspesno promenjene uloge")
        elif opcija == "5":
            print("Unesite novu zemlju porekla filma")
            unos = input(">>").strip()
            film["zemlja_porekla"] = unos
            print("Uspesno promenjena zemlja porekla")
        elif opcija == "6":
            print("Unesite novu godinu proizvodnje filma")
            unos = dodaj_godinu_proizvodnje()
            film["godina_proizvodnje"] = unos
            print("Uspesno promenjena godina proizvodnje")
        elif opcija == "7":
            print("Unesite novi zanr filma")
            unos = input(">>").strip()
            film["zanr"] = unos
            print("Uspesno promenjen zanr")

        elif opcija == "0":
            break
        else:
            print("Nepoznata akcija! Probajte ponovo...")

    sacuvaj_sve()
    print("Sacuvane sve promene nad filmom u fajlovima!")
