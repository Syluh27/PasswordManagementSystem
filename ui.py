import tkinter as tk
from tkinter import ttk, messagebox
from database import guardar_contraseña, obtener_contraseña, listar_contraseñas, eliminar_contraseña

# Contraseña maestra
MASTER_PASSWORD = "admin123"  # Cambia esta contraseña según tus necesidades


def verificar_contraseña_maestra():
    """Función para verificar la contraseña maestra."""
    entrada = entry_maestra.get()
    if entrada == MASTER_PASSWORD:
        ventana_maestra.destroy()  # Cierra la ventana de contraseña maestra
        iniciar_sistema()  # Llama a la función para iniciar el sistema principal
    else:
        messagebox.showerror("Acceso denegado", "Contraseña maestra incorrecta.")


def iniciar_sistema():
    """Función principal del gestor de contraseñas."""
    def eliminar():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showwarning("Error", "Selecciona una fila para eliminar.")
            return

        # Obtener los valores de la fila seleccionada
        item = tree.item(seleccionado)
        sitio, usuario = item["values"]

        # Confirmar la eliminación
        confirmar = messagebox.askyesno("Confirmar eliminación",
                                        f"¿Deseas eliminar la contraseña para {sitio} - {usuario}?")
        if confirmar:
            eliminar_contraseña(sitio, usuario)
            actualizar_lista()
            messagebox.showinfo("Éxito", "Contraseña eliminada exitosamente")

    def guardar():
        sitio = entry_sitio.get()
        usuario = entry_usuario.get()
        contrasena = entry_contraseña.get()
        if sitio and usuario and contrasena:
            guardar_contraseña(sitio, usuario, contrasena)
            messagebox.showinfo("Éxito", "Contraseña guardada exitosamente")
            entry_sitio.delete(0, tk.END)
            entry_usuario.delete(0, tk.END)
            entry_contraseña.delete(0, tk.END)
            actualizar_lista()
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

    def actualizar_lista():
        contraseñas = listar_contraseñas()
        for row in tree.get_children():
            tree.delete(row)
        for sitio, usuario in contraseñas:
            tree.insert("", "end", values=(sitio, usuario))

    # Configuración de la ventana principal
    root = tk.Tk()
    root.title("Gestor de Contraseñas")
    root.geometry("500x450")
    root.resizable(False, False)

    # Marco principal
    frame = ttk.Frame(root, padding=10)
    frame.pack(expand=True, fill="both")

    # Etiquetas y entradas
    ttk.Label(frame, text="Sitio:").grid(row=0, column=0, sticky="w")
    entry_sitio = ttk.Entry(frame, width=30)
    entry_sitio.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Usuario:").grid(row=1, column=0, sticky="w")
    entry_usuario = ttk.Entry(frame, width=30)
    entry_usuario.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Contraseña:").grid(row=2, column=0, sticky="w")
    entry_contraseña = ttk.Entry(frame, width=30, show="*")
    entry_contraseña.grid(row=2, column=1, padx=5, pady=5)

    # Botones
    ttk.Button(frame, text="Guardar", command=guardar).grid(row=3, column=0, columnspan=2, pady=10)
    ttk.Button(frame, text="Recuperar", command=recuperar).grid(row=4, column=0, columnspan=2, pady=5)
    ttk.Button(frame, text="Eliminar", command=eliminar).grid(row=6, column=0, columnspan=2, pady=5)

    # Tabla para visualizar contraseñas
    tree = ttk.Treeview(frame, columns=("Sitio", "Usuario"), show="headings", height=5)
    tree.heading("Sitio", text="Sitio")
    tree.heading("Usuario", text="Usuario")
    tree.column("Sitio", width=200)
    tree.column("Usuario", width=150)
    tree.grid(row=5, column=0, columnspan=2, pady=10)

    # Barra de estado
    status_bar = ttk.Label(root, text="Gestor de Contraseñas - Seguridad Primero 🔐", relief="sunken", anchor="center")
    status_bar.pack(side="bottom", fill="x")

    # Cargar datos en la tabla al iniciar
    actualizar_lista()

    root.mainloop()


# Ventana de inicio para la contraseña maestra
ventana_maestra = tk.Tk()
ventana_maestra.title("Acceso al Gestor de Contraseñas")
ventana_maestra.geometry("400x200")
ventana_maestra.resizable(False, False)

ttk.Label(ventana_maestra, text="Ingrese la contraseña maestra:", font=("Arial", 12)).pack(pady=20)
entry_maestra = ttk.Entry(ventana_maestra, width=30, show="*")
entry_maestra.pack(pady=5)

ttk.Button(ventana_maestra, text="Ingresar", command=verificar_contraseña_maestra).pack(pady=10)

ventana_maestra.mainloop()
