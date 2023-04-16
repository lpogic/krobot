# krobot
Software for Jansen's linkage based robot.

# PL
Oprogramowanie dla robota opartego na mechaniźmie Jansena.
## Wymagane urządzenia
- Raspberry Pi
- Waveshare HRB8825 Stepper Motor HAT For Raspberry Pi
- 2x silnik krokowy
## Wymagane oprogramowanie na Raspberry Pi
- interpreter języka Python + biblioteki: RPi.GPIO, paho-mqtt
- interpreter języka Ruby + biblioteki: sinatra, mqtt
- mosquitto (apt-get install mosquitto)
## Konfiguracja
- Raspberry powinno działać w trybie hotspota uruchamianego automatycznie przy starcie systemu
- skrypt `krobot` powinien być uruchomiony automatycznie po utworzeniu sieci Wi-Fi
## Zasada działania
Skrypt `krobot` uruchamia 4 procesy: serwer mqtt (mosquitto), serwer http (sinatra), serwer gpio (PRi.GPIO) i proces sterujący. Komunikacja między procesami jest realizowana za pośrednictwem protokołu mqtt. Serwer http pozwala na sterowanie robotem z poziomu przeglądarki internetowej.

Aby wyświetlić panel sterowania w przeglądarce, należy połączyć się z siecią wewnętrzną robota (SSID: krobot) i przejść pod url: `http://10.42.0.1:4567/do`.
