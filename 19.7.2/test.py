from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()

_, auth_key = pf.get_api_key(valid_email, valid_password)
pet_photo = 'tests/images/cat1.jpg'
status, result = pf.delete_pet(auth_key, '6d10ba10-afdd-462d-a685-73e09bbb1420')
print(status)
print(result)
print(len(result))