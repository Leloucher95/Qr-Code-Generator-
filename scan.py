import cv2
from pyzbar.pyzbar import decode
import webbrowser





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
        if len(decoded_objects) > 0:
            break


    # Libérer les ressources
    cap.release()
    cv2.destroyAllWindows()
    print("Merci")




# Fonction pour scanner les QR codes dans une image
    data=""
def scan_qr_code_image(image_path):
    # Charger l'image
    image = cv2.imread(image_path)

    # Convertir l'image en niveaux de gris
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Décoder les QR codes
    decoded_objects = decode(gray_image)

    # Afficher les résultats
    #for obj in decoded_objects:
     #   print(f"Type: {obj.type}, Data: {obj.data.decode('utf-8')}")

    for obj in decoded_objects:
        qr_data = obj.data.decode('utf-8')
        print(f"Type: {obj.type}, Data: {qr_data}")
        data=qr_data


        # Vérifier si c'est un lien
        if obj.type == "QRCODE" and qr_data.startswith("http"):
            # Ouvrir le lien dans le navigateur par défaut
            webbrowser.open(qr_data)
            print(f"Le lien a été ouvert dans votre navigateur.")

        # Dessiner un rectangle autour du QR code
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(points, returnPoints=False)
            for i in range(len(hull)):
                cv2.line(image, tuple(hull[i][0]), tuple(hull[(i+1) % len(hull)][0]), (0, 255, 0), 3)

    # Afficher l'image avec les rectangles entourant les QR codes
    cv2.imshow("QR Code Scanner", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Merci")
    return data

# Fonction principale pour choisir entre scanner avec la caméra ou une image
def main():
    user_choice = input("Choisissez 'c' pour scanner avec la caméra ou 'i' pour scanner une image : ")

    if user_choice.lower() == 'c':
        scan_qr_code_camera()
    elif user_choice.lower() == 'i':
        image_path = input("Entrez le chemin de l'image contenant le QR code : ")
        scan_qr_code_image(image_path)
    else:
        print("Choix invalide. Veuillez choisir 'c' ou 'i'.")

#if __name__ == "__main__":
#main()
# Exemple d'utilisation avec une image contenant un QR code
#image_path = "gilcia.png"
#scan_qr_code(image_path)
