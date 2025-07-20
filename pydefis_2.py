"""Challenges from https://pydefis.callicode.fr Part 2
"""
import random
from time import sleep

import requests
from PIL import Image


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

        return minimums(profondeurs, prof_min)

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


if __name__ == "__main__":
    compter_les_etoiles_chaudes()
