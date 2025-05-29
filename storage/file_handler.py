import json
import os
from models.auto import VehicleFactory, Vehicle
from models.berles import Berles
from models.felhasznalo import Felhasznalo


class FileHandler:
    """
    Ez az osztály kezeli az adatok fájlba mentését és betöltését.
    Külön kezeli az autókat, bérléseket és felhasználókat JSON formátumban.
    """

    def __init__(self, autok_fajl: str = "data/autok.json", berlesek_fajl: str = "data/berlesek.json", felhasznalok_fajl: str = "data/felhasznalok.json"):
        self._autok_fajl = autok_fajl
        self._berlesek_fajl = berlesek_fajl
        self._felhasznalok_fajl = felhasznalok_fajl

    def mentes_autok(self, autok: list[Vehicle]):
        adatok = [auto.to_dict() for auto in autok]
        with open(self._autok_fajl, "w", encoding="utf-8") as f:
            json.dump(adatok, f, indent=4, ensure_ascii=False)

    def betoltes_autok(self) -> list[Vehicle]:
        if not os.path.exists(self._autok_fajl):
            return []
        with open(self._autok_fajl, "r", encoding="utf-8") as f:
            adatok = json.load(f)
            return [VehicleFactory.from_dict(obj) for obj in adatok]

    def mentes_berlesek(self, berlesek: list[Berles]):
        adatok = [b.to_dict() for b in berlesek]
        with open(self._berlesek_fajl, "w", encoding="utf-8") as f:
            json.dump(adatok, f, indent=4, ensure_ascii=False)

    def betoltes_berlesek(self) -> list[Berles]:
        if not os.path.exists(self._berlesek_fajl):
            return []
        with open(self._berlesek_fajl, "r", encoding="utf-8") as f:
            adatok = json.load(f)
            return [Berles.from_dict(obj) for obj in adatok]

    def mentes_felhasznalok(self, felhasznalok: list[Felhasznalo]):
        adatok = [f.to_dict() for f in felhasznalok]
        with open(self._felhasznalok_fajl, "w", encoding="utf-8") as f:
            json.dump(adatok, f, indent=4, ensure_ascii=False)

    def betoltes_felhasznalok(self) -> list[Felhasznalo]:
        if not os.path.exists(self._felhasznalok_fajl):
            return []
        with open(self._felhasznalok_fajl, "r", encoding="utf-8") as f:
            adatok = json.load(f)
            return [Felhasznalo.from_dict(obj) for obj in adatok]

    def torol_mindent(self):
        """
        Hasznos lehet teszteléshez – törli az összes adatot.
        """
        for fajl in [self._autok_fajl, self._berlesek_fajl, self._felhasznalok_fajl]:
            if os.path.exists(fajl):
                os.remove(fajl)
