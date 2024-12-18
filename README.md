# Projekt na Sieci Sterowane Programowo

## Skład zespołu

Konrad Pękala, Marcjanna Bąkowska, Marek Borkowski

## Topologia

W naszym rozwiązaniu użyjemy [topologii polskiej](https://sndlib.put.poznan.pl/home.action?fbclid=IwZXh0bgNhZW0CMTEAAR3tA3f6QjfDBMvHCTL5tdeqrTLAXejLmolCGpzL3xaQmjhuOEpV4jYTQyM_aem_m1RIC6h83HPIrBJi2hVbdQ)

![Polsa](./mininet/polska.jpg)

## Instalacja / Uruchomienie

Aby pobrać projekt w środowisku Floodlight VM należy wpisać w konsoli `git clone https://github.com/kpekala/floodlight-sdn-project.git`

Skrypt python służący do instalacji urządzeń mininet znajduje się w katalogu mininet/init_net.py.

Aby go uruchomić wystarczy wpisać w konsoli `sudo python ./mininet/init_net.py`
Warto po każdym uruchomeniu wpisać `sudo mn -c` aby wyczyścić środowisko mininet

### Uruchomienie generatora ruchu

Zakładamy, że używamy minimalnej topologii: `sudo mn --topo single,2 --controller remote`

1. W środowisku mininet uruchamiamy xterm `xterm h1 h2`
2. Na h1 włączamy serwer: `python3 ./mininet/generator/server.py`
3. Na h2 włączamy klienta: `python3 ./mininet/generator/client.py` i przerywamy wysyłanie używając ctrl + c

## Algorytm

Pseudokod algorytmu znajduję się w folderze algorithm
