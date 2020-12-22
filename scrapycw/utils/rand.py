import random
import string


def rand_str(num):
    return ''.join(random.sample(string.ascii_letters + string.digits, num))


if __name__ == "__main__":
    print(rand_str(10))
