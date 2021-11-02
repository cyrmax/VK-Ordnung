from getpass import getpass
from os import path
import vk_api
from consolemenu import ConsoleMenu
from consolemenu.items import *
from vk_api import VkApi
from encryption import encrypt, decrypt
from actions import FriendsCleaner
import VkAuth
from ConfigStorage import ConfigStorage


class VkOrdnung:
  configStorage: ConfigStorage
  authenticated: bool = False
  api: vk_api.VkApi
  
  def __init__(self) -> None:
    self.configStorage = ConfigStorage()
    self.authenticate()
  
  def mainMenu(self):
    # create the main menu
    main_menu = ConsoleMenu("Vk Ortnung : main menu", "Select one of options with corresponding number and press enter.")
    # Friends management
    friendsmenu = ConsoleMenu("Friends management")
    friendsmenu.append_item(FunctionItem("Clean deleted or banned friends", FriendsCleaner.cleanDeletedFriends, [self.api]))
    friendsmenu.append_item(FunctionItem("Cancel all outcoming friend requests", FriendsCleaner.cleanOutcomingRequests, [self.api]))
    friendsSubmenu = SubmenuItem("Friends management", friendsmenu, main_menu)
    main_menu.append_item(friendsSubmenu)
    
    # Wall management
    
    main_menu.show()
  
  def authenticate(self):
    if self.configStorage.hasToken:
      if self.configStorage.tokenIsEncrypted:
        token = decrypt(self.configStorage.token)
      else:
        token = self.configStorage.token
      self.authenticated = VkAuth.checkToken(token)
      self.api = VkAuth.makeApi(token)
    if not self.authenticated:
      token = VkAuth.authenticate()
      answer = input("Authentication successful! Do you want to encrypt your authentication with a password? Y or N")
      if answer == "y":
        self.configStorage.tokenIsEncrypted = True
        self.configStorage.token = encrypt(token)
      else:
        self.configStorage.tokenIsEncrypted = False
        self.configStorage.token = token
      self.api = VkAuth.makeApi(token)
      self.authenticated = True
      

if __name__ == "__main__":
  app = VkOrdnung()
  app.mainMenu()