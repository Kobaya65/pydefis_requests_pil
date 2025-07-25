"""Challenges from https://pydefis.callicode.fr Part 2
"""
import random
from time import sleep

import pandas as pd
import requests
from PIL import Image, ImageDraw


def compter_les_etoiles_chaudes() -> None:
    """https://pydefis.callicode.fr/defis/C23_CompteEtoiles/txt"""
    # open image
    img = Image.open('./compter_les_etoiles_chaudes/ciel.png')
    rgb_img = img.convert('RGB')
    nb_hot_stars = 0
    # browse pixels
    for x in range(rgb_img.width):
        for y in range(rgb_img.height):
            r, g, b = rgb_img.getpixel((x, y))
            if b > r and b > g:
                print(f"x={x:>4} y={y:>4}, r={r:>3} g={g:>3} b={b:>3}")
                nb_hot_stars += 1

    print("Resultat ", nb_hot_stars)


def portrait_colore() -> None:
    """https://pydefis.callicode.fr/defis/LePortraitColore/txt"""
    fichier = "./portrait_colore/portrait.png"
    # charger l'image
    image = Image.open(fichier)
    pixels = image.load()
    largeur, hauteur = image.size

    for y in range(hauteur):
        for x in range(largeur):
            r, g, b = pixels[x, y]
            r_bin = format(r, "b")
            r_bin_rev = r_bin[::-1]
            new_r = int(r_bin_rev, 2)
            g_bin = format(g, "b")
            g_bin_rev = g_bin[::-1]
            new_g = int(g_bin_rev, 2)
            b_bin = format(b, "b")
            b_bin_rev = b_bin[::-1]
            new_b = int(b_bin_rev, 2)

            pixels[x, y] = (new_r, new_g, new_b)

    image.save("./portrait_colore/portrait_verlan.png")
    print("Terminé")


def les_oiseaux_du_lac_de_stymphale() -> None:
    """https://pydefis.callicode.fr/defis/Herculito06Oiseaux/txt"""
    fichier = "./les_oiseaux_du_lac_de_stymphale/lake.png"
    # charger l'image
    image = Image.open(fichier)
    pixels = image.load()
    largeur, hauteur = image.size

    nb_fleches = 0
    for y in range(hauteur):
        for x in range(largeur):
            val = pixels[x, y]
            nb_fleches += val

    print(f"Résultat = {nb_fleches}")


def les_ecailles_du_dragon() -> None:
    """https://pydefis.callicode.fr/defis/C22_Dungeons/txt"""
    fichier = "./les_ecailles_du_dragon/dungeons_portal_enc.png"
    # charger l'image
    image = Image.open(fichier)
    pixels = image.load()
    largeur, hauteur = image.size
    n = 10000

    for y in range(hauteur):
        for x in range(largeur):
            val = pixels[x, y]
            # niveau de gris inférieur à 128) ((x^3 + y^7) xor n) % 256
            if val < 128:
                pixels[x, y] = ((x**3 + y**7) ^ n) % 256
            else:
                pixels[x, y] = random.randint(0, 255)

    image.save("./les_ecailles_du_dragon/dungeons_portal_decoded_10000.png")

    print("Fin")


def carte_du_marauder() -> None:
    """https://pydefis.callicode.fr/defis/MaraudeurConfusio/txt
    20250714 non résolu
    """
    fichier = "./carte_du_marauder/maraudeur_cr.png"
    cible = "./carte_du_marauder/maraudeur_cr.png"
    # charger l'image
    image_fichier = Image.open(fichier)
    pixels_fichier = image_fichier.load()
    hauteur, largeur = image_fichier.size

    image_cible = Image.open(cible)
    pixels_cible = image_cible.load()

    a = 53911
    b = 15677
    n = largeur * hauteur
    # (a * i + b) % n
    for x in range(hauteur):
        for y in range(largeur):
            no_pixel = x * y * largeur
            new_pos = (a * no_pixel + b) % n
            new_x = new_pos % largeur
            new_y = new_pos // largeur
            pixels_cible[new_x, new_y] = pixels_fichier[x, y]

    image_cible.save("./carte_du_marauder/maraudeur_decrypte.png")
    print("Fin.")

    def get_max_depth() -> tuple[int, int]:
        """Find the deepest point around a given point (y, x).
        Return row and column of that deepest point.
        """
        profondeurs = [[100.0] * hauteur for _ in range(largeur)]
        prof_min = 100.0

        return (profondeurs, prof_min)

    url_get = "https://pydefis.callicode.fr/defis/C24_Mimas/get/Kobaya/a1f1c"
    url_post = "https://pydefis.callicode.fr/defis/C24_Mimas/post/Kobaya/a1f1c"
    objet_cartes = requests.get(url_get, verify=True)
    objet_cartes_json = objet_cartes.json()
    dict_result = {}

    # filter dictionary to keep only keys starting with 'carte'
    # thanks to dictionary comprehension
    cartes = {key: value for key, value in objet_cartes_json.items()
              if key.startswith('carte')}

    for carte in cartes:
        hauteur = len(cartes[carte])
        largeur = len(cartes[carte][0])
        dict_result[f'trou{carte[-2:]}'] = get_max_depth()

    dict_result['signature'] = objet_cartes_json['signature']
    retour = requests.post(url_post, json=dict_result, verify=True)
    print(retour.json())


def exemple_url_2() -> None:
    """https://pydefis.callicode.fr/defis/ExempleURL/txt
    """
    url_get = "https://pydefis.callicode.fr/defis/ExempleURL/get/Kobaya/96190"
    url_post = "https://pydefis.callicode.fr/defis/ExempleURL/post/Kobaya/96190"

    res = requests.get(url_get, verify=True)
    lignes = res.text.split("\n")
    somme = int(lignes[1]) + int(lignes[2])
    ret = requests.post(url_post, verify=True, data={
                        "sig": lignes[0], "rep": somme})
    print(ret.text)


def les_cartes_chocogrenouille_a_trier() -> str:
    """https://pydefis.callicode.fr/defis/MLPotter01/txt
    """
    url_carte = (
        "https://pydefis.callicode.fr/defis/MLPotter01/intern/"
        "aMI7JVIH+mN1UYdSNih7hMO9A0wstHyI2QyDe7tkV2RmjDs3/card.png"
    )
    url_nom_personnage = (
        "https://pydefis.callicode.fr/defis/MLPotter01/intern/"
        "aMI7JVIH+mN1UYdSNih7hMO9A0wstHyI2QyDe7tkV2RmjDs3/reponse"
    )

    personnages = ["harry", "hermione", "ron", "luna",
                   "neville", "ginny", "fred", "george", "dobby", "hedwige"]

    idx = 1
    while idx <= 100:
        reponse = requests.get(url_carte, verify=True)
        image = reponse.text
        idhr = image.find("IHDR")
        image = image[idhr:]
        image = "\x80\x50\x4E\x47\x0D\x0A\x1A\x0A" + image
        if reponse.text.startswith("Password"):
            mot_de_passe = reponse.text.split(": ")[1]
            break

        alea = random.randint(0, len(personnages) - 1)
        sleep(1)
        retour = requests.get(
            f'{url_nom_personnage}/{personnages[alea]}', verify=True)
        print(f'{idx:>3} {retour.text[:-1]}')

        with open(f"./les_cartes_chocogrenouille/{idx:0>3}_{retour.text[1:-2]}.png", "wb") as f:
            f.write(image.encode())

        idx += 1

    return mot_de_passe


def le_coffre_d_electro() -> None:
    """https://pydefis.callicode.fr/defis/UrlElectro/txt"""
    HTTPS = "https://"
    url_get = "https://pydefis.callicode.fr/defis/UrlElectro/intern/code/03fCF23cfE"

    while url_get:
        rep = requests.get(url_get, verify=True)
        rep_str = str(rep.content)
        https_count = rep_str.count(HTTPS)
        https = rep_str.find(HTTPS)
        if https_count == 2:
            https = rep_str.find(HTTPS, https + 8)

        fin = rep_str.find(" ", https)
        if fin == -1:
            fin = rep_str.find("'", https)

        url_get = rep_str[https:fin]
        print(url_get)


def balade_sur_un_echiquier() -> None:
    """https://pydefis.callicode.fr/defis/BaladeEchiquier/txt"""
    recup_entree = "https://pydefis.callicode.fr/defis/BaladeEchiquier/get/Kobaya/d2488"
    soumission_rep = "https://pydefis.callicode.fr/defis/BaladeEchiquier/post/Kobaya/d2488"
    ordres = requests.get(recup_entree, verify=True)

    rep = str(ordres.content)
    rep = rep.split("\\n")
    # direction horizontale
    x = 0
    # direction verticale
    y = 1
    # positions de départ
    col = 1
    ligne = 1
    cases_visitees = {}
    cases_visitees[(col, ligne)] = 1

    for ordre in rep[1]:
        if ordre == "A":
            col += x
            ligne += y

            if cases_visitees.get((col, ligne)):
                cases_visitees[(col, ligne)] += 1
            else:
                cases_visitees[(col, ligne)] = 1

        # direction nord
        elif ordre == "D" and x == 0 and y == 1:
            x = 1
            y = 0
        elif ordre == "G" and x == 0 and y == 1:
            x = -1
            y = 0
        # direction est
        elif ordre == "D" and x == 1 and y == 0:
            x = 0
            y = -1
        elif ordre == "G" and x == 1 and y == 0:
            x = 0
            y = 1
        # direction sud
        elif ordre == "D" and x == 0 and y == -1:
            x = -1
            y = 0
        elif ordre == "G" and x == 0 and y == -1:
            x = 1
            y = 0
        # direction ouest
        elif ordre == "D" and x == -1 and y == 0:
            x = 0
            y = 1
        elif ordre == "G" and x == -1 and y == 0:
            x = 0
            y = -1

    reponse = f"{str(len(cases_visitees))}{chr(col + 64)}{ligne}"
    retour = requests.post(soumission_rep, verify=True, data={
                           "sig": rep[0][2:], "rep": reponse})
    print(f"Résultat = {retour.content.decode("utf-8")}")


def le_retourneur_de_temps() -> None:
    """https://pydefis.callicode.fr/defis/RetourneurTemps/txt"""
    minutes = max_minutes = 0
    for nb_tours in range(1, 101):
        somme_minutes = 0
        for mi in str(minutes):
            somme_minutes += int(mi)

        if (somme_minutes // 7) == (somme_minutes / 7) and minutes != 0:
            minutes -= 7
        else:
            minutes += 2

        max_minutes = max(max_minutes, minutes)
        print(f"{nb_tours:>3} {minutes:>4} {max_minutes:>4}")


def vous_parlez_fourchelangue() -> None:
    """https://pydefis.callicode.fr/defis/Fourchelangue/txt"""
    dico = {
        "HFH": "A",
        "FFH": "B",
        "SHS": "C",
        "SHH": "D",
        "SSH": "E",
        "FHF": "F",
        "FSS": "G",
        "HFF": "H",
        "HHH": "I/J",
        "SFS": "K",
        "FFS": "L",
        "FHS": "M",
        "SSF": "N",
        "FHH": "O",
        "HHF": "P",
        "SFF": "Q",
        "FSF": "R",
        "FSH": "S",
        "HHS": "T",
        "FFF": "U/V",
        "SSS": "W",
        "HFS": "X",
        "SHF": "Y",
        "SFH": "Z",
    }
    entree = "FHSFHHSSFHSSHSHFFSSHFSFHSSSFHFHFSSFFFHHHSSFHHHHSSHHSSHFHSHFHHHHSSFHSSSHFSHHHSHSFFFSSFHSFSSFSFHFHSSFSHHHSHHHFHHFFFFSFHSHHFFHHFFFFSFHSSSFF\
HHFFFFSHHSSHSHFHFSFHSSSFFHHFFFFSHHSHFHFFSFFSFHHSSFFSHHSSSHSSFFHFHHHSSFHSHHFFHHFFFFFFFHHHHHFSFHSSSFFHHFFFFSHHSFHHSHSSHSFFFHHFSSHFSFHSSHHSSHHSSH\
SSSHFSHHSHHSFSFFHHHHHFSHHSHHHFSSSSFFHHFFHFFSSSHFSHHSHHSFSFHFHHHHHHSFSFSSHFSHHSSSHHHSHSFFSFHHFSFFSHSFFFFFSSHHSHHSHFFSSHFHHSHHHFHFSFSHHHSHFHFFSH\
FHFSHHHSFHHFSFHSSSHHHSHSSHSFHHFSFFHSHFHSHSHSSSFSSHHSSSFFHHFFFFSHHSFSSSSHSSFSSHFSFFHHSSFHHSHSHHFFFSFFFFSHHSSSFFHHFFFFSHHSSSFFHHFFFFSHHSFHHSHSSH\
SFFFHHFSSHFSFFHHSSFFSHHSSHHSSHFSHHSHFHFFFHHSFSFSSHFSH"
    len_entree = len(entree)
    message = ""
    increment = 3
    pos = 0
    while pos <= len_entree:
        syllabe = entree[pos: pos + increment]
        traduction = dico.get(syllabe, " ")
        if traduction == " ":
            pos += 2
        else:
            pos += 3

        message += traduction

    print(f"Résultat = {message}")


def entree_au_ministere() -> None:
    """https://pydefis.callicode.fr/defis/CodeCabine/txt
    """
    entree = 64225
    compare = ["1", "2", "4", "6", "7"]
    prochains_chiffres = []
    while len(prochains_chiffres) < 3:
        chiffres = []
        carre = entree ** 2
        carre_str = str(carre)
        for l in carre_str:
            if l not in chiffres:
                chiffres.append(l)
        chiffres.sort()

        if chiffres == compare:
            prochains_chiffres.append(entree)
            print(f"{entree:>5} {carre:>12} {chiffres}")

        entree += 1

    print(f"Résultat = {prochains_chiffres[0]}, {prochains_chiffres[1]}, {prochains_chiffres[2]}")


def parametrage_du_vif_d_or() -> None:
    """https://pydefis.callicode.fr/defis/TrajetVifOr/txt
    (y, z, (x + y + z) % n)
    """
    nominal = [0, 0, 1]
    solutions = {}
    for n in range(2, 201):
        position = nominal.copy()
        nb_coups = 0
        exit_loop = True
        while exit_loop:
            x = position[0]
            y = position[1]
            z = position[2]

            position[0] = y
            position[1] = z
            position[2] = (x + y + z) % n
            nb_coups += 1
            if position == nominal:
                solutions[n] = nb_coups
                exit_loop = False

    tries = sorted(solutions.items(), key=lambda x: x[1], reverse=True)
    for x in tries[:10]:
        print(f"{x[0]},", end="")


def l_echarpe_de_mme_weasley() -> None:
    """https://pydefis.callicode.fr/defis/EcharpeWeasley/txt"""
    def traitement(carre: Image.Image) -> None:
        """Get numbers of different colors in this area of the image.
        Args:
            carre (Image.Image): part of the image (8 * 8 pixels)
        Returns:
            _type_: number of colors minu s1
        """
        couleurs = []
        for x1 in range(8):
            for y1 in range(8):
                r, g, b = carre.getpixel((x1, y1))
                couleur = r * 65536 + g * 256 + b
                if couleur not in couleurs:
                    couleurs.append(couleur)

        return len(couleurs) - 1

    rgb_img = Image.open('./l_echarpe_de_mme_weasley/message_echarpe.png')

    largeur = rgb_img.width
    hauteur = rgb_img.height
    column, row = int(largeur / 8), int(hauteur / 8)
    result = [["__" for _ in range(column)] for _ in range(row)]

    # browse pixels
    for x in range(0, largeur, 8):
        for y in range(0, hauteur, 8):
            carre = rgb_img.crop((x, y, x + 8, y + 8))
            num = traitement(carre)
            result[y // 8][x // 8] = num

    res = ""
    # read message
    for x in range(int(largeur / 8)):
        for y in range(0, int(hauteur / 8), 2):
            octet1 = result[y][x]
            octet2 = result[y + 1][x]
            chaine = f"{hex(octet1)}{hex(octet2)[2:]}"
            res += chr(int(chaine[2:], 16))

    print(f"Résultat = {res}")


def le_rayon_carre_des_daleks() -> None:
    """https://pydefis.callicode.fr/defis/C23_RayonCarre/txt
    20250724 : non résolu
    """
    data = pd.read_csv(filepath_or_buffer="./le_rayon_carre_des_daleks/entree.csv", delimiter=",", names=["x", "y", "largeur","hauteur"])

    data.iloc[:, 0] = data.iloc[:, 0] + 1000
    data.iloc[:, 1] = data.iloc[:, 1] + 1000
    # create blank image (canvas)
    image = Image.new('RGB', (2000, 2000), 'white')
    # create a drawing object
    drawing_object = ImageDraw.Draw(image)
    # draw rectangles
    for rect in data.itertuples():
        x = rect.x - (rect.largeur / 2)
        y = rect.y - (rect.largeur / 2)
        x1 = rect.x + (rect.largeur / 2)
        y1 = rect.y + (rect.largeur / 2)
        drawing_object.rectangle( (x, y, x1, y1), fill=(0, 255, 0), outline=None)

    image.save(fp="./le_rayon_carre_des_daleks/image_vert_perso.png")
    surface = 0
    for x in range(image.width):
        for y in range(image.height):
            couleur = image.getpixel((x, y))
            if couleur == (0, 255, 0):
                surface += 1

    print(f"Résultat = {surface}")


def la_paranoia_de_calot() -> None:
    """https://pydefis.callicode.fr/defis/ParanoiaCalot/txt"""
    def decode(x: str, i: int) -> str:
        """_summary_
        Args:
            x (str): character to be decrypted
            i (int): shift value
        Returns:
            str: decrypted character
        """
        line = 0
        position = -1
        decyphered = ""
        while decyphered == "":
            if x in clavier[line]:
                position = clavier[line].index(x)
            if position > -1:
                new_pos = (position + i) % 10
                decyphered = clavier[line][new_pos]
            line += 1

        return decyphered

    def browse_text(i: int) -> str:
        """Browse texte
        Args:
            i (int): shift value
        Returns:
            str: decrypted text
        """
        decyphered_text = ""
        for x in texte:
            if x != "\n":
                decyphered_text += decode(x, i)
            else:
                decyphered_text += "\n"

        return decyphered_text


    clavier = [
        ["a", "z", "e", "r", "t", "y", "u", "i", "o", "p"],
        ["q", "s", "d", "f", "g", "h", "j", "k", "l", "m"],
        ["w", "x", "c", "v", "b", "n", ",", ";", ":", "!"],
    ]
    with open(file="./la_paranoia_de_calot/texte.txt", mode="r", encoding="utf-8") as f:
        texte = f.read()


    for i in range(-9, 10):
        print(f"i={i}")
        print(browse_text(i))



if __name__ == "__main__":
    la_paranoia_de_calot()
