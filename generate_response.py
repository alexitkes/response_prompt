import os
import sys

from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()


AUTHORIZATION_KEY = os.getenv("AUTHORIZATION_KEY")

MODEL = "GigaChat-2"
TEMPERATURE=0.5


def generate_response(skills_text: str, order_text: str) -> None:
    """Генерация отклика на заказ

    Генерирует отклик на заказ order_text для разработчика с умениями
    skills_text и выводит его на экран.
    """
    kwargs = {
        "skills_text": skills_text,
        "order_text": order_text,
    }

    with open("prompt.txt") as fd:
        prompt = fd.read().format(**kwargs)

    print(prompt)

    with GigaChat(credentials=AUTHORIZATION_KEY, model=MODEL) as client:
        response = client.chat.create(
            {
                "messages": [
                    {"role": "user", "content": prompt},
                ],
                "temperature": TEMPERATURE,
            }
        )

        print(response.messages[0].content[0].text)


if __name__ == "__main__":
    with open(sys.argv[1]) as fd:
        skills_text = fd.read()

    with open(sys.argv[2]) as fd:
        order_text = fd.read()

    generate_response(skills_text, order_text)
