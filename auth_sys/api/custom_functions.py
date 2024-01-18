import re
from .models import User


# functions to valid email

# check if email already exists
def check_email_exists(email):
    return User.objects.filter(email=email).exists()


# check if is a valid email
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None
