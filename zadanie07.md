Wyniki skanowania obrazów produkcyjnych po przebudowaniu z flagą `--pull`:

```text
# breach-checker-frontend:prod (bez --ignore-unfixed)
Total: 3 (HIGH: 3, CRITICAL: 0)

# breach-checker-frontend:prod (z --ignore-unfixed)
Total: 3 (HIGH: 3, CRITICAL: 0)

# breach-checker-backend:prod (bez --ignore-unfixed)
Total: 49 (HIGH: 49, CRITICAL: 0)

# breach-checker-backend:prod (z --ignore-unfixed)
Total: 2 (HIGH: 2, CRITICAL: 0)



Przebudowanie z flagą --pull pobrało najnowsze wersje obrazów bazowych redukując liczbę podatności z dostępną poprawką (fixed) do pojedynczych przypadków, podczas gdy pozostałe luki nie mają jeszcze wydanych łatek przez opiekunów dystrybucji. Wpływ --pull jest znacznie większy dla obrazu backend:prod, ponieważ bazuje on na rozbudowanym systemie Debian zawierającym większą liczbę pakietów systemowych i bibliotek niż minimalny obraz nginx:alpine we frontendzie.




2.
backend-1  | FileNotFoundError: [Errno 2] No usable temporary directory found in ['/tmp', '/var/tmp', '/usr/tmp', '/app']

docker compose exec backend touch /etc/test
touch: cannot touch '/etc/test': Read-only file system

docker compose exec backend touch /tmp/test
(brak)


docker compose exec backend grep CapEff /proc/1/status
CapEff: 0000000000000000


docker compose exec backend pytest
==================== test session starts ====================
platform linux -- Python 3.12.15, pytest-8.4.2, pluggy-1.7.0
rootdir: /app
collected 8 items                                           

tests/test_check.py ........                          [100%]

===================== 8 passed in 0.24s =====================

read_only: true blokuje zapis na dysku kontenera, cap_drop: [ALL] odbiera wszystkie uprawnienia jądra Linux, a no-new-privileges:true blokuje eskalację uprawnień (np. przez sudo lub pliki setuid).

W przeciwieństwie do USER appuser, które ogranicza jedynie kto wykonuje proces (użytkownik bez praw roota nadal może pisać w katalogach, do których ma dostęp, np. /tmp), read_only: true całkowicie blokuje zapis na systemie plików kontenera dla każdego użytkownika (nawet roota), poza jawnie zamontowanymi wolumenami i tmpfs.


3.
docker history sekret-demo:plik
IMAGE          CREATED          CREATED BY             SIZE      COMMENT
ddf08d0c3225   20 seconds ago   RUN /bin/sh -c rm /tmp/klucz.txt #buildkit     8.19kB    buildkit.dockerfile.v0
<missing>      20 seconds ago   RUN /bin/sh -c test -s /tmp/klucz.txt && ech…   4.1kB     buildkit.dockerfile.v0
<missing>      21 seconds ago   COPY klucz.txt /tmp/klucz.txt # buildkit        12.3kB    buildkit.dockerfile.v0
<missing>      6 days ago       CMD ["/bin/sh"]             0B        buildkit.dockerfile.v0
<missing>      6 days ago       ADD alpine-minirootfs-3.22.8-x86_64.tar.gz /…   8.97MB    buildkit.dockerfile.v0

tajny-klucz-marcel

Obrazy Docker składają się z niemodyfikowalnych warstw, dlatego polecenie RUN rm /tmp/klucz.txt jedynie ukrywa plik w nowej, wyższej warstwie, ale nie usuwa go fizycznie z wcześniejszej warstwy utworzonej przez COPY. Sekret należało przekazać bezpiecznie podczas budowania za pomocą mechanizmu BuildKit (RUN --mount=type=secret,id=klucz ...), który montuje plik tymczasowo w pamięci tylko na czas wykonywania pojedynczej komendy i nie zapisuje go w żadnej warstwie obrazu.