Webhook to mechanizm komunikacji między różnymi systemami przez HTTP, umożliwiający automatyczne powiadamianie jednej aplikacji o zdarzeniach zachodzących w drugiej. Działa na zasadzie "odwróconego API" - zamiast ciągłego odpytywania o zmiany, jedna aplikacja wysyła dane na określony URL drugiej aplikacji, gdy coś istotnego się wydarzy.

Przykładowe zastosowania webhooków:
- Powiadomienie systemu płatności o nowym zamówieniu
- Aktualizacja workflow po zmianach w repozytorium git
- Automatyczne uruchamianie testów po push'u do repozytorium
- Informowanie o zmianie statusu dostawy

W Pythonie można zarówno implementować odbiorniki webhooków (np. z użyciem Flask lub Django), jak i wysyłać powiadomienia do innych systemów.
