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
Digest: sha256:67647b78562d2b7a5ff5c650d2550edc8127dd7300d6f22c59b8072fd4ef121a
Status: Downloaded newer image for ghcr.io/marceltarczykowski/breach-checker-backend:latest
ghcr.io/marceltarczykowski/breach-checker-backend:latest



docker pull ghcr.io/marceltarczykowski/breach-checker-backend:03f4048               
03f4048: Pulling from marceltarczykowski/breach-checker-backend
4ee020ea4155: Pull complete 
286d8c291daa: Pull complete 
e3e428093f5e: Pull complete 
25c2fc776534: Pull complete 
60c278d7165a: Pull complete 
83a14706aa6d: Pull complete 
30cf67d7101c: Pull complete 
5a6e20b00272: Pull complete 
52dba87a5011: Pull complete 
Digest: sha256:67647b78562d2b7a5ff5c650d2550edc8127dd7300d6f22c59b8072fd4ef121a
Status: Downloaded newer image for ghcr.io/marceltarczykowski/breach-checker-backend:03f4048
ghcr.io/marceltarczykowski/breach-checker-backend:03f4048



docker images --digests ghcr.io/marceltarczykowski/breach-checker-backend
REPOSITORY                                          TAG       DIGEST                                                                    IMAGE ID       CREATED         SIZE
ghcr.io/marceltarczykowski/breach-checker-backend   03f4048   sha256:67647b78562d2b7a5ff5c650d2550edc8127dd7300d6f22c59b8072fd4ef121a   67647b78562d   3 minutes ago   212MB
ghcr.io/marceltarczykowski/breach-checker-backend   latest    sha256:67647b78562d2b7a5ff5c650d2550edc8127dd7300d6f22c59b8072fd4ef121a   67647b78562d   3 minutes ago   212MB

docker push ghcr.io/marceltarczykowski/breach-checker-backend:latest
The push refers to repository [ghcr.io/marceltarczykowski/breach-checker-backend]
83a14706aa6d: Layer already exists 
30cf67d7101c: Layer already exists 
e3e428093f5e: Layer already exists 
286d8c291daa: Layer already exists 
5a6e20b00272: Layer already exists 
25c2fc776534: Layer already exists 
60c278d7165a: Layer already exists 
52dba87a5011: Layer already exists 
4ee020ea4155: Layer already exists 
latest: digest: sha256:67647b78562d2b7a5ff5c650d2550edc8127dd7300d6f22c59b8072fd4ef121a size: 2199


Digesty obu tagów (latest oraz skrótu ostatniego commita) są identyczne, co potwierdza, że oba wskazują na dokładnie ten sam, zweryfikowany obraz w rejestrze. Polecenie docker pull zadziałało bez logowania, ponieważ po zmianie widoczności pakietu na publiczną odczyt (pobieranie) obrazów jest otwarty dla każdego bez uwierzytelniania. Natomiast docker push tez zakonczyl sie pomyslnie lecz powinien pojawic się błąd odmowy dostępu, ponieważ publikowanie zmian w rejestrze zawsze wymaga uwierzytelnienia i odpowiednich uprawnień do zapisu — dokładnie do tego celu służył token z zakresem write:packages w kroku 1, umożliwiając wypchnięcie obrazu przez pipeline lub z lokalnego terminala
