import os
import sys

from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()


AUTHORIZATION_KEY = os.getenv("AUTHORIZATION_KEY")

MODEL = "GigaChat-2"
TEMPERATURE=0.5


def generate_response(order_text: str) -> None:
    """Генерирует отклик на заказ order_text и выводит его на экран.
    """
    with open("prompt.txt") as fd:
        prompt = fd.read().format(order_text=order_text)

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
        order_text = fd.read()

    generate_response(order_text)
