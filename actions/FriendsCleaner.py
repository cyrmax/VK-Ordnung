from time import sleep
from formater import *

def cleanDeletedFriends(api):
  response = api.friends.get(fields="nickname,domain")
  if not "items" in response or not "count" in response:
    print("Unable to get list of friends. Going to main menu.")
    return
  
  allFriends = response["items"]
  friendsCount = response["count"]
  if friendsCount > len(allFriends):
    print("Warning! Not all friends will be processed. Too many friends. This will be fixed later")
  
  deactivatedFriends = []
  for item in allFriends:
    if "deactivated" in item: deactivatedFriends.append(item)
  
  while True:
    print(f"Found {len(deactivatedFriends)} deleted or banned friends")
    answer = input("To delete those friends type 'delete' and press enter. Type 'list' for full list. Othervise enter anything else to abort.")
    if answer == "list":
      formatedList(deactivatedFriends, contentType=ContentType.deletedUser)
    elif answer == "delete":
      deletedCount = 0
      for item in deactivatedFriends:
        sleep(0.4)
        result = api.friends.delete(user_id=item["id"])
        if "success" in result:
          if result["success"] == 1: deletedCount += 1
      print(f"{deletedCount} out of {len(deactivatedFriends)} were deleted from your friend list")
    else:
      return
  input("Press enter to return to previous menu")
  return

def cleanOutcomingRequests(api):
  try: response = api.friends.getRequests(count=1000, out=1, fields="nickname,domain")
  except Exception as e: input(e)
  if not "items" in response or not "count" in response:
    input("Unable to get outcoming friend requests. Exiting")
    return
  
  allRequests = response["items"]
  requestCount = response["count"]
  
  if requestCount > len(allRequests):
    print("Warning! Not all outcoming requests were loaded. This will be fixed in future")
  
  while True:
    print(f"{len(allRequests)} outcoming friend requests found.")
    answer = input("To cancel all found requests type 'delete' and press enter. To list all requests type 'list'. To abort deletion type anything else and press enter")
    if answer == "list":
      formatedList(allRequests, contentType=ContentType.user)
    elif answer == "delete":
      deletedCount = 0
      for item in allRequests:
        sleep(0.4)
        result = api.friends.delete(user_id=item)
        if "success" in result:
          if result["success"] == 1: deletedCount += 1
      print(f"{deletedCount} out of {len(allRequests)} outcoming friend requests were cancelled.")
    else:
      return
  input("Press enter tto return to previous menu")
  return

