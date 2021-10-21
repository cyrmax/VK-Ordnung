from os import environ

o = f"""
app_id = "{environ['VK_APP_ID']}"
app_secret = "{environ['VK_APP_SECRET']}"
"""

with open("vkoptions.py", "w") as f:
  f.write(o)
