import random
import os
import string

if os.path.exists("mysecret.txt"):
    f = open('mysecret.txt')
    random_string = f.readline()
else:
    char_set = string.ascii_uppercase + string.digits
    random_string = ''.join(random.sample(char_set*80, 80))
    with open('mysecret.txt', 'a') as the_file:
        the_file.write(random_string)