#!/usr/bin/env python3

"""
GitHub API Helper

Author: marekkoc
Created: 2025.05.20
Updated: 2025.05.22

Description:
    Skrypt do interakcji z GitHub API. Umożliwia wykonywanie podstawowych operacji na koncie GitHub, 
    takich jak pobieranie informacji o profilu, listowanie repozytoriów (publicznych i prywatnych),
    tworzenie nowych repozytoriów, dodawanie issues oraz sprawdzanie gwiazdek dla repozytoriów.

Użycie:
    1. Upewnij się, że masz zainstalowane wymagane biblioteki: requests, python-dotenv
    2. Utwórz plik .env w katalogu skryptu lub katalogu nadrzędnym z GITHUB_API_TOKEN="twój_token"
    3. Uruchom skrypt: python3 mks-git-info.py

Funkcje:
    - get_user_info() - Wyświetla podstawowe informacje o profilu użytkownika
    - list_repositories() - Wyświetla listę wszystkich repozytoriów (publicznych i prywatnych)
    - create_repository() - Tworzy nowe repozytorium
    - create_issue() - Dodaje nowe issue do wybranego repozytorium
    - get_repository_stars() - Pobiera listę użytkowników, którzy dodali gwiazdkę do repozytorium

Uwagi:
    Wymagany jest token GitHub API z odpowiednimi uprawnieniami.
    Aby wygenerować token, przejdź do: Settings > Developer settings > Personal access tokens
"""

import requests
import json
import os

from pathlib import Path
from dotenv import load_dotenv

# Próba wczytania zmiennych z pliku .env w bieżącym katalogu
load_dotenv()

# Jeśli token nie został znaleziony, spróbuj w katalogu nadrzędnym
if not os.getenv("GITHUB_API_TOKEN"):
    # Ścieżka do katalogu nadrzędnego
    parent_dir = Path(__file__).parent.parent
    
    # Ścieżka do pliku .env w katalogu nadrzędnym
    env_path = os.path.join(parent_dir, '.env')
    
    # Wczytanie zmiennych z pliku .env w katalogu nadrzędnym
    load_dotenv(dotenv_path=env_path)

token = os.getenv("GITHUB_API_TOKEN")
if not token:
    print("BŁĄD: Nie znaleziono tokenu GITHUB_API_TOKEN w pliku .env")
    print("Utwórz plik .env w bieżącym katalogu lub katalogu nadrzędnym z zawartością:")
    print('GITHUB_API_TOKEN="twój_token"')
    exit(1)

# Konfiguracja
username = "marekkoc"
# Możesz wygenerować token dostępu w ustawieniach GitHub:
# Settings > Developer settings > Personal access tokens

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}
base_url = "https://api.github.com"

# 1. Pobieranie informacji o użytkowniku
def get_user_info():
    response = requests.get(f"{base_url}/user", headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        
        # Pobierz dokładną liczbę repozytoriów za pomocą paginacji
        total_repos = count_all_repositories()
        
        # Wyświetlenie informacji bez zbędnych pustych linii
        print(f"Nazwa użytkownika: {user_data['login']}")
        print(f"Data utworzenia konta: {user_data['created_at']}")
        print(f"Liczba wszystkich repozytoriów: {total_repos}")
        print(f"Liczba repozytoriów publicznych: {user_data.get('public_repos', 0)}")
        if 'total_private_repos' in user_data:
            print(f"Liczba repozytoriów prywatnych: {user_data['total_private_repos']}")
    else:
        print(f"Błąd: {response.status_code}, {response.text}")

# Funkcja pomocnicza do liczenia wszystkich repozytoriów z uwzględnieniem paginacji
def count_all_repositories():
    all_repos_count = 0
    page = 1
    per_page = 100  # Maksymalna dozwolona wartość to 100
    
    # Pobieranie wszystkich stron repozytoriów
    while True:
        # Parametr visibility=all zapewnia, że pobierane są zarówno publiczne jak i prywatne repozytoria
        response = requests.get(
            f"{base_url}/user/repos?visibility=all&page={page}&per_page={per_page}", 
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Błąd podczas liczenia repozytoriów: {response.status_code}, {response.text}")
            return 0
        
        repos_page = response.json()
        if not repos_page:  # Jeśli nie ma więcej repozytoriów, kończymy pętlę
            break
            
        all_repos_count += len(repos_page)
        page += 1
        
        # Jeśli pobrano mniej repozytoriów niż per_page, to nie ma więcej stron
        if len(repos_page) < per_page:
            break
    
    return all_repos_count

# 2. Pobieranie listy repozytoriów użytkownika (publicznych i prywatnych) z obsługą paginacji
def list_repositories():
    all_repos = []
    page = 1
    per_page = 100  # Maksymalna dozwolona wartość to 100
    
    # Pobieranie wszystkich stron repozytoriów
    while True:
        # Parametr visibility=all zapewnia, że pobierane są zarówno publiczne jak i prywatne repozytoria
        # Dodajemy parametry paginacji: page i per_page
        response = requests.get(
            f"{base_url}/user/repos?visibility=all&page={page}&per_page={per_page}", 
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"Błąd: {response.status_code}, {response.text}")
            return
        
        repos_page = response.json()
        if not repos_page:  # Jeśli nie ma więcej repozytoriów, kończymy pętlę
            break
            
        all_repos.extend(repos_page)
        page += 1
        
        # Jeśli pobrano mniej repozytoriów niż per_page, to nie ma więcej stron
        if len(repos_page) < per_page:
            break
    
    # Podział na publiczne i prywatne
    public_repos = []
    private_repos = []
    
    for repo in all_repos:
        if repo['private']:
            private_repos.append(repo)
        else:
            public_repos.append(repo)
    
    # Wyświetl informację o liczbie prywatnych repozytoriów na początku
    print(f"\nLiczba repozytoriów prywatnych: {len(private_repos)}")
    
    # Wypisanie repozytoriów publicznych
    print(f"\nTwoje repozytoria publiczne ({len(public_repos)}):")
    for repo in public_repos:
        print(f"- {repo['name']} (gwiazdki: {repo['stargazers_count']})")
    
    # Wypisanie repozytoriów prywatnych
    print(f"\nTwoje repozytoria prywatne ({len(private_repos)}):")
    for repo in private_repos:
        print(f"- {repo['name']} (gwiazdki: {repo['stargazers_count']})")
    
    print(f"\nPodsumowanie: {len(all_repos)} repozytoriów ({len(public_repos)} publicznych, {len(private_repos)} prywatnych)")

# 3. Tworzenie nowego repozytorium
def create_repository(repo_name, description, private=False):
    data = {
        "name": repo_name,
        "description": description,
        "private": private,
        "auto_init": True  # Automatycznie inicjalizuje repozytorium z README
    }
    
    response = requests.post(f"{base_url}/user/repos", 
                           headers=headers, 
                           data=json.dumps(data))
    
    if response.status_code == 201:
        repo_data = response.json()
        print(f"\nUtworzono nowe repozytorium: {repo_data['html_url']}")
        print(f"Typ: {'prywatne' if repo_data['private'] else 'publiczne'}")
    else:
        print(f"Błąd: {response.status_code}, {response.text}")

# 4. Dodawanie issue do repozytorium
def create_issue(repo_owner, repo_name, title, body):
    data = {
        "title": title,
        "body": body
    }
    
    response = requests.post(
        f"{base_url}/repos/{repo_owner}/{repo_name}/issues",
        headers=headers,
        data=json.dumps(data)
    )
    
    if response.status_code == 201:
        issue_data = response.json()
        print(f"\nDodano nowe issue: {issue_data['html_url']}")
    else:
        print(f"Błąd: {response.status_code}, {response.text}")

# 5. Pobieranie listy gwiazdek (stars) dla repozytorium
def get_repository_stars(repo_owner, repo_name):
    response = requests.get(
        f"{base_url}/repos/{repo_owner}/{repo_name}/stargazers",
        headers=headers
    )
    
    if response.status_code == 200:
        stargazers = response.json()
        print(f"\nUżytkownicy, którzy dodali gwiazdkę do {repo_owner}/{repo_name}:")
        for user in stargazers:
            print(f"- {user['login']}")
        print(f"Łączna liczba gwiazdek: {len(stargazers)}")
    else:
        print(f"Błąd: {response.status_code}, {response.text}")

# Przykład użycia
if __name__ == "__main__":
    get_user_info()
    list_repositories()
    
    # Odkomentuj poniższe linie, jeśli chcesz utworzyć nowe repozytorium
    # create_repository("test-api-repo", "Repozytorium testowe utworzone przez API")
    # create_repository("test-private-repo", "Prywatne repozytorium testowe", private=True)
    
    # Podaj właściciela i nazwę istniejącego repozytorium, aby utworzyć issue
    # create_issue("właściciel_repo", "nazwa_repo", "Testowe issue", "To jest testowe issue utworzone przez API")
    
    # Podaj właściciela i nazwę repozytorium, aby pobrać listę gwiazdek
    # get_repository_stars("tensorflow", "tensorflow")
