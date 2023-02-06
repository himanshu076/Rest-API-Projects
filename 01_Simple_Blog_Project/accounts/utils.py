import random
import string
from django.utils.timezone import timezone
from datetime import date


#  ----------------- FUNCTIONS ----------------------

# Function to generate random string of number having random
def randomString():
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(int(random.choice(string.digits))))


# Function to define avatar upload location
def avatar_upload_location(instance, filename):
  return "static/profile_pic/{0}/{1}".format(instance.id, filename)
