import string , secrets
import hashlib
import base64
from pathlib import Path
from cryptography.fernet import Fernet

def __init__(self, key):
  if not isinstance(key, bytes):
   key = key.encode()
  
  self.fernet = Fernet(key)
    

class FernetHasher:
  random_string_chars = string.ascii_lowercase + string.ascii_uppercase
  base_dir= Path(__file__).resolve().parent
  key_dir = base_dir / "key"

@classmethod
def __init__(self, key):
  if not isinstance(key, bytes):
   key = key.encode()
  
  self.fernet = Fernet(key)


  @classmethod
  def _get_random_string(cls, length=25):
    string=""
    for i in range(length):
      string=string + secrets.choice(cls.random_string_chars)

    return(string)

  @classmethod
  def create_key(cls, archive=False):
    value= cls._get_random_string()
    hasher = hashlib.sha256(value.encode("utf-8")).digest()
    key = base64.b64encode(hasher)  
    if archive:
      return key, cls.archive_key(key)
    return key, None

  @classmethod
  def archive_key(cls, key):
    file = "key.key"
    while Path(cls.key_dir / file). exists(): 
      file= f"key_{cls._get_random_string(length=5)}.key"

    with open(cls.key_dir / file, "wb") as arq:
      arq.write(key)

    return cls.key_dir / file
  
  def encrypt(self, value):
    if not isinstance(value, bytes):
      value = value.encode()
    return self.fernet.encrypt(value)
  
Fernet_pablo = FernetHasher('z3TQwyPHmkmcnByVwWEnR0EWZMlVpGeJq7vvxdqYqKo=')
print(Fernet_pablo.encrypt("minha senha"))