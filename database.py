import sqlite3
import csv
from encryption import encrypt_password, decrypt_password
import bcrypt


def init_config():
    """Crea la tabla de configuración y almacena la contraseña maestra si no existe."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clave_maestra TEXT NOT NULL
        )
    ''')

    cursor.execute("SELECT clave_maestra FROM config LIMIT 1")
    if not cursor.fetchone():
        clave_maestra = "123"  # 🔹 Cambia aquí tu contraseña maestra
        clave_cifrada = bcrypt.hashpw(clave_maestra.encode(), bcrypt.gensalt())
        cursor.execute("INSERT INTO config (clave_maestra) VALUES (?)", (clave_cifrada,))

    conn.commit()
    conn.close()


def verificar_clave_maestra(clave_ingresada):
    """Verifica si la contraseña maestra ingresada es correcta."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()

    cursor.execute("SELECT clave_maestra FROM config LIMIT 1")
    resultado = cursor.fetchone()
    conn.close()

    if resultado and bcrypt.checkpw(clave_ingresada.encode(), resultado[0]):
        return True
    return False


def init_db():
    """Crea la base de datos y la tabla si no existen."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sitio TEXT NOT NULL,
            usuario TEXT NOT NULL,
            contraseña_cifrada TEXT NOT NULL,
            iv TEXT NOT NULL,
            tag TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def guardar_contraseña(sitio, usuario, contraseña):
    """Cifra y almacena la contraseña en la base de datos."""
    iv, contraseña_cifrada, tag = encrypt_password(contraseña)
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO passwords (sitio, usuario, contraseña_cifrada, iv, tag) VALUES (?, ?, ?, ?, ?)",
                   (sitio, usuario, contraseña_cifrada, iv, tag))
    conn.commit()
    conn.close()
    print("✅ Contraseña guardada exitosamente.")


def obtener_contraseña(sitio, usuario):
    """Recupera y descifra la contraseña almacenada."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT contraseña_cifrada, iv, tag FROM passwords WHERE sitio=? AND usuario=?", (sitio, usuario))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        contraseña_cifrada, iv, tag = resultado
        return decrypt_password(contraseña_cifrada, iv, tag)
    return None


import sqlite3

def eliminar_contraseña(sitio, usuario):
    conn = sqlite3.connect("contraseñas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contraseñas WHERE sitio = ? AND usuario = ?", (sitio, usuario))
    conn.commit()
    conn.close()
def listar_contraseñas():
    """Lista todas las contraseñas almacenadas en la base de datos."""
    try:
        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute("SELECT sitio, usuario FROM passwords")  # Verifica que la tabla se llame 'passwords'
        contraseñas = cursor.fetchall()
        conn.close()

        return contraseñas  # Asegura que siempre devuelva una lista

    except Exception as e:
        print(f"Error al listar contraseñas: {e}")
        return []


def eliminar_contraseña(sitio, usuario):
    """Elimina una contraseña específica de la base de datos."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE sitio=? AND usuario=?", (sitio, usuario))
    conn.commit()
    conn.close()
    print("✅ Contraseña eliminada exitosamente.")


def exportar_contraseñas():
    """Exporta todas las contraseñas a un archivo CSV."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT sitio, usuario, contraseña_cifrada, iv, tag FROM passwords")
    resultados = cursor.fetchall()
    conn.close()

    with open("contraseñas_backup.csv", "w", newline="") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Sitio", "Usuario", "Contraseña Cifrada", "IV", "Tag"])
        escritor.writerows(resultados)
    print("✅ Contraseñas exportadas exitosamente a 'contraseñas_backup.csv'.")


def importar_contraseñas():
    """Importa contraseñas desde un archivo CSV."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()

    with open("contraseñas_backup.csv", "r") as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltar la cabecera
        for sitio, usuario, contraseña_cifrada, iv, tag in lector:
            cursor.execute("INSERT INTO passwords (sitio, usuario, contraseña_cifrada, iv, tag) VALUES (?, ?, ?, ?, ?)",
                           (sitio, usuario, contraseña_cifrada, iv, tag))

    conn.commit()
    conn.close()
    print("✅ Contraseñas importadas exitosamente desde 'contraseñas_backup.csv'.")


def menu():
    """Interfaz de línea de comandos para gestionar contraseñas."""
    clave_ingresada = input("\n🔑 Ingrese la contraseña maestra: ")
    if not verificar_clave_maestra(clave_ingresada):
        print("❌ Contraseña incorrecta. Saliendo...")
        return

    while True:
        print("\n--- 🔐 GESTOR DE CONTRASEÑAS 🔐 ---")
        print("1️⃣ Guardar una nueva contraseña")
        print("2️⃣ Recuperar una contraseña")
        print("3️⃣ Listar todas las contraseñas")
        print("4️⃣ Eliminar una contraseña")
        print("5️⃣ Exportar contraseñas a CSV")
        print("6️⃣ Importar contraseñas desde CSV")
        print("7️⃣ Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            sitio = input("🔹 Ingrese el sitio web: ")
            usuario = input("👤 Ingrese el nombre de usuario: ")
            contraseña = input("🔑 Ingrese la contraseña: ")
            guardar_contraseña(sitio, usuario, contraseña)
        elif opcion == "2":
            sitio = input("🔹 Ingrese el sitio web: ")
            usuario = input("👤 Ingrese el nombre de usuario: ")
            contraseña = obtener_contraseña(sitio, usuario)
            if contraseña:
                print(f"✅ Contraseña recuperada: {contraseña}")
            else:
                print("⚠️ No se encontró una contraseña para esos datos.")
        elif opcion == "3":
            listar_contraseñas()
        elif opcion == "4":
            sitio = input("🔹 Ingrese el sitio web: ")
            usuario = input("👤 Ingrese el nombre de usuario: ")
            eliminar_contraseña(sitio, usuario)
        elif opcion == "5":
            exportar_contraseñas()
        elif opcion == "6":
            importar_contraseñas()
        elif opcion == "7":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("⚠️ Opción no válida, intente de nuevo.")


if __name__ == "__main__":
    init_db()
    init_config()
    menu()
