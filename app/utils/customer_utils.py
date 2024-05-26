import string
import random

def generate_unique_id():
    characters = string.ascii_lowercase + string.digits  # a-z and 0-9
    unique_id = ''.join(random.choices(characters, k=12))
    return unique_id