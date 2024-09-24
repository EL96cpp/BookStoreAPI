import string, random


def generate_code():
    return ''.join(random.choices(string.digits, k=4))