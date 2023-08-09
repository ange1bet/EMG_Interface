# La parte de la comunicacion

import serial

class Arduino():
    def __init__(self):
        self.is_conected = False
        self.baud_dispo = ['1200', '2400', '4800', '9600', '19200', '38400', '115200']
        self.port_dispo = [f'COM{i}' for i in range (0,16)]
        
    
    def conexion(self, puerto, baudrate):
        self.puerto = puerto
        self.baudrate = baudrate
        self.arduino = serial.Serial(self.puerto, self.baudrate)
        self.arduino.timeout = 0.1
        self.is_conected = True
    
    def leer(self) -> float:
        try: #intentar hacer cosas
            mensaje_entrada = self.arduino.readline().decode('utf-8').split(',')[1]
            print(mensaje_entrada)
            if mensaje_entrada == '' or mensaje_entrada == '\r\n':
                return '0.0'
        except:
            mensaje_entrada = "0.0"
        return float(mensaje_entrada)
    
    def cerrar(self):
        self.arduino.close()