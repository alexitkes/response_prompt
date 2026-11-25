import os
import sys

from argparse import ArgumentParser
from dotenv import load_dotenv

from gigachat import GigaChat

load_dotenv()


AUTHORIZATION_KEY = os.getenv("AUTHORIZATION_KEY")

MODEL = "GigaChat-2"
TEMPERATURE=0.2


def generate_response(*, skills_text: str, order_text: str, name: Optional[str] = None) -> None:
    """Генерация отклика на заказ

    Генерирует отклик на заказ order_text для разработчика с умениями
    skills_text и выводит его на экран.
    """
    kwargs = {
        "skills_text": skills_text,
        "order_text": order_text,
        "name_text": f"Твое имя {name}" if name else "",
    }

    with open("prompt.txt") as fd:
        prompt = fd.read().format(**kwargs)

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
    parser = ArgumentParser()
    parser.add_argument(
        "--name",
        type=str,
        default=None,
        metavar="NAME",
        help="Имя фрилансера для подписи",
    )
    parser.add_argument(
        "skills_file",
        metavar="SKILLS_FILENAME",
        type=str,
        help="Файл с описанием навыков фрилансера",
    )
    parser.add_argument(
        "order_file",
        metavar="ORDER_FILENAME",
        type=str,
        help="Файл с текстом заказа",
    )

    args = parser.parse_args()

    with open(args.skills_file) as fd:
        skills_text = fd.read()

    with open(args.order_file) as fd:
        order_text = fd.read()

    generate_response(
        skills_text=skills_text,
        order_text=order_text,
        name=args.name
    )
