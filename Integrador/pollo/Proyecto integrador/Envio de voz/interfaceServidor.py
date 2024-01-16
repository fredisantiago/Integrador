import tkinter as tk

def on_button_click(button_number):
    # Esta función se llama cuando se hace clic en un botón
    print(f"Botón {button_number} presionado")

# Crear la ventana principal
root = tk.Tk()


# Crear los 4 ocupando toda la pantalla
button1 = tk.Button(root, text="Botón 1", command=lambda: on_button_click(1), height=50, width=50)
button2 = tk.Button(root, text="Botón 2", command=lambda: on_button_click(2), height=50, width=50)
button3 = tk.Button(root, text="Botón 3", command=lambda: on_button_click(3), height=50, width=50)
button4 = tk.Button(root, text="Botón 4", command=lambda: on_button_click(4), height=50, width=50)

# Colocar los botones en la ventana, asigna las posiciones en el grid de la interface
button1.grid(row=0, column=0)
button2.grid(row=0, column=1)
button3.grid(row=0, column=2)
button4.grid(row=0, column=3)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
