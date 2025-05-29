# Konzolos Autókölcsönző Rendszer

Ez egy egyszerű Pythonos konzolprogram, amivel autókat lehet kölcsönözni.  
A felhasználók regisztrálhatnak, bejelentkezhetnek, kiválaszthatják a szabad autókat, és lefoglalhatják őket adott napokra.  
Minden adat fájlba mentődik, így kilépés után is megmaradnak a bérlések.

---

## Funkciók

- Regisztráció és bejelentkezés  
- Szabad autók listázása  
- Kétféle jármű: személyautók és teherautók (külön listázva)  
- Bérlés megadott kezdődátummal és napok számával  
- Bérlés lemondása  
- Összes bérlés megtekintése (tesztfelhasználókkal együtt)  
- Adatok mentése fájlba (JSON)  
- Hibák naplózása (`naplo.log`)

---

## Működés

- Objektumorientált Python kód  
- Minden objektumnak (autó, bérlés, felhasználó) van egyedi azonosítója (UUID, lerövidítve)  
- Minden adat fájlba mentődik:
  - `autok.json` – autók  
  - `berlesek.json` – bérlések  
  - `felhasznalok.json` – felhasználók és bérléseik  
- A kód külön fájlokra van bontva (modellek, szolgáltatások, fájlkezelés stb.)  
- Nem használ külső csomagokat, csak a Python beépített moduljait

---

## Mappa felépítés

<pre>
```
autokolcsonzo/
├── main.py              # A program indítása innen
├── menu.py              # Konzolos menürendszer és vezérlés
├── models/              # Járművek, felhasználók, bérlések
│   ├── auto.py
│   ├── berles.py
│   └── felhasznalo.py
├── services/            # Kölcsönző működése és naplózás
│   ├── kolcsonzo_service.py
│   └── logger_service.py
├── storage/             # Fájlok mentése és betöltése
│   └── file_handler.py
├── exceptions/          # Saját hibakezelő osztályok
│   └── errors.py
├── data/                # Mentett adatok
│   ├── autok.json
│   ├── berlesek.json
│   └── felhasznalok.json
├── naplo.log            # Hibák naplófájlja
└── readme.md            # Ez a leírás itt
```
</pre>

A projekt a beadandó követelményei alapján készült, és igyekeztem minden elvárást teljesíteni.
Köszönöm az értékelést.
