from typing import List
from enum import Enum, auto

class ContentType(Enum):
  user = auto()
  deletedUser = auto()
  post = auto()


def formatedList(data: List, contentType: ContentType) -> None:
  if contentType == ContentType.deletedUser:
    for user in data:
      print(f"{user['id']} \t\t https://vk.com/id{user['id']}")
  elif contentType == ContentType.user:
    for user in data:
      #print(f"{user['first_name']}  {user['last_name']} \t\t https://vk.com/id{user['id']}")
      print(user)