# Instrukcja pracy na forku GitHub (bez pull requestów)

Oto najprostsza instrukcja pracy z forkiem na GitHub, gdy chcesz tylko pracować na własnej kopii bez modyfikowania oryginalnego repozytorium:

## 1. Utwórz fork

1. Przejdź do repozytorium GitHub, które chcesz skopiować
2. Kliknij przycisk "Fork" w prawym górnym rogu strony
3. Wybierz swoje konto jako miejsce docelowe forka

## 2. Sklonuj fork lokalnie

```bash
git clone https://github.com/TWOJA-NAZWA-UŻYTKOWNIKA/NAZWA-REPOZYTORIUM.git
cd NAZWA-REPOZYTORIUM
```

## 3. Pracuj na swoim forku

Teraz możesz normalnie pracować z repozytorium:

```bash
# Wprowadź zmiany w plikach
git add .
git commit -m "Opis wprowadzonych zmian"
git push origin main  # lub master w starszych repozytoriach
```

## 4. Synchronizacja z oryginalnym repozytorium (opcjonalnie)

Jeśli chcesz pobierać aktualizacje z oryginalnego repozytorium:

```bash
# Dodaj oryginalne repozytorium jako "upstream"
git remote add upstream https://github.com/ORYGINALNY-WŁAŚCICIEL/NAZWA-REPOZYTORIUM.git

# Pobierz zmiany z oryginalnego repozytorium
git fetch upstream

# Scal zmiany do swojego głównego brancha
git merge upstream/main  # lub upstream/master
```

To wszystko! Ta instrukcja pozwala Ci pracować na własnej kopii repozytorium bez konieczności tworzenia dodatkowych gałęzi czy wysyłania pull requestów.
