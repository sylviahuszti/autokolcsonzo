Konzolos Autókölcsönző Rendszer 

Ez egy egyszerű Pythonos konzolprogram, amivel autókat lehet kölcsönözni. A felhasználók regisztrálhatnak, bejelentkezhetnek, kiválaszthatják a szabad autókat, és lefoglalhatják őket adott napokra. Minden adat elmentődik fájlba, így kilépés után is megmaradnak a bérlések.

  Mit tud a program?
	•	Regisztráció és bejelentkezés
	•	Szabad autók listázása
	•	Kétféle jármű: személyautók és teherautók (külön listázva)
	•	Bérlés megadott dátummal és napok számával
	•	Bérlés lemondása
	•	Összes bérlés megtekintése (tesztfelhasználókkal együtt)
	•	Mentés fájlba (JSON)
	•	Hibák naplózása (naplo.log)

  Hogyan működik?
	•	Objektumorientált Python kód
	•	Minden járműnek és bérlésnek van egyedi azonosítója (UUID, lerövidítve)
	•	Minden adat elmentődik: autok.json, berlesek.json, felhasznalok.json
	•	A program külön fájlokba van szétbontva (modellek, szolgáltatások, fájlkezelés stb.)
	•	Nem használ külső csomagokat – csak a Python beépített dolgait

├── main.py              # A program elindítása innen történik
├── menu.py              # Itt van a konzolos menü és a vezérlés
├── models/              # Járművek, felhasználók és bérlések
│   ├── auto.py
│   ├── berles.py
│   └── felhasznalo.py
├── services/            # Kölcsönző működése és hibanaplózás
│   ├── kolcsonzo_service.py
│   └── logger_service.py
├── storage/             # Fájlok mentése és betöltése
│   └── file_handler.py
├── exceptions/          # Saját hibakezelő osztályok
│   └── errors.py
├── data/                # Itt vannak az adatok
│   ├── autok.json
│   ├── berlesek.json
│   └── felhasznalok.json
├── naplo.log            # Ide kerülnek a hibák
└── readme.md            # Ez a leírás itt