# REST API
REST API (Representational State Transfer Application Programming Interface) to zestaw reguł i konwencji dla budowania i interakcji z usługami internetowymi. Jest to architektoniczny styl komunikacji, który wykorzystuje protokół HTTP do wymiany danych.

Oto podstawowe cechy REST API:

1. Bezstanowość - każde żądanie od klienta musi zawierać wszystkie informacje potrzebne do zrozumienia i obsłużenia żądania. Serwer nie przechowuje stanu sesji klienta.

2. Jednolity interfejs - zasoby są identyfikowane przez URL, manipulowane za pomocą standardowych metod HTTP (GET, POST, PUT, DELETE), i reprezentowane w standardowych formatach (najczęściej JSON lub XML).

3. System warstwowy - klient nie ma bezpośredniego dostępu do serwera, komunikacja może przechodzić przez pośrednie warstwy (np. load balancery, cache).

4. Cacheable - odpowiedzi można oznaczyć jako cacheable lub non-cacheable, co pozwala na optymalizację wydajności.

5. Kod na żądanie (opcjonalnie) - serwer może tymczasowo rozszerzyć funkcjonalność klienta przesyłając kod wykonawczy.

Podstawowe metody HTTP używane w REST API:
- GET - pobieranie zasobów
- POST - tworzenie nowych zasobów
- PUT - aktualizacja istniejących zasobów
- DELETE - usuwanie zasobów
- PATCH - częściowa aktualizacja zasobów

Przykładowe użycie w Pythonie z biblioteką requests:

```python
import requests

# Pobranie danych
response = requests.get('https://api.example.com/users')
users = response.json()

# Utworzenie nowego użytkownika
new_user = {"name": "Jan Kowalski", "email": "jan@example.com"}
response = requests.post('https://api.example.com/users', json=new_user)

# Aktualizacja użytkownika
updated_data = {"email": "jan.kowalski@example.com"}
response = requests.put('https://api.example.com/users/123', json=updated_data)

# Usunięcie użytkownika
response = requests.delete('https://api.example.com/users/123')
```

REST API jest powszechnie stosowane w tworzeniu nowoczesnych aplikacji webowych, mobilnych i systemów rozproszonych ze względu na swoją prostotę, skalowalność i zgodność z istniejącą infrastrukturą internetową.
