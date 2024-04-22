import redis
from colorama import Back, Fore, Style
from settings import redis_config as rc

# Redis Setup

class redisConnectionData:
  __connection = None
  def __new__(cls):
    if cls.__connection is None:
      cls.__connection = super(redisConnectionData, cls).__new__(cls)
      cls.__connection.config = rc
      cls.__connection.connectToRedis()
      print(F'{Fore.GREEN}REDIS-CONNECTED: \n REDIS-LOGS {Fore.LIGHTCYAN_EX}>>> ( {Fore.YELLOW}Success {Fore.LIGHTCYAN_EX}) \n {Fore.GREEN}REDIS-LOGS: {Fore.LIGHTCYAN_EX}>>> {Fore.YELLOW}No info...{Style.RESET_ALL}')
    else:
      print(f'{Fore.RED}REDIS-CONNECTION: ALREADY /// FIX YOUR CODE CONNECTION!{Style.RESET_ALL}')
    return cls.__connection

  def display_redis(self, boolean:bool):
    """ 
    Logging Redis Connection
    
    Params: boolean[bool]
    Returning: Logs[Str]
    """
    try:
      if boolean == True:
        return print(f"{Fore.CYAN}REDIS-SUCESSFULLY: Already!{Style.RESET_ALL}")
      print(f'REDIS-TYPES: {type(boolean)} need >>> [ (String, Boolean) True,False ]')
    except TypeError as e:
      print(f'REDIS-ERROR: {e}')

  def connectToRedis(self) -> object:
    try:
      self.display_redis(True)
      return redis.StrictRedis(**self.config)
    except Exception as e:
      print(F'REDIS-ERROR: {e}') 
rRedis = redisConnectionData()