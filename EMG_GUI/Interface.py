# Interfaz gráfica
#Frame divisiones de la ventana
#En cada division se usa grid
#En cada grid se usa pack (botones)

from tkinter import *
from tkinter import Tk, Frame,  ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from ASerial import Arduino
import collections
import random

class Ventana(Frame):
    def __init__(self, master):
        self.master = master 
        self.conexion = Arduino()
        self.master.protocol('WM_DELETE_WINDOW', self.close)
        super().__init__(self.master)
          #GRAFICA
        self.muestra = 100 #RANGO
        self.datos = 0.0 #se ponen los datos que se grafican 
        self.fig, ax = plt.subplots(facecolor='#4D4D4D', dpi=100, figsize=(4,2)) #devuelve figuras y ejes
        plt.title('Gráfica', color='white', size=12, family='Arial')#da parametros a los bordes
        ax.tick_params(direction='out', width=2, colors='white', grid_color='r', grid_alpha=0.5)#linea

        self.line, = ax.plot([], [], color='w', marker='o', linewidth=2, markersize=1, markeredgecolor='w')
        #limites
        plt.xlim([0, self.muestra])
        plt.ylim([-50,1100])

        ax.set_facecolor('#6E6D7000')
        #iniciar lista que empiece y solo tenga 0, del tamaño de la muestra
        self.datos_señal = collections.deque([0]*self.muestra,maxlen=self.muestra)

        self.widgets()
     # Botones y  cosas para interactuar
    def widgets(self):
        # 4 frame (ventana dividida en 4)
        # Relativo = se puede mover y contraer
        # Absoluto = fijo, con posicion x, y
        frame = Frame(self.master, bg='gray30')
        frame.grid(column=0, row=0, columnspan=2, sticky='NSEW') #NSEW=norte,sur,este,oeste
        frame1 = Frame(self.master, bg='gray30')
        frame1.grid(column=2, row=0, sticky='NSEW')
        frame2 = Frame(self.master, bg='gray30')
        frame2.grid(column=1, row=1, sticky='NSEW')
        frame3 = Frame(self.master, bg='gray30')
        frame3.grid(column=2, row=1, sticky='NSEW')
        frame4 = Frame(self.master, bg='gray30')
        frame4.grid(column=0, row=1, sticky='NSEW')
        # Configuraciones de las frames
        #Columna
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        #Fila
        self.master.rowconfigure(0, weight=5)
        self.master.rowconfigure(1, weight=1)
        #Grafica
        self.canvas = FigureCanvasTkAgg(self.fig, master = frame)
        self.canvas.get_tk_widget().pack(padx=0, pady=0, expand=1, fill='both')
        #Botones
        self.btn_graficar = Button(frame4, text='Gráficar', font=("Arial", 12), bg='RoyalBlue1', fg='white', command=self.iniciar)
        self.btn_graficar.pack(pady=5, expand=1, fill='both')
        
        self.btn_pausar = Button(frame4, text='Pausar', font=("Arial", 12), bg='red', fg='white', command=self.pausar)
        self.btn_pausar.pack(pady=5, expand=1, fill='both')
        
        self.btn_reanudar = Button(frame4, text='Reanudar', font=("Arial", 12), bg='RoyalBlue1', fg='white', command=self.reanudar)
        self.btn_reanudar.pack(pady=5, expand=1, fill='both')
        # Etiqueta
        Label(frame2, text='Control Analogico', font=('Arial', 15), bg='gray30', fg='white').pack(padx=5, expand=1)
        # Barrita deslizante
        estilo = ttk.Style()
        estilo.configure('Horizontal.TScale', background='gray30')

        self.slider_uno = ttk.Scale(frame2, command=self.dato_slider_uno, state='disabled', to=255, from_=0, orient='horizontal', length=280, style='TScale')
        self.slider_uno.pack(pady=5, expand=1)

        self.slider_dos = ttk.Scale(frame2, command=self.dato_slider_dos, state='disabled', to=255, from_=0, orient='horizontal', length=280, style='TScale')
        self.slider_dos.pack(pady=5, expand=1)
        # Puertos Com
        Label(frame1, text='Puertos COM', bg='gray30', fg='white', font=('Arial', 12, 'bold')).pack(expand=1, fill='both')
        self.cmbx_ports = ttk.Combobox(frame1, values=self.conexion.port_dispo, justify='center', width=12, font=('Arial', 12))
        self.cmbx_ports.pack(expand=1, fill='x')
        self.cmbx_ports.current(4)
        
        self.cmbx_baudrates = ttk.Combobox(frame1, values=self.conexion.baud_dispo, justify='center', width=12, font=('Arial', 12))
        self.cmbx_baudrates.pack(expand=1, fill='x')
        self.cmbx_baudrates.current(3)
    # Recibir datos para iniciar grafica
    def animate(self, i):
        self.datos = self.conexion.leer()
        self.datos_señal.append(self.datos)
        self.line.set_data(range(self.muestra), self.datos_señal)
    # Botones (activar funciones)
    def iniciar(self):
            self.conexion.conexion(self.cmbx_ports.get(), self.cmbx_baudrates.get())
            print('iniciando grafica')
            self.animacion = animation.FuncAnimation(self.fig, self.animate, interval=10, blit=False)
            self.canvas.draw()

    def pausar(self):
            print('pausando grafica')
            self.animacion.event_source.stop()

    def reanudar(self):
            print('reanudando grafica')
            self.animacion.event_source.start()

    def dato_slider_uno(self, *args):
        print(int(self.slider_uno.get()))
    # Barrita que se desliza (activar funcion)
    def dato_slider_dos(self, *args):
        print(int(self.slider_dos.get()))

    def close(self, event=None) -> None:
        if self.conexion.is_conected: # verificamos si existe una conexion serial
            self.conexion.cerrar()
        self.master.quit()
        self.master.destroy()

if __name__ == "__main__":# Main: iniciar el programa
    root = Tk()
    root.geometry("742x535")
    root.config(bg='gray30')#poner caracteristicas de colores y formas de la ventana (bg=background)
    root.wm_title('ECG CURSO CERTIFICACIÓN')#window manager title
    root.minsize(width=700, height=400) #tamaño minimo
    app = Ventana(root)
    app.mainloop()#ejecuta la ventana