import os
from openai import OpenAI
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv("../.env")

# Baza danych w pamięci
database = [
    {"id": 1, "name": "Adam", "age": 28, "occupation": "Software Engineer", "hobby": "Rock climbing"},
    {"id": 2, "name": "Michał", "age": 35, "occupation": "Data Scientist", "hobby": "Playing guitar"},
    {"id": 3, "name": "Jakub", "age": 31, "occupation": "UX Designer", "hobby": "Photography"},
]

async def select_person(question: str) -> int:
    # METODA 1: Używamy domyślnego konstruktora, który pobierze klucz API z zmiennej środowiskowej
    # openai = OpenAI()
    
    # METODA 2: Jawnie przekazujemy klucz API z zmiennej środowiskowej
    openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    messages = [
        {"role": "system", "content": "You are an assistant that selects the most relevant person for a given question. Respond with only the person's ID (1 for Adam, 2 for Michał, or 3 for Jakub)."},
        {"role": "user", "content": question}
    ]

    try:
        chat_completion = openai.chat.completions.create(
            messages=messages,
            model="gpt-4o",
            max_tokens=1,
            temperature=0,
        )

        completion = chat_completion.choices[0].message.content
        return int(completion.strip()) if completion else 1
    except Exception as error:
        print(f"Error in select_person: {error}")
        return 1  # Domyślnie Adam w przypadku błędu

async def answer_question(question: str, person_id: int) -> str:
    # METODA 1: Używamy domyślnego konstruktora, który pobierze klucz API z zmiennej środowiskowej
    # openai = OpenAI()
    
    # METODA 2: Jawnie przekazujemy klucz API z zmiennej środowiskowej
    openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    person = next((p for p in database if p["id"] == person_id), database[0])

    messages = [
        {"role": "system", "content": f"You are an assistant answering questions about {person['name']}. Use the following information: {person}"},
        {"role": "user", "content": question}
    ]

    try:
        chat_completion = openai.chat.completions.create(
            messages=messages,
            model="gpt-4o",
            max_tokens=500,
            temperature=0.7,
        )

        return chat_completion.choices[0].message.content or "I couldn't generate an answer."
    except Exception as error:
        print(f"Error in answer_question: {error}")
        return "Sorry, I encountered an error while trying to answer the question."

# Przykładowe użycie
async def main():
    questions = [
        "Who is the oldest person?",
        "Tell me about Adam's hobby",
        "What does Michał do for a living?",
        "How old is Jakub?",
    ]

    for question in questions:
        selected_person_id = await select_person(question)
        answer = await answer_question(question, selected_person_id)
        print(f'Question: "{question}"\nAnswer: {answer}\n')

# Uruchomienie programu z obsługą asyncio
if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 