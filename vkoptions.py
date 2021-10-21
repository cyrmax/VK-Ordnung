from os import environ, path
import json

scope = 2 | 4 | 8 | 16 | 128 | 1024 | 2048 | 4096 | 8192 | 65536 | 131072 | 262144 | 524288 | 4194304
#scope = "all"

elif "VK_APP_ID" in environ and "VK_APP_SECRET" in environ:
  app_id = environ["VK_APP_ID"]
  app_secret = environ["VK_APP_SECRET"]
elif path.isfile("vk_config.json"):
  with open("vk_config.json") as f:
    conf = json.load(f)
    app_id = conf["vk_app_id"]
    app_secret = conf["vk_app_secret"]
    del conf
else:
  app_id = ""
  app_secret = ""