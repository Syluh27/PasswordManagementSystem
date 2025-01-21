import tkinter as tk
from tkinter import messagebox, simpledialog  # Importar simpledialog correctamente
from database import guardar_contraseña, obtener_contraseña, exportar_contraseñas, importar_contraseñas

def guardar():
    sitio = entry_sitio.get()
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    if sitio and usuario and contrasena:
        guardar_contraseña(sitio, usuario, contrasena)
        messagebox.showinfo("Éxito", "Contraseña guardada exitosamente")
        entry_sitio.delete(0, tk.END)
        entry_usuario.delete(0, tk.END)
        entry_contrasena.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "Todos los campos son obligatorios")

def recuperar():
    sitio = entry_sitio.get()
    usuario = entry_usuario.get()
    if sitio and usuario:
        contrasena = obtener_contraseña(sitio, usuario)
        if contrasena:
            messagebox.showinfo("Contraseña Recuperada", f"Contraseña: {contrasena}")
        else:
            messagebox.showwarning("Error", "No se encontró la contraseña")
    else:
        messagebox.showwarning("Error", "Debes ingresar el sitio y usuario")

def exportar():
    exportar_contraseñas()
    messagebox.showinfo("Éxito", "Contraseñas exportadas correctamente")

def importar():
    importar_contraseñas()
    messagebox.showinfo("Éxito", "Contraseñas importadas correctamente")
# Definir la contraseña maestra
MASTER_PASSWORD = "123"  # Cambia esto por tu contraseña segura

def verificar_maestra():
    """Solicita la contraseña maestra antes de acceder a la aplicación."""
    entrada = tk.simpledialog.askstring("Contraseña Maestra", "Ingrese la contraseña maestra:", show="*")
    if entrada != MASTER_PASSWORD:
        messagebox.showerror("Acceso Denegado", "Contraseña incorrecta. Cerrando aplicación.")
        root.destroy()  # Cierra la aplicación si la contraseña es incorrecta

# Crear ventana principal
root = tk.Tk()
root.withdraw()  # Oculta la ventana hasta que se ingrese la contraseña maestra

verificar_maestra()  # Pide la contraseña maestra antes de mostrar la ventana

root.deiconify()  # Muestra la ventana si la contraseña es correcta
root.title("Gestor de Contraseñas")
root.geometry("400x300")

# Etiquetas y entradas
tk.Label(root, text="Sitio:").pack()
entry_sitio = tk.Entry(root)
entry_sitio.pack()

tk.Label(root, text="Usuario:").pack()
entry_usuario = tk.Entry(root)
entry_usuario.pack()

tk.Label(root, text="Contraseña:").pack()
entry_contrasena = tk.Entry(root, show="*")
entry_contrasena.pack()

# Botones
tk.Button(root, text="Guardar", command=guardar).pack()
tk.Button(root, text="Recuperar", command=recuperar).pack()
tk.Button(root, text="Exportar CSV", command=exportar).pack()
tk.Button(root, text="Importar CSV", command=importar).pack()

# Iniciar bucle de Tkinter
root.mainloop()
