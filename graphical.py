import cv2
from pyzbar.pyzbar import decode
import webbrowser
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import qrcodedef
from scan import *
#_________________

app = tk.Tk()
app.geometry("500x320")


# Fonctions pour générer le code QR

def generate_qr_code():
    global contenu_var, titre_var
    contenu_var = tk.StringVar()
    titre_var = tk.StringVar()

    generate_button.destroy() #Pour suppprimer les anciens widgets
    scan_button.destroy()


    # Contenu
    tk.Label(app, text="Quel est le contenu du qrcode ? (texte ou lien)").pack()
    tk.Entry(app, textvariable=contenu_var).pack()

    # Titre
    tk.Label(app, text="Quel est le titre du qrcode ?").pack()
    tk.Entry(app, textvariable=titre_var).pack()

    # Bouton de validation
    tk.Button(app, text="Valider", command=generate).pack()

def generate():
    contenu = contenu_var.get()
    titre = titre_var.get() + ".png" #l'extension sera .png
    output_folder = filedialog.askdirectory()
    qrcodedef.generate_qr_code(contenu, titre, output_folder)
    messagebox.showinfo("Information", "Votre code QR a été généré dans :{}".format(output_folder))
    app.quit()

#________________________________________________________________________________________________________

def ask_path (): #sélection de l'image
    global output, data
    app.withdraw() #masuqe la fenetre
    while True:
        output=filedialog.askopenfilename(filetypes=[("Fichiers PNG", "*.png")])
        if output :
            if output.endswith('.png'): #test l'extension du fichier
                result=tk.StringVar()
                show_result=tk.Label(app, textvariable=result)
                data=scan_qr_code_image(output)
                result.set("Le contenu du code qr est: \n{} ".format(data))
                show_result.pack()

                copy_result=tk.Button(app, text="Copier le contenu du code QR", command=app.clipboard_append(data)).pack(pady=7)
                break
            else:
                messagebox.showerror("Erreur" ,"L'image doit etre au format png (.png)")
        else :
            break


    app.deiconify() #rend visible la fenetre





def scan ():
    global ask_path_button, label_scan_image,camera_button_proceed

    generate_button.destroy()
    scan_button.destroy()

    label_scan_image=tk.Label(app, text="Veuillez choisir l'image contenant le code QR à scanner.").pack()
    ask_path_button=tk.Button(app, text="Sélectionner une image", command=ask_path).pack()


    camera_button_proceed=tk.Button(app, text="Scanner en utilisant la caméra", command=scan_qr_code_camera).pack(pady=20)





# Fonction pour scanner les QR codes depuis la caméra et ouvrir les liens
def scan_qr_code_camera():
    cap = cv2.VideoCapture(0)  # Ouvrir la caméra

    while True:
        ret, frame = cap.read()  # Lire un frame de la caméra

        # Convertir le frame en niveaux de gris
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Décoder les QR codes
        decoded_objects = decode(gray_frame)

        # Afficher les résultats
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            print(f"Type: {obj.type}, Data: {qr_data}")

            # Vérifier si c'est un lien
            if obj.type == "QRCODE" and qr_data.startswith("http"):
                # Ouvrir le lien dans le navigateur par défaut
                webbrowser.open(qr_data)
                print(f"Le lien a été ouvert dans votre navigateur.")





        # Afficher le frame avec les rectangles entourant les QR codes
        cv2.imshow("QR Code Scanner", frame)

        # Sortir de la boucle si la touche 'q' est pressée
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Sortir de la boucle while si tous les QR codes ont été scannés
        #Afficher le contenu du code à l'écran
        if len(decoded_objects) > 0:
            result_txt=tk.StringVar()
            result=tk.Label(app, textvariable=result_txt).pack(pady=5)
            result_txt.set("Le contenu de votre code QR est le suivant: \n {}".format(qr_data))

            copy_result=tk.Button(app, text="Copier le contenu du code QR", command=app.clipboard_append(qr_data)).pack(pady=7)
            break

    # Libérer les ressources
    cap.release()
    cv2.destroyAllWindows()
    print("Merci")



global generate_button
# Bouton pour générer un code QR
generate_button = tk.Button(app, text="Générer un code QR", command=generate_qr_code)
generate_button.pack()

# Bouton pour scanner un code QR
scan_button = tk.Button(app, text="Scanner un code QR", command=scan)
scan_button.pack(pady=20)





app.mainloop()
