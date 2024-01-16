from tkinter import PhotoImage

class Bicicl:
    def __init__(self, tipo="", stock=0, ocupadas=0, costo=0, imagen_path=None):
        self.tipo = tipo
        self.stock = stock
        self.ocupadas = ocupadas
        self.costo = costo
        self.imagen = PhotoImage(file=imagen_path) if imagen_path else None
    def prestar(self):
        if self.stock > 0:
            self.stock -= 1
            self.ocupadas += 1
    def devolver(self):
        if self.ocupadas > 0:
            self.ocupadas -= 1
            self.stock += 1




