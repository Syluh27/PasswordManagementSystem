import sqlite3
from encryption import encrypt_password, decrypt_password


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
    print("Contraseña guardada exitosamente.")


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
    else:
        return None


def listar_contraseñas():
    """Muestra todos los sitios y usuarios almacenados."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("SELECT sitio, usuario FROM passwords")
    resultados = cursor.fetchall()
    conn.close()

    if resultados:
        print("\n--- Contraseñas Guardadas ---")
        for sitio, usuario in resultados:
            print(f"Sitio: {sitio}, Usuario: {usuario}")
    else:
        print("No hay contraseñas almacenadas.")


def eliminar_contraseña(sitio, usuario):
    """Elimina una contraseña específica de la base de datos."""
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE sitio=? AND usuario=?", (sitio, usuario))
    conn.commit()
    conn.close()
    print("Contraseña eliminada exitosamente.")


def menu():
    """Interfaz de línea de comandos para gestionar contraseñas."""
    while True:
        print("\n--- Gestor de Contraseñas ---")
        print("1. Guardar una nueva contraseña")
        print("2. Recuperar una contraseña")
        print("3. Listar todas las contraseñas")
        print("4. Eliminar una contraseña")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            sitio = input("Ingrese el sitio web: ")
            usuario = input("Ingrese el nombre de usuario: ")
            contraseña = input("Ingrese la contraseña: ")
            guardar_contraseña(sitio, usuario, contraseña)
        elif opcion == "2":
            sitio = input("Ingrese el sitio web: ")
            usuario = input("Ingrese el nombre de usuario: ")
            contraseña = obtener_contraseña(sitio, usuario)
            if contraseña:
                print(f"Contraseña recuperada: {contraseña}")
            else:
                print("No se encontró una contraseña para esos datos.")
        elif opcion == "3":
            listar_contraseñas()
        elif opcion == "4":
            sitio = input("Ingrese el sitio web: ")
            usuario = input("Ingrese el nombre de usuario: ")
            eliminar_contraseña(sitio, usuario)
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente de nuevo.")


if __name__ == "__main__":
    init_db()
    menu()
