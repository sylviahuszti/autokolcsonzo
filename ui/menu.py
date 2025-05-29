from models.felhasznalo import Felhasznalo
from services.kolcsonzo_service import KolcsonzoService
from services.logger_service import LoggerService
from storage.file_handler import FileHandler
from models.auto import Szemelyauto, Teherauto
from datetime import date, datetime, timedelta

def menu():
    logger = LoggerService()
    fajlkezelo = FileHandler()
    kolcsonzo = KolcsonzoService("Profi Autókölcsönző")

    autok = fajlkezelo.betoltes_autok()
    if not autok:
        szemely_tipusok = [
            ("Suzuki", "Swift", 9500, 5),
            ("Ford", "Focus", 10000, 5),
            ("Mazda", "3", 11000, 5),
            ("Toyota", "Corolla", 10500, 5),
            ("BMW", "1-es", 13000, 5),
            ("Audi", "A3", 12500, 5),
            ("Opel", "Astra", 9800, 5),
            ("Kia", "Ceed", 10200, 5),
            ("Hyundai", "i30", 10100, 5),
            ("Volkswagen", "Golf", 10900, 5),
            ("Renault", "Megane", 9700, 5),
            ("Peugeot", "308", 9600, 5),
            ("Skoda", "Octavia", 9900, 5),
            ("Honda", "Civic", 10800, 5),
            ("Seat", "Leon", 9800, 5),
        ]

        teher_tipusok = [
            ("Ford", "Transit", 16000, 1200),
            ("Mercedes", "Sprinter", 17500, 1400),
            ("Volkswagen", "Crafter", 17000, 1350),
            ("Renault", "Master", 16200, 1100),
            ("Peugeot", "Boxer", 15800, 1150),
            ("Citroen", "Jumper", 15900, 1120),
            ("Iveco", "Daily", 18000, 1500),
            ("Fiat", "Ducato", 16100, 1180),
            ("Opel", "Movano", 16300, 1200),
            ("Nissan", "NV400", 16700, 1250),
            ("Hyundai", "H350", 16900, 1300),
            ("Toyota", "ProAce", 16500, 1270),
            ("MAN", "TGE", 17200, 1450),
            ("Isuzu", "N-Serie", 19000, 2000),
            ("Mitsubishi", "Fuso", 18500, 1800),
        ]

        for i, (marka, tipus, dij, ulohelyek) in enumerate(szemely_tipusok):
            auto = Szemelyauto(
                rendszam=f"SZM-{i+1:03}",
                marka=f"{marka} {tipus}",
                napi_dij=dij,
                ulohelyek=ulohelyek
            )
            kolcsonzo.auto_hozzaadas(auto)

        for i, (marka, tipus, dij, teherbiras) in enumerate(teher_tipusok):
            auto = Teherauto(
                rendszam=f"TEH-{i+1:03}",
                marka=f"{marka} {tipus}",
                napi_dij=dij,
                teherbiras=teherbiras
            )
            kolcsonzo.auto_hozzaadas(auto)

        fajlkezelo.mentes_autok(kolcsonzo.autok)
    else:
        for auto in autok:
            kolcsonzo.auto_hozzaadas(auto)

    felhasznalok = fajlkezelo.betoltes_felhasznalok()
    if not felhasznalok:
        felhasznalok = Felhasznalo.tesztfelhasznalok()
        datum = date.today().isoformat()
        for i in range(3):
            auto = kolcsonzo.autok[i]
            berles = kolcsonzo.uj_berles(auto.id, datum, datum)
            felhasznalok[i].hozzaad_berles(berles)
        fajlkezelo.mentes_felhasznalok(felhasznalok)
        fajlkezelo.mentes_berlesek(kolcsonzo.berlesek)

    aktiv_felhasznalo = None

    print("\n==== AUTÓKÖLCSÖNZŐ RENDSZER ====")
    while True:
        if not aktiv_felhasznalo:
            print("\n1. Bejelentkezés")
            print("2. Regisztráció")
            print("3. Kilépés")
            valasztas = input("Választás: ")

            if valasztas == "1":
                email = input("Email: ")
                jelszo = input("Jelszó: ")
                for f in felhasznalok:
                    if f.email == email and f.ellenoriz_jelszo(jelszo):
                        aktiv_felhasznalo = f
                        print(f"Sikeres bejelentkezés: {f.nev}")
                        break
                else:
                    print("Hibás email vagy jelszó.")

            elif valasztas == "2":
                nev = input("Név: ")
                email = input("Email: ")
                jelszo = input("Jelszó: ")
                uj = Felhasznalo(nev, email, jelszo)
                felhasznalok.append(uj)
                fajlkezelo.mentes_felhasznalok(felhasznalok)
                print("Sikeres regisztráció.")

            elif valasztas == "3":
                print("Kilépés...")
                fajlkezelo.mentes_felhasznalok(felhasznalok)
                fajlkezelo.mentes_berlesek(kolcsonzo.berlesek)
                break

        else:
            print(f"\nBejelentkezve mint: {aktiv_felhasznalo.nev}")
            print("1. Elérhető személyautók")
            print("2. Elérhető teherautók")
            print("3. Autóbérlés")
            print("4. Bérléseim megtekintése")
            print("5. Bérlés lemondása")
            print("6. Összes bérlés listázása")
            print("7. Kijelentkezés")
            valasztas = input("Választás: ")

            if valasztas == "1":
                print("\nSzemélyautók:")
                for auto in kolcsonzo.autok:
                    if isinstance(auto, Szemelyauto):
                        print(auto.info())

            elif valasztas == "2":
                print("\nTeherautók:")
                for auto in kolcsonzo.autok:
                    if isinstance(auto, Teherauto):
                        print(auto.info())

            elif valasztas == "3":
                kolcsonzo.autoberles_menete(aktiv_felhasznalo, felhasznalok)

            elif valasztas == "4":
                berlesek = aktiv_felhasznalo.get_berlesek()
                if not berlesek:
                    print("Nincs aktív bérlésed.")
                else:
                    for b in berlesek:
                        auto = next((a for a in kolcsonzo.autok if a.id == b.auto_id), None)
                        if auto:
                            print(f"Bérlés azonosító: {b.berles_id} | {auto.rendszam} – {auto.marka} | {b.datum_kezd} – {b.datum_veg}")

            elif valasztas == "5":
                sajat_berlesek = aktiv_felhasznalo.get_berlesek()
                if not sajat_berlesek:
                    print("Nincs mit lemondani.")
                    continue
                for i, b in enumerate(sajat_berlesek, 1):
                    auto = next((a for a in kolcsonzo.autok if a.id == b.auto_id), None)
                    if auto:
                        print(f"{i}. {auto.rendszam} – {auto.marka} | {b.datum_kezd} – {b.datum_veg}")
                valasz = input("Melyik bérlést szeretnéd törölni? (szám, 0 = vissza): ")
                if valasz == "0":
                    continue
                try:
                    index = int(valasz) - 1
                    berles_id = sajat_berlesek[index].berles_id
                    kolcsonzo.berles_lemondasa(berles_id)
                    aktiv_felhasznalo.torol_berles(berles_id)
                    print("Bérlés törölve.")
                except Exception as e:
                    print(f"Hiba: {e}")
                    logger.log_kivetel(e)

            elif valasztas == "6":
                print("\nÖsszes bérlés és felhasználó:")
                for felh in felhasznalok:
                    for b in felh.get_berlesek():
                        auto = next((a for a in kolcsonzo.autok if a.id == b.auto_id), None)
                        if auto:
                            print(f"{felh.nev} ({felh.email}): {auto.rendszam} – {auto.marka} | {b.datum_kezd} – {b.datum_veg}")

            elif valasztas == "7":
                print(f"Viszlát, {aktiv_felhasznalo.nev}!")
                fajlkezelo.mentes_felhasznalok(felhasznalok)
                fajlkezelo.mentes_berlesek(kolcsonzo.berlesek)
                aktiv_felhasznalo = None

            else:
                print("Érvénytelen választás.")
