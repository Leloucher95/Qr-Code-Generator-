import qrcodedef
import scan
import os

print("Bienvenue !")
choix = int(input("Souhaiter vous : \n 1-Creer un code qr?  \n 2-Scanner un code qr?  \n 3-Quitter \n"))

while (choix > 0 or choix < 4)  :
    if choix == 1 :
        contenue = input("Quel est le contenue du qrcode ?")
        titre = input("Quel est le titre du projet. Veillez a ajouter lextension .png ?")
        qrcodedef.generate_qr_code(contenue,titre)

        #choix = int(input("Souhaiter vous : \n 1-Creer un code qr? \n 2-Scanner un code qr? \n 3-Quitter \n"))
    elif choix == 2 :
        scan.main()
        #choix = int(input("Souhaiter vous : \n 1-Creer un code qr? \n 2-Scanner un code qr? \n 3-Quitter \n"))
    else :
        print("Aurevoir")
        break
        #image_path = input("Entrer le chemin d'acces vers le qrcode.")
        #scan.scan_qr_code(image_path)

    choix = int(input("Souhaiter vous : \n 1-Creer un code qr? \n 2-Scanner un code qr? \n 3-Quitter \n"))

os.system('pause')