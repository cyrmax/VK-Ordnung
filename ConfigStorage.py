import json
from os import path
from typing import IO, Dict, Any

import portalocker


class ConfigStorage:
  filename:str = "VkOrdnung-config.json"
  config: Dict[str, Any]
  writelock: portalocker.utils.Lock
  readlock: portalocker.utils.Lock
  configfile: IO
  
  def createConfig(self) -> None:
    defaultConfigString = """
    {
      "token": "",
      "token_is_encrypted": false
    }
    """
    self.config = json.loads(defaultConfigString)
  
  def saveConfig(self) -> None:
    json.dump(self.config, self.configfile, indent=2, ensure_ascii=True)
  
  @property
  def hasToken(self) -> bool:
    return "token" in self.config and len(self.config["token"]) != 0
  
  @property
  def token(self) -> str:
    return self.config["token"]
  @token.setter
  def token(self, value: str) -> None:
    self.config["token"] = value
    self.saveConfig()
  
  @property
  def tokenIsEncrypted(self) -> bool:
    return self.config["token_is_encrypted"]
  @tokenIsEncrypted.setter
  def tokenIsEncrypted(self, value: bool) -> None:
    self.config["token_is_encrypted"] = value
    self.saveConfig()
  
  def __init__(self) -> None:
    self.readlock = portalocker.Lock(self.filename, mode="r", timeout=0, flags=portalocker.LOCK_EX|portalocker.LOCK_NB)
    self.writelock = portalocker.Lock(self.filename, mode="w", timeout=0, flags=portalocker.LOCK_EX|portalocker.LOCK_NB)
    if path.isfile(self.filename):
      try:
        with self.readlock.acquire() as f:
          self.config = json.load(f)
        self.configfile = self.writelock.acquire()
      except portalocker.exceptions.LockException:
        raise PermissionError()
    else:
      self.createConfig()
      try:
        self.configfile = self.writelock.acquire()
        self.saveConfig()
      except portalocker.exceptions.LockException:
        raise PermissionError()
  
