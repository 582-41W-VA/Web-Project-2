import random
import string

def generate_meeting_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
