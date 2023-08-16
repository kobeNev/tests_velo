import os

def clear():
    os.system("cls") # Ingesteld op Windows, voor Linux(mac): os.system("clear")

clear()
print("             Welkom bij Velo!")
print("Het beste fietsverhuurbedrijf van Antwerpen!")
input("        Druk op enter om verder te gaan.")
clear()

while True:
    print("      Wat wilt u doen?:")
    print("    H: Handmatig invoeren")
    print("   S: Een simulatie starten")
    print("     G: De site genereren")
    keuze = (input("   Q: de toepassing stoppen     \n")).upper()
    if keuze == "H":
        clear()
        print("U koos voor handmatig invoeren.")
        break
    if keuze == "S":
        clear()
        print("De simulatie word gestart.")
        break
    if keuze == "G":
        clear()
        print("De site word gegenereerd.")
        break
    if keuze == "Q":
        clear()
        print("De toepassing word gestopt.")
        break
    else:
        clear()
        print("U heeft geen geldige input gegeven. Probeer het opnieuw.")

