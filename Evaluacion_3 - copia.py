import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import networkx as nx

# ventana principal
ventana = tk.Tk()
ventana.title("Calculadora de Rutas entre Ciudades")
ventana.geometry("800x700")
ventana.config(bg="lightblue")

# Variables para almacenar el grafo y las ciudades
grafo = nx.Graph()
ciudades = []

# Función para cargar el archivo
def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    ciudad1, ciudad2, distancia = linea.strip().split(',')
                    distancia = int(distancia.strip())
                    grafo.add_edge(ciudad1.strip(), ciudad2.strip(), weight=distancia)
                    ciudades.extend([ciudad1.strip(), ciudad2.strip()])
            # Eliminar duplicados y actualizar la UI
            ciudades_unique = list(set(ciudades))
            actualizar_tablas(ciudades_unique)
            messagebox.showinfo("Éxito", "Archivo cargado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

# Función para actualizar los treeviews y tablas
def actualizar_tablas(ciudades):
    # Actualizar Treeview de ciudades extraídas
    treeview_ciudades.delete(*treeview_ciudades.get_children())
    for ciudad in ciudades:
        treeview_ciudades.insert("", "end", values=(ciudad,))

    # Actualiza tabla de distancias
    tabla_ciudades.delete(*tabla_ciudades.get_children())
    for ciudad1, ciudad2, datos in grafo.edges(data=True):
        tabla_ciudades.insert("", "end", values=(ciudad1, ciudad2, datos['weight']))

    # Actualiza ComboBox de origen y destino
    combo_origen['values'] = combo_destino['values'] = ciudades

# Función para calcular la ruta más corta
def calcular_ruta(event=None):
    origen = combo_origen.get()
    destino = combo_destino.get()
    if not origen or not destino or origen == destino:
        messagebox.showwarning("Advertencia", "Por favor, selecciona dos ciudades distintas.")
        return

    try:
        distancia, ruta = nx.single_source_dijkstra(grafo, origen, destino)
        tabla_ruta.delete(*tabla_ruta.get_children())
        distancia_acumulada = 0
        for i, ciudad in enumerate(ruta):
            if i > 0:
                distancia_acumulada += grafo[ruta[i-1]][ciudad]['weight']
            tabla_ruta.insert("", "end", values=(ciudad, distancia_acumulada))
        resultado.set(f"Distancia mínima: {distancia} km\nRuta: {' -> '.join(ruta)}")
    except nx.NetworkXNoPath:
        messagebox.showerror("Error", "No hay ruta disponible entre las ciudades seleccionadas.")
        tabla_ruta.delete(*tabla_ruta.get_children())

# Creamos los elementos de la interfaz
canvas = tk.Canvas(ventana, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_text(400, 20, text="Calculadora de Rutas entre Ciudades",font=("Arial", 16, "bold"), fill="black")

# Treeview de ciudades extraídas
treeview_ciudades = ttk.Treeview(canvas, columns=("Ciudad",), show="headings")
treeview_ciudades.heading("Ciudad", text="Nombre de Ciudad")
treeview_ciudades.column("Ciudad", width=200)
canvas.create_window(200, 150, window=treeview_ciudades)

# Enunciados  y ComboBox de Origen y Destino
tk.Label(canvas, text="Origen:", bg="lightblue", font=("Arial", 10)).place(x=45, y=410)
tk.Label(canvas, text="Destino:", bg="lightblue", font=("Arial", 10)).place(x=42, y=450)

combo_origen = ttk.Combobox(canvas, state="readonly")
combo_origen.place(x=100, y=410)
combo_destino = ttk.Combobox(canvas, state="readonly")
combo_destino.place(x=100, y=450)

combo_origen.bind("<<ComboboxSelected>>", calcular_ruta)
combo_destino.bind("<<ComboboxSelected>>", calcular_ruta)

# Botón para cargar el archivo
tk.Button(canvas, text="Cargar archivo .txt", font=("Arial", 14),command=cargar_archivo).place(x=90, y=340)

# Tabla de Ciudades con Distancias
tabla_ciudades = ttk.Treeview(canvas, columns=("Ciudad 1", "Ciudad 2", "Distancia (km)"), show="headings")
tabla_ciudades.heading("Ciudad 1", text="Ciudad 1")
tabla_ciudades.heading("Ciudad 2", text="Ciudad 2")
tabla_ciudades.heading("Distancia (km)", text="Distancia (km)")
tabla_ciudades.column("Ciudad 1", width=150)
tabla_ciudades.column("Ciudad 2", width=150)
tabla_ciudades.column("Distancia (km)", width=100)
canvas.create_window(550, 150, window=tabla_ciudades)

# Tabla de Resultados de la Ruta
tabla_ruta = ttk.Treeview(canvas, columns=("Ciudad", "Distancia Acumulada"), show="headings")
tabla_ruta.heading("Ciudad", text="Ciudad")
tabla_ruta.heading("Distancia Acumulada", text="Distancia Acumulada (km)")
canvas.create_window(550, 450, window=tabla_ruta)

# Resultado del cálculo
resultado = tk.StringVar()
tk.Label(canvas, textvariable=resultado, font=("Arial", 12), fg="black", bg="lightblue").place(x=370, y=600)

ventana.mainloop()