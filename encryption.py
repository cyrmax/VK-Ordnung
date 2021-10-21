import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from getpass import getpass
salt = b'\r\xb0\x81\x90\x1b\x82\xe7]\xb8{,)\x02\xd7\x1aR'

def kdf():
  return PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
  )

def encrypt(data):
  while True:
    password = getpass(prompt="Enter password to encrypt your VK authorization token. Password: ")
    password_again = getpass(prompt="Enter password again. Password: ")
    if password == password_again:
      break
    else:
      print("Passwords do not match. try again.")
  key = base64.urlsafe_b64encode(kdf().derive(password.encode()))
  f = Fernet(key)
  return base64.urlsafe_b64encode(f.encrypt(data.encode()))

def decrypt(data):
  password = getpass(prompt="Enter password to decrypt your VK authorization token. Password: ")
  key = base64.urlsafe_b64encode(kdf().derive(password.encode()))
  decodedData = base64.urlsafe_b64decode(data)
  f = Fernet(key)
  return f.decrypt(decodedData).decode()
