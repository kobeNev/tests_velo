import json
import random
import time

"""nu = time.time()
print(time.localtime(nu))"""


class Fiets:
    def __init__(self, fiets_id):
        self.fiets_id = fiets_id


class Slot:
    def __init__(self, slot_id):
        self.fiets = None
        self.beschikbaar = True
        self.slot_id = slot_id

    def plaats_fiets(self, fiets):
        if self.beschikbaar:
            self.fiets = fiets
            self.beschikbaar = False

    def verwijder_fiets(self, fiets):
        if not self.beschikbaar:
            self.fiets = None
            self.beschikbaar = True
            return fiets


class Station:
    def __init__(self, station_id, naam, capaciteit):
        self.station_id = station_id
        self.naam = naam
        self.sloten = []
        self.capaciteit = capaciteit
        self.maak_sloten()

    def maak_sloten(self):
        for i in range(self.capaciteit):
            slot = Slot(f"S{i}")
            self.sloten.append(slot)

    def aantal_beschikbare_slots(self):
        return len([slot for slot in self.sloten if slot.beschikbaar])

    def aantal_beschikbare_fietsen(self):
        return len([slot for slot in self.sloten if not slot.beschikbaar])

    def __str__(self):
        return f"{self.naam} heeft {self.aantal_beschikbare_slots()} vrije plaatsen, en {self.aantal_beschikbare_fietsen()} fietsen beschikbaar."


class Gebruiker:
    def __init__(self, gebruiker_id, naam, velo):
        self.gebruiker_id = gebruiker_id
        self.naam = naam
        self.max_capaciteit = 1
        self.fiets = []
        self.velo = velo

    def leen_fiets(self, fiets):
        if len(self.fiets) < self.max_capaciteit:
            self.fiets.append(fiets)
            fiets_slot = None
            for station in self.velo.stations:
                for slot in station.sloten:
                    if slot.fiets == fiets:
                        fiets_slot = slot
                        break
                if fiets_slot:
                    fiets_slot.verwijder_fiets(fiets)
                    """print(
                        f"Fiets {fiets.fiets_id} geleend door {self.naam} uit slot {fiets_slot.slot_id}"
                    )"""
                else:
                    """print(f"Fiets {fiets.fiets_id} kon niet worden geleend.")"""
        else:
            """print(f"Gebruiker {self.naam} heeft al een fiets geleend.")"""

    def retourneer_fiets(self, fiets):
        if fiets in self.fiets:
            self.fiets.remove(fiets)
            for slot in random.choice((self.velo.stations).sloten):
                if slot.beschikbaar:
                    slot.plaats_fiets(fiets)
                    """print(
                        f"Fiets {fiets.fiets_id} teruggebracht door {self.naam} in slot {slot.slot_id}"
                    )"""
                    break
            else:
                """print(
                    f"Geen beschikbare sloten om de fiets {fiets.fiets_id} terug te brengen."
                )"""
        else:
            """print(f"Gebruiker {self.naam} heeft deze fiets niet geleend.")"""


class Velo:
    def __init__(self):
        self.stations = []
        self.fietsen = []
        self.gebruikers = []

    def maak_stations_van_json(self):
        with open("velo.geojson", "r") as json_file:
            json_gegevens = json.load(json_file)

        for item in json_gegevens["features"]:
            naam = item["properties"]["Naam"]
            capaciteit = item["properties"]["Aantal_plaatsen"]
            station = Station(item["properties"]["Objectcode"], naam, capaciteit)
            station.maak_sloten()
            self.stations.append(station)

    def maak_fietsen(self):
        for i in range(1, 9950):
            fiets = Fiets(f"F{i}")
            self.fietsen.append(fiets)

    def maak_gebruikers(self):
        with open("namenlijst.json", "r") as json_file:
            json_gegevens = json.load(json_file)

        while len(self.gebruikers) < 55000:
            for index, item in enumerate(json_gegevens):
                naam = item["name"]
                gebruiker = Gebruiker(f"G{index}", naam, self)
                self.gebruikers.append(gebruiker)

    def plaats_fietsen_in_station(self):
        random.shuffle(self.stations)  # Meng de volgorde van de stations willekeurig
        random.shuffle(self.fietsen)  # Meng de volgorde van de fietsen willekeurig

        for station in self.stations:
            # Bepaal een willekeurig aantal fietsen om toe te wijzen aan dit station
            aantal_fietsen = random.randint(
                0, min(len(self.fietsen), station.aantal_beschikbare_slots())
            )

            for _ in range(aantal_fietsen):
                slot = next((s for s in station.sloten if s.beschikbaar), None)
                if slot:
                    slot.plaats_fiets(self.fietsen.pop())

    def __str__(self):
        return f"Velo heeft {len(self.stations)} stations, {len(self.fietsen)} fietsen en {len(self.gebruikers)} gebruikers."


class main:
    def __init__(self):
        self.velo = Velo()
        print("Velo object aangemaakt")
        self.velo.maak_stations_van_json()
        print("Stations aangemaakt")
        self.velo.maak_fietsen()
        print("Fietsen aangemaakt")
        self.velo.maak_gebruikers()
        print("Gebruikers aangemaakt")
        self.velo.plaats_fietsen_in_station()
        print("Fietsen in stations geplaatst")

    def start(self):
        for gebruiker in self.velo.gebruikers:
            if random.random() < 0.5:
                station = random.choice(self.velo.stations)
                if station.aantal_beschikbare_fietsen() > 0:
                    slot = random.choice(station.sloten)
                    if not slot.beschikbaar:
                        if slot.fiets is not None:  # Check if the slot has a bike
                            gebruiker.leen_fiets(slot.fiets)  # Lease the bike
                            print(
                                f"Gebruiker {gebruiker.naam} leent fiets uit station {station.naam}"
                            )

    def stop(self):
        for gebruiker in self.velo.gebruikers:
            if gebruiker.fiets:  # Check if the user has a bike
                station = random.choice(self.velo.stations)
                if station.aantal_beschikbare_slots() > 0:
                    slot = random.choice(station.sloten)
                    if slot.beschikbaar:
                        slot.plaats_fiets(
                            gebruiker.fiets
                        )  # Return the bike to the slot
                        print(
                            f"Gebruiker {gebruiker.naam} retourneert fiets bij station {station.naam}"
                        )


if __name__ == "__main__":
    main_program = main()
    print(Station("1", "test", 10).aantal_beschikbare_fietsen())
    input("duw op enter om te starten met het uitlenen van fietsen")
    main_program.start()
    input("duw op enter om te stoppen met het uitlenen van fietsen")
    main_program.stop()
