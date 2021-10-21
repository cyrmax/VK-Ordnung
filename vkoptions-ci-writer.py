from os import environ

o = f"""
app_id = "{environ['VK_APP_ID']}"
app_secret = "{environ['VK_APP_SECRET']}"
scope = 2 | 4 | 8 | 16 | 128 | 1024 | 2048 | 4096 | 8192 | 65536 | 131072 | 262144 | 524288 | 4194304
"""

with open("vkoptions.py", "w") as f:
  f.write(o)
