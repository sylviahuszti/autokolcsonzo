import os
from datetime import datetime


class LoggerService:
    """
    Egyszeru naplozo osztaly, amely minden fontos esemenyt elment egy log fajlba.
    Singleton-kent viselkedik: minden hivas ugyanahhoz az objektumhoz tartozik.
    """

    _instance = None
    _log_file = "naplo.log"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerService, cls).__new__(cls)
        return cls._instance

    def log(self, uzenet: str):
        """
        Egy sor naplozasa idobelyeggel, fajlba.
        """
        idopont = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sor = f"[{idopont}] {uzenet}\n"

        with open(self._log_file, mode="a", encoding="utf-8") as fajl:
            fajl.write(sor)

    def log_kivetel(self, kivetel: Exception):
        """
        Kivetel objektum naplozasa teljes szoveggel.
        """
        self.log(f"KIVETEL: {str(kivetel)}")

    def torles(self):
        """
        A naplofajl torlese, pl. teszteleshez vagy uj inditashoz.
        """
        if os.path.exists(self._log_file):
            os.remove(self._log_file)

    def beolvas(self) -> list[str]:
        """
        Naplofajl tartalmanak visszaolvasasa soronkent.
        """
        if not os.path.exists(self._log_file):
            return []

        with open(self._log_file, mode="r", encoding="utf-8") as fajl:
            return fajl.readlines()
