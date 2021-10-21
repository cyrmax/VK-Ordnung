from time import sleep

def cleanEntireWall(api):
  answer = input("WARNING!!! This action will delete EVERY post on your VK wall! If you want tto continue, enter 'sure' and press enter. To go back type anything else and press enter.")
  if answer != "sure": return
  
  response = api.wall.get(count=100, offset=0)
  if not "count" in response or not "items" in response:
    print("Unable to reach wall posts"); return
  
  answer = input(f"WARNING! You are about to delete {response['count']} posts from your wall! This is the last warning. If you enter 'delete' and press enter the process will begin")
  if answer != "delete": return
  
  print("Loading all posts...")
  postCount = response["count"]
  allPosts = response["items"]
  
  offset = 100
  while postCount > len(allPosts):
    response = api.wall.get(count=100, offset=offset)
    allPosts += response["items"]
    offset += 100
  
  print(f"{len(allPosts)} loaded. total count was {postCount}")
  
  print("Deleting all posts. This may take long time if you have many posts on your wall. Please be patient.")
  
  deletedCount = 0
  for item in allPosts:
    sleep(0.3)
    deletedCount += api.wall.delete(post_id=item["id"])
  
  input(f"{deletedCount} out of {postCount} total. Press enter to back to previous menu.")