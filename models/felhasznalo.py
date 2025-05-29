import uuid
import hashlib
from models.berles import Berles


class Felhasznalo:
    """
    A rendszerben regisztrált felhasználó.
    Tartalmazza az azonosítóját, nevét, emailjét, jelszavát és bérléseit.
    """

    def __init__(self, nev: str, email: str, jelszo: str, felhasznalo_id: str = None, hashelt: bool = False):
        self._id = felhasznalo_id if felhasznalo_id else str(uuid.uuid4())
        self._nev = nev.strip()
        self._email = email.strip().lower()
        self._jelszo = jelszo if hashelt else self._hashel(jelszo)
        self._berlesek: list[Berles] = []

    def _hashel(self, jelszo: str) -> str:
        return hashlib.sha256(jelszo.encode()).hexdigest()

    @property
    def id(self):
        return self._id

    @property
    def nev(self):
        return self._nev

    @property
    def email(self):
        return self._email

    def ellenoriz_jelszo(self, jelszo: str) -> bool:
        return self._hashel(jelszo) == self._jelszo

    def hozzaad_berles(self, berles: Berles):
        self._berlesek.append(berles)

    def torol_berles(self, berles_id: str):
        self._berlesek = [b for b in self._berlesek if b.berles_id != berles_id]

    def get_berlesek(self) -> list[Berles]:
        return self._berlesek.copy()

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "nev": self._nev,
            "email": self._email,
            "jelszo": self._jelszo,
            "berlesek": [b.to_dict() for b in self._berlesek]
        }

    @staticmethod
    def tesztfelhasznalok() -> list:
        return [
            Felhasznalo("Kiss Pista", "pista@example.com", "titok123"),
            Felhasznalo("Nagy Anna", "anna.nagy@example.com", "jelszo456"),
            Felhasznalo("Szabo Bela", "bela.szabo@example.com", "abc123")
        ]

    @staticmethod
    def from_dict(adatok: dict):
        felh = Felhasznalo(
            nev=adatok["nev"],
            email=adatok["email"],
            jelszo=adatok["jelszo"],  # már hash-elve van!
            felhasznalo_id=adatok["id"],
            hashelt=True
        )
        berlesek = [Berles.from_dict(b) for b in adatok.get("berlesek", [])]
        for b in berlesek:
            felh.hozzaad_berles(b)
        return felh

    def __str__(self):
        return f"{self._nev} ({self._email}) – {len(self._berlesek)} bérlés"