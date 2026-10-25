{"status":"ok"}
172.20.0.1 - - [22/Oct/2026 14:28:04] "GET /health HTTP/1.1" 200 -


backend: OK
backend: UNREACHABLE
backend: UNREACHABLE

Kontener uruchomiony bez parametru --network trafia do domyślnej sieci bridge, która nie posiada rozwiązywania nazw po nazwach kontenerów

po restarcie
 docker exec backend cat /tmp/notatka.txt
notatka

po usunieciu
docker exec backend cat /tmp/notatka.txt
cat: /tmp/notatka.txt: No such file or directory

historia.txt
Sun Oct 25 14:03:45 UTC 2026
Sun Oct 25 14:03:52 UTC 2026

/tmp przetrwał restart, ale nie rm: Restart zachowuje warstwę zapisywalną kontenera (container layer), a polecenie docker rm bezpowrotnie ją usuwa wraz z plikiem.

Dlaczego historia.txt przetrwała: Dane zapisano w wolumenie (breach-dane), którego cykl życia jest niezależny od kontenerów i istnieje w systemie hosta po ich usunięciu.

Czy lista wycieków przetrwa docker rm: Przetrwa tylko wtedy, gdy baza/plik z wyciekami zapisuje dane w wolumenie lub montowanym katalogu hosta (bind mount); w warstwie zapisywalnej kontenera zostanie utracona.


