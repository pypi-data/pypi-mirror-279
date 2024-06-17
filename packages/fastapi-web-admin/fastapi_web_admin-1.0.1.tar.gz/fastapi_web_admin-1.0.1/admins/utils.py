import random


def get_random_secret_key(length: int = 15):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
    return "".join(random.choice(chars) for _ in range(length))
