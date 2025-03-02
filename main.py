import network  # Módulo para conexión Wi-Fi
import urequests  # Módulo para solicitudes HTTP
import utime  # Módulo para manejo de tiempos
from machine import ADC  # Módulo para el uso del ADC

# Configuración de credenciales Wi-Fi
WIFI_SSID = "NOMBRE-DE-LA-RED"
WIFI_PASSWORD = "CONTRASEÑA-DE-LA-RED"

# Configuración de ThingSpeak
THING_SPEAK_CHANNEL_ID = "CHANNEL-ID"
THING_SPEAK_API_KEY = "WRITE-API-KEY"
THING_SPEAK_URL = f"https://api.thingspeak.com/update?api_key={THING_SPEAK_API_KEY}"

# Función para conectar a la red Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Conectando a {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        timeout = 15  # Espera máxima de conexión
        while not wlan.isconnected() and timeout > 0:
            utime.sleep(1)
            timeout -= 1
            print("Intentando conectar...")
        
    if wlan.isconnected():
        print("Conectado a Wi-Fi! IP:", wlan.ifconfig()[0])
    else:
        print("Error: No se pudo conectar a Wi-Fi.")

# Función para leer la temperatura de la Pico W
def read_temperature():
    sensor_temp = ADC(4)  # Usa el canal ADC 4 (sensor interno)
    conversion_factor = 3.3 / 65535  # Factor de conversión ADC a voltios
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721  # Conversión a grados Celsius
    return round(temperature, 2)

# Función para enviar datos a ThingSpeak
def send_to_thingspeak(temperature):
    try:
        query_string = f"&field1={temperature}"
        response = urequests.get(THING_SPEAK_URL + query_string)
        print("Enviado a ThingSpeak: ", response.text)
        response.close()
    except Exception as e:
        print("Error al enviar datos a ThingSpeak:", str(e))

# Ejecutar el sistema
connect_wifi()

if network.WLAN(network.STA_IF).isconnected():  # Solo ejecuta si hay conexión Wi-Fi
    while True:
        temp = read_temperature()
        print(f"Temperatura: {temp} °C")
        send_to_thingspeak(temp)
        utime.sleep(180)  # Espera 3 minutos antes de la siguiente lectura
else:
    print("No se pudo conectar a Wi-Fi. Deteniendo ejecución.")
