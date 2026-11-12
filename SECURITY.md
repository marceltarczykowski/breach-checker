
 **Trivy `0.76.0`** (`--severity HIGH,CRITICAL`).


| Komponent | Wersja | Rozmiar | Podatności (`HIGH,CRITICAL`) | Z poprawką (`--ignore-unfixed`) |
| :--- | :--- | :--- | :--- | :--- |
| **Backend** | `:dev` | 227 MB | **51** (51 HIGH, 0 CRIT) | **4** (4 HIGH) |
| **Backend** | `:prod` | **212 MB** | **49** | **2** |
| **Frontend** | `:przed` | 229 MB | **28** (27 HIGH, 1 CRIT) | **28** (27 HIGH, 1 CRIT) |
| **Frontend** | `:prod` | **93.7 MB** | **3** | **3** |

W celu redukcji powierzchni ataku oraz rozmiaru obrazów wdrożono wieloetapowe budowanie (multi-stage builds) oraz wymuszono pobieranie najnowszych obrazów bazowych przy budowaniu (docker build --pull), co wyeliminowało wszystkie podatności z dostępnymi poprawkami (fixed) i odchudziło obrazy produkcyjne.

Na dziś nie da się naprawić podatności oznaczonych jako unfixed (występujących w bibliotekach systemowych obrazu bazowego przed optymalizacją), ponieważ ich opiekunowie (upstream maintainers) nie wydali jeszcze oficjalnych łatek.

Ponowne skanowanie obrazów za pomocą narzędzia Trivy zostanie przeprowadzone automatycznie w potoku CI/CD przy kolejnej aktualizacji kodu lub przy cotygodniowej przebudowie obrazów (--pull), gdy tylko pojawią się nowe wersje obrazów bazowych.