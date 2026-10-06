import tkinter as tk
import random

root = tk.Tk()
root.title("Supervision TGV autonome")

# Toutes les données du train sont rangées dans un dictionnaire
train = {}


def maj_donnees():
    # 1) Simulation des capteurs (les pannes sont assez rares)
    train["vitesse"] = random.randint(0, 320)
    train["temperature"] = random.randint(15, 45)
    train["porte_fermee"] = random.random() > 0.2
    train["signal"] = random.choice(["Voie libre", "Voie libre", "Ralentissement", "Arrêt"])
    train["lidar"] = random.random() < 0.1
    train["gps"] = f"{random.uniform(48, 49):.4f}N, {random.uniform(2, 3):.4f}E"
    train["interne"] = random.random() > 0.1
    train["gsmr"] = random.random() > 0.3
    train["frmcs"] = random.random() > 0.1
    train["batterie"] = random.randint(20, 100)
    train["wifi"] = random.random() > 0.2


def reseau_actif():
    # Redondance : si le GSM-R tombe, le FRMCS prend le relais
    if train["gsmr"]:
        return "GSM-R"
    elif train["frmcs"]:
        return "FRMCS"
    else:
        return "AUCUN"


def analyse_IA():
    # 2) Les règles sont testées de la plus grave à la moins grave
    if not train["porte_fermee"] or train["signal"] == "Arrêt" or train["lidar"]:
        return "DANGER : depart interdit", "red"
    elif train["vitesse"] > 300 or train["temperature"] > 40 or train["batterie"] < 30 or reseau_actif() == "AUCUN":
        return "ALERTE", "orange"
    else:
        return "OK - circulation normale", "green"


def maj_affichage():
    # 3) On écrit les valeurs dans les labels
    label_vitesse.config(text=f"{train['vitesse']} km/h")

    texte, couleur = analyse_IA()
    label_etat.config(text=texte, bg=couleur)

    label_secu.config(text=f"Portes : {'fermees' if train['porte_fermee'] else 'OUVERTES'}\n"
                           f"Signal (camera) : {train['signal']}\n"
                           f"LIDAR : {'OBSTACLE' if train['lidar'] else 'voie degagee'}")
    label_capt.config(text=f"GPS : {train['gps']}\n"
                           f"Temperature : {train['temperature']} C")
    label_res.config(text=f"Reseau interne : {'OK' if train['interne'] else 'PANNE'}\n"
                          f"GSM-R : {'OK' if train['gsmr'] else 'PANNE'}\n"
                          f"FRMCS : {'OK' if train['frmcs'] else 'PANNE'}\n"
                          f"Liaison utilisee : {reseau_actif()}")
    label_conf.config(text=f"Batterie : {train['batterie']} %\n"
                           f"Wi-Fi : {'actif' if train['wifi'] else 'coupe'}")


def boucle():
    maj_donnees()
    maj_affichage()
    root.after(2000, boucle)  # on recommence dans 2 secondes


# ---------- Interface ----------
label_vitesse = tk.Label(root, font=("Arial", 28), bg="lightblue")
label_vitesse.pack(fill="x")
label_etat = tk.Label(root, font=("Arial", 14, "bold"), fg="white")
label_etat.pack(fill="x")

zones = tk.Frame(root)
zones.pack()


def creer_zone(titre, ligne, colonne):
    cadre = tk.LabelFrame(zones, text=titre, padx=10, pady=5)
    cadre.grid(row=ligne, column=colonne, padx=5, pady=5, sticky="nw")
    label = tk.Label(cadre, justify="left", width=28, anchor="w")
    label.pack()
    return label


label_secu = creer_zone("Securite", 0, 0)
label_capt = creer_zone("Capteurs modernes", 0, 1)
label_res = creer_zone("Reseaux", 1, 0)
label_conf = creer_zone("Energie et confort", 1, 1)

boucle()
root.mainloop()
