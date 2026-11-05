docker compose exec backend pytest -v
===================== test session starts ======================
platform linux -- Python 3.12.15, pytest-8.4.2, pluggy-1.7.0 --/usr/local/bin/python3.12
cachedir: .pytest_cache
rootdir: /app
collected 8 items                                              

tests/test_check.py::test_leaked_hash_is_found PASSED    [ 12%]
tests/test_check.py::test_unknown_hash_is_not_found PASSED [ 25%]
tests/test_check.py::test_missing_hash_field PASSED      [ 37%]
tests/test_check.py::test_plaintext_password_is_rejected PASSED[ 50%]
tests/test_check.py::test_uppercase_hash_is_rejected PASSED [ 62%]
tests/test_check.py::test_invalid_hash_length PASSED     [ 75%]
tests/test_check.py::test_invalid_hex_characters PASSED  [ 87%]
tests/test_check.py::test_non_json_request_payload PASSED [100%]

====================== 8 passed in 0.27s =======================


docker compose exec backend pytest -v
===================== test session starts ======================
platform linux -- Python 3.12.15, pytest-8.4.2, pluggy-1.7.0 --/usr/local/bin/python3.12
cachedir: .pytest_cache
rootdir: /app
collected 8 items                                              

tests/test_check.py::test_leaked_hash_is_found PASSED    [ 12%]
tests/test_check.py::test_unknown_hash_is_not_found PASSED [ 25%]
tests/test_check.py::test_missing_hash_field PASSED      [ 37%]
tests/test_check.py::test_plaintext_password_is_rejected PASSED[ 50%]
tests/test_check.py::test_uppercase_hash_is_rejected FAILED [ 62%]
tests/test_check.py::test_invalid_hash_length PASSED     [ 75%]
tests/test_check.py::test_invalid_hex_characters PASSED  [ 87%]
tests/test_check.py::test_non_json_request_payload PASSED [100%]

=========================== FAILURES ===========================
_______________ test_uppercase_hash_is_rejected ________________

client = <FlaskClient <Flask 'app'>>

    def test_uppercase_hash_is_rejected(client):
        # API przyjmuje tylko skrót w małych literach - hasło wpostaci jawnej musi zostać odrzucone
        response = client.post("/check", json={"hash": LEAKED.upper()})
>       assert response.status_code == 200
E       assert 400 == 200
E        +  where 400 = <WrapperTestResponse streamed [400 BAD REQUEST]>.status_code

tests/test_check.py:28: AssertionError
=================== short test summary info ====================
FAILED tests/test_check.py::test_uppercase_hash_is_rejected - assert 400 == 200
================= 1 failed, 7 passed in 0.31s ==================
Testy z zajęć korzystały wyłącznie ze stałej LEAKED, która zawiera skrót SHA-1 zapisany małymi literami.W bazie danych lub próbce wycieków skróty również były zapisane małymi literami, więc porównanie bez użycia .lower() nadal zwracało True.


HTTP 500
docker compose ps -a

NAME                        IMAGE                     COMMAND               SERVICE    CREATED          STATUS               PORTS
breach-checker-backend-1    breach-checker-backend    "flask --app app run…"   backend    54 minutes ago   Exited (1) Less thana second ago   
breach-checker-db-1         postgres:16-alpine        "docker-entrypoint.s…"   db         54 minutes ago   Exited (0) About a minute ago       
breach-checker-frontend-1   breach-checker-frontend   "/docker-entrypoint.…"   frontend   54 minutes ago   Up 53 minutes               0.0.0.0:8080->80/tcp, [::]:8080->80/tcp

docker inspect --format '{{.State.Status}} {{.State.ExitCode}}' breach-checker-backend-1
exited 1

Plik blad.html zawierał domyślną stronę błędu serwera deweloperskiego Werkzeug (Flask Debugger) wraz z pełnym stosem wywołań (traceback).
Zwracanie takiej odpowiedzi na serwerze produkcyjnym stanowi poważne zagrożenie bezpieczeństwa (kategoria Information Disclosure / Stack Trace Exposure). Ujawnia ona atakującemu dokładną strukturę kodu źródłowego (/app/app.py)




 curl.exe http://localhost:8080/nginx.conf
server {
    listen 80;

    # Pliki strony (index.html, style.css, script.js)
    location / {
        root /usr/share/nginx/html;
        index index.html;
    }

    # Wszystko pod /api/ nginx przekazuje do usługi backend w sieci Compose
    location /api/ {
        proxy_pass http://backend:5000/;
    }
}


HTTP/1.1 404 Not Found
Server: nginx/1.31.6
Date: Thu, 05 Nov 2026 17:02:52 GMT
Content-Type: text/html
Content-Length: 153
Connection: keep-alive






Obraz produkcyjny frontendu nie ma tego problemu, ponieważ instrukcje w frontend/Dockerfile (COPY index.html style.css script.js /usr/share/nginx/html/) jawnie kopiują do obrazu wyłącznie statyczne zasoby strony internetowej, z pominięciem plików konfiguracyjnych czy samych instrukcji budowania (Dockerfile, nginx.conf).

Montowanie całego katalogu projektu do katalogu serwowanego przez serwer WWW jest bardzo ryzykowne, ponieważ nieumyślnie ujawnia publicznie wrażliwe pliki infrastruktury, pliki konfiguracyjne oraz kod źródłowy