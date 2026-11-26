1.
log_attempts_total{found="true"} 2.0
log_attempts_total{found="false"} 4.0

Time
{__name__="log_attempts_total", found="false", instance="log:5001", job="log"}
2026-11-26 16:25:20
4
2026-11-26 16:25:40
4
2026-11-26 16:26:00
4
2026-11-26 16:26:20
4
2026-11-26 16:26:40
4
2026-11-26 16:27:00
4
2026-11-26 16:27:20
4
2026-11-26 16:27:40
4
2026-11-26 16:28:00
4
2026-11-26 16:28:20
4
2026-11-26 16:28:40
12
{__name__="log_attempts_total", found="false", instance="log:5001", job="log"}


Time
{__name__="log_attempts_total", found="true", instance="log:5001", job="log"}
2026-11-26 16:25:20
2
2026-11-26 16:25:40
2
2026-11-26 16:26:00
2
2026-11-26 16:26:20
2
2026-11-26 16:26:40
2
2026-11-26 16:27:00
2
2026-11-26 16:27:20
2
2026-11-26 16:27:40
2
2026-11-26 16:28:00
2
2026-11-26 16:28:20
2
2026-11-26 16:28:40
6
{__name__="log_attempts_total", found="true", instance="log:5001", job="log"}

Prywatność: ujawnienie prefiksu w metrykach (często dostępnych bez autoryzacji, jak tutaj Prometheus) ułatwia zgadywanie sprawdzanych haseł.
liczba szeregów czasowych: 5 znaków szesnastkowych to bardzo duzo możliwych kombinacji, co stworzyłoby ogromną liczbę osobnych szeregów czasowych i mogłoby przeciążyć pamięć Prometheusa.
Co dzieje się z licznikiem po docker compose up -d --build log i dlaczego: licznik zeruje się, ponieważ jego stan jest przechowywany wyłącznie w pamięci RAM procesu Pythona/Gunicorna przebudowa i uruchomienie nowego kontenera tworzy świeży proces od zera

2.
https://github.com/marceltarczykowski/breach-checker/actions/runs/45860712756

zapisanie proby:
Run docker compose logs log | grep "'hash_prefix': '7c4a8'"
time="2026-11-26T16:40:47Z" level=warning msg="The \"GRAFANA_PASSWORD\" variable is not set. Defaulting to a blank string."
log-1  | log: {'time': '2026-11-26T16:40:47+00:00', 'hash_prefix': '7c4a8', 'found': True}

Backend wysyła żądanie do usługi log asynchronicznie / w trybie best-effort (z obsługą wyjątków, aby błąd logowania nie przerywał głównej ścieżki odpowiedzi), więc poprawne działanie API nie gwarantuje, że usługa log faktycznie odebrała i zapisała zdarzenie. Sprawdzenie logów kontenera log potwierdza komunikację między kontenerami w sieci wewnętrznej oraz poprawne działanie samego obrazu produkcyjnego log


3.
'{"hash":"bc45408273d7e1914b741c3407b0b559764f7876"}' | curl.exe -s -w " czas: %{time_total}s\n" -X POST http://localhost:8080/api/check -H "Content-Type: application/json" -d '@-'
{
  "found": false
}
 czas: 0.026589s


 '{"hash":"bc45408273d7e1914b741c3407b0b559764f7876"}' | curl.exe -s -w " czas: %{time_total}s\n" -X POST http://localhost:8080/api/check -H "Content-Type: application/json" -d '@-'
{
  "found": false
}
 czas: 0.009160s


docker compose exec redis redis-cli TTL "bc45408273d7e1914b741c3407b0b559764f7876"
(integer) 129

docker compose exec redis redis-cli DEL "hash:bc45408273d7e1914b741c3407b0b559764f7876"
(integer) 0

'{"hash":"bc45408273d7e1914b741c3407b0b559764f7876"}' | curl.exe -s -w " czas: %{time_total}s\n" -X POST http://localhost:8080/api/check -H "Content-Type: application/json" -d '@-'
{
  "found": true
}
 czas: 0.024427s

po zatrzymaniu redisa:

'{"hash":"bc45408273d7e1914b741c3407b0b559764f7876"}' | curl.exe -s -w " czas: %{time_total}s\n" -X POST http://localhost:8080/api/check -H "Content-Type: application/json" -d '@-'
{
  "found": true
}
 czas: 4.003410s

backend-1  | check: hash=bc454... cache=miss
backend-1  | check: hash=bc454... cache=hit
backend-1  | check: hash=bc454... cache=niedostępny

Dlaczego backend odpowiadał false, choć skrót był w bazie: 
pierwsze zapytanie zapisało w Redisie negatywny wynik (found=false) z określonym czasem życia (TTL), więc przy drugim zapytaniu backend trafił w pamięć podręczną (cache=hit) i zwrócił nieaktualną wartość bez odpytywania PostgreSQL.

Jak można by to naprawić (dwa sposoby): (1) jawnie unieważniać/aktualizować wpis w Redisie (DEL lub nadpisanie klucza) w momencie dodawania nowych skrótów do bazy (cache invalidation / write-through), albo (2) znacznie skrócić TTL dla odpowiedzi negatywnych (found=false) lub w ogóle nie buforować wyników negatywnych.

Co by się stało przy zatrzymanym Redisie bez except redis.RedisError: próba połączenia z nieosiągalnym kontenerem Redisa rzuciłaby nieobsłużony wyjątek (ConnectionError / RedisError), przez co endpoint /api/check zwracałby klientowi błąd serwera (HTTP 500 Internal Server Error) zamiast pobrać wynik awaryjnie z bazy danych.