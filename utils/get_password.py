import string
import random


def get_password(length=12, special=True, numbers=True, uppercase=True):
    
    password = []

    char_list = string.ascii_lowercase

    if special:
        char_list += string.punctuation
    if numbers:
        char_list += string.digits
    if uppercase:
        char_list += string.ascii_uppercase

    for i in range(length):

        randomchar = random.choice(char_list)
        password.append(randomchar)

    print(f'Most recent passwrod: {"".join(password)}')

    return ''.join(password)