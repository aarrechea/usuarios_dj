""" Imports """
import random, string


""" Code generator to create user """
def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

