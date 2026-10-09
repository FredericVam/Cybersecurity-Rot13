import winreg
import codecs

def get_userassist_data():
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                 r"Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist")
        
        subkeys = []
        i = 0
        while True:
            try:
                subkey = winreg.EnumKey(reg_key, i)
                subkeys.append(subkey)
                i += 1
            except OSError:
                break

        with open('userassist.txt', 'w', encoding='utf-8') as file:
            for subkey in subkeys:
                try:
                    subkey_path = f"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist\\{subkey}\\Count"
                    subkey_handle = winreg.OpenKey(winreg.HKEY_CURRENT_USER, subkey_path)
                    value_count = winreg.QueryInfoKey(subkey_handle)[1]

                    for j in range(value_count):
                        value_name, value_data, _ = winreg.EnumValue(subkey_handle, j)
                        file.write(f"{value_name}: {value_data}\n")

                except FileNotFoundError:
                    continue
                except Exception as e:
                    print(f"Erreur lors de la récupération de la clé {subkey}: {e}")
        print("Les données de UserAssist ont été extraites et enregistrées dans userassist.txt.")
    except Exception as e:
        print(f"Erreur lors de l'accès au registre: {e}")


def rot13(text):
    """
    Fonction pour appliquer l'algorithme ROT13 au texte donné.
    """
    return codecs.encode(text, 'rot_13')

def decode_userassist():
    """
    Lit les valeurs de userassist.txt, les décode avec ROT13, puis les écrit dans decode_userassist.txt.
    """
    try:
        with open('userassist.txt', 'r') as infile:
            data = infile.readlines()

        with open('decode_userassist.txt', 'w') as outfile:
            for line in data:
        # on applique ROT13 sur chaque ligne (en ignorant les lignes vides)
                decoded_line = rot13(line.strip())
                outfile.write(f"{decoded_line}\n")

        print("Le fichier userassist.txt a été décodé et enregistré dans decode_userassist.txt.")
    except FileNotFoundError:
        print("Le fichier userassist.txt n'a pas été trouvé.")
    except Exception as e:
        print(f"Erreur lors du décodage du fichier: {e}")

# Exemple d'exécution du programme
if __name__ == "__main__":
    # on récupère les données de UserAssist et on les enregistrer dans un fichier
    get_userassist_data()

    # on décode le fichier userassist.txt et on écrit les résultats dans decode_userassist.txt
    decode_userassist()
