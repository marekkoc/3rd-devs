## Czym są porty?

Port to **logiczny punkt końcowy** komunikacji w sieci. To jak "numery pokojów" w budynku - jeden adres IP (budynek) może mieć wiele różnych usług (pokoi) działających na różnych portach.

## Analogia z budynkiem
- **Adres IP** = adres budynku (np. ul. Główna 5)
- **Port** = numer pokoju/mieszkania (np. mieszkanie 80, 443, 22)
- **Protokół** = sposób komunikacji (TCP/UDP)

## Jak działają porty?

**Zakres portów:** 0-65535 (16-bit)

**Kategorie:**
- **0-1023** - porty systemowe (wymagają uprawnień root)
- **1024-49151** - porty zarejestrowane 
- **49152-65535** - porty dynamiczne/prywatne

## Popularne porty i ich przeznaczenie

```
22   - SSH (bezpieczny dostęp zdalny)
80   - HTTP (strony internetowe)
443  - HTTPS (bezpieczne strony)
21   - FTP (transfer plików)
25   - SMTP (wysyłanie emaili)
110  - POP3 (odbieranie emaili)
143  - IMAP (odbieranie emaili)
3306 - MySQL (baza danych)
5432 - PostgreSQL (baza danych)
3690 - SVN (Subversion)
8080 - alternatywny HTTP
3000 - często Node.js apps
5000 - często Flask apps
```

## Praktyczny przykład

Gdy wpisujesz `google.com` w przeglądarce:
1. DNS tłumaczy `google.com` na IP (np. 142.250.191.14)
2. Przeglądarka łączy się z **142.250.191.14:443** (port HTTPS)
3. Serwer Google nasłuchuje na porcie 443 i odpowiada

## Na jednym serwerze może działać:
```
IP: 192.168.1.100
├── Port 22  → SSH
├── Port 80  → Apache (strona www)
├── Port 443 → Apache SSL
├── Port 3306 → MySQL
└── Port 8080 → aplikacja testowa
```

## W kontekście Pythona/programowania

```python
# Serwer nasłuchuje na porcie
server_socket.bind(('localhost', 8000))

# Klient łączy się z portem
client_socket.connect(('192.168.1.1', 8000))
```

Port to po prostu **numer identyfikujący konkretną usługę** na danym komputerze w sieci.
