from getpass import getpass
from os import path
import vk_api
import requests
from consolemenu import *
from consolemenu.items import *
from vk_api.exceptions import ApiError
from encryption import encrypt, decrypt
from actions import FriendsCleaner
import vkoptions

http = requests.Session()
#http.headers.update({
  #"User-agent": "VKAndroidApp/4.13.1-1206 (Android 7.1.1; SDK 25; armeabi-v7a; ; ru)"
#})


class VkOrdnung:
  def mainMenu(self):
    if not hasattr(self, "api"): self.authenticate()
    
    # create the main menu
    main_menu = ConsoleMenu("Vk Ortnung : main menu", "Select one of options with corresponding number and press enter.")
    friendsmenu = ConsoleMenu("Friends management")
    friendsmenu.append_item(FunctionItem("Clean deleted or banned friends", FriendsCleaner.cleanDeletedFriends, [self.api]))
    friendsmenu.append_item(FunctionItem("Cancel all outcoming friend requests", FriendsCleaner.cleanOutcomingRequests, [self.api]))
    friendsSubmenu = SubmenuItem("Friends management", friendsmenu, main_menu)
    main_menu.append_item(friendsSubmenu)
    main_menu.show()
  
  def authenticate(self):
    if path.isfile("token"):
      self.tokenFile = open("token", "rb")
      encryptedToken = self.tokenFile.read()
      self.tokenFile.close()
      try:
        self.token = decrypt(encryptedToken)
      except:
        input("You have entered wrong password or something went wrong. exitting.")
        exit()
      
      vksession = vk_api.VkApi(token=self.token, session=http)
      if vksession._check_token():
        self.api = vksession.get_api()
      else:
        username = input("Enter your vk login: ")
        passwd = getpass(prompt="Enter your vk password: ")
        vksession = vk_api.VkApi(login=username, password=passwd, auth_handler=lambda: (input("enter two factor code: "), True), app_id=vkoptions.app_id, client_secret=vkoptions.app_secret, scope=vkoptions.scope, session=http)
        try:
          vksession.auth()
        except Exception as e:
          print(e)
          input("authentication error"); exit()
        self.api = vksession.get_api()
        self.token = vksession.token["access_token"]
        encryptedToken = encrypt(self.token)
        self.tokenFile = open("token", "wb")
        self.tokenFile.write(encryptedToken)
        self.tokenFile.close()
    else:
        username = input("Enter your vk login: ")
        passwd = getpass(prompt="Enter your vk password: ")
        vksession = vk_api.VkApi(login=username, password=passwd, auth_handler=lambda: (input("enter two factor code: "), True), app_id=vkoptions.app_id, client_secret=vkoptions.app_secret, scope=vkoptions.scope, session=http)
        try:
          vksession.auth()
        except Exception as e:
          print(e)
          input("authentication error"); exit()
        self.api = vksession.get_api()
        self.token = vksession.token["access_token"]
        encryptedToken = encrypt(self.token)
        self.tokenFile = open("token", "wb")
        self.tokenFile.write(encryptedToken)
        self.tokenFile.close()

if __name__ == "__main__":
  app = VkOrdnung()
  app.mainMenu()