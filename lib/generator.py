
import random
import string


def generate_password(master_key: str, service_name: str, n: int, special_symbols: bool, iterations: int) -> str:
    random.seed(master_key+str(iterations)+service_name)

    chars = string.ascii_letters + (string.punctuation if special_symbols else "")

    password = ""

    for _ in range(n):
        password += random.choice(chars)

    return password


def ISaver():
    def save(self):
        pass
