import pyaudio
import socket

ESP_IP = "192.168.1.180"  # Reemplaza con la IP fija del ESP8266
ESP_PORT = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

try:
    while True:
        data = stream.read(1024)
        sock.sendto(data, (ESP_IP, ESP_PORT))
except KeyboardInterrupt:
    print("Cerrando...")
    stream.stop_stream()
    stream.close()
    p.terminate()
