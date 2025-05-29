class KolcsonzoHiba(Exception):
    """
    Alap kivételosztály a kölcsönző logikához tartozó hibákhoz.
    Minden más specifikus kivétel ebből öröklődik.
    """
    pass


class AutoNemLetezikError(KolcsonzoHiba):
    def __init__(self, auto_id):
        super().__init__(f"A megadott autó azonosítója nem található: {auto_id}")


class AutoMarBerelveError(KolcsonzoHiba):
    def __init__(self, auto_id):
        super().__init__(f"Az autó ({auto_id}) már bérlés alatt áll a megadott időszakban.")


class ErvenytelenDatumError(KolcsonzoHiba):
    def __init__(self, datum):
        super().__init__(f"Érvénytelen dátumformátum: {datum}. Elvárt: ÉÉÉÉ-HH-NN")


class NemTalalhatoBerlesError(KolcsonzoHiba):
    def __init__(self, berles_id):
        super().__init__(f"Nincs ilyen azonosítójú bérlés: {berles_id}")


class BerlesUtkozesError(KolcsonzoHiba):
    def __init__(self, auto_id, uj_kezd, uj_veg, letezo_kezd, letezo_veg):
        super().__init__(
            f"Ütközés a bérlésnél: az autó ({auto_id}) már foglalt "
            f"{letezo_kezd} és {letezo_veg} között. Új bérlés: {uj_kezd} – {uj_veg}."
        )