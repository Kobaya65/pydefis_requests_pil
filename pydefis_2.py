"""Challenges from https://pydefis.callicode.fr Part 2
"""
import random
from time import sleep
from zipfile import ZipFile
from glob import glob
import unidecode

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

def gestion_espace_temps_par_le_tardis() -> None:
    """https://pydefis.callicode.fr/defis/C23_TardisFirmware10/txt"""
    img = Image.open('./gestion_espace_temps_par_le_tardis/tardis_machine_02.png')
    pile = []
    nombres = []
    annee = 0
    for y in range(0, img.height, 20):
        for x in range(0, img.width, 20):
            r, g, b = img.getpixel((x, y))
            if r == 0 and g == 0 and b == 0:
                print("Rien à faire...")
            elif g == 0 and b == 0 and r > 0:
                pile.append(r)
            elif r == 0 and g == 0 and b in [230, 240]:
                un = pile.pop()
                deux = pile.pop()
                if b == 230:
                    pile.append((un + deux) % 256)
                elif b == 240:
                    pile.append((un * deux) % 256)
                else:
                    print("b != 230 et 230")
            elif r == 200 and g == 200 and b == 200:
                nombres.append(pile[len(pile) - 1])
                if len(nombres) == 2:
                    annee += (256 * nombres[0] + nombres[1] - 10000)
                    nombres.clear()
            else:
                print("combinaison inconnue !")

    print(f"annee = {annee}")
            

def un_message_des_etoiles() -> None:
    """https://pydefis.callicode.fr/defis/C25_SkyMap01/txt"""
    my_zip_file = "./un_message_des_etoiles_1/telescope01.zip"
    destination_folder = "./un_message_des_etoiles_1"
    
    with ZipFile(my_zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)

    # create a new blank image
    img_result = Image.new(mode="RGB", size=(800, 800))
    pixels_result = img_result.load()

    fichiers = glob("./un_message_des_etoiles_1/telescope_img_*.png")
    lon = len(fichiers)

    # first image set as reference
    image_ref = Image.open(fichiers[0]) 
    tab_ref = list(image_ref.getdata())

    nb_pixels_diffents = 0
    for i in range(1, lon):
        print(f"image {i}")
        img = Image.open(fichiers[i])
        tab_i = list(img.getdata())

        if tab_ref != tab_i:
            for idx in range(640000):
                if tab_ref[idx] != tab_i[idx]:
                    y = idx % 800
                    x = idx // 800
                    pixels_result[x, y] = (255, 255, 255)
                    nb_pixels_diffents += 1

        img.close()

    image_ref.close()

    print(f"Nombre de pixeles différents : {nb_pixels_diffents}")
    img_result.save("./un_message_des_etoiles_1/img_result.png")
    img_result.show()
    img_result.close()


def sw_v_le_message_chiffre_de_vader() -> None:
    """https://pydefis.callicode.fr/defis/ChiffreVader/txt"""
    def letter_to_figure(lettre: str) -> int:
        if lettre == "_":
            val = 26
        else:
            val = ord(lettre) - 65
        return val

    def figure_to_letter(chiffre: int) -> str:
        if chiffre == 26:
            ret = "_"
        else:
            ret = chr(chiffre + 65)
        return ret

    def to_figures(texte: str) -> list[int]:
        longeur = len(texte) - 1
        liste_chiffres = []
        for i in range(0, longeur, 2):
            x = texte[i]
            y = texte[i + 1]
            liste_chiffres.append(letter_to_figure(x))
            liste_chiffres.append(letter_to_figure(y))

        return liste_chiffres

    def transform_figures(coeff: tuple[int], liste_chiffres: list[int]) -> list[str]:
        a, b, c, d = coeff
        liste_codee = []
        for idx in range(0, len(liste_chiffres), 2):
            x = liste_chiffres[idx]
            y = liste_chiffres[idx + 1]

            liste_codee.append((a * x + b * y) % 27)
            liste_codee.append((c * x + d * y) % 27)

        result = []
        for x in liste_codee:
            result.append(figure_to_letter(x))

        return result

    entree = "MPLCCFOMNFXGUDOUG_CFED_ANFXPHGLXB_HTOSYKG_KRMWG_PUXJMWCFQAUMZP_WIAKERYWXQQJZREZPWMWKSUOSYKOMNFLXIPASBW_NPIEP_EJDBW "

    result = to_figures(entree)
    for a in range(-20, 21):
        for b in range(-20, 21):
            for c in range(-20, 21):
                for d in range(-20, 21):
                    resultat = "".join(transform_figures((a, b, c, d), result))
                    if "VADER" in resultat:
                        print(resultat)


def sa_legende_est_son_anagramme_2() -> None:
    """https://pydefis.callicode.fr/defis/NomAnagramme1/txt"""
    with open(file="./sa_legende_est_son_anagramme_2/texte.txt", mode="r", encoding="utf-8") as f:
        noms = f.readlines()

    dico_resultat = {}

    for n in noms:
        nom_cleaned = n[:-1]
        # get rid of accent and final newline
        nom = unidecode.unidecode(nom_cleaned)
        # get rid of spaces
        nom = nom.replace(" ", "").lower()
        nom = sorted(nom)
        compil = "".join(nom)
        if dico_resultat.get(compil):
            liste_noms = dico_resultat[compil]["nom"]
            liste_noms.append(nom_cleaned)
            dico_resultat[compil] = {
                "nom": liste_noms,
                "nb_légendes": int(dico_resultat[compil]["nb_légendes"]) + 1
            }
        else:
            dico_resultat[compil] = {
                "nom": [nom_cleaned],
                "nb_légendes": 1
            }

    # sort dico by its values
    dico_resultat = dict(sorted(dico_resultat.items(), key=lambda x: x[1]["nb_légendes"], reverse=True))

    # first_value = next(iter(my_dict.values()))
    for x in dico_resultat:
        print(dico_resultat[x]["nb_légendes"], dico_resultat[x]["nom"])


def sw_v_joue_avec_yoda() -> None:
    """https://pydefis.callicode.fr/defis/JeuYoda/txt
    20250808 : non résolu
    """
    entree = "sassai eaux-de-vie cessaient acerbité eaux sceau tiendra hasard acéphale auxiliairement vesce eurafricaine hâtai saignant entachassent alentie césar vieillerie messéant taillable ives testacé dracéna ardentes ensablant blessas entachasses ioniens antarctique sessiles ineffaçables quercitrine besace lessivasses acerbes descellaient entachas lessive gestation lessivâtes antécédentes énamourâmes antécédent entachât inefficace testacelles sarabandes entachant rieur itérâmes antécédences messages sesquioxydes testacés"

    liste_mots = entree.split()
    nb_mots = len(liste_mots)
    mots_tries = []
    while len(mots_tries) != nb_mots:
        idx_init = 0
        copie_mots = liste_mots.copy()
        mot = copie_mots[idx_init]
        print(f"{idx_init / nb_mots:0.1%} {mot}")
        mots_tries = []
        while len(copie_mots):
            mot = copie_mots[idx_init]
            copie_mots.remove(mot)

            mots_tries.append(mot)
            fin = mot[-3:]
            idx_copie = 0
            try:
                while len(mots_tries) < nb_mots:
                    debut = copie_mots[idx_copie][:3]
                    if debut == fin:
                        mots_tries.append(copie_mots[idx_copie])
                        # new end of word to search for
                        fin = copie_mots[idx_copie][-3:]
                        copie_mots.remove(copie_mots[idx_copie])
                        idx_copie = 0
                    else:
                        idx_copie += 1
            except IndexError:
                idx_init += 1
                break
    
    liste = ""
    for x in mots_tries:
        liste += f"\"{x}\", "

    liste = liste[:-2]
    print(liste)

def sw_iv_il_a_mis_son_mot_de_passe_sur_un_post_it() -> None:
    """https://pydefis.callicode.fr/defis/LunetteAstro/txt"""
    x1 = 1694
    y1 = 1546
    nb_iterations = 50

    while nb_iterations:
        x = (x1      + 2 * y1) % 2018
        y = (-3 * x1 +     y1) % 2018

        x1 = x
        y1 = y

        nb_iterations -= 1

    declinaison = (x - 900)  / 10
    ascension_droite = (y / 150) * 2

    print(f"Déclinaison      : {declinaison}")
    print(f"Ascension droite : {ascension_droite}")


if __name__ == "__main__":
    sw_iv_il_a_mis_son_mot_de_passe_sur_un_post_it()
