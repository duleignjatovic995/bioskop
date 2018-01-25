import sys

import filmovi
import korisnici
import projekcije
import sale
import termini
import karte


def init():
    korisnici.ucitavanje_korisnika()
    filmovi.ucitavanje_filmova()
    sale.ucitavanje_sala()
    projekcije.ucitavanje_projekcija()
    termini.ucitavanje_termina()
    karte.ucitavanje_karti()


def sacuvaj_ceo_sistem():
    """
    Metodu koristimo u slucaju izmene "primarnog" kljuca
    Na ovaj nacin omogucavamo pravilno funkcionisanje str2 metoda
    """
    # prvo cuvamo objekte koji ne zavise ni od koga
    filmovi.sacuvaj_sve()
    sale.sacuvaj_sve()
    # projekcije zavise od flmova i sala (sadrze film i salu u sebi)
    projekcije.sacuvaj_sve()
    # termini samo od projekcija
    termini.sacuvaj_sve()
    # karte od termina
    karte.sacuvaj_sve()
    korisnici.sacuvaj_sve()


def homepage():
    init()
    while True:
        print("\t BIOSKOP")
        print("\t 0. Izlazak iz aplikacije")
        print("\t 1. Prijavi se kao kupac")
        print("\t 2. Prijavi se kao radnik")
        print("\t 3. Pregled filmova")
        print("\t 4. Pretraga filmova")
        print("\t 5. Pretraga projekcija")

        opcija = input(">>").strip()

        if opcija == "1":
            main_kupac()
        elif opcija == "2":
            main_radnik()
        elif opcija == "3":
            filmovi.print_filmove()
        elif opcija == "4":
            pretraga_filmova()
        elif opcija == "5":
            pretraga_projekcija()
        elif opcija == "0":
            return
        else:
            print("Nepoznata akcija. Probajte ponovo")


def main_kupac():
    while True:
        print("\t 0. Nazad")
        print("\t 1. Registracija")
        print("\t 2. Prijava")

        opcija = input(">>").strip()

        if opcija == "1":
            korisnik = korisnici.registracija_korisnika()
            print("Uspesno ste se registrovali.")
            meni_kupac(korisnik)

        elif opcija == "2":
            korisnik = korisnici.prijava()
            while korisnik is None:
                print("\nPogresno korisnicko ime ili lozinka\n")
                korisnik = korisnici.prijava()
            if korisnik["tip"] != "kupac":
                print("Nemate pristup ovom nalogu")
                continue
            print("Uspesno logovanje")
            meni_kupac(korisnik)

        elif opcija == "0":
            return

        else:
            print("Nepoznata opcija!")


def meni_kupac(korisnik):
    while True:
        print("\t 0. Izlazak iz aplikacije")
        print("\t 1. Pregled dostupnih filmova")
        print("\t 2. Pretraga filmova")
        print("\t 3. Pretraga projekcija")
        print("\t 4. Rezervacija karata")
        print("\t 5. Pregled rezervisanih karata")
        print("\t 6. Ponistavanje rezervacija karata")
        print("\t 7. Odjava sa sistema")

        opcija = input(">>").strip()
        if opcija == "1":
            filmovi.print_filmove()

        elif opcija == "2":
            pretraga_filmova()

        elif opcija == "3":
            pretraga_projekcija()

        elif opcija == "4":
            rezervacija_karata(korisnik)

        elif opcija == "5":
            lst = karte.pretrazi_karte(korisnik)
            karte.print_karte(lst)

        elif opcija == "6":
            while True:
                print("---PONISTAVANJE REZERVACIJA---")
                print("\t 0. Nazad")
                print("\t 1. Ponisti rezervaciju")
                opcija = input(">>").strip()
                if opcija == "1":
                    ponistavanje_rezervacija(korisnik)
                elif opcija == "0":
                    break
                else:
                    print("Nepoznata operacija!")

        elif opcija == "7":
            print("Odjavili ste se sa sistema.")
            return

        elif opcija == "0":
            sys.exit()

        else:
            print("Nepoznata opcija!")


def main_radnik():
    while True:
        print("\t 0. Nazad")
        print("\t 1. Prijava")
        opcija = input(">>").strip()

        if opcija == "1":
            korisnik = korisnici.prijava()
            if korisnik is None:
                print("\nPogresno korisnicko ime ili lozinka\n")
                return
            print("Uspesno logovanje")
            if korisnik["tip"] == "menadzer":
                meni_menadzer()
            else:
                meni_prodavac()

        elif opcija == "0":
            return

        else:
            print("Nepoznata opcija!")


def meni_prodavac():
    while True:
        print("\t 0. Izlazak iz aplikacije")
        print("\t 1. Pregled dostupnih filmova")
        print("\t 2. Pretraga filmova")
        print("\t 3. Pretraga projekcija")
        print("\t 4. Rezervacija karata")
        print("\t 5. Pregled rezervisanih karata")
        print("\t 6. Ponistavanje karata")
        print("\t 7. Pretraga karata")
        print("\t 8. Prodaja karata")
        print("\t 9. Odjava sa sistema")

        opcija = input(">>").strip()

        if opcija == "1":
            filmovi.print_filmove()

        elif opcija == "2":
            pretraga_filmova()

        elif opcija == "3":
            pretraga_projekcija()

        elif opcija == "4":
            rezervacija_karata_prodavac()

        elif opcija == "5":
            lst = karte.pretrazi_karte_po_tipu(tip="rezervisana")
            karte.print_karte(lst)

        elif opcija == "6":
            print("Ponistavanje karata")
            print("\t 0. Nazad")
            print("\t 1. Ponisti kartu")
            opcija = input(">>").strip()
            if opcija == "1":
                ponistavanje_karata_prodavac()
            elif opcija == "0":
                break
            else:
                print("Nepoznata operacija!")

        elif opcija == "7":
            pretraga_karata_prodavac()

        elif opcija == "8":
            prodaja_karata()

        elif opcija == "9":
            print("Odjavili ste se sa sistema.")
            return

        elif opcija == "0":
            sys.exit()

        else:
            print("Nepoznata opcija!")


def meni_menadzer():
    while True:
        print("\t 0. Izlazak iz aplikacije")
        print("\t 1. Pregled dostupnih filmova")
        print("\t 2. Pretraga filmova")
        print("\t 3. Pretraga projekcija")
        print("\t 4. Unos entiteta")
        print("\t 5. Brisanje entiteta")
        print("\t 6. Izmena entiteta")
        print("\t 7. Registracija novih radnika")
        print("\t 8. Izvestavanje")
        print("\t 9. Odjava sa sistema")

        opcija = input(">>").strip()

        if opcija == "1":
            filmovi.print_filmove()

        elif opcija == "2":
            pretraga_filmova()

        elif opcija == "3":
            pretraga_projekcija()

        elif opcija == "4":
            unos_entiteta()

        elif opcija == "5":
            brisanje_entiteta()

        elif opcija == "6":
            izmena_entiteta()

        elif opcija == "7":
            registracija_radnika()

        elif opcija == "8":
            izvestaji()

        elif opcija == "9":
            return

        elif opcija == "0":
            sys.exit()


# funkcionalnosti


def pretraga_filmova():
    while True:
        print("\t Pretraga filmova:")
        print("\t 0. Nazad")
        print("\t 1. Pretraga po nazivu")
        print("\t 2. Pretraga po zanru")
        print("\t 3. Pretraga po trajanju filma")
        print("\t 4. Pretraga po reziserima")
        print("\t 5. Pretraga po glavnim ulogama")
        print("\t 6. Pretraga po zemlji porekla")
        print("\t 7. Pretraga po godini proizvodnje")
        opcija = input(">>").strip()

        if opcija == "1":
            kriterijum = "naziv_filma"
            break

        elif opcija == "2":
            kriterijum = "zanr"
            break

        elif opcija == "3":
            kriterijum = "trajanje"
            break

        elif opcija == "4":
            kriterijum = "reziseri"
            break

        elif opcija == "5":
            kriterijum = "uloge"
            break

        elif opcija == "6":
            kriterijum = "zemlja_porekla"
            break

        elif opcija == "7":
            kriterijum = "godina_proizvodnje"
            break

        elif opcija == "0":
            return

        else:
            print("Nepoznata opcija! Probajte ponovo.")
    rec_pretrage = input("Unesite upit: ").strip().lower()
    filmovi_lst = filmovi.pretraga_filmova(kriterijum, rec_pretrage)
    filmovi.print_filmove(lst=filmovi_lst)


def pretraga_projekcija():
    while True:
        print("\t Pretraga projekcija:")
        print("\t 0. Nazad")
        print("\t 1. Pretraga po filmu")
        print("\t 2. Pretraga po sali")
        print("\t 3. Pretraga po datumu i vremenu pocetka (hh:mm)")
        print("\t 4. Pretraga po datumu i vremenu kraja (hh:mm)")

        opcija = input(">>").strip()

        if opcija == "1":
            upit = input("Unesite upit: ").strip().lower()
            projekcije_lst = projekcije.pretraga_po_filmu(upit)
            projekcije.print_projekcije(projekcije_lst)

        elif opcija == "2":
            upit = input("Unesite upit: ").strip().lower()
            projekcije_lst = projekcije.pretraga_po_sali(upit)
            projekcije.print_projekcije(projekcije_lst)

        elif opcija == "3":
            upit = input("Unesite upit: ").strip().lower()
            projekcije_lst = projekcije.pretraga_po_pocetku(upit)
            projekcije.print_projekcije(projekcije_lst)

        elif opcija == "4":
            upit = input("Unesite upit: ").strip().lower()
            projekcije_lst = projekcije.pretraga_po_kraju(upit)
            projekcije.print_projekcije(projekcije_lst)

        elif opcija == "0":
            return

        else:
            print("Nepoznata opcija! Probajte ponovo.")


def rezervacija_karata(korisnik):
    while True:
        print("\t Rezervacija karata: ")
        print("\t 0. Nazad")
        print("\t 1. Pretrazi projekcije")
        print("\t 2. Unesi sifru termina projekcije")

        opcija = input(">>").strip()

        if opcija == "1":
            projekcije.print_projekcije()
            print("Unesite sifru zeljene projekcije")
            sifra_proj = input(">>").strip()
            lst = termini.pretraga_termina(sifra_proj)
            print("Dostupne projekcije su:\n")
            termini.print_termine(lst)
            print("\nUnesite sifru termina koji hocete da rezervisete:")
            sifra_termina = input(">>").strip()
            termin = termini.vrati_termin(sifra_termina)
            termini.print_sedista(termin)
            print("Unesite slobodan red (1, 2, 3...):")
            red = int(input(">>").strip()) - 1
            print("Unesite slobodnu kolonu (A, B, C...):")
            kolona = ord(input(">>").strip().lower()) - 97  # get acii value of lowercase letter - a
            termini.rezervisi_sediste(korisnik, termin, red, kolona)

        elif opcija == "2":
            print("\nUnesite sifru termina koji hocete da rezervisete:")
            sifra_termina = input(">>").strip()
            termin = termini.vrati_termin(sifra_termina)
            termini.print_sedista(termin)
            print("Unesite slobodan red (1, 2, 3...):")
            red = int(input(">>").strip()) - 1
            print("Unesite slobodnu kolonu (A, B, C...):")
            kolona = ord(input(">>").strip().lower()) - 97  # get acii value of lowercase letter - a
            termini.rezervisi_sediste(korisnik, termin, red, kolona)

        elif opcija == "0":
            return
        else:
            print("Nepoznata opcija! Probajte ponovo...")


def rezervacija_karata_prodavac():
    while True:
        print("\t Rezervacija karata: ")
        print("\t 0. Nazad")
        print("\t 1. Rezervisi")

        opcija = input(">>").strip()

        if opcija == "0":
            return
        if opcija == "1":
            termini.print_termine()
            print("\nUnesite sifru termina koji hocete da rezervisete:")
            sifra_termina = input(">>").strip()
            termin = termini.vrati_termin(sifra_termina)
            if termin is None:
                print("Nema termina sa sifrom koju ste uneli")
                continue

            korisnici.print_korisnike(korisnici.vrati_kupce())
            print("Unesite korisnicko ime kupca:")
            username = input(">>").strip().lower()
            korisnik = korisnici.vrati_korisnika(username)
            if korisnik is None:
                print("Korisnik koga ste uneli ne postoji u bazi")
                continue

            termini.print_sedista(termin)
            print("Unesite slobodan red (1, 2, 3...):")
            red = int(input(">>").strip()) - 1
            print("Unesite slobodnu kolonu (A, B, C...):")
            kolona = ord(input(">>").strip().lower()) - 97  # get acii value of lowercase letter - a
            termini.rezervisi_sediste(korisnik, termin, red, kolona)


def ponistavanje_rezervacija(korisnik):
    print("\t Rezervacije: ")
    lst = karte.pretrazi_karte(korisnik)
    karte.print_karte(lst)
    print("Unesite naziv filma od rezervacije koju hocete da otkazete.")
    naziv_filma = input(">>").strip().lower()
    film_filter = []
    for karta in lst:
        if naziv_filma == karta["termin"]["projekcija"]["film"]["naziv_filma"].lower():
            film_filter.append(karta)
    karte.print_karte(film_filter)
    if len(film_filter) == 0:
        print("Nije pronadjena nijedna rezervacija pomenutog filma.")
        return
    print("Unesite sediste koje zelite da otkazete:")
    sediste = input(">>").strip().lower()
    rezervacija = None
    for karta in film_filter:
        if karta["oznaka"].lower() == sediste:
            rezervacija = karta

    if rezervacija is None:
        print("Nije pronadjena nijedna rezervacija sa tim sedistem")
        return

    karte.obrisi_kartu(rezervacija)


def ponistavanje_karata_prodavac():
    print("Unesite korisnicko ime kupca:")
    username = input(">>").strip().lower()
    korisnik = korisnici.vrati_korisnika(username)
    if korisnik is None:
        print("Korisnik koga ste uneli ne postoji u bazi")
        return
    lst = karte.pretrazi_karte_svi_tipovi(korisnik)
    karte.print_karte(lst)
    print("Unesite naziv filma od rezervacije koju hocete da otkazete.")
    naziv_filma = input(">>").strip().lower()
    film_filter = []
    for karta in lst:
        if naziv_filma == karta["termin"]["projekcija"]["film"]["naziv_filma"].lower():
            film_filter.append(karta)
    karte.print_karte(film_filter)
    if len(film_filter) == 0:
        print("Nije pronadjena nijedna rezervacija pomenutog filma.")
        return
    print("Unesite sediste koje zelite da otkazete:")
    sediste = input(">>").strip().lower()
    rezervacija = None
    for karta in film_filter:
        if karta["oznaka"].lower() == sediste:
            rezervacija = karta

    if rezervacija is None:
        print("Nije pronadjena nijedna rezervacija sa tim sedistem")
        return

    karte.obrisi_kartu(rezervacija)


def pretraga_karata_prodavac():
    while True:
        print("\t Pretraga karata:")
        print("\t 0. Nazad")
        print("\t 1. Pretraga po sifri projekcije")
        print("\t 2. Pretraga po imenu kupca")
        print("\t 3. Pretraga po prezimenu kupca")
        print("\t 4. Pretraga po korisnickom imenu kupca")
        print("\t 5. Pretraga po vremenu pocetka")
        print("\t 6. Pretraga po vremenu kraja")
        print("\t 7. Pretraga po datumu")
        print("\t 8. Pretraga po tipu karte (rezervsisana, kupljena)")

        opcija = input(">>").strip()

        if opcija == "1":
            projekcije.print_projekcije()
            print("Unesite sifru projekcije: ")
            upit = input(">>").strip().lower()
            lst = karte.pretrazi_sifra_projekcije(upit)
            karte.print_karte(lst)

        elif opcija == "2":
            kriterijum = "ime"
            print("Unesite ime korisnika: ")
            upit = input(">>").strip().lower()
            lst = karte.pretrazi_karte_po_korisniku(kriterijum, upit)
            karte.print_karte(lst)

        elif opcija == "3":
            kriterijum = "prezime"
            print("Unesite prezime korisnika: ")
            upit = input(">>").strip().lower()
            lst = karte.pretrazi_karte_po_korisniku(kriterijum, upit)
            karte.print_karte(lst)

        elif opcija == "4":
            kriterijum = "korisnicko_ime"
            print("Unesite korisnicko ime korisnika: ")
            upit = input(">>").strip().lower()
            lst = karte.pretrazi_karte_po_korisniku(kriterijum, upit)
            karte.print_karte(lst)

        elif opcija == "5":
            print("Unesite vreme pocetka projekcije (hh:mm) ")
            upit = input(">>").strip().lower()
            lst = karte.pretrazi_vreme_projekcije(upit, tip="pocetak")
            karte.print_karte(lst)

        elif opcija == "6":
            print("Unesite vreme kraja projekcije (hh:mm) ")
            upit = input(">>").strip().lower()
            lst = karte.pretrazi_vreme_projekcije(upit, tip="kraj")
            karte.print_karte(lst)

        elif opcija == "7":
            print("Unesite datum za pretragu (dd-mm-yyyy)")
            datum = input(">>").strip()
            lst = karte.pretrazi_karte_datum(datum)
            karte.print_karte(lst)

        elif opcija == "8":
            while True:
                print("Unesite tip karte: ")
                print("1. Rezervisane")
                print("2. Kupljene")

                opcija = input(">>").strip().lower()

                if opcija == "1":
                    lst = karte.pretrazi_karte_po_tipu("rezervisana")

                elif opcija == "2":
                    lst = karte.pretrazi_karte_po_tipu("kupljena")

                else:
                    print("Nepoznata opcija! Probajte ponovo")
                    continue

                karte.print_karte(lst)
                break

        elif opcija == "0":
            return

        else:
            print("Nepoznat unos, probajte ponovo.")


def prodaja_karata():
    while True:
        print("Prodaja karata:")
        print("0. Nazad")
        print("1. Direktna prodaja")
        print("2. Prodaja rezervisanih karata")

        opcija = input(">>").strip()

        if opcija == "1":
            prodaja_direktna()

        elif opcija == "2":
            prodaja_rezervisanih()

        elif opcija == "0":
            return

        else:
            print("Nepoznata opcija. Probajte ponovo")


def prodaja_rezervisanih():
    print("Prodaja rezervisanih karata:")
    rezervisane_karte = karte.pretrazi_karte_po_tipu(tip="rezervisana")
    karte.print_karte(rezervisane_karte)

    print("Unesite korisnicko ime:")
    username = input(">>").strip().lower()

    korisnik = korisnici.vrati_korisnika(username)
    if korisnik is None:
        print("Ne postoji korisnik sa datim korisnickim imenom")
        return

    karte_korisnik = karte.pretrazi_karte(korisnik, tip="rezervisana")
    if len(karte_korisnik) == 0:
        print("Nema odgovarajucih karata za ovog korisnika")
        return
    karte.print_karte(karte_korisnik)

    print("Unesite sifru termina:")
    sifra_termina = input(">>").strip()
    termin = termini.vrati_termin(sifra_termina)
    if termin is None:
        print("Ne postoji termin sa datom sifrom")
        return
    karte_termin = karte.pretrazi_karte_sifra_termina(sifra_termina, lista=karte_korisnik)
    if len(karte_termin) == 0:
        print("Ne postoji karta za odgovarajuci termin i korisnika")
        return
    karte.print_karte(karte_termin)

    print("Unesite sediste za prodaju:")
    sediste = input(">>").strip().lower()
    karte_sediste = karte.pretrazi_karte_po_sedistu(sediste, lista=karte_termin)
    if len(karte_sediste) == 0:
        print("Nema karata za ovo sediste")
        return

    karte.print_karte(karte_sediste)

    print("Da li sigurno prodajete ovu kartu?")
    print("1. Da")
    print("2. Ne")

    opcija = input(">>").strip()

    if opcija == "1":
        konacna = karte_sediste[0]
        termini.prodaj_rezervisano_sediste(konacna)
        print("Karta uspesno prodata")
    elif opcija == "2":
        return
    else:
        print("Nepoznata opcija")


def prodaja_direktna():
    while True:
        print("Direktna prodaja karata:")
        print("0. Nazad")
        print("1. Pretrazi projekcije")
        print("2. Direktan unos termina")

        opcija = input(">>").strip()

        if opcija == "1":
            pretraga_projekcija()
            print("Unesite sifru zeljene projekcije")
            sifra_proj = input(">>").strip()
            lst = termini.pretraga_termina(sifra_proj)
            print("Dostupne projekcije su:\n")
            termini.print_termine(lst)

            print("Unesite sifru termina:")
            sifra_termina = input(">>").strip()
            termin = termini.vrati_termin(sifra_termina)
            if termin is None:
                print("Ne postoji termin sa datom sifrom")
                continue

            print("Unesite korisnicko ime:")
            username = input(">>").strip().lower()
            if username is None:
                print("Ne postoji korisnik sa datim korisnickim imenom")
                continue

            korisnik = korisnici.vrati_korisnika(username)

            termini.print_sedista(termin)
            print("Unesite slobodan red (1, 2, 3...):")
            red = int(input(">>").strip()) - 1
            print("Unesite slobodnu kolonu (A, B, C...):")
            kolona = ord(input(">>").strip().lower()) - 97  # get acii value of lowercase letter - a
            termini.prodaj_sediste(korisnik, termin, red, kolona)

        elif opcija == "2":
            termini.print_termine()
            print("Unesite sifru termina:")
            sifra_termina = input(">>").strip()
            termin = termini.vrati_termin(sifra_termina)
            if termin is None:
                print("Ne postoji termin sa datom sifrom")
                continue

            print("Unesite korisnicko ime:")
            username = input(">>").strip().lower()
            if username is None:
                print("Ne postoji korisnik sa datim korisnickim imenom")
                continue

            korisnik = korisnici.vrati_korisnika(username)

            termini.print_sedista(termin)
            print("Unesite slobodan red (1, 2, 3...):")
            red = int(input(">>").strip()) - 1
            print("Unesite slobodnu kolonu (A, B, C...):")
            kolona = ord(input(">>").strip().lower()) - 97  # get acii value of lowercase letter - a
            termini.prodaj_sediste(korisnik, termin, red, kolona)

        elif opcija == "0":
            return

        else:
            print("Nepoznata opcija. Probajte ponovo")


def unos_entiteta():
    while True:
        print("Unos entiteta: ")
        print("0. Nazad")
        print("1. Unesi film")
        print("2. Unesi salu")
        print("3. Unesi projekciju")
        print("4. Unesi termin projekcije")

        opcija = input(">>").strip()

        if opcija == "1":
            filmovi.dodaj_film()
        elif opcija == "2":
            sale.dodaj_salu()
        elif opcija == "3":
            projekcije.dodaj_projekciju()
        elif opcija == "4":
            projekcije.print_projekcije()
            print("Unesite sifru projekcije za koju kreirate termin")
            sifra_proj = input(">>").strip()
            projekcija = projekcije.vrati_projekciju(sifra_proj)
            termini.dodaj_termin(projekcija)
        elif opcija == "0":
            return
        else:
            print("Nepoznata akcija! Probajte ponovo...")


def brisanje_entiteta():
    while True:
        print("Brisanje entiteta: ")
        print("0. Nazad")
        print("1. Obrisi film")
        print("2. Obrisi salu")
        print("3. Obrisi projekciju")
        print("4. Obrisi termin projekcije")

        opcija = input(">>").strip()

        if opcija == "1":
            filmovi.print_filmove()
            print("Unesite naziv filma koji hocete da obrisete:")
            naziv = input(">>").strip()
            film = filmovi.vrati_film(naziv)
            if film is None:
                print("Ne postoji film sa tim nazivom!")
                continue
            print("Da li ste sigurni da zelite da obrisete film?")
            print("Brisanjem filma brisete projekcije, termine projekcija i karte vezane za dati film!")
            print("1. Da")
            print("2. Ne")

            dane = input(">>").strip()
            if dane == "1":
                filmovi.obrisi_film(film)
            else:
                continue

        elif opcija == "2":
            sale.print_sale()
            print("Unesite sifru sale koju hocete da obrisete")
            sifra_sale = input(">>").strip()
            sala = sale.vrati_salu(sifra_sale)
            if sala is None:
                print("Ne postoji sala sa tom sifrom")
                continue
            print("Da li ste sigurni da zelite da obrisete salu?")
            print("Brisanjem sale brisete projekcije, termine projekcija i karte vezane za datu salu!")
            print("1. Da")
            print("2. Ne")

            dane = input(">>").strip()
            if dane == "1":
                sale.obrisi_salu(sala)
            else:
                continue

        elif opcija == "3":
            projekcije.print_projekcije()
            print("Unesite sifru projekcije:")
            sifra_projekcije = input(">>").strip()
            projekcija = projekcije.vrati_projekciju(sifra_projekcije)
            if projekcija is None:
                print("Ne postoji projekcija sa datom sifrom.")
                continue
            print("Da li ste sigurni da zelite da obrisete projekciju?")
            print("Brisanjem projekcije brisete termine projekcija i karte vezane za datu projekciju!")
            print("1. Da")
            print("2. Ne")

            dane = input(">>").strip()
            if dane == "1":
                projekcije.obrisi_projekciju(projekcija)
            else:
                continue

        elif opcija == "4":
            termini.print_termine()
            print("Unesite sifru termina:")
            sifra_termina = input(">>").strip()
            termin = termini.vrati_termin(sifra_termina)
            if termin is None:
                print("Ne postoji termin sa datom sifrom.")
                continue
            print("Da li ste sigurni da zelite da obrisete projekciju?")
            print("Brisanjem projekcije brisete termine projekcija i karte vezane za datu projekciju!")
            print("1. Da")
            print("2. Ne")

            dane = input(">>").strip()
            if dane == "1":
                termini.obrisi_termin(termin)
            else:
                continue

        elif opcija == "0":
            return

        else:
            print("Nepoznata akcija! Probajte ponovo...")


def izmena_entiteta():
    while True:
        print("Izmena entiteta: ")
        print("0. Nazad")
        print("1. Izmeni film")
        print("2. Izmeni salu")
        print("3. Izmeni projekciju")
        print("4. Izmeni termin projekcije")

        opcija = input(">>").strip()

        if opcija == "1":
            filmovi.print_filmove()
            print("Unesite naziv filma koji hocete da izmenite:")
            naziv = input(">>").strip()
            film = filmovi.vrati_film(naziv)
            if film is None:
                print("Ne postoji film sa tim nazivom!")
                continue
            filmovi.izmeni_film(film)

        elif opcija == "2":
            sale.print_sale()
            print("Unesite sifru sale koju hocete da izmenite")
            sifra_sale = input(">>").strip()
            sala = sale.vrati_salu(sifra_sale)
            if sala is None:
                print("Ne postoji sala sa tom sifrom")
                continue
            sale.izmeni_salu(sala)

        elif opcija == "3":
            projekcije.print_projekcije()
            print("Unesite sifru projekcije:")
            sifra_projekcije = input(">>").strip()
            projekcija = projekcije.vrati_projekciju(sifra_projekcije)
            if projekcija is None:
                print("Ne postoji projekcija sa datom sifrom.")
                continue
            projekcije.izmeni_projekciju(projekcija)

        elif opcija == "4":
            termini.print_termine()
            print("Unesite sifru termina:")
            sifra_termina = input(">>").strip()
            termin = termini.vrati_termin(sifra_termina)
            if termin is None:
                print("Ne postoji termin sa datom sifrom.")
                continue
            termini.izmeni_termin(termin)

        elif opcija == "0":
            return
        else:
            print("Nepoznata akcija! Probajte ponovo...")


def registracija_radnika():
    korisnici.registracija_radnika()


def izvestaji():
    pass


if __name__ == "__main__":
    # homepage()
    init()
    # main_kupac()
    # main_radnik()

