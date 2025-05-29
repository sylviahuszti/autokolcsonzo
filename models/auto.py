import re
import uuid
from abc import ABC, abstractmethod


class Vehicle(ABC):
    """
    Alaposztály minden járműhöz. Egységes azonosítás, validálás és
    adatkonverzió, hogy jól lehessen fájlba írni és onnan visszaolvasni.
    """

    def __init__(self, rendszam: str, marka: str, napi_dij: int, jarmu_id: str = None):
        # Egységes azonosító minden járműhöz – vagy külső betöltésből, vagy új UUID
        self._id = jarmu_id if jarmu_id else str(uuid.uuid4())

        # Validáció a rendszámra – szabványos magyar formátum (ABC-123)
        if not re.match(r"^[A-Z]{3}-\d{3}$", rendszam.upper()):
            raise ValueError(f"Hibás rendszám: {rendszam}. Példa: ABC-123")
        self._rendszam = rendszam.upper()

        self._marka = marka.strip()
        if not (1000 <= napi_dij <= 100000):
            raise ValueError("A napi díj irreális (1000–100000 Ft).")
        self._napi_dij = napi_dij

    @property
    def id(self):
        return self._id

    @property
    def rendszam(self):
        return self._rendszam

    @property
    def marka(self):
        return self._marka

    @property
    def napi_dij(self):
        return self._napi_dij

    def __eq__(self, other):
        return isinstance(other, Vehicle) and self._id == other._id

    def __hash__(self):
        return hash(self._id)

    def __str__(self):
        return f"{self._rendszam} - {self._marka} ({self._napi_dij} Ft/nap)"

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "rendszam": self._rendszam,
            "marka": self._marka,
            "napi_dij": self._napi_dij,
            "tipus": self.__class__.__name__.lower(),
        }

    @abstractmethod
    def info(self) -> str:
        pass


class Szemelyauto(Vehicle):
    def __init__(self, rendszam, marka, napi_dij, ulohelyek, jarmu_id=None):
        super().__init__(rendszam, marka, napi_dij, jarmu_id)
        if ulohelyek < 2:
            raise ValueError("Legalább 2 ülőhely szükséges egy személyautóhoz.")
        self._ulohelyek = ulohelyek

    @property
    def ulohelyek(self):
        return self._ulohelyek

    def info(self):
        return f"{super().__str__()} - Személyautó, {self._ulohelyek} ülőhely"

    def to_dict(self):
        d = super().to_dict()
        d["extra"] = self._ulohelyek
        return d


class Teherauto(Vehicle):
    def __init__(self, rendszam, marka, napi_dij, teherbiras, jarmu_id=None):
        super().__init__(rendszam, marka, napi_dij, jarmu_id)
        if teherbiras < 100:
            raise ValueError("A teherbírás minimum 100 kg kell legyen.")
        self._teherbiras = teherbiras

    @property
    def teherbiras(self):
        return self._teherbiras

    def info(self):
        return f"{super().__str__()} - Teherautó, {self._teherbiras} kg teherbírás"

    def to_dict(self):
        d = super().to_dict()
        d["extra"] = self._teherbiras
        return d


class VehicleFactory:
    """
    Egyedi gyártó osztály, amely egy szótárból (pl. JSON betöltésből) képes
    a megfelelő járműtípus példányát létrehozni.
    """

    @staticmethod
    def from_dict(data: dict) -> Vehicle:
        tipus = data.get("tipus")
        if tipus == "szemelyauto":
            return Szemelyauto(
                rendszam=data["rendszam"],
                marka=data["marka"],
                napi_dij=data["napi_dij"],
                ulohelyek=data["extra"],
                jarmu_id=data["id"]
            )
        elif tipus == "teherauto":
            return Teherauto(
                rendszam=data["rendszam"],
                marka=data["marka"],
                napi_dij=data["napi_dij"],
                teherbiras=data["extra"],
                jarmu_id=data["id"]
            )
        else:
            raise ValueError(f"Nem ismert járműtípus: {tipus}")