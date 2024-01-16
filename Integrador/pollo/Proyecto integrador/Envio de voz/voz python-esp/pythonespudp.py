import pyaudio
import socket

UDP_IP = "192.168.1.68"#ip de la pc
UDP_PORT = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

p = pyaudio.PyAudio()

stream = p.open(format=32, channels=1, rate=11111, output=True)

try:
    while True:
        data, addr = sock.recvfrom(1024) # buffer de 1024 bytes
        stream.write(data)
        
except KeyboardInterrupt:  #precionar Crtl + C para salir
    print("Cerrando...")
    stream.stop_stream()
    stream.close()
    p.terminate()