 Image breach-checker-frontend       Built                1.9s
 ✔ Image breach-checker-backend        Built                1.8s
 ✔ Container breach-checker-db-1       Healthy              4.0s
 ✔ Container breach-checker-backend-1  Healthy             14.7s
 ✔ Container breach-checker-frontend-1 Started              0.3s

 breach-checker-backend-1    breach-checker-backend                                                    "python app.py"          backend    4 minutes ago   Up 4 minutes (healthy)   5000/tcp

 breach-checker-db-1         postgres:16-alpine                                                        "docker-entrypoint.s…"   db         7 minutes ago   Up 7 minutes (healthy)   5432/tcp


2.
 {"found":true}
 {"found":true}
 {"found":false}

3.
 docker compose exec frontend nslookup backend
Server:         127.0.0.11
Address:        127.0.0.11:53

Non-authoritative answer:

Non-authoritative answer:
Name:   backend
Address: 172.21.0.6
Name:   backend
Address: 172.21.0.5
Name:   backend
Address: 172.21.0.3

breach-checker-backend-1    breach-checker-backend    "python app.py"          backend    5 minutes ago   Up 5 minutes (healthy)   5000/tcp
breach-checker-backend-2    breach-checker-backend    "python app.py"          backend    2 minutes ago   Up 2 minutes (healthy)   5000/tcp
breach-checker-backend-3    breach-checker-backend    "python app.py"          backend    2 minutes ago   Up 2 minutes (healthy)   5000/tcp
breach-checker-db-1         postgres:16-alpine        "docker-entrypoint.s…"   db         5 minutes ago   Up 5 minutes (healthy)   5432/tcp
breach-checker-frontend-1   breach-checker-frontend   "/docker-entrypoint.…"   frontend   5 minutes ago   Up 5 minutes             0.0.0.0:8080->80/tcp, [::]:8080->80/tcp

przed:
backend-1  | 172.21.0.4 - - [29/Oct/2026 15:13:49] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.21.0.4 - - [29/Oct/2026 15:13:49] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.21.0.4 - - [29/Oct/2026 15:13:49] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.21.0.4 - - [29/Oct/2026 15:13:49] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.21.0.4 - - [29/Oct/2026 15:13:49] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...

po:
backend-1  | 172.21.0.4 - - [29/Oct/2026 15:13:49] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.21.0.4 - - [29/Oct/2026 15:13:49] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...
backend-1  | 172.21.0.4 - - [29/Oct/2026 15:13:49] "POST /check HTTP/1.1" 200 -
backend-1  | check: hash=bc454...



backend-3  | 172.21.0.4 - - [29/Oct/2026 15:17:35] "POST /check HTTP/1.1" 200 -
backend-3  | check: hash=bc454...
backend-3  | 172.21.0.4 - - [29/Oct/2026 15:17:35] "POST /check HTTP/1.1" 200 -
backend-3  | check: hash=bc454...
backend-3  | 172.21.0.4 - - [29/Oct/2026 15:17:35] "POST /check HTTP/1.1" 200 -
backend-3  | check: hash=bc454...


backend-2  | 172.21.0.4 - - [29/Oct/2026 15:17:36] "POST /check HTTP/1.1" 200 -
backend-2  | check: hash=bc454...
backend-2  | 172.21.0.4 - - [29/Oct/2026 15:17:36] "POST /check HTTP/1.1" 200 -

Przed restartem kontener frontend (Nginx) miał już w pamięci podręcznej (cache DNS) rozwiązany adres IP z nazwy backend z momentu pierwszego uruchomienia, gdy istniała tylko jedna replika. Nginx rozwiązuje nazwy hostów przy starcie (lub zgodnie z czasem TTL) i bez ponownego przeładowania kierował cały ruch pod zapamiętany wcześniej pojedynczy adres IP. Restart kontenera zmusił Nginxa do ponownego odpytania wewnętrznego DNS Dockera, co pozwoliło mu pobrać zaktualizowaną listę adresów IP wszystkich trzech replik.

Dlaczego skalowanie byłoby niemożliwe, gdyby backend nadal miał mapowanie portów "5000:5000"?
Mapowanie portów w formacie "5000:5000" próbuje przypisać port 5000 maszyny hosta bezpośrednio do portu 5000 kontenera. wystapiłby blad z powodu konfliktu portów