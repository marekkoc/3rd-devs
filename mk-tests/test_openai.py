import os
from dotenv import load_dotenv
from openai import OpenAI

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Pobierz klucz API z zmiennych środowiskowych
api_key = os.getenv("OPENAI_API_KEY")

# Sprawdź czy klucz został poprawnie załadowany
if api_key:
    print("Klucz API został poprawnie załadowany.")
    # Inicjalizacja klienta OpenAI
    client = OpenAI(api_key=api_key)
    
    # Prosty test API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Powiedz 'Działa poprawnie!'"}]
        )
        print("Odpowiedź API:", response.choices[0].message.content)
        print("Połączenie działa poprawnie!")
    except Exception as e:
        print("Wystąpił błąd podczas łączenia z API:", e)
else:
    print("Nie znaleziono klucza API w pliku .env")
