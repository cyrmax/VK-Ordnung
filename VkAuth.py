from getpass import getpass
from vk_api import VkApi
import vkoptions

def authenticate() -> str:
  vksession = VkApi(login=input("Enter your VK login: "), password=getpass(prompt="Enter your VK password: "), auth_handler= lambda: (input("Enter two factor authentication code: "), True), app_id=vkoptions.app_id, client_secret=vkoptions.app_secret, scope=vkoptions.scope)
  vksession.auth()
  return vksession.token["access_token"]

def checkToken(token: str) -> bool:
  vksession = VkApi(token=token)
  return vksession._check_token()

def makeApi(token: str) -> VkApi:
  return VkApi(token=token).get_api()
