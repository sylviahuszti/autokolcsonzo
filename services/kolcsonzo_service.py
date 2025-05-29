from datetime import date, datetime, timedelta
from models.auto import Vehicle
from models.berles import Berles
from exceptions.errors import (
    AutoNemLetezikError,
    AutoMarBerelveError,
    BerlesUtkozesError,
    NemTalalhatoBerlesError,
)


class KolcsonzoService:
    def __init__(self, nev: str):
        self._nev = nev
        self._autok: list[Vehicle] = []
        self._berlesek: list[Berles] = []

    @property
    def autok(self):
        return self._autok.copy()

    @property
    def berlesek(self):
        return self._berlesek.copy()

    def auto_hozzaadas(self, auto: Vehicle):
        self._autok.append(auto)

    def keres_auto_id_alapjan(self, auto_id: str) -> Vehicle:
        for auto in self._autok:
            if auto.id == auto_id:
                return auto
        raise AutoNemLetezikError(auto_id)

    def auto_elerheto(self, auto_id: str, datum_kezd: date, datum_veg: date) -> bool:
        for berles in self._berlesek:
            if berles.auto_id == auto_id:
                if not (datum_veg < berles.datum_kezd or datum_kezd > berles.datum_veg):
                    return False
        return True

    def uj_berles(self, auto_id: str, datum_kezd: str, datum_veg: str) -> Berles:
        auto = self.keres_auto_id_alapjan(auto_id)

        try:
            kezd = date.fromisoformat(datum_kezd)
            veg = date.fromisoformat(datum_veg)
        except ValueError:
            raise ValueError("A dátum formátuma hibás. Használj: ÉÉÉÉ-HH-NN")

        if kezd > veg:
            raise ValueError("A kezdődátum nem lehet későbbi, mint a végdátum.")

        for b in self._berlesek:
            if b.auto_id == auto_id:
                if not (veg < b.datum_kezd or kezd > b.datum_veg):
                    raise BerlesUtkozesError(
                        auto_id=auto_id,
                        uj_kezd=kezd,
                        uj_veg=veg,
                        letezo_kezd=b.datum_kezd,
                        letezo_veg=b.datum_veg
                    )

        if not self.auto_elerheto(auto_id, kezd, veg):
            raise AutoMarBerelveError(auto_id)

        uj = Berles(auto_id=auto_id, mettol=datum_kezd, meddig=datum_veg)
        self._berlesek.append(uj)
        return uj

    def berles_lemondasa(self, berles_id: str) -> None:
        for berles in self._berlesek:
            if berles.berles_id == berles_id:
                self._berlesek.remove(berles)
                return
        raise NemTalalhatoBerlesError(berles_id)

    def aktiv_berlesek_ma(self) -> list[Berles]:
        return [b for b in self._berlesek if b.is_aktiv_ma()]

    def autok_listazasa(self) -> list[str]:
        return [auto.info() for auto in self._autok]

    def berlesek_listazasa(self) -> list[str]:
        return [str(b) for b in self._berlesek]

    def autoberles_menete(self, felhasznalo, osszes_felhasznalo):
        elerheto_autok = self._autok.copy()
        if not elerheto_autok:
            print("Nincs szabad autó.")
            return

        for i, auto in enumerate(elerheto_autok, 1):
            print(f"{i}. {auto.rendszam} – {auto.marka} | {auto.napi_dij} Ft/nap")

        valasz = input("Melyik autót szeretnéd bérelni? (szám, 0 = vissza): ")
        if valasz == "0":
            return
        try:
            index = int(valasz) - 1
            auto_obj = elerheto_autok[index]
        except (IndexError, ValueError):
            print("Érvénytelen választás.")
            return

        while True:
            print("Kérlek, add meg a bérlés kezdőnapját az alábbi formátumban:")
            print("   ➤ ÉÉÉÉ.HH.NN (pl.: 2025.06.01)")
            datum_input = input("Dátum (vagy 0 = vissza): ")
            if datum_input == "0":
                return
            try:
                datum = datetime.strptime(datum_input, "%Y.%m.%d").date()
                if datum < datetime.today().date():
                    print("A dátum nem lehet múltbeli.")
                else:
                    break
            except ValueError:
                print("Hibás dátumformátum! Pl.: 2025.06.01")

        while True:
            napok = input("Hány napra szeretnéd bérelni? (pl. 3): ")
            try:
                napok_szama = int(napok)
                if napok_szama < 1:
                    raise ValueError
                break
            except ValueError:
                print("Érvénytelen napérték. Írj be egy pozitív egész számot.")

        datum_veg = datum + timedelta(days=napok_szama - 1)

        try:
            berles = self.uj_berles(auto_obj.id, datum.strftime("%Y-%m-%d"), datum_veg.strftime("%Y-%m-%d"))
            felhasznalo.hozzaad_berles(berles)
            osszeg = auto_obj.napi_dij * napok_szama
            print(f"Sikeres bérlés: {auto_obj.rendszam}, {datum} – {datum_veg} | Ár: {osszeg} Ft")
        except Exception as e:
            print(f"Hiba történt: {e}")