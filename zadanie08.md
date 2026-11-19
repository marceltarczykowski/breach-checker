1
nieudany:
https://github.com/marceltarczykowski/breach-checker/actions/runs/44587918826

0.279                    ^ Tag must be paired, missing: [ </h1> ], start tag match failed [ <h1> ] on line 14. (tag-pair)


udany:
https://github.com/marceltarczykowski/breach-checker/actions/runs/44588674220

W nowej wersji pipeline'u zarówno backend, jak i frontend są budowane jako obrazy produkcyjne, wypychane do rejestru GHCR, a następnie pobierane z niego w kroku verify za pomocą docker-compose.ci.yml — dzięki czemu test dymny weryfikuje dokładnie te same artefakty, które trafią na produkcję. We wcześniejszej wersji z rejestru pobierany był wyłącznie obraz backendu, natomiast frontend był budowany lokalnie na potrzeby testu (build: z docker-compose.yml), przez co nie weryfikowano docelowego obrazu produkcyjnego publikowanego do rejestru.

2
nieudany:
https://github.com/marceltarczykowski/breach-checker/actions/runs/44591491629

udany:
https://github.com/marceltarczykowski/breach-checker/actions/runs/44594891738

Po nieudanym uruchomieniu tag `latest` backendu nadal wskazywał na obraz z poprzedniego, udanego i zweryfikowanego wdrożenia, ponieważ job `promote` został pominięty i nie nadpisał go wadliwym obrazem z `127.0.0.1`. Jest to kluczowe dla każdego, kto pobiera obraz bez podawania konkretnego tagu (np. podczas wdrożenia na produkcję), ponieważ domyślnie pobierany jest właśnie tag `latest` — dzięki temu użytkownik lub serwer produkcyjny nie ściągnie zepsutej wersji aplikacji.



3
docker pull ghcr.io/marceltarczykowski/breach-checker-backend:latest
latest: Pulling from marceltarczykowski/breach-checker-backend
7b8a86dce565: Pull complete 
5cba6e73d6ab: Pull complete 
52b8eff6db70: Pull complete 
81f8c484a563: Pull complete 
247d9c5b36ee: Pull complete 
Digest: sha256:404209b4e4c68c5fc8d2e819ba494c6d3aa663985b034645d5f3fa95abd6a631
Status: Downloaded newer image for ghcr.io/marceltarczykowski/breach-checker-backend:latest
ghcr.io/marceltarczykowski/breach-checker-backend:latest



docker pull ghcr.io/marceltarczykowski/breach-checker-backend:2cadad1               
2cadad1: Pulling from marceltarczykowski/breach-checker-backend
Digest: sha256:cfd954e31c6de193fcc381605c075a76e8425cf714c281b5a59c28b2c39d523e
Status: Downloaded newer image for ghcr.io/marceltarczykowski/breach-checker-backend:2cadad1
ghcr.io/marceltarczykowski/breach-checker-backend:2cadad1



docker images --digests ghcr.io/marceltarczykowski/breach-checker-backend
REPOSITORY                                          TAG       DIGEST                                                                    IMAGE ID       CREATED         SIZE
ghcr.io/marceltarczykowski/breach-checker-backend   2cadad1   sha256:cfd954e31c6de193fcc381605c075a76e8425cf714c281b5a59c28b2c39d523e   cfd954e31c6d   5 minutes ago   182MB
ghcr.io/marceltarczykowski/breach-checker-backend   latest    sha256:404209b4e4c68c5fc8d2e819ba494c6d3aa663985b034645d5f3fa95abd6a631   404209b4e4c6   5 minutes ago   182MB


docker push ghcr.io/marceltarczykowski/breach-checker-backend:latest
The push refers to repository [ghcr.io/marceltarczykowski/breach-checker-backend]
2dc99d2d0a39: Layer already exists 
05e0eee5572e: Layer already exists 
c74288390aeb: Layer already exists 
68bced9e0afa: Layer already exists 
5cba6e73d6ab: Layer already exists 
52b8eff6db70: Layer already exists 
81f8c484a563: Layer already exists 
247d9c5b36ee: Layer already exists 
7b8a86dce565: Layer already exists 
latest: digest: sha256:404209b4e4c68c5fc8d2e819ba494c6d3aa663985b034645d5f3fa95abd6a631 size: 403


Digesty obu tagów (latest oraz skrótu ostatniego commita) są identyczne, co potwierdza, że oba wskazują na dokładnie ten sam, zweryfikowany obraz w rejestrze. Polecenie docker pull zadziałało bez logowania, ponieważ po zmianie widoczności pakietu na publiczną odczyt (pobieranie) obrazów jest otwarty dla każdego bez uwierzytelniania. Natomiast docker push tez zakonczyl sie pomyslnie lecz powinien pojawic się błąd odmowy dostępu, ponieważ publikowanie zmian w rejestrze zawsze wymaga uwierzytelnienia i odpowiednich uprawnień do zapisu — dokładnie do tego celu służył token z zakresem write:packages w kroku 1, umożliwiając wypchnięcie obrazu przez pipeline lub z lokalnego terminala
