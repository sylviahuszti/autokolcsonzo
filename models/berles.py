from __future__ import annotations
from datetime import date
import random
import string


def generate_berles_id(length: int = 6) -> str:
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=length))


class Berles:
    """
    Egy bérlés reprezentációja:
    - auto_id: az autó azonosítója
    - mettol: kezdődátum (ISO string)
    - meddig: végdátum (ISO string)
    - berles_id: egyedi azonosító (automatikusan generált, 6 karakteres, olvasható)
    """

    def __init__(self, auto_id: str, mettol: str, meddig: str, berles_id: str = None):
        self._berles_id = berles_id if berles_id else generate_berles_id()
        self._auto_id = auto_id
        self._datum_kezd = date.fromisoformat(mettol)
        self._datum_veg = date.fromisoformat(meddig)

    @property
    def berles_id(self) -> str:
        return self._berles_id

    @property
    def auto_id(self) -> str:
        return self._auto_id

    @property
    def datum_kezd(self) -> date:
        return self._datum_kezd

    @property
    def datum_veg(self) -> date:
        return self._datum_veg

    def is_aktiv_ma(self) -> bool:
        return self._datum_kezd <= date.today() <= self._datum_veg

    def is_aktiv_datum(self, adott_nap: date) -> bool:
        return self._datum_kezd <= adott_nap <= self._datum_veg

    def atfed(self, masik: Berles) -> bool:
        return self._auto_id == masik.auto_id and not (
            self._datum_veg < masik.datum_kezd or self._datum_kezd > masik.datum_veg
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "berles_id": self._berles_id,
            "auto_id": self._auto_id,
            "datum_kezd": self._datum_kezd.isoformat(),
            "datum_veg": self._datum_veg.isoformat(),
        }

    @classmethod
    def from_dict(cls, adatok: dict[str, str]) -> Berles:
        return cls(
            auto_id=adatok["auto_id"],
            mettol=adatok["datum_kezd"],
            meddig=adatok["datum_veg"],
            berles_id=adatok.get("berles_id"),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Berles):
            return NotImplemented
        return self._berles_id == other._berles_id

    def __hash__(self) -> int:
        return hash(self._berles_id)

    def __str__(self) -> str:
        return f"{self._berles_id}: {self._auto_id} ({self._datum_kezd} - {self._datum_veg})"


Berles = Berles