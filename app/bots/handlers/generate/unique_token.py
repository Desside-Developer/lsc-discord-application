import random
import string


def generate_unique_token():
    # characters = string.ascii_letters + string.digits
    characters = string.ascii_uppercase + string.digits
    token = ''.join(random.choices(characters, k=4))
    return f"[{token}]"


def generate_ticket_token():
    # characters = string.ascii_letters + string.digits
    characters = string.ascii_uppercase + string.digits
    token = ''.join(random.choices(characters, k=10))
    return f"{token}"