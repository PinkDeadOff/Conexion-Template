import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import pyodbc

# Create the application
app = tk.Tk()
app.geometry("850x400")
app.title("Mi Template")
app.config(bg="#314252")
app.resizable(0, 0)

# Bypass para validaciones
def bypass():
    pass

# Version control
def version():
    messagebox.showinfo("Version", "V 1.0.0.1 \\ Created by Yair Carvajal")
    


# Establish Connection functionality
def establish_connection():
    def connect_to_sql_server():
        project_name = project_combobox.get()
        
        # Conexión a la base de datos SQLite
        conn_sqlite = sqlite3.connect(r"C:\Users\gdlycarv\Desktop\Juniper- Move to Production\DB\DB_Conection.db")
        cursor_sqlite = conn_sqlite.cursor()
        
        cursor_sqlite.execute("SELECT Server, DataBase, User, Password FROM Connection WHERE Project = ?", (project_name,))
        result = cursor_sqlite.fetchone()
        
        if result:
            server, database, user, password = result
            try:
                # Conexión a SQL Server
                conn_sql_server = pyodbc.connect(
                    f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password}'
                )
                messagebox.showinfo("Success", f"Connected to SQL Server database '{database}'")
            except Exception as e:
                messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
        else:
            messagebox.showerror("Error", "Project not found.")
        
        conn_sqlite.close()

    # Crear ventana de conexión
    connection_window = tk.Toplevel(app)
    connection_window.title("Link Connection")
    connection_window.geometry("200x200")
    connection_window.resizable(0, 0)
    
    tk.Label(connection_window, text="Select Project").pack(pady=10)
    
    # Obtener lista de proyectos desde SQLite
    conn_sqlite = sqlite3.connect(r"C:\Users\gdlycarv\Desktop\Juniper- Move to Production\DB\DB_Conection.db")
    cursor_sqlite = conn_sqlite.cursor()
    cursor_sqlite.execute("SELECT Project FROM Connection")
    projects = [row[0] for row in cursor_sqlite.fetchall()]
    conn_sqlite.close()

    # Combobox para seleccionar el proyecto
    project_combobox = ttk.Combobox(connection_window, values=projects)
    project_combobox.pack(pady=5)
    
    # Botón de habilitar conexión
    tk.Button(connection_window, text="Enable", command=connect_to_sql_server).pack(pady=5)
    # Botón de cancelar
    tk.Button(connection_window, text="Cancel", command=connection_window.destroy).pack(pady=5)

# New Connection functionality
def new_connection():
    def add_connection():
        project = entry_project.get()
        server = entry_server.get()
        database = entry_database.get()
        user = entry_user.get()
        password = entry_password.get()

        conn_sqlite = sqlite3.connect(r"C:\Users\gdlycarv\Desktop\Juniper- Move to Production\DB\DB_Conection.db")
        cursor_sqlite = conn_sqlite.cursor()

        # Validación de existencia del proyecto
        cursor_sqlite.execute("SELECT Project FROM Connection WHERE Project = ?", (project,))
        if cursor_sqlite.fetchone():
            messagebox.showerror("Error", "Project already exists.")
        else:
            cursor_sqlite.execute("INSERT INTO Connection (Project, Server, DataBase, User, Password) VALUES (?, ?, ?, ?, ?)",
                                  (project, server, database, user, password))
            conn_sqlite.commit()
            messagebox.showinfo("Success", "New connection added.")
        
        conn_sqlite.close()
        new_conn_window.destroy()

    # Crear ventana para nueva conexión
    new_conn_window = tk.Toplevel(app)
    new_conn_window.title("New Connection")
    new_conn_window.geometry("600x400")
    new_conn_window.resizable(0, 0)

    # Campos para ingresar los datos de la conexión
    tk.Label(new_conn_window, text="Project").pack(pady=5)
    entry_project = tk.Entry(new_conn_window)
    entry_project.pack(pady=5)

    tk.Label(new_conn_window, text="Server").pack(pady=5)
    entry_server = tk.Entry(new_conn_window)
    entry_server.pack(pady=5)

    tk.Label(new_conn_window, text="Database").pack(pady=5)
    entry_database = tk.Entry(new_conn_window)
    entry_database.pack(pady=5)

    tk.Label(new_conn_window, text="User").pack(pady=5)
    entry_user = tk.Entry(new_conn_window)
    entry_user.pack(pady=5)

    tk.Label(new_conn_window, text="Password").pack(pady=5)
    entry_password = tk.Entry(new_conn_window, show="*")
    entry_password.pack(pady=5)

    tk.Button(new_conn_window, text="Add", command=add_connection).pack(pady=5)
    tk.Button(new_conn_window, text="Cancel", command=new_conn_window.destroy).pack(pady=5)

# Update Connection functionality
def update_connection():
    def load_connection():
        project_name = project_combobox.get()
        conn_sqlite = sqlite3.connect(r"C:\Users\gdlycarv\Desktop\Juniper- Move to Production\DB\DB_Conection.db")
        cursor_sqlite = conn_sqlite.cursor()
        cursor_sqlite.execute("SELECT Server, DataBase, User, Password FROM Connection WHERE Project = ?", (project_name,))
        result = cursor_sqlite.fetchone()
        
        if result:
            entry_server.delete(0, tk.END)
            entry_database.delete(0, tk.END)
            entry_user.delete(0, tk.END)
            entry_password.delete(0, tk.END)
            
            entry_server.insert(0, result[0])
            entry_database.insert(0, result[1])
            entry_user.insert(0, result[2])
            entry_password.insert(0, result[3])
        
        conn_sqlite.close()

    def save_update():
        if messagebox.askyesno("Confirm Update", "Are you sure you want to update this connection?"):
            project_name = project_combobox.get()
            server = entry_server.get()
            database = entry_database.get()
            user = entry_user.get()
            password = entry_password.get()
            
            conn_sqlite = sqlite3.connect(r"C:\Users\gdlycarv\Desktop\Juniper- Move to Production\DB\DB_Conection.db")
            cursor_sqlite = conn_sqlite.cursor()
            cursor_sqlite.execute("UPDATE Connection SET Server = ?, DataBase = ?, User = ?, Password = ? WHERE Project = ?",
                                  (server, database, user, password, project_name))
            conn_sqlite.commit()
            conn_sqlite.close()
            messagebox.showinfo("Success", "Connection updated.")
            update_conn_window.destroy()

    # Crear ventana para actualizar conexión
    update_conn_window = tk.Toplevel(app)
    update_conn_window.title("Update Connection")
    update_conn_window.geometry("600x420")
    update_conn_window.resizable(0, 0)

    # Obtener lista de proyectos desde SQLite
    conn_sqlite = sqlite3.connect(r"C:\Users\gdlycarv\Desktop\Juniper- Move to Production\DB\DB_Conection.db")
    cursor_sqlite = conn_sqlite.cursor()
    cursor_sqlite.execute("SELECT Project FROM Connection")
    projects = [row[0] for row in cursor_sqlite.fetchall()]
    conn_sqlite.close()

    tk.Label(update_conn_window, text="Select Project").pack(pady=10)
    project_combobox = ttk.Combobox(update_conn_window, values=projects)
    project_combobox.pack(pady=5)
    tk.Button(update_conn_window, text="Load", command=load_connection).pack(pady=5)

    tk.Label(update_conn_window, text="Server").pack(pady=5)
    entry_server = tk.Entry(update_conn_window)
    entry_server.pack(pady=5)

    tk.Label(update_conn_window, text="Database").pack(pady=5)
    entry_database = tk.Entry(update_conn_window)
    entry_database.pack(pady=5)

    tk.Label(update_conn_window, text="User").pack(pady=5)
    entry_user = tk.Entry(update_conn_window)
    entry_user.pack(pady=5)

    tk.Label(update_conn_window, text="Password").pack(pady=5)
    entry_password = tk.Entry(update_conn_window, show="*")
    entry_password.pack(pady=5)

    tk.Button(update_conn_window, text="Update", command=save_update).pack(pady=5)
    tk.Button(update_conn_window, text="Cancel", command=update_conn_window.destroy).pack(pady=5)
    
# Delete Connection functionality
def delete_connection():
    def confirm_delete():
        project_name = project_combobox.get()
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the connection for '{project_name}'?"):
            conn_sqlite = sqlite3.connect(r"C:\Users\gdlycarv\Desktop\Juniper- Move to Production\DB\DB_Conection.db")
            cursor_sqlite = conn_sqlite.cursor()
            cursor_sqlite.execute("DELETE FROM Connection WHERE Project = ?", (project_name,))
            conn_sqlite.commit()
            conn_sqlite.close()
            
            messagebox.showinfo("Success", f"Connection for '{project_name}' deleted successfully.")
            delete_conn_window.destroy()
        else:
            messagebox.showinfo("Canceled", "Delete operation canceled.")

    # Crear ventana para eliminar conexión
    delete_conn_window = tk.Toplevel(app)
    delete_conn_window.title("Delete Connection")
    delete_conn_window.geometry("400x200")
    delete_conn_window.resizable(0, 0)

    # Obtener lista de proyectos desde SQLite
    conn_sqlite = sqlite3.connect(r"C:\Users\gdlycarv\Desktop\Juniper- Move to Production\DB\DB_Conection.db")
    cursor_sqlite = conn_sqlite.cursor()
    cursor_sqlite.execute("SELECT Project FROM Connection")
    projects = [row[0] for row in cursor_sqlite.fetchall()]
    conn_sqlite.close()

    tk.Label(delete_conn_window, text="Select Project to Delete").pack(pady=10)
    project_combobox = ttk.Combobox(delete_conn_window, values=projects)
    project_combobox.pack(pady=5)

    # Botones para confirmar o cancelar
    tk.Button(delete_conn_window, text="Delete", command=confirm_delete).pack(pady=5)
    tk.Button(delete_conn_window, text="Cancel", command=delete_conn_window.destroy).pack(pady=5)

# Application menu
menu = tk.Menu(app)
app.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Version Control", command=version)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit)

db_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Connection", menu=db_menu)
db_menu.add_command(label="Link to database", command=establish_connection)
db_menu.add_command(label="New Connection", command=new_connection)
db_menu.add_command(label="Update Connection", command=update_connection)
db_menu.add_command(label="Delete Connection", command=delete_connection)
db_menu.add_separator()
db_menu.add_command(label="Exit", command=quit)

app.mainloop()